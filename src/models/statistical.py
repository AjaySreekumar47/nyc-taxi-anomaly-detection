import numpy as np

def z_score_anomalies(data, threshold=3):
    """
    Detect anomalies using Z-score method
    
    Parameters:
    -----------
    data : array-like
        Input data
    threshold : float
        Z-score threshold for anomaly detection
        
    Returns:
    --------
    list
        Boolean list where True indicates an anomaly
    """
    mean = np.mean(data)
    std = np.std(data)
    z_scores = [(y - mean) / std for y in data]
    return [abs(z) > threshold for z in z_scores]

def iqr_anomalies(data, multiplier=1.5):
    """
    Detect anomalies using IQR method
    
    Parameters:
    -----------
    data : array-like
        Input data
    multiplier : float
        IQR multiplier for determining outlier boundaries
        
    Returns:
    --------
    list
        Boolean list where True indicates an anomaly
    """
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_bound = q1 - (multiplier * iqr)
    upper_bound = q3 + (multiplier * iqr)
    return [(y < lower_bound) or (y > upper_bound) for y in data]