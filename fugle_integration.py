from configparser import ConfigParser
from fugle_trade.sdk import SDK

class FugleIntegration:
    def __init__(self, config_file):
        config = ConfigParser()
        config.read(config_file)
        self.sdk = SDK(config)
        self.sdk.login()

    def login(self):
        self.sdk.login()

    async def get_inventories(self, stock_id):
        while True:
            try:
                inventory = self.sdk.get_inventories()
                return self.format_inventory(inventory, stock_id)
            except ValueError as e:
                if e.args[0].startswith(": Must login first"):
                    self.login()
                elif e.args[0] == "AGR0003: Please wait for 10 seconds":
                    await asyncio.sleep(10)
                elif e.args[0].startswith("A00001: response parse Error"):
                    raise Exception("Unexpected error, restarting bot")
            except Exception as err:
                print(f"Unexpected {err=}, {type(err)=}")
                break

    def format_inventory(self, inventories, stock_id):
        total_cost_sum = 0
        total_value_now = 0
        inv_msg = ""

        for stock in inventories:
            total_cost_sum = total_cost_sum + abs(int(stock['cost_sum']))
            total_value_now = total_value_now + abs(int(stock['value_now']))

            if not stock_id or stock['stk_no'] in stock_id:
                inv_msg = inv_msg + f"{stock['stk_na']}({stock['stk_no']}) - 損益：{stock['make_a_sum']}\n"
                inv_msg = inv_msg + f"\t成本總計：{abs(int(stock['cost_sum']))}\n"
                inv_msg = inv_msg + f"\t總市值：{stock['value_now']}\n"
                inv_msg = inv_msg + f"\t總股數：{stock['cost_qty']}\n"
                inv_msg = inv_msg + f"\t現價：{stock['price_now']}\n"
                inv_msg = inv_msg + f"\t成交均價：{stock['price_avg']}\n"
                inv_msg = inv_msg + f"\t損益平衡價：{stock['price_evn']}\n"
                inv_msg = inv_msg + f"\t獲利率：{(abs(float(stock['price_now'])/abs(float(stock['price_evn']))))-1:.2%}\n"

            if stock_id and stock['stk_no'] in stock_id:
                for data in stock['stk_dats']:
                    buy_sell = '購買' if data['buy_sell'] == 'B' else '出售'
                    inv_msg = inv_msg + f"\t\t日期：{data['t_date']}\n"
                    inv_msg = inv_msg + f"\t\t買賣：{buy_sell}\n"
                    inv_msg = inv_msg + f"\t\t價格：{data['price']}\n"
                    inv_msg = inv_msg + f"\t\t股數：{data['qty']}\n"
                    inv_msg = inv_msg + f"\t\t手續費：{data['fee']}\n"
                    inv_msg = inv_msg + f"\t\t總金額：{abs(int(data['pay_n']))}\n\n"
            else:
                inv_msg = inv_msg + "\n"

            total_msg = f"總支出：{total_cost_sum}\n"
            total_msg = total_msg + f"總市值：{total_value_now}\n"
            total_msg = total_msg + f"未實現損益：{total_value_now - total_cost_sum}\n"
            total_msg = total_msg + f"損益比：{(total_value_now/total_cost_sum)-1:.2%}"

        return f"\n{total_msg}\n=====\n{inv_msg}"
