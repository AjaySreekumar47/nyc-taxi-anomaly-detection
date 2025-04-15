# NYC Taxi Anomaly Detection

## Overview
This project implements a hybrid machine learning approach for detecting anomalies in NYC taxi trip data, achieving 93% precision. The system combines statistical methods with neural networks to identify unusual patterns in transportation data and provide real-time alerts.

## Key Features
- Comprehensive data preprocessing pipeline for taxi trip data
- Multi-method anomaly detection:
  - Statistical methods (Z-score, IQR) for basic outlier detection
  - Isolation Forest for detecting point anomalies
  - LSTM Autoencoder for capturing temporal patterns
  - Hybrid approach combining all methods
- Real-time alert system for monitoring live data
- Interactive visualizations of detected anomalies
- Detailed performance evaluation metrics

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/nyc-taxi-anomaly-detection.git
cd nyc-taxi-anomaly-detection

# Create and activate a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
