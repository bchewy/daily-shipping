from datetime import datetime, timedelta
import pandas as pd

def get_date_range(entries, days=30):
    df = pd.DataFrame(entries)
    if len(entries) > 0 and 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        return df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    return df

def calculate_streak(entries):
    if not entries:
        return 0
        
    df = pd.DataFrame(entries)
    if 'date' not in df.columns or len(df) == 0:
        return 0
        
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    current_streak = 0
    last_date = datetime.now().date()
    
    dates = df['date'].dt.date.tolist()
    if not dates:
        return 0
        
    for date in dates[::-1]:
        if (last_date - date).days == 1:
            current_streak += 1
            last_date = date
        else:
            break
    
    return current_streak
