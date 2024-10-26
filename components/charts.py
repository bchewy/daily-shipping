import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

def create_shipping_timeline(entries):
    """Create a timeline visualization with proper data validation"""
    df = pd.DataFrame(entries)
    
    # Check if dataframe is empty or missing required columns
    if len(df) == 0 or not all(col in df.columns for col in ['date', 'project_name']):
        fig = go.Figure()
        fig.update_layout(
            title='No timeline data available',
            xaxis_title="Date",
            yaxis_title="Project",
            showlegend=False
        )
        return fig
    
    try:
        # Ensure proper date formatting
        df['date'] = pd.to_datetime(df['date'])
        
        # Create explicit start and end dates for timeline
        df['start_date'] = df['date']
        df['end_date'] = df['date'] + pd.Timedelta(days=1)
        
        # Ensure status has a default value if missing
        if 'status' not in df.columns:
            df['status'] = 'Unknown'
        
        fig = px.timeline(
            df,
            x_start='start_date',
            x_end='end_date',
            y='project_name',
            color='status',
            title='Shipping Timeline'
        )
        
        # Update layout for better visualization
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Project",
            height=400,
            showlegend=True,
            xaxis={
                'type': 'date',
                'rangeslider_visible': False
            }
        )
        return fig
    except Exception as e:
        print(f"Error creating timeline: {e}")
        return go.Figure()

def create_category_distribution(entries):
    """Create a pie chart of categories with data validation"""
    df = pd.DataFrame(entries)
    
    # Check if dataframe is empty or missing category column
    if len(df) == 0 or 'category' not in df.columns:
        fig = go.Figure(go.Pie(labels=['No Data'], values=[1]))
        fig.update_layout(title='No categories available')
        return fig
    
    try:
        # Remove any null categories and get value counts
        category_counts = df['category'].fillna('Uncategorized').value_counts()
        
        fig = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title='Project Categories Distribution'
        )
        
        # Update layout for better visibility
        fig.update_layout(
            showlegend=True,
            height=400
        )
        return fig
    except Exception as e:
        print(f"Error creating category distribution: {e}")
        return go.Figure()

def create_shipping_frequency(entries):
    """Create a bar chart of shipping frequency with proper data validation"""
    df = pd.DataFrame(entries)
    
    # Check if dataframe is empty or missing date column
    if len(df) == 0 or 'date' not in df.columns:
        fig = go.Figure()
        fig.update_layout(
            title='No shipping data available',
            xaxis_title="Date",
            yaxis_title="Number of Shipments"
        )
        return fig
    
    try:
        # Ensure proper date formatting
        df['date'] = pd.to_datetime(df['date'])
        
        # Create date range for all dates
        if len(df) > 0:
            date_range = pd.date_range(
                start=df['date'].min(),
                end=df['date'].max(),
                freq='D'
            )
            
            # Group by date and count entries
            daily_counts = df.groupby('date').size().reindex(date_range, fill_value=0)
            
            # Create DataFrame with counts, ensuring no infinite values
            daily_df = pd.DataFrame({
                'date': daily_counts.index,
                'count': daily_counts.values
            })
            
            # Replace any potential infinite values with 0
            daily_df['count'] = daily_df['count'].replace([float('inf'), float('-inf')], 0)
            
            fig = px.bar(
                daily_df,
                x='date',
                y='count',
                title='Daily Shipping Frequency'
            )
            
            # Update layout for better visualization
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Number of Shipments",
                bargap=0.1,
                height=400,
                showlegend=False
            )
        else:
            fig = go.Figure()
            fig.update_layout(
                title='No shipping data available',
                xaxis_title="Date",
                yaxis_title="Number of Shipments"
            )
        
        return fig
    except Exception as e:
        print(f"Error creating frequency chart: {e}")
        return go.Figure()
