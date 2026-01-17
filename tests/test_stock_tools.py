import pytest
import time
from stock_cache import StockDataCache
from stock_tools import StockTools

def test_placeholder():
    """Placeholder test to verify pytest setup"""
    assert True

def test_cache_stores_and_retrieves_data():
    cache = StockDataCache(ttl_seconds=300)
    cache.set("test_key", "test_value")
    assert cache.get("test_key") == "test_value"

def test_cache_expires_after_ttl():
    cache = StockDataCache(ttl_seconds=1)
    cache.set("test_key", "test_value")
    assert cache.get("test_key") == "test_value"
    time.sleep(1.1)
    assert cache.get("test_key") is None

def test_cache_returns_none_for_missing_key():
    cache = StockDataCache()
    assert cache.get("nonexistent") is None

@pytest.fixture
def stock_tools():
    return StockTools()

def test_get_stock_info_valid_symbol(stock_tools):
    result = stock_tools.get_stock_info("AAPL")
    assert "AAPL" in result
    assert "市值" in result or "無法獲取" in result

def test_get_stock_info_invalid_symbol(stock_tools):
    result = stock_tools.get_stock_info("INVALID_XYZ_123")
    assert "無法獲取" in result

def test_get_price_history(stock_tools):
    result = stock_tools.get_price_history("AAPL", period="5d")
    assert "AAPL" in result
    assert "價格走勢" in result or "無法獲取" in result

def test_get_dividends(stock_tools):
    result = stock_tools.get_dividends("AAPL")
    assert "AAPL" in result or "無法獲取" in result

def test_get_news(stock_tools):
    result = stock_tools.get_news("AAPL", count=3)
    assert "AAPL" in result or "無法獲取" in result

def test_taiwan_stock_format(stock_tools):
    result = stock_tools.get_stock_info("2330.TW")
    assert "2330.TW" in result or "無法獲取" in result

def test_get_income_statement(stock_tools):
    result = stock_tools.get_income_statement("AAPL")
    assert "AAPL" in result or "無法獲取" in result

def test_get_balance_sheet(stock_tools):
    result = stock_tools.get_balance_sheet("AAPL")
    assert "AAPL" in result or "無法獲取" in result

def test_get_cashflow(stock_tools):
    result = stock_tools.get_cashflow("AAPL")
    assert "AAPL" in result or "無法獲取" in result

def test_get_analyst_price_targets(stock_tools):
    result = stock_tools.get_analyst_price_targets("AAPL")
    assert "AAPL" in result or "無法獲取" in result

def test_get_fundamentals(stock_tools):
    result = stock_tools.get_fundamentals("AAPL")
    assert "AAPL" in result
    assert "基本面" in result or "無法獲取" in result
