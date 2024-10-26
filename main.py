import streamlit as st
import pandas as pd
from database import init_db
from models import ShippingEntry, User
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

def initialize_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"

def login_form():
    st.title("🚢 Shipping Dashboard")
    
    with st.expander("Login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            user = User.authenticate(username, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.user = user
                st.success("Successfully logged in!")
                st.rerun()
            else:
                st.error("Invalid username or password")

def main():
    st.set_page_config(
        page_title="Shipping Dashboard",
        page_icon="🚢",
        layout="wide"
    )
    
    # Initialize database
    init_db()
    
    # Initialize session state
    initialize_session_state()
    
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

    # User info and login/logout
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.session_state.authenticated:
            st.write(f"Welcome, {st.session_state.user['username']} ({st.session_state.user['role']})")
        else:
            st.write("Welcome, Guest! Please login to add entries.")
    with col2:
        if st.session_state.authenticated:
            if st.button("Logout"):
                st.session_state.authenticated = False
                st.session_state.user = None
                st.rerun()
        else:
            if st.button("Login"):
                st.session_state.show_login = True
                st.rerun()

    if not st.session_state.authenticated and st.session_state.get('show_login', False):
        login_form()

    cols = st.columns([1, 1, 1, 1, 1])
    pages = {
        "📊 Dashboard": "Dashboard",
        "➕ New": "Add Entry",
        "📈 Analytics": "Analytics",
        "🏆 Awards": "Achievements",
        "💡 Ideas": "Idea Generator"
    }

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
    
    # Check achievements if authenticated
    if st.session_state.authenticated:
        check_achievements(entries)
    
    # Display content based on selected page
    if st.session_state.current_page == "Add Entry":
        if st.session_state.authenticated:
            render_entry_form()
        else:
            st.warning("Please login to add new entries.")
            login_form()
    elif st.session_state.current_page == "Dashboard":
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
