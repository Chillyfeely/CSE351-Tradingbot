from typing import List
from observers import Observer
from strategies import TradingStrategyInterface
import pandas as pd
from datetime import datetime
from abc import ABC, abstractmethod


class TradingBot(ABC):
    def __init__(self, strategy: TradingStrategyInterface):
        self.strategy = strategy
        self.observers: List[Observer] = []

    def attach_observer(self, observer: Observer):
        self.observers.append(observer)

    def detach_observer(self, observer: Observer):
        self.observers.remove(observer)

    def notify_observers(self, message: str):
        for observer in self.observers:
            observer.update(message)

    def set_strategy(self, strategy: TradingStrategyInterface):
        self.strategy = strategy

    @abstractmethod
    def run(self, market_data: pd.DataFrame):
        pass

    def _get_market_info(self, market_data: pd.DataFrame) -> str:
        """Get the latest market data information from given dataframe."""
        latest_data = market_data.iloc[-1]
        return (
            f"========[{self._get_timestamp()}]========\n"
            "Latest market data:\n"
            f"OPEN: {latest_data['Open']}\n"
            f"CLOSE: {latest_data['Close']}\n"
            f"HIGH: {latest_data['High']}\n"
            f"LOW: {latest_data['Low']}\n"
            f"VOLUME: {latest_data['Volume']}\n"
        )

    def _get_timestamp(self) -> str:
        return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


class BinanceTradingBot(TradingBot):
    def run(self, market_data: pd.DataFrame):
        """Make a decision with the given market data."""
        decision = self.strategy.execute(market_data)
        market_info = self._get_market_info(market_data)
        strategy_info = (
            f"Strategy is {self.strategy.__class__.__name__}\n"
            f"Decision: {decision}\n"
            f"========[{self._get_timestamp()}]========"
        )

        self.notify_observers(market_info + strategy_info)
