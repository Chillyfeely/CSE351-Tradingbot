import pandas as pd
import numpy as np
from interface import implements, Interface


class TradingStrategyInterface(Interface):
    def execute(self, market_data: pd.DataFrame) -> str:
        """
        Process the DataFrame and return 'BUY', 'SELL', or 'HOLD' for the latest data point.
        """
        pass


class MomentumStrategy(implements(TradingStrategyInterface)):
    def execute(self, market_data: pd.DataFrame) -> str:
        if len(market_data) < 2:
            return "HOLD"
        momentum = market_data["Close"].iloc[-1] - market_data["Close"].iloc[-2]
        return "BUY" if momentum > 0 else "SELL" if momentum < 0 else "HOLD"


class MovingAverageStrategy(implements(TradingStrategyInterface)):
    def execute(self, market_data: pd.DataFrame) -> str:
        if len(market_data) < 50:
            return "HOLD"
        sma_20 = market_data["Close"].iloc[-20:].mean()
        sma_50 = market_data["Close"].iloc[-50:].mean()
        return "BUY" if sma_20 > sma_50 else "SELL" if sma_20 < sma_50 else "HOLD"


class SVMStrategy(implements(TradingStrategyInterface)):
    def __init__(self, model, scaler):
        self.model = model
        self.scaler = scaler

    def execute(self, market_data: pd.DataFrame) -> str:
        if len(market_data) < 50:
            return "HOLD"

        features = self.__extract_features(market_data)
        scaled_features = self.scaler.transform([features])
        prediction = self.model.predict(scaled_features)[0]
        return {0: "BUY", 1: "SELL", 2: "HOLD"}[prediction]

    def __extract_features(self, market_data: pd.DataFrame) -> np.ndarray:
        close_prices = market_data["Close"]
        sma_20 = close_prices.iloc[-20:].mean()
        sma_50 = close_prices.iloc[-50:].mean()
        momentum = close_prices.iloc[-1] - close_prices.iloc[-2]
        return np.array(
            [
                market_data["Open"].iloc[-1],
                market_data["High"].iloc[-1],
                market_data["Low"].iloc[-1],
                market_data["Close"].iloc[-1],
                market_data["Volume"].iloc[-1],
                momentum,
                sma_20,
                sma_50,
            ]
        )
