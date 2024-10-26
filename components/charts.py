import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

def create_shipping_timeline(entries):
    df = pd.DataFrame(entries)
    if len(df) > 0 and 'date' in df.columns and 'project_name' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        fig = px.timeline(
            df,
            x_start='date',
            y='project_name',
            color='status',
            title='Shipping Timeline'
        )
        return fig
    return px.timeline(title='No data available')

def create_category_distribution(entries):
    df = pd.DataFrame(entries)
    if len(df) > 0 and 'category' in df.columns:
        category_counts = df['category'].value_counts()
        fig = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title='Project Categories Distribution'
        )
        return fig
    return px.pie(title='No categories available')

def create_shipping_frequency(entries):
    df = pd.DataFrame(entries)
    if len(df) > 0 and 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        
        # Group by date and count entries
        daily_counts = df.groupby('date').size().reset_index(name='count')
        
        fig = px.bar(
            daily_counts,
            x='date',
            y='count',
            title='Daily Shipping Frequency'
        )
        return fig
    return px.bar(title='No shipping data available')
