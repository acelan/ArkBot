from google.genai import types


stock_tools_declarations = [
    types.FunctionDeclaration(
        name="get_stock_info",
        description="獲取股票基本資訊，包含市值、產業類別、員工數、公司簡介等。適用於了解公司基本面。",
        parameters={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "股票代號，例如 AAPL (蘋果), TSLA (特斯拉), 2330.TW (台積電)"
                }
            },
            "required": ["symbol"]
        }
    ),
    types.FunctionDeclaration(
        name="get_price_history",
        description="獲取歷史股價資料，可指定時間範圍。用於技術面分析和趨勢判斷。",
        parameters={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "股票代號"
                },
                "period": {
                    "type": "string",
                    "description": "時間範圍：1d(一天), 5d(五天), 1mo(一個月), 3mo, 6mo, 1y(一年), 2y, 5y, 10y, ytd(今年至今), max(全部)",
                    "enum": ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
                }
            },
            "required": ["symbol"]
        }
    ),
    types.FunctionDeclaration(
        name="get_income_statement",
        description="獲取公司損益表，包含營收、毛利、淨利等財務指標。",
        parameters={
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "股票代號"},
                "quarterly": {"type": "boolean", "description": "是否顯示季度資料（預設為年度資料）"}
            },
            "required": ["symbol"]
        }
    ),
    types.FunctionDeclaration(
        name="get_balance_sheet",
        description="獲取資產負債表，了解公司財務結構和償債能力。",
        parameters={
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "股票代號"},
                "quarterly": {"type": "boolean", "description": "是否顯示季度資料"}
            },
            "required": ["symbol"]
        }
    ),
    types.FunctionDeclaration(
        name="get_cashflow",
        description="獲取現金流量表，分析公司現金管理能力。",
        parameters={
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "股票代號"},
                "quarterly": {"type": "boolean", "description": "是否顯示季度資料"}
            },
            "required": ["symbol"]
        }
    ),
    types.FunctionDeclaration(
        name="get_dividends",
        description="獲取股息發放歷史，適合價值投資和股息分析。",
        parameters={
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "股票代號"}
            },
            "required": ["symbol"]
        }
    ),
    types.FunctionDeclaration(
        name="get_splits",
        description="獲取股票分割歷史記錄。",
        parameters={
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "股票代號"}
            },
            "required": ["symbol"]
        }
    ),
    types.FunctionDeclaration(
        name="get_recommendations",
        description="獲取分析師建議（買入、持有、賣出）及歷史趨勢。",
        parameters={
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "股票代號"}
            },
            "required": ["symbol"]
        }
    ),
    types.FunctionDeclaration(
        name="get_analyst_price_targets",
        description="獲取分析師目標價，包含最高、最低、平均目標價。",
        parameters={
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "股票代號"}
            },
            "required": ["symbol"]
        }
    ),
    types.FunctionDeclaration(
        name="get_major_holders",
        description="獲取主要持股人資訊，了解持股結構。",
        parameters={
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "股票代號"}
            },
            "required": ["symbol"]
        }
    ),
    types.FunctionDeclaration(
        name="get_institutional_holders",
        description="獲取機構投資者持股明細。",
        parameters={
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "股票代號"}
            },
            "required": ["symbol"]
        }
    ),
    types.FunctionDeclaration(
        name="get_news",
        description="獲取股票相關最新新聞，用於市場面分析。",
        parameters={
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "股票代號"},
                "count": {"type": "integer", "description": "新聞數量（預設5則）"}
            },
            "required": ["symbol"]
        }
    ),
    types.FunctionDeclaration(
        name="get_earnings",
        description="獲取公司盈餘資訊和財報發布日期。",
        parameters={
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "股票代號"}
            },
            "required": ["symbol"]
        }
    ),
    types.FunctionDeclaration(
        name="get_calendar",
        description="獲取公司財報日曆，包含下次財報發布日期。",
        parameters={
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "股票代號"}
            },
            "required": ["symbol"]
        }
    ),
    types.FunctionDeclaration(
        name="get_fundamentals",
        description="獲取綜合基本面資訊，整合多個財務指標提供完整分析。",
        parameters={
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "股票代號"}
            },
            "required": ["symbol"]
        }
    ),
]

tool_config = types.Tool(function_declarations=stock_tools_declarations)
