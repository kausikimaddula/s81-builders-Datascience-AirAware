"""
AirAware Flask Backend Application

Simple REST API for serving air quality forecasts and current data.

Run: python app/app.py
"""

import logging
from flask import Flask, jsonify, render_template
from flask_cors import CORS
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# TODO: Import inference function once model is trained
# from src.inference import predict_next_day_aqi


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "AirAware API"}), 200


@app.route("/api/current", methods=["GET"])
def get_current_aqi():
    """
    Get current air quality for target city.
    
    Returns:
        JSON with fields: aqi, pm25, status, timestamp, recommendation
    """
    # TODO: Implement function to load latest data from data/processed/
    
    return jsonify({
        "location": "New Delhi",
        "aqi": 145,
        "pm25": 45.3,
        "status": "Moderate",
        "recommendation": "Sensitive groups should limit outdoor activities",
        "timestamp": "2024-01-16T10:30:00Z",
    }), 200


@app.route("/api/forecast", methods=["GET"])
def get_forecast():
    """
    Get next-day AQI forecast.
    
    Returns:
        JSON with fields: aqi_forecast, aqi_forecast_lower, aqi_forecast_upper, 
        recommendation, confidence
    """
    # TODO: Call inference function with latest features
    
    return jsonify({
        "aqi_forecast": 152,
        "aqi_forecast_lower": 137,
        "aqi_forecast_upper": 167,
        "recommendation": "Moderate; plan indoor activities",
        "confidence": "±15",
        "timestamp": "2024-01-16T10:30:00Z",
    }), 200


@app.route("/api/history", methods=["GET"])
def get_history():
    """
    Get historical AQI data (last 30 days).
    
    Returns:
        JSON with array of {date, aqi, status}
    """
    # TODO: Load historical data from data/processed/
    
    return jsonify({
        "data": [
            {"date": "2024-01-16", "aqi": 145, "status": "Moderate"},
            {"date": "2024-01-15", "aqi": 142, "status": "Moderate"},
            # ... more historical points
        ],
        "count": 30,
    }), 200


@app.route("/", methods=["GET"])
def index():
    """Serve dashboard HTML."""
    # TODO: Create HTML dashboard template in templates/index.html
    
    return """
    <html>
        <head>
            <title>AirAware Dashboard</title>
            <style>
                body { font-family: Arial; margin: 20px; }
                .metric { font-size: 24px; font-weight: bold; margin: 10px; }
                .moderate { color: orange; }
            </style>
        </head>
        <body>
            <h1>🌍 AirAware Air Quality Dashboard</h1>
            <div class="metric">
                Current AQI: <span class="moderate">145 (Moderate)</span>
            </div>
            <div class="metric">
                Tomorrow's Forecast: <span class="moderate">152 (Moderate)</span>
            </div>
            <p><a href="/api/current">View JSON Data</a></p>
        </body>
    </html>
    """


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
