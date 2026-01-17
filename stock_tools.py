import yfinance as yf
from typing import Optional
from stock_cache import StockDataCache


class StockTools:
    """
    Comprehensive stock analysis tools using yfinance
    All output in Traditional Chinese (正體中文)
    """
    def __init__(self):
        self.cache = StockDataCache(ttl_seconds=300)  # 5-min cache
        self.tickers = {}  # Cache ticker objects

    def _get_ticker(self, symbol: str) -> yf.Ticker:
        """Get or create cached ticker object"""
        if symbol not in self.tickers:
            self.tickers[symbol] = yf.Ticker(symbol)
        return self.tickers[symbol]

    def get_stock_info(self, symbol: str) -> str:
        """
        獲取股票基本資訊

        Args:
            symbol: 股票代號，例如 AAPL, TSLA, 2330.TW

        Returns:
            格式化的中文資訊字串
        """
        cache_key = f"info:{symbol}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        try:
            ticker = self._get_ticker(symbol)
            info = ticker.info

            # Handle missing data gracefully
            market_cap = info.get('marketCap', 'N/A')
            if isinstance(market_cap, (int, float)):
                market_cap = f"{market_cap:,} USD"

            result = f"""
股票代號: {symbol}
公司名稱: {info.get('longName', 'N/A')}
產業: {info.get('industry', 'N/A')}
市值: {market_cap}
當前價格: {info.get('currentPrice', 'N/A')} USD
本益比 (P/E): {info.get('trailingPE', 'N/A')}
股息率: {info.get('dividendYield', 0) * 100:.2f}%
52週最高: {info.get('fiftyTwoWeekHigh', 'N/A')}
52週最低: {info.get('fiftyTwoWeekLow', 'N/A')}
""".strip()

            self.cache.set(cache_key, result)
            return result

        except Exception as e:
            return f"無法獲取 {symbol} 的資訊: {str(e)}"

    def get_price_history(self, symbol: str, period: str = "1mo") -> str:
        """
        獲取歷史股價資料

        Args:
            symbol: 股票代號
            period: 時間範圍 (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)

        Returns:
            格式化的歷史價格資料
        """
        cache_key = f"history:{symbol}:{period}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        try:
            ticker = self._get_ticker(symbol)
            hist = ticker.history(period=period)

            if hist.empty:
                return f"無法獲取 {symbol} 的歷史資料"

            info = ticker.info
            company_name = info.get('longName', info.get('shortName', symbol))

            total_days = len(hist)
            start_date = hist.index[0].strftime('%Y-%m-%d')
            end_date = hist.index[-1].strftime('%Y-%m-%d')
            start_price = hist['Close'].iloc[0]
            end_price = hist['Close'].iloc[-1]
            price_change = ((end_price / start_price - 1) * 100)
            high = hist['High'].max()
            low = hist['Low'].min()
            avg_volume = hist['Volume'].mean()

            result = f"股票 {symbol} ({company_name}) 最近 {period} 的價格走勢:\n\n"
            result += f"期間: {start_date} 至 {end_date} (共 {total_days} 個交易日)\n"
            result += f"起始價: {start_price:.2f}\n"
            result += f"結束價: {end_price:.2f}\n"
            result += f"期間漲跌: {price_change:+.2f}%\n"
            result += f"期間最高: {high:.2f}\n"
            result += f"期間最低: {low:.2f}\n"
            result += f"平均成交量: {avg_volume:,.0f}\n\n"
            result += "最近10個交易日:\n"
            result += hist[['Open', 'High', 'Low', 'Close', 'Volume']].tail(10).to_string()

            self.cache.set(cache_key, result)
            return result

        except Exception as e:
            return f"無法獲取 {symbol} 的歷史資料: {str(e)}"

    def get_dividends(self, symbol: str) -> str:
        """獲取股息發放歷史"""
        cache_key = f"dividends:{symbol}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        try:
            ticker = self._get_ticker(symbol)
            dividends = ticker.dividends

            if dividends.empty:
                return f"{symbol} 沒有股息發放記錄"

            result = f"股票 {symbol} 股息發放歷史（最近10筆）:\n\n"
            result += dividends.tail(10).to_string()

            self.cache.set(cache_key, result)
            return result

        except Exception as e:
            return f"無法獲取 {symbol} 的股息資料: {str(e)}"

    def get_news(self, symbol: str, count: int = 5) -> str:
        """獲取股票相關最新新聞"""
        cache_key = f"news:{symbol}:{count}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        try:
            ticker = self._get_ticker(symbol)
            news = ticker.news

            if not news:
                return f"{symbol} 沒有相關新聞"

            result = f"股票 {symbol} 最新 {count} 則新聞:\n\n"
            for i, item in enumerate(news[:count], 1):
                title = item.get('title', 'N/A')
                publisher = item.get('publisher', 'N/A')
                result += f"{i}. {title} (來源: {publisher})\n"

            self.cache.set(cache_key, result)
            return result

        except Exception as e:
            return f"無法獲取 {symbol} 的新聞: {str(e)}"

    def get_recommendations(self, symbol: str) -> str:
        """獲取分析師建議"""
        cache_key = f"rec:{symbol}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        try:
            ticker = self._get_ticker(symbol)
            rec = ticker.recommendations

            if rec is None or rec.empty:
                return f"{symbol} 沒有分析師建議資料"

            result = f"股票 {symbol} 分析師建議（最近10筆）:\n\n"
            result += rec.tail(10).to_string()

            self.cache.set(cache_key, result)
            return result

        except Exception as e:
            return f"無法獲取 {symbol} 的分析師建議: {str(e)}"

    def get_income_statement(self, symbol: str, quarterly: bool = False) -> str:
        cache_key = f"income:{symbol}:{quarterly}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        try:
            ticker = self._get_ticker(symbol)
            stmt = ticker.quarterly_income_stmt if quarterly else ticker.income_stmt

            if stmt is None or stmt.empty:
                return f"{symbol} 沒有損益表資料"

            period_type = "季度" if quarterly else "年度"
            result = f"股票 {symbol} {period_type}損益表:\n\n"
            result += stmt.to_string()

            self.cache.set(cache_key, result)
            return result

        except Exception as e:
            return f"無法獲取 {symbol} 的損益表: {str(e)}"

    def get_balance_sheet(self, symbol: str, quarterly: bool = False) -> str:
        cache_key = f"balance:{symbol}:{quarterly}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        try:
            ticker = self._get_ticker(symbol)
            sheet = ticker.quarterly_balance_sheet if quarterly else ticker.balance_sheet

            if sheet is None or sheet.empty:
                return f"{symbol} 沒有資產負債表資料"

            period_type = "季度" if quarterly else "年度"
            result = f"股票 {symbol} {period_type}資產負債表:\n\n"
            result += sheet.to_string()

            self.cache.set(cache_key, result)
            return result

        except Exception as e:
            return f"無法獲取 {symbol} 的資產負債表: {str(e)}"

    def get_cashflow(self, symbol: str, quarterly: bool = False) -> str:
        cache_key = f"cashflow:{symbol}:{quarterly}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        try:
            ticker = self._get_ticker(symbol)
            cf = ticker.quarterly_cashflow if quarterly else ticker.cashflow

            if cf is None or cf.empty:
                return f"{symbol} 沒有現金流量表資料"

            period_type = "季度" if quarterly else "年度"
            result = f"股票 {symbol} {period_type}現金流量表:\n\n"
            result += cf.to_string()

            self.cache.set(cache_key, result)
            return result

        except Exception as e:
            return f"無法獲取 {symbol} 的現金流量表: {str(e)}"

    def get_splits(self, symbol: str) -> str:
        cache_key = f"splits:{symbol}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        try:
            ticker = self._get_ticker(symbol)
            splits = ticker.splits

            if splits.empty:
                return f"{symbol} 沒有股票分割記錄"

            result = f"股票 {symbol} 分割歷史:\n\n"
            result += splits.to_string()

            self.cache.set(cache_key, result)
            return result

        except Exception as e:
            return f"無法獲取 {symbol} 的股票分割資料: {str(e)}"

    def get_analyst_price_targets(self, symbol: str) -> str:
        cache_key = f"target:{symbol}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        try:
            ticker = self._get_ticker(symbol)
            targets = ticker.analyst_price_targets

            if not targets:
                return f"{symbol} 沒有分析師目標價資料"

            result = f"股票 {symbol} 分析師目標價:\n"
            result += f"當前價: {targets.get('current', 'N/A')}\n"
            result += f"最高目標價: {targets.get('high', 'N/A')}\n"
            result += f"最低目標價: {targets.get('low', 'N/A')}\n"
            result += f"平均目標價: {targets.get('mean', 'N/A')}\n"
            result += f"中位數: {targets.get('median', 'N/A')}\n"

            self.cache.set(cache_key, result)
            return result

        except Exception as e:
            return f"無法獲取 {symbol} 的目標價資料: {str(e)}"

    def get_major_holders(self, symbol: str) -> str:
        cache_key = f"holders:{symbol}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        try:
            ticker = self._get_ticker(symbol)
            holders = ticker.major_holders

            if holders is None or holders.empty:
                return f"{symbol} 沒有主要持股人資料"

            result = f"股票 {symbol} 主要持股人:\n\n"
            result += holders.to_string()

            self.cache.set(cache_key, result)
            return result

        except Exception as e:
            return f"無法獲取 {symbol} 的持股人資料: {str(e)}"

    def get_institutional_holders(self, symbol: str) -> str:
        cache_key = f"inst:{symbol}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        try:
            ticker = self._get_ticker(symbol)
            inst = ticker.institutional_holders

            if inst is None or inst.empty:
                return f"{symbol} 沒有機構持股資料"

            result = f"股票 {symbol} 機構持股:\n\n"
            result += inst.to_string()

            self.cache.set(cache_key, result)
            return result

        except Exception as e:
            return f"無法獲取 {symbol} 的機構持股資料: {str(e)}"

    def get_earnings(self, symbol: str) -> str:
        cache_key = f"earnings:{symbol}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        try:
            ticker = self._get_ticker(symbol)
            earnings = ticker.earnings

            if earnings is None or earnings.empty:
                return f"{symbol} 沒有盈餘資料"

            result = f"股票 {symbol} 盈餘資訊:\n\n"
            result += earnings.to_string()

            self.cache.set(cache_key, result)
            return result

        except Exception as e:
            return f"無法獲取 {symbol} 的盈餘資料: {str(e)}"

    def get_calendar(self, symbol: str) -> str:
        cache_key = f"calendar:{symbol}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        try:
            ticker = self._get_ticker(symbol)
            calendar = ticker.calendar

            if calendar is None or (hasattr(calendar, 'empty') and calendar.empty):
                return f"{symbol} 沒有財報日曆資料"

            result = f"股票 {symbol} 財報日曆:\n\n"
            result += str(calendar)

            self.cache.set(cache_key, result)
            return result

        except Exception as e:
            return f"無法獲取 {symbol} 的財報日曆: {str(e)}"

    def get_fundamentals(self, symbol: str) -> str:
        cache_key = f"fund:{symbol}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        try:
            info = self.get_stock_info(symbol)
            earnings = self.get_earnings(symbol)
            recommendations = self.get_recommendations(symbol)

            result = f"股票 {symbol} 綜合基本面分析:\n\n"
            result += "=== 基本資訊 ===\n" + info + "\n\n"
            result += "=== 盈餘資訊 ===\n" + earnings + "\n\n"
            result += "=== 分析師建議 ===\n" + recommendations

            self.cache.set(cache_key, result)
            return result

        except Exception as e:
            return f"無法獲取 {symbol} 的綜合基本面: {str(e)}"
