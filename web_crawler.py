from os import read
from linebot.models import TextSendMessage, FlexSendMessage
from pyquery import PyQuery as pq
from urllib.request import urlopen
from firebase import MyDataBase


class StockInfo:

    def __init__(self) -> None:
        self.db = MyDataBase()

    def __request_code(self, sid):
        # sid 個股代號
        # 目標網站
        try:
            url = f'https://tw.stock.yahoo.com/q/q?s={sid}'
            html = urlopen(url)
            html = html.read().decode('big5')
            html = pq(html)
            reply = html
        except:
            reply = -1
        return reply

    @staticmethod
    def get_stock_info(sid):
        try:
            url = f'https://tw.stock.yahoo.com/q/q?s={sid}'
            html = urlopen(url)
            html = html.read().decode('big5')
            html = pq(html)
        except:
            return TextSendMessage(f'查無代號: {sid}')

        # 檢索目標 標籤 == td && align == center
        search_term = 'td[align=center]'
        result = html(search_term).text().split()
        color = '#0abf53' if '▽' in result[6] else '#ff4c4c'
        stock = {
            'name': result[0],
            'time': result[2],
            'deal_price': result[3],
            'buying_price': result[4],
            'selling_price': result[5],
            'variation': result[6],
            'volume': result[7],
            'closeing_price': result[8],
            'opening_price': result[9],
            'highest_price': result[10],
            'lowest_price': result[11],
        }
        # print(stock)
        report = f"個股名稱: {stock['name']}, 成交價: {stock['deal_price']}, 買價: {stock['buying_price']}, 賣價: {stock['selling_price']}"
        return FlexSendMessage(
            alt_text=report,
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "股價資訊",
                            "weight": "bold",
                            "color": "#1DB446",
                            "size": "sm"
                        },
                        {
                            "type": "text",
                            "text": f"{stock['name']}",
                            "weight": "bold",
                            "size": "xxl",
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": f"時間{stock['time']}",
                            "size": "xs",
                            "color": "#aaaaaa",
                            "wrap": True
                        },
                        {
                            "type": "separator",
                            "margin": "xxl"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "xxl",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "成交價",
                                            "size": "sm",
                                            "color": "#555555",
                                            "flex": 0
                                        },
                                        {
                                            "type": "text",
                                            "text": f"${stock['deal_price']}",
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "買入",
                                            "size": "sm",
                                            "color": "#555555",
                                            "flex": 0
                                        },
                                        {
                                            "type": "text",
                                            "text": f"${stock['buying_price']}",
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "賣出",
                                            "size": "sm",
                                            "color": "#555555",
                                            "flex": 0
                                        },
                                        {
                                            "type": "text",
                                            "text": f"${stock['selling_price']}",
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "漲跌",
                                            "size": "sm",
                                            "color": "#555555",
                                            "flex": 0
                                        },
                                        {
                                            "type": "text",
                                            "text": f"{stock['variation']}",
                                            "size": "sm",
                                            "color": f"{color}",
                                            "align": "end"
                                        }
                                    ]
                                },
                                {
                                    "type": "separator",
                                    "margin": "xxl"
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "margin": "xxl",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "張數",
                                            "size": "sm",
                                            "color": "#555555"
                                        },
                                        {
                                            "type": "text",
                                            "text": f"{stock['volume']}",
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "開盤",
                                            "size": "sm",
                                            "color": "#555555"
                                        },
                                        {
                                            "type": "text",
                                            "text": f"${stock['opening_price']}",
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "昨收",
                                            "size": "sm",
                                            "color": "#555555"
                                        },
                                        {
                                            "type": "text",
                                            "text": f"${stock['closeing_price']}",
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "最高",
                                            "size": "sm",
                                            "color": "#555555"
                                        },
                                        {
                                            "type": "text",
                                            "text": f"${stock['highest_price']}",
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "最低",
                                            "size": "sm",
                                            "color": "#555555"
                                        },
                                        {
                                            "type": "text",
                                            "text": f"${stock['lowest_price']}",
                                            "size": "sm",
                                            "color": "#111111",
                                            "align": "end"
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "separator",
                            "margin": "xxl"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "md",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "資料來源",
                                    "size": "xs",
                                    "color": "#aaaaaa",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": "Yahoo股市",
                                    "color": "#aaaaaa",
                                    "size": "xs",
                                    "align": "end"
                                }
                            ]
                        }
                    ]
                },
                "styles": {
                    "footer": {
                        "separator": True
                    }
                }
            }
        )

    def get_list(self, uid):
        try:
            db_read = self.db.read('stock', uid)
            print(db_read)
            if len(db_read['data']['stocks']) == 0 or db_read['msg'] == 'document not exists':
                return TextSendMessage('尚未建立清單')
            contents = []
            stocks = db_read['data']['stocks']
            for key in stocks.keys():
                item = {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"名稱: {stocks[key]}",
                            "size": "md",
                            "color": "#555555"
                        },
                        {
                            "type": "text",
                            "text": f"代號: {key}",
                            "size": "md",
                            "color": "#555555"
                        }
                    ]
                }
                contents.append(item)

            rep = {
                "type": "bubble",
                "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "觀察清單",
                                "weight": "bold",
                                "size": "xxl",
                                "margin": "md",
                            },
                            {
                                "type": "separator",
                                "margin": "xs",
                                "color": "#787878"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "margin": "xxl",
                                "spacing": "sm",
                                "contents": contents
                            }
                        ]
                },
                "styles": {
                    "footer": {
                        "separator": True
                    }
                }
            }
            reply = FlexSendMessage(
                alt_text="觀察清單...",
                contents=rep)
        except Exception as err:
            reply = TextSendMessage(f'{err}')

        return reply

    def get_list_info(self):
        pass

    def add_code_to_list(self, sid, uid):
        html = self.__request_code(sid)
        if html != -1:
            search_term = 'td[align=center]'
            result = html(search_term).text().split()
            db_read = self.db.read('stock', uid)
            if db_read['msg'] == 'document not exists' or len(db_read['data']['stocks']) == 0:
                data = {'stocks':
                        {
                            sid: result[0].strip(sid)
                        }
                        }
                db_create = self.db.create('stock', data, uid)
            else:
                if sid in db_read['data']['stocks']:
                    return TextSendMessage(f'代號已存在: {sid}')

                new_data = db_read['data']['stocks']
                new_data[sid] = result[0].strip(sid)
                db_create = self.db.update(
                    'stock', {'stocks': new_data}, uid)
            reply = TextSendMessage(db_create['msg'])
        else:
            reply = TextSendMessage(f'查無代號: {sid}')
        return reply

    def pop_item(self, sid, uid):
        try:
            db_read: dict = self.db.read('stock', uid)[
                'data']['stocks']
            new_list = db_read.pop(sid)
            db_update = self.db.update(
                'stock', {'stocks': new_list}, uid)
            reply = TextSendMessage(db_update['msg'])
        except:
            reply = TextSendMessage('清單更新失敗')

        return reply

    @staticmethod
    def get_commands():
        return FlexSendMessage(
            alt_text='指令表...',
            contents={
                "type": "bubble",
                "size": "micro",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "指令表",
                            "weight": "bold",
                            "size": "xl",
                            "margin": "md",
                            "contents": []
                        },
                        {
                            "type": "separator",
                            "margin": "xs",
                            "color": "#787878"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "xxl",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "新增股票:",
                                            "size": "md",
                                            "color": "#555555"
                                        },
                                        {
                                            "type": "text",
                                            "text": "/a 代號",
                                            "align": "end"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "刪除股票:",
                                            "size": "md",
                                            "color": "#555555"
                                        },
                                        {
                                            "type": "text",
                                            "text": "/d 代號",
                                            "align": "end"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                "styles": {
                    "footer": {
                        "separator": True
                    }
                }
            }
        )


if __name__ == '__main__':
    s = StockInfo()
    uid = 'Uc159e2de5a6e1a5f816b44e04e15527e'
    print(s.get_list(uid))
