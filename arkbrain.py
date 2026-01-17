import os
import logging
from functools import wraps
import asyncio
from dotenv import load_dotenv
from google import genai
from google.genai import types
from stock_tools import StockTools
from gemini_tools import tool_config

load_dotenv()

logger = logging.getLogger('ArkBot')
log_level = logging.DEBUG if os.getenv('LOG_LEVEL') == "DEBUG" else logging.INFO
logging.basicConfig(
    level=log_level,
    format='%(levelname)s %(asctime)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)

def retry_on_api_error(max_retries=3, delay=1.0):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        logger.warning(f"API call failed (attempt {attempt+1}/{max_retries}): {e}")
                        await asyncio.sleep(delay * (2 ** attempt))
                    else:
                        logger.error(f"API call failed after {max_retries} attempts: {e}")
            raise APIError(f"Failed after {max_retries} retries") from last_error
        return wrapper
    return decorator

class ArkBrain:
    def __init__(self):
        api_key = os.getenv('GOOGLE_GENAI_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_GENAI_API_KEY not found in environment")

        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-flash-lite-latest"
        self.system_prompt = os.getenv('SYSTEM_PROMPT')

        self.stock_tools = StockTools()

        self.chat_sessions = {}

        logger.info(f"ArkBrain initialized with model: {self.model_id}")

    async def thinking(self, reference_id: str, user_input: str) -> str:
        logger.debug(f"thinking() - {reference_id}: {user_input}")

        if reference_id not in self.chat_sessions:
            self.chat_sessions[reference_id] = self._create_chat_session()

        chat = self.chat_sessions[reference_id]

        try:
            response = await self._chat_with_tools(chat, user_input)
            return response
        except APIError as e:
            logger.error(f"API error in thinking(): {e}")
            return "抱歉，我現在無法處理您的請求，請稍後再試。"
        except Exception as e:
            logger.error(f"Unexpected error in thinking(): {e}", exc_info=True)
            return "發生未預期的錯誤，請聯繫管理員。"

    def _create_chat_session(self):
        return self.client.chats.create(
            model=self.model_id,
            config={
                "system_instruction": self.system_prompt,
                "tools": [tool_config],
                "temperature": 0,
            }
        )

    @retry_on_api_error(max_retries=3)
    async def _send_message_with_retry(self, chat, message):
        return chat.send_message(message)

    async def _chat_with_tools(self, chat, user_message: str, max_iterations: int = 5) -> str:
        response = await self._send_message_with_retry(chat, user_message)

        for iteration in range(max_iterations):
            if not response.candidates or not response.candidates[0].content.parts:
                break

            function_calls = [
                part.function_call
                for part in response.candidates[0].content.parts
                if hasattr(part, 'function_call') and part.function_call
            ]

            if not function_calls:
                return response.text or "我無法生成回應。"

            logger.debug(f"Iteration {iteration + 1}: Executing {len(function_calls)} tool(s)")

            function_responses = []
            for fc in function_calls:
                logger.debug(f"Executing tool: {fc.name} with args: {fc.args}")

                result = self._execute_tool(fc.name, dict(fc.args))
                function_responses.append(
                    types.Part.from_function_response(
                        name=fc.name,
                        response={"result": result}
                    )
                )

            response = await self._send_message_with_retry(chat, function_responses)

        logger.warning(f"Max iterations ({max_iterations}) reached")
        return response.text or "抱歉，我無法完成這個請求，請稍後再試。"

    def _execute_tool(self, function_name: str, args: dict) -> str:
        tool_method = getattr(self.stock_tools, function_name, None)
        if not tool_method:
            error_msg = f"Unknown tool: {function_name}"
            logger.error(error_msg)
            raise ToolExecutionError(error_msg)

        try:
            return tool_method(**args)
        except TypeError as e:
            error_msg = f"Invalid arguments for {function_name}: {e}"
            logger.error(error_msg)
            raise ToolExecutionError(error_msg)
        except Exception as e:
            error_msg = f"Tool execution error in {function_name}: {e}"
            logger.error(error_msg)
            raise ToolExecutionError(error_msg)


class ArkBrainError(Exception):
    pass

class ToolExecutionError(ArkBrainError):
    pass

class APIError(ArkBrainError):
    pass
