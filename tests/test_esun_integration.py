import pytest
from unittest.mock import Mock, patch, AsyncMock
from esun_integration import EsunIntegration
import asyncio


@pytest.fixture
def mock_config_file(tmp_path):
    """Create a temporary config file for testing"""
    config_file = tmp_path / "config.ini"
    config_file.write_text("""
[Core]
Entry = https://test.example.com/api/v1
[Cert]
Path = test.p12
[Api]
Key = TEST_KEY
Secret = TEST_SECRET
[User]
Account = TEST_ACCOUNT
""")
    return str(config_file)


def test_esun_integration_initialization_with_fugle_fallback(mock_config_file):
    """Test that EsunIntegration initializes with Fugle SDK fallback"""
    with patch('esun_integration.SDK') as mock_sdk_class:
        mock_sdk_instance = Mock()
        mock_sdk_class.return_value = Mock(return_value=mock_sdk_instance)

        integration = EsunIntegration(mock_config_file)

        assert integration.sdk is not None
        mock_sdk_instance.login.assert_called_once()


@pytest.mark.asyncio
async def test_get_inventories_success(mock_config_file):
    """Test successful inventory retrieval"""
    with patch('esun_integration.SDK') as mock_sdk_class:
        mock_sdk_instance = Mock()
        mock_sdk_class.return_value = Mock(return_value=mock_sdk_instance)
        mock_sdk_instance.get_inventories = Mock(return_value=[
            {
                'stk_no': '2330',
                'stk_na': '台積電',
                'cost_sum': '100000',
                'value_now': '105000',
                'cost_qty': '1000',
                'price_now': '105',
                'price_avg': '100',
                'price_evn': '100',
                'make_a_sum': '5000',
                'stk_dats': []
            }
        ])

        integration = EsunIntegration(mock_config_file)
        result = await integration.get_inventories('2330')

        assert '台積電' in result
        assert '2330' in result
        assert '105000' in result


@pytest.mark.asyncio
async def test_get_inventories_login_retry(mock_config_file):
    """Test that get_inventories retries login on authentication failure"""
    with patch('esun_integration.SDK') as mock_sdk_class:
        mock_sdk_instance = Mock()
        mock_sdk_class.return_value = Mock(return_value=mock_sdk_instance)

        call_count = 0
        def get_inventories_side_effect():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError(": Must login first")
            return [{
                'stk_no': '2330',
                'stk_na': '台積電',
                'cost_sum': '100000',
                'value_now': '105000',
                'cost_qty': '1000',
                'price_now': '105',
                'price_avg': '100',
                'price_evn': '100',
                'make_a_sum': '5000',
                'stk_dats': []
            }]

        mock_sdk_instance.get_inventories = Mock(side_effect=get_inventories_side_effect)

        integration = EsunIntegration(mock_config_file)
        result = await integration.get_inventories('2330')

        assert '台積電' in result
        assert mock_sdk_instance.login.call_count >= 2


@pytest.mark.asyncio
async def test_get_inventories_rate_limit(mock_config_file):
    """Test that get_inventories handles rate limiting"""
    with patch('esun_integration.SDK') as mock_sdk_class:
        mock_sdk_instance = Mock()
        mock_sdk_class.return_value = Mock(return_value=mock_sdk_instance)

        call_count = 0
        def get_inventories_side_effect():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("AGR0003: Please wait for 10 seconds")
            return [{
                'stk_no': '2330',
                'stk_na': '台積電',
                'cost_sum': '100000',
                'value_now': '105000',
                'cost_qty': '1000',
                'price_now': '105',
                'price_avg': '100',
                'price_evn': '100',
                'make_a_sum': '5000',
                'stk_dats': []
            }]

        mock_sdk_instance.get_inventories = Mock(side_effect=get_inventories_side_effect)

        integration = EsunIntegration(mock_config_file)

        start_time = asyncio.get_event_loop().time()
        result = await integration.get_inventories('2330')
        elapsed_time = asyncio.get_event_loop().time() - start_time

        assert '台積電' in result
        assert elapsed_time >= 10


def test_format_inventory_with_stock_id(mock_config_file):
    """Test inventory formatting with specific stock ID"""
    with patch('esun_integration.SDK') as mock_sdk_class:
        mock_sdk_instance = Mock()
        mock_sdk_class.return_value = Mock(return_value=mock_sdk_instance)

        integration = EsunIntegration(mock_config_file)
        inventories = [
            {
                'stk_no': '2330',
                'stk_na': '台積電',
                'cost_sum': '100000',
                'value_now': '105000',
                'cost_qty': '1000',
                'price_now': '105',
                'price_avg': '100',
                'price_evn': '100',
                'make_a_sum': '5000',
                'stk_dats': [{
                    't_date': '2026-01-15',
                    'buy_sell': 'B',
                    'price': '100',
                    'qty': '1000',
                    'fee': '285',
                    'pay_n': '-100285'
                }]
            },
            {
                'stk_no': '2317',
                'stk_na': '鴻海',
                'cost_sum': '50000',
                'value_now': '52000',
                'cost_qty': '500',
                'price_now': '104',
                'price_avg': '100',
                'price_evn': '100',
                'make_a_sum': '2000',
                'stk_dats': []
            }
        ]

        result = integration.format_inventory(inventories, '2330')

        assert '台積電' in result
        assert '2330' in result
        assert '2026-01-15' in result
        assert '購買' in result
        assert '2317' not in result or '鴻海' not in result


def test_format_inventory_all_stocks(mock_config_file):
    """Test inventory formatting with all stocks"""
    with patch('esun_integration.SDK') as mock_sdk_class:
        mock_sdk_instance = Mock()
        mock_sdk_class.return_value = Mock(return_value=mock_sdk_instance)

        integration = EsunIntegration(mock_config_file)
        inventories = [
            {
                'stk_no': '2330',
                'stk_na': '台積電',
                'cost_sum': '100000',
                'value_now': '105000',
                'cost_qty': '1000',
                'price_now': '105',
                'price_avg': '100',
                'price_evn': '100',
                'make_a_sum': '5000',
                'stk_dats': []
            },
            {
                'stk_no': '2317',
                'stk_na': '鴻海',
                'cost_sum': '50000',
                'value_now': '52000',
                'cost_qty': '500',
                'price_now': '104',
                'price_avg': '100',
                'price_evn': '100',
                'make_a_sum': '2000',
                'stk_dats': []
            }
        ]

        result = integration.format_inventory(inventories, '')

        assert '台積電' in result
        assert '鴻海' in result
        assert '總支出：150000' in result
        assert '總市值：157000' in result
        assert '未實現損益：7000' in result


def test_format_inventory_calculates_profit_percentage(mock_config_file):
    """Test that format_inventory calculates profit percentage correctly"""
    with patch('esun_integration.SDK') as mock_sdk_class:
        mock_sdk_instance = Mock()
        mock_sdk_class.return_value = Mock(return_value=mock_sdk_instance)

        integration = EsunIntegration(mock_config_file)
        inventories = [{
            'stk_no': '2330',
            'stk_na': '台積電',
            'cost_sum': '100000',
            'value_now': '105000',
            'cost_qty': '1000',
            'price_now': '105',
            'price_avg': '100',
            'price_evn': '100',
            'make_a_sum': '5000',
            'stk_dats': []
        }]

        result = integration.format_inventory(inventories, '')

        assert '獲利率：5.00%' in result
        assert '損益比：4.67%' in result
