import os
import time
import schedule
from dotenv import load_dotenv
from binance.client import Client

from bot import BinanceTradingBot
from strategy_factory import ConcreteStrategyFactoryClient
from observers import ConsoleLogger, FileLogger, TelegramLogger
from utils import (
    get_spot_market,
    run_trading_bot,
)

if __name__ == "__main__":

    # region ENVIRONMENTAL VARIABLES
    load_dotenv()

    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    if not api_key or not api_secret:
        raise ValueError(
            "Binance API credentials are not set in the environment variables."
        )

    symbol = os.getenv("SYMBOL", "ETHUSDT")
    interval = os.getenv("INTERVAL", "5m")
    days = float(os.getenv("DAYS", 1))
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_ids = os.getenv("TELEGRAM_CHAT_IDS", "")
    observers = [
        ConsoleLogger(),
        FileLogger(os.getenv("LOG_FILE_PATH", "trading_log.txt")),
    ]
    # endregion

    # region PYTHON-BINANCE SETUP
    client = Client(api_key=api_key, api_secret=api_secret, tld="com")

    main_data = get_spot_market(
        client=client, symbol=symbol, interval=interval, days=days
    )
    # endregion

    # region BINANCE TRADINGBOT SETUP
    factory_client = ConcreteStrategyFactoryClient(metric=0)
    strategy = factory_client.get_strategy(factory_client.metric)
    bot = BinanceTradingBot(strategy)
    # endregion

    # region OBSERVERS SETUP
    if telegram_bot_token and telegram_chat_ids:
        chat_ids = telegram_chat_ids.split(",")
        for chat_id in chat_ids:
            observers.append(
                TelegramLogger(bot_token=telegram_bot_token, chat_id=chat_id.strip())
            )

    for observer in observers:
        bot.attach_observer(observer)
    # endregion

    # region INITIAL RUN
    run_trading_bot(client=client, bot=bot, main_data=main_data, factory=factory_client)
    # endregion

    # region SCHEDULED RUN
    run_interval = int(os.getenv("RUN_INTERVAL", 5))
    schedule.every(run_interval).minutes.do(
        run_trading_bot,
        client=client,
        bot=bot,
        main_data=main_data,
        factory=factory_client,
    )

    while True:
        schedule.run_pending()
        time.sleep(1)
    # endregion
