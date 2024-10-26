import streamlit as st
import pandas as pd
from models import Achievement
from datetime import datetime, timedelta

def check_achievements(entries):
    """Check and unlock achievements based on shipping entries"""
    if not entries:
        return
    
    df = pd.DataFrame(entries)
    df['date'] = pd.to_datetime(df['date'])
    
    # Check "Starter Ship"
    if len(df) >= 1:
        Achievement.unlock_achievement("Starter Ship")
    
    # Check streak achievements
    current_streak = calculate_current_streak(df)
    if current_streak >= 7:
        Achievement.unlock_achievement("Weekly Warrior")
    if current_streak >= 30:
        Achievement.unlock_achievement("Monthly Master")
    
    # Check category collection
    if len(df['category'].unique()) >= 5:  # All categories shipped
        Achievement.unlock_achievement("Category Collector")
    
    # Check daily shipping count
    daily_ships = df.groupby('date').size()
    if any(count >= 3 for count in daily_ships):
        Achievement.unlock_achievement("Speed Demon")

def calculate_current_streak(df):
    if df.empty:
        return 0
        
    df = df.sort_values('date')
    current_streak = 0
    last_date = datetime.now().date()
    
    dates = df['date'].dt.date.unique()
    dates = sorted(dates, reverse=True)
    
    for date in dates:
        if (last_date - date).days == 1:
            current_streak += 1
            last_date = date
        else:
            break
    
    return current_streak

def render_achievements():
    """Display achievements section in the dashboard"""
    st.subheader("🏆 Achievements")
    
    achievements = Achievement.get_achievements()
    
    if not achievements:
        st.info("No achievements available yet.")
        return
    
    # Create two columns for unlocked and locked achievements
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Unlocked")
        unlocked = [a for a in achievements if a['unlocked_at']]
        if unlocked:
            for achievement in unlocked:
                st.markdown(f"""
                    {achievement['badge_icon']} **{achievement['name']}**  
                    _{achievement['description']}_  
                    Unlocked: {achievement['unlocked_at'].strftime('%Y-%m-%d')}
                    ---
                """)
        else:
            st.info("No achievements unlocked yet. Keep shipping!")
    
    with col2:
        st.markdown("### Locked")
        locked = [a for a in achievements if not a['unlocked_at']]
        if locked:
            for achievement in locked:
                st.markdown(f"""
                    🔒 **{achievement['name']}**  
                    _{achievement['description']}_
                    ---
                """)
        else:
            st.success("Wow! You've unlocked all achievements! 🎉")
