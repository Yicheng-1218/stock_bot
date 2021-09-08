from os import read
from linebot.models import TextSendMessage, FlexSendMessage
from pyquery import PyQuery as pq
from urllib.request import urlopen


def get_stock_info(sid):
    # sid 個股代號
    # 目標網站
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


# get_stock_info(2330)
