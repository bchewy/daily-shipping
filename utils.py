from datetime import datetime, timedelta
import pandas as pd

def get_date_range(entries, days=30):
    df = pd.DataFrame(entries)
    df['date'] = pd.to_datetime(df['date'])
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    return df[(df['date'] >= start_date) & (df['date'] <= end_date)]

def calculate_streak(entries):
    df = pd.DataFrame(entries)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    current_streak = 0
    last_date = datetime.now().date()
    
    for date in df['date'].dt.date[::-1]:
        if (last_date - date).days == 1:
            current_streak += 1
            last_date = date
        else:
            break
    
    return current_streak
