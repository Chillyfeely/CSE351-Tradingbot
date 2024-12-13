from strategies import (
    TradingStrategyInterface,
    MomentumStrategy,
    MovingAverageStrategy,
    SVMStrategy,
)
from abc import ABC, abstractmethod
import joblib


class StrategyFactoryClient(ABC):
    def __init__(self, metric: float):
        self.metric = metric
        self.strategy_instances = {
            "momentum": None,
            "moving_average": None,
            "svm": {
                "strategy": None,
                "model": None,
                "scaler": None,
            },
        }

    @abstractmethod
    def get_strategy(self, metric: float) -> TradingStrategyInterface:
        """Return a strategy based on the metric value."""

    def select_factory(self):
        if self.metric < 0.3:
            factory = MomentumStrategyFactory(self.strategy_instances)
        elif self.metric < 0.7:
            factory = MovingAverageStrategyFactory(self.strategy_instances)
        else:
            factory = SVMStrategyFactory(self.strategy_instances)

        return factory


class ConcreteStrategyFactoryClient(StrategyFactoryClient):
    def get_strategy(self, metric: float) -> TradingStrategyInterface:
        factory = self.select_factory()
        return factory.get_strategy()


class MomentumStrategyFactory(StrategyFactoryClient):
    def __init__(self, strategy_instances):
        self.strategy_instances = strategy_instances

    def get_strategy(self) -> TradingStrategyInterface:
        if self.strategy_instances["momentum"] is None:
            self.strategy_instances["momentum"] = MomentumStrategy()
        return self.strategy_instances["momentum"]


class MovingAverageStrategyFactory(StrategyFactoryClient):
    def __init__(self, strategy_instances):
        self.strategy_instances = strategy_instances

    def get_strategy(self) -> TradingStrategyInterface:
        if self.strategy_instances["moving_average"] is None:
            self.strategy_instances["moving_average"] = MovingAverageStrategy()
        return self.strategy_instances["moving_average"]


class SVMStrategyFactory(StrategyFactoryClient):
    def __init__(self, strategy_instances):
        self.strategy_instances = strategy_instances

    def get_strategy(self) -> TradingStrategyInterface:
        if self.strategy_instances["svm"]["strategy"] is None:
            if (
                self.strategy_instances["svm"]["model"] is None
                or self.strategy_instances["svm"]["scaler"] is None
            ):
                try:
                    self.strategy_instances["svm"]["model"] = joblib.load(
                        "svm_model_training/svm_model.pkl"
                    )
                    self.strategy_instances["svm"]["scaler"] = joblib.load(
                        "svm_model_training/scaler.pkl"
                    )
                except FileNotFoundError as exception:
                    raise exception
            self.strategy_instances["svm"]["strategy"] = SVMStrategy(
                model=self.strategy_instances["svm"]["model"],
                scaler=self.strategy_instances["svm"]["scaler"],
            )
        return self.strategy_instances["svm"]["strategy"]
