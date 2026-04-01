"""
AirAware Data Fetching Module

Fetches air quality and weather data from APIs and stores in data/raw/

Usage:
    python src/fetch_data.py --mode historical --days 365
    python src/fetch_data.py --mode daily
"""

import argparse
import logging
import pandas as pd
from datetime import datetime, timedelta
from src.config import TARGET_CITY, DATA_RAW_PATH, OPENWEATHER_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_air_quality_historical(days: int = 365) -> pd.DataFrame:
    """
    Fetch historical air quality data from OpenWeatherMap API.
    
    Args:
        days: Number of historical days to fetch
        
    Returns:
        DataFrame with columns: date, aqi, pm25, pm10, location, latitude, longitude
    """
    logger.info(f"Fetching {days} days of historical air quality data...")
    
    # TODO: Implement API call to OpenWeatherMap Air Pollution API
    # See: https://openweathermap.org/api/air-pollution
    
    # Placeholder: Return empty DataFrame
    return pd.DataFrame({
        'date': pd.date_range(end=datetime.now(), periods=days),
        'aqi': [0] * days,  # Placeholder
        'pm25': [0.0] * days,
        'pm10': [0.0] * days,
        'location': TARGET_CITY,
        'latitude': 28.7041,
        'longitude': 77.1025,
    })


def fetch_weather_data(days: int = 365) -> pd.DataFrame:
    """
    Fetch weather data from OpenWeatherMap API.
    
    Args:
        days: Number of historical days to fetch
        
    Returns:
        DataFrame with columns: date, temp_max, temp_min, humidity, wind_speed, precipitation
    """
    logger.info(f"Fetching {days} days of weather data...")
    
    # TODO: Implement API call to OpenWeatherMap Weather API
    
    # Placeholder: Return empty DataFrame
    return pd.DataFrame({
        'date': pd.date_range(end=datetime.now(), periods=days),
        'temp_max': [25.0] * days,  # Placeholder
        'temp_min': [15.0] * days,
        'humidity': [65] * days,
        'wind_speed': [10.0] * days,
        'precipitation': [0.0] * days,
    })


def validate_data(df: pd.DataFrame) -> bool:
    """Validate fetched data against schema expectations."""
    logger.info("Validating data schema...")
    
    # Check required columns
    required_cols = ['date', 'aqi', 'pm25', 'pm10']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        logger.error(f"Missing required columns: {missing}")
        return False
    
    # Check data types
    if not pd.api.types.is_datetime64_any_dtype(df['date']):
        logger.error("'date' column is not datetime type")
        return False
    
    logger.info(f"✓ Data validation passed ({len(df)} rows)")
    return True


def save_data(df: pd.DataFrame, filename: str, mode: str) -> None:
    """Save data to CSV file."""
    filepath = f"{DATA_RAW_PATH}{filename}"
    df.to_csv(filepath, index=False)
    logger.info(f"✓ Saved {len(df)} rows to {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch air quality and weather data for AirAware"
    )
    parser.add_argument(
        "--mode",
        choices=["historical", "daily"],
        default="daily",
        help="Fetch mode: historical (full dataset) or daily (update)",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=365,
        help="Number of historical days to fetch (for historical mode)",
    )
    
    args = parser.parse_args()
    
    try:
        if args.mode == "historical":
            logger.info(f"Fetching {args.days} days of historical data...")
            aqi_df = fetch_air_quality_historical(days=args.days)
            weather_df = fetch_weather_data(days=args.days)
            
            # Merge on date
            merged_df = aqi_df.merge(weather_df, on='date', how='inner')
            
            if validate_data(merged_df):
                save_data(merged_df, "historical_aqi_weather.csv", "historical")
                logger.info(f"✓ Successfully fetched and saved {args.days} days of data")
        
        elif args.mode == "daily":
            logger.info("Fetching today's data...")
            # For daily mode, fetch last 2 days to ensure data availability
            aqi_df = fetch_air_quality_historical(days=2)
            weather_df = fetch_weather_data(days=2)
            merged_df = aqi_df.merge(weather_df, on='date', how='inner')
            
            if validate_data(merged_df):
                save_data(merged_df, "daily_aqi_weather.csv", "daily")
                logger.info("✓ Successfully fetched and saved today's data")
    
    except Exception as e:
        logger.error(f"✗ Data fetch failed: {e}")
        raise


if __name__ == "__main__":
    main()
