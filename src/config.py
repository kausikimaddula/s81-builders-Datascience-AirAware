# Configuration file for AirAware project
# Use environment variables to override defaults

import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
TARGET_CITY = os.getenv("TARGET_CITY", "New Delhi")
TARGET_LATITUDE = float(os.getenv("TARGET_LAT", "28.7041"))
TARGET_LONGITUDE = float(os.getenv("TARGET_LON", "77.1025"))

# Data Paths
DATA_RAW_PATH = "data/raw/"
DATA_PROCESSED_PATH = "data/processed/"
MODELS_PATH = "models/"
OUTPUTS_PATH = "outputs/"

# Model Configuration
MODEL_PATH = os.path.join(MODELS_PATH, "aqi_forecast_v1.0.pkl")
TARGET_VARIABLE = "aqi_next_day"
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Performance Targets
MAE_TARGET = 20
RMSE_TARGET = 30
R2_TARGET = 0.70

# API Configuration
API_PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
