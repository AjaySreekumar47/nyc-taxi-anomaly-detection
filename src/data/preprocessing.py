import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def load_taxi_data(file_path):
    """
    Load taxi data from Parquet file
    
    Parameters:
    -----------
    file_path : str
        Path to the Parquet file
        
    Returns:
    --------
    DataFrame
        Loaded taxi data
    """
    import pyarrow.parquet as pq
    return pq.read_table(file_path).to_pandas()

def preprocess_taxi_data(df, min_duration=1, max_duration=24*60, 
                         min_distance=0.1, max_distance=100, min_fare=2.5):
    """
    Preprocess taxi data by filtering out erroneous records and creating features
    
    Parameters:
    -----------
    df : DataFrame
        Raw taxi data
    min_duration : float
        Minimum allowed trip duration in minutes
    max_duration : float
        Maximum allowed trip duration in minutes
    min_distance : float
        Minimum allowed trip distance in miles
    max_distance : float
        Maximum allowed trip distance in miles
    min_fare : float
        Minimum allowed fare amount
        
    Returns:
    --------
    DataFrame
        Preprocessed taxi data
    """
    # Convert datetime columns
    if 'tpep_pickup_datetime' in df.columns:
        df['pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    elif 'pickup_datetime' in df.columns:
        df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
        
    if 'tpep_dropoff_datetime' in df.columns:
        df['dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    elif 'dropoff_datetime' in df.columns:
        df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'])
    
    # Calculate trip duration
    df['trip_duration'] = (df['dropoff_datetime'] - df['pickup_datetime']).dt.total_seconds() / 60
    
    # Apply filters
    df_filtered = df[(df['trip_duration'] >= min_duration) & (df['trip_duration'] <= max_duration)]
    
    # Filter by distance if column exists
    if 'trip_distance' in df_filtered.columns:
        df_filtered = df_filtered[
            (df_filtered['trip_distance'] >= min_distance) & 
            (df_filtered['trip_distance'] <= max_distance)
        ]
    
    # Filter by fare if column exists
    fare_column = None
    for col in ['fare_amount', 'total_amount']:
        if col in df_filtered.columns:
            fare_column = col
            break
            
    if fare_column:
        df_filtered = df_filtered[df_filtered[fare_column] >= min_fare]
    
    # Extract time-based features
    df_filtered['pickup_hour'] = df_filtered['pickup_datetime'].dt.hour
    df_filtered['pickup_day'] = df_filtered['pickup_datetime'].dt.day
    df_filtered['pickup_month'] = df_filtered['pickup_datetime'].dt.month
    df_filtered['pickup_dayofweek'] = df_filtered['pickup_datetime'].dt.dayofweek
    
    return df_filtered