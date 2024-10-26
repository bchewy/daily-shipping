import streamlit as st
import pandas as pd
from database import init_db
from models import ShippingEntry
from components.forms import render_entry_form
from components.charts import (
    create_shipping_timeline,
    create_category_distribution,
    create_shipping_frequency
)
from components.analytics import calculate_metrics, render_project_details
from utils import get_date_range, calculate_streak

def main():
    st.set_page_config(
        page_title="Shipping Dashboard",
        page_icon="🚢",
        layout="wide"
    )
    
    # Initialize database
    init_db()
    
    # Page header
    st.title("🚢 Daily Shipping Dashboard")
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Add Entry", "Analytics"])
    
    # Get all entries
    entries = ShippingEntry.get_all_entries()
    
    if page == "Dashboard":
        # Display metrics
        calculate_metrics(entries)
        
        # Display current streak
        streak = calculate_streak(entries)
        st.info(f"🔥 Current Shipping Streak: {streak} days")
        
        # Create two columns for charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Timeline chart
            st.plotly_chart(
                create_shipping_timeline(
                    get_date_range(entries, 30)
                ),
                use_container_width=True
            )
        
        with col2:
            # Category distribution
            st.plotly_chart(
                create_category_distribution(entries),
                use_container_width=True
            )
        
        # Shipping frequency
        st.plotly_chart(
            create_shipping_frequency(entries),
            use_container_width=True
        )
        
        # Project details
        render_project_details(entries)
    
    elif page == "Add Entry":
        render_entry_form()
    
    else:  # Analytics
        st.subheader("Shipping Analytics")
        
        # Additional analytics and insights
        df = pd.DataFrame(entries)
        
        # Most productive day
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            df['day_of_week'] = df['date'].dt.day_name()
            productive_day = df['day_of_week'].mode().iloc[0]
            st.info(f"Most productive day: {productive_day}")
        
        # Category breakdown
        st.subheader("Category Breakdown")
        if not df.empty:
            category_stats = df['category'].value_counts()
            st.bar_chart(category_stats)

if __name__ == "__main__":
    main()
