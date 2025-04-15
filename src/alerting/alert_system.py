import numpy as np

def real_time_anomaly_detector(trip_data, isolation_forest_model, scaler, 
                              lstm_model=None, ts_scaler=None, threshold=None):
    """
    Real-time anomaly detection for taxi trips
    
    Parameters:
    -----------
    trip_data : dict
        Dictionary containing trip data
    isolation_forest_model : IsolationForest
        Trained Isolation Forest model
    scaler : StandardScaler
        Fitted scaler for feature normalization
    lstm_model : Keras Model, optional
        Trained LSTM model for time series anomaly detection
    ts_scaler : MinMaxScaler, optional
        Fitted scaler for time series data
    threshold : float, optional
        Threshold for LSTM anomaly detection
        
    Returns:
    --------
    dict
        Dictionary containing anomaly flags and explanations
    """
    # Extract and prepare features
    features = ['trip_duration', 'pickup_hour', 'pickup_dayofweek', 
                'trip_distance', 'fare_amount', 'passenger_count']
    
    # Create feature array
    features_array = []
    for feature in features:
        if feature in trip_data:
            features_array.append(trip_data[feature])
        else:
            features_array.append(0)  # Default value if missing
    
    # Scale features
    features_array = np.array(features_array).reshape(1, -1)
    features_scaled = scaler.transform(features_array)
    
    # Detect anomalies using Isolation Forest
    if_result = isolation_forest_model.predict(features_scaled)[0]
    if_anomaly = if_result == -1
    
    # Prepare result
    result = {
        'is_anomaly': if_anomaly,
        'anomaly_type': [],
        'explanation': []
    }
    
    # If it's an anomaly, determine why
    if if_anomaly:
        result['anomaly_type'].append('point_anomaly')
        
        # Check which features are unusual
        for i, feature in enumerate(features):
            if feature in trip_data:
                # This would need actual data distribution statistics in real implementation
                if feature == 'trip_duration' and trip_data[feature] > 60:
                    result['explanation'].append(f"Unusually long trip: {trip_data[feature]:.1f} minutes")
                elif feature == 'trip_distance' and trip_data[feature] > 20:
                    result['explanation'].append(f"Unusually long distance: {trip_data[feature]:.1f} miles")
                elif feature == 'fare_amount' and trip_data[feature] > 100:
                    result['explanation'].append(f"Unusually high fare: ${trip_data[feature]:.2f}")
    
    return result