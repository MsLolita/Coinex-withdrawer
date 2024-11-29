import asyncio
import ctypes
import random
import sys
import traceback

import ccxt.async_support as ccxt
from art import text2art
from termcolor import colored, cprint

from core import Coinex
from core.autoreger import AutoReger
from core.utils import logger
from data.config import ADDRESSES_FILE_PATH, THREADS, ACCESS_ID, SECRET_KEY, TICKER, AMOUNT, CHAIN, DELAY


def bot_info(name: str = ""):
    cprint(text2art(name), 'green')

    if sys.platform == 'win32':
        ctypes.windll.kernel32.SetConsoleTitleW(f"{name}")

    print(
        f"{colored('EnJoYeR <crypto/> moves:', color='light_yellow')} "
        f"{colored('https://t.me/+tdC-PXRzhnczNDli', color='light_green')}"
    )


async def worker_task(_id, address: str):
    coinex = None

    try:
        coinex = Coinex(ACCESS_ID, SECRET_KEY)

        response = await coinex.withdraw(TICKER, get_random_amount(*AMOUNT), address, params={"chain": CHAIN})
        resp_info = response['info']
        explorer = resp_info['explorer_tx_url']
        amount = resp_info['amount']
        fees = resp_info['fee_amount']
        actual_amount = resp_info['actual_amount']

        logger.info(f"{_id} | Withdraw {actual_amount} {TICKER} ({amount} (cost) - {fees} (fees)) to {address} | {explorer}")
        return True
    except ccxt.ExchangeError as e:
        logger.error(f"{_id} | Exchange error: {e} | {traceback.format_exc()}")
    except Exception as e:
        logger.error(f"{_id} | not handled exception | error: {e} {traceback.format_exc()}")
    finally:
        if coinex:
            await coinex.exchange.close()


def get_random_amount(start, end, increased_decimal_on: int = 2):
    start_float = float(start)
    end_float = float(end)

    start_has_decimal = '.' in str(start)
    end_has_decimal = '.' in str(end)

    random_float = random.uniform(start_float, end_float)

    if start_has_decimal or end_has_decimal:
        max_decimal_places = max(len(str(start).split('.')[1]), len(str(end).split('.')[1]))
        random_number = round(random_float, max_decimal_places + increased_decimal_on)
    else:
        random_number = round(random_float, increased_decimal_on)

    return random_number


async def main():
    autoreger = AutoReger.get_accounts(
        (ADDRESSES_FILE_PATH, ),
        with_id=True
    )

    if autoreger:
        await autoreger.start(worker_task, THREADS, delay=DELAY)


if __name__ == "__main__":
    bot_info("COINEX_WITHDRAWER")

    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
