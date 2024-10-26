import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

def calculate_metrics(entries):
    df = pd.DataFrame(entries)
    df['date'] = pd.to_datetime(df['date'])
    
    # Calculate metrics
    total_ships = len(df)
    ships_last_week = len(df[df['date'] >= datetime.now() - timedelta(days=7)])
    completion_rate = len(df[df['status'] == 'Completed']) / total_ships * 100
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Ships", total_ships)
    
    with col2:
        st.metric("Ships Last Week", ships_last_week)
    
    with col3:
        st.metric("Completion Rate", f"{completion_rate:.1f}%")

def render_project_details(entries):
    df = pd.DataFrame(entries)
    
    st.subheader("Recent Projects")
    
    for _, row in df.head(5).iterrows():
        with st.expander(f"{row['project_name']} - {row['date']}"):
            st.write(f"**Category:** {row['category']}")
            st.write(f"**Status:** {row['status']}")
            st.write(f"**Description:** {row['description']}")
