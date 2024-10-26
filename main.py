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
from components.achievements import check_achievements, render_achievements
from components.idea_generator import render_idea_generator
from utils import get_date_range, calculate_streak

def main():
    st.set_page_config(
        page_title="Shipping Dashboard",
        page_icon="🚢",
        layout="wide"
    )
    
    # Initialize database
    init_db()
    
    # Navigation menu with icons
    st.markdown("""
        <style>
        .nav-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            padding: 10px;
            background-color: #f0f2f6;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .nav-item {
            display: flex;
            align-items: center;
            padding: 8px 16px;
            border-radius: 5px;
            text-decoration: none;
            color: #262730;
            cursor: pointer;
        }
        .nav-item:hover {
            background-color: #e0e2e6;
        }
        .nav-item.active {
            background-color: #FF4B4B;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    cols = st.columns([1, 1, 1, 1, 1])
    pages = {
        "📊 Dashboard": "Dashboard",
        "➕ New": "Add Entry",
        "📈 Analytics": "Analytics",
        "🏆 Awards": "Achievements",
        "💡 Ideas": "Idea Generator"
    }

    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"

    for idx, (icon_label, page_name) in enumerate(pages.items()):
        with cols[idx]:
            if st.button(
                icon_label,
                key=f"nav_{page_name}",
                use_container_width=True,
                type="primary" if st.session_state.current_page == page_name else "secondary"
            ):
                st.session_state.current_page = page_name
                st.rerun()

    st.markdown("---")  # Divider between navigation and content
    
    # Get all entries
    entries = ShippingEntry.get_all_entries()
    
    # Check achievements
    check_achievements(entries)
    
    # Display content based on selected page
    if st.session_state.current_page == "Dashboard":
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
    
    elif st.session_state.current_page == "Add Entry":
        render_entry_form()
    
    elif st.session_state.current_page == "Achievements":
        render_achievements()
    
    elif st.session_state.current_page == "Idea Generator":
        render_idea_generator()
    
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
