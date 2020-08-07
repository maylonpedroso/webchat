import csv
import io
import logging
import requests

from asgiref.sync import sync_to_async
from datetime import datetime

from . import register

USERNAME = 'StockBot'

VALID_MESSAGE_TPL = "{} quote is ${} per share"
INVALID_MESSAGE_TPL = '{} is not a valid stock code'

logger = logging.getLogger(__name__)


@register.add('/stock')
async def stock_bot(stock_code):
    stock_data = await pull_stock_data(stock_code)
    stock_result = io.StringIO(stock_data)
    row = next(csv.DictReader(stock_result), {})
    if row.get('Date', 'N/D') != 'N/D':
        message = VALID_MESSAGE_TPL.format(
            row.get('Symbol'), row.get('Close')
        )
    else:
        message = INVALID_MESSAGE_TPL.format(row.get('Symbol', stock_code.upper()))
    return stock_message(message)


async def pull_stock_data(stock_code):
    try:
        response = await sync_to_async(requests.get)(
            f'https://stooq.com/q/l/?s={stock_code}&f=sd2t2ohlcv&h&e=csv'
        )
    except requests.RequestException:
        return ''
    if response.status_code == 200:
        return response.content.decode()
    else:
        return ''


def stock_message(message):
    return {
        'type': 'chat_message',
        'message': message,
        'datetime': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        'username': USERNAME,
    }
