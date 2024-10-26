import streamlit as st
from datetime import datetime
from models import ShippingEntry

def render_entry_form():
    st.subheader("Add New Shipping Entry")
    
    with st.form("shipping_entry_form"):
        date = st.date_input("Date", datetime.now())
        project_name = st.text_input("Project Name")
        description = st.text_area("Description")
        category = st.selectbox("Category", [
            "Feature", "Bug Fix", "Enhancement", 
            "Documentation", "Refactoring"
        ])
        status = st.selectbox("Status", [
            "Completed", "In Progress", "Planned"
        ])
        
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            if project_name and description:
                user_id = st.session_state.user['id'] if st.session_state.authenticated else None
                ShippingEntry.add_entry(
                    date, project_name, description, 
                    category, status, user_id
                )
                st.success("Entry added successfully!")
            else:
                st.error("Please fill in all required fields.")
