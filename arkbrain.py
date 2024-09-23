import os
import logging
from dotenv import load_dotenv
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.agent import ReActAgent
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from llama_index.tools.yahoo_finance.base import YahooFinanceToolSpec
from llama_index.tools.tavily_research import TavilyToolSpec

load_dotenv()

ollama_addr = os.getenv('OLLAMA_ADDR')
ollama_model = os.getenv('OLLAMA_MODEL')
system_prompt = os.getenv('SYSTEM_PROMPT')
tavily_search_api = os.getenv('TAVILY_SEARCH_API')
openai_api = os.getenv('OPENAI_API_KEY')

log_format = '%(levelname)s %(asctime)s - %(message)s'
log_datefmt='%m/%d/%Y %I:%M:%S %p'
logger = logging.getLogger('ArkBot')
log_level = logging.DEBUG if os.getenv('LOG_LEVEL') == "DEBUG" else logging.INFO
logging.basicConfig(level=log_level, format=log_format, datefmt=log_datefmt)

class ArkBrain:
    def __init__(self):
        llm = None
        if openai_api:
            llm = OpenAI(
                model="gpt-4o-mini",
                temperature=0,
                system_prompt=system_prompt,
            )
        elif ollama_addr:
            llm = Ollama(
                model=ollama_model,
                base_url=ollama_addr,
                temperature=0,
                context_window=128000,
                request_timeout=300,
            )
        self.llm = llm

        def scrape_website(url: str) -> str:
            """ Useful to retrieve webpage from a given url"""
            return SimpleWebPageReader(html_to_text=True).load_data([url])[0]

        scrape_website_tool = FunctionTool.from_defaults(scrape_website)
        finance_tool_list = YahooFinanceToolSpec().to_tool_list()
        search_tool_list = TavilyToolSpec(api_key=tavily_search_api).to_tool_list()
        self.tools = [scrape_website_tool] + finance_tool_list + search_tool_list

        self.agents = {}

    async def thinking(self, reference_id, user_input) -> str:
        logger.debug(f"thinking() - {reference_id}: {user_input}")

        if reference_id not in self.agents:
            agent = OpenAIAgent if openai_api else ReActAgent
            self.agents[reference_id] = agent.from_tools(
                self.tools,
                llm=self.llm,
                max_iterations=30,
                allow_parallel_tool_calls=False,
                verbose=True,
                chat_history=[ChatMessage(role=MessageRole.USER, content=system_prompt)],
            )

        return await self.agents[reference_id].achat(message=user_input)
