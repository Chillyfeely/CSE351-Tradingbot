from datetime import datetime, timedelta
from strategy_factory import StrategyFactoryClient
import pandas as pd


def get_spot_market(client, symbol, interval, days):
    """Get historic market data from Binance."""
    now = datetime.utcnow()
    past = str(now - timedelta(days=days))

    bars = client.get_historical_klines(
        symbol=symbol, interval=interval, start_str=past, end_str=str(now)
    )

    df = pd.DataFrame(bars)
    df["Date"] = pd.to_datetime(df.iloc[:, 0], unit="ms")
    df.columns = [
        "Open Time",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "Clos Time",
        "Quote Asset Volume",
        "Number of Trades",
        "Taker Buy Base Asset Volume",
        "Taker Buy Quote Asset Volume",
        "Ignore",
        "Date",
    ]
    df = df[["Date", "Open", "High", "Low", "Close", "Volume"]].copy()
    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


def load_data(file_path: str) -> pd.DataFrame:
    """Load historical data from a CSV file."""
    df = pd.read_csv(file_path, parse_dates=["Date"])
    df.set_index("Date", inplace=True)
    return df


def calculate_metric(market_data: pd.DataFrame) -> float:
    """Calculate a combined metric based on volatility, momentum, and volume change."""
    if len(market_data) < 50:
        return 0

    volatility = (
        market_data["High"].iloc[-10:].mean() - market_data["Low"].iloc[-10:].mean()
    )

    momentum = market_data["Close"].iloc[-1] - market_data["Close"].iloc[-2]

    short_term_volume = market_data["Volume"].iloc[-10:].mean()
    long_term_volume = market_data["Volume"].iloc[-50:].mean()
    volume_change = short_term_volume - long_term_volume

    metric = 0.5 * volatility + 0.3 * momentum + 0.2 * volume_change
    return metric


def get_unique_rows(historical_data, new_data):
    """Combine historical and new data, remove duplicates, and return the unique rows."""
    combined_data = pd.concat([historical_data, new_data])
    unique_data = combined_data.drop_duplicates(subset="Date", keep="last")
    return unique_data


def run_trading_bot(client, bot, main_data, factory: StrategyFactoryClient):
    """Run the trading bot with the specified strategy."""
    live_data = get_spot_market(
        client=client, symbol="ETHUSDT", interval="5m", days=15 / 1440
    )

    main_data = get_unique_rows(main_data, live_data).iloc[-100:]

    metric = calculate_metric(main_data)
    strategy = factory.get_strategy(metric)
    bot.set_strategy(strategy)

    bot.run(main_data)
