import streamlit as st
import random
import pandas as pd
from models import ShippingEntry

def generate_project_idea(entries):
    """Generate a project idea based on existing entries and predefined patterns"""
    
    # Get existing project data
    df = pd.DataFrame(entries) if entries else pd.DataFrame()
    
    # Base project types
    project_types = [
        "Dashboard", "API", "CLI Tool", "Mobile App", "Browser Extension",
        "Data Visualization", "Automation Script", "Web Service"
    ]
    
    # Common tech domains
    domains = [
        "Analytics", "Productivity", "Communication", "Learning",
        "Social", "Entertainment", "Business", "Development"
    ]
    
    # Project features
    features = [
        "Real-time", "AI-powered", "Collaborative", "Cross-platform",
        "Open-source", "Cloud-based", "Customizable", "Integrated"
    ]
    
    # Get unique categories from existing projects if available
    if not df.empty and 'category' in df.columns:
        existing_categories = df['category'].unique().tolist()
    else:
        existing_categories = ["Feature", "Enhancement", "Integration"]
    
    # Generate random combinations
    project_type = random.choice(project_types)
    domain = random.choice(domains)
    feature = random.choice(features)
    category = random.choice(existing_categories)
    
    # Generate project name
    name_patterns = [
        f"{feature} {domain} {project_type}",
        f"{domain} {project_type} with {feature} capabilities",
        f"{feature} {project_type} for {domain}",
    ]
    
    project_name = random.choice(name_patterns)
    
    # Generate description patterns
    desc_patterns = [
        f"Create a {feature.lower()} {project_type.lower()} that helps users with {domain.lower()} tasks.",
        f"Build a {domain.lower()}-focused {project_type.lower()} that leverages {feature.lower()} technology.",
        f"Develop a {feature.lower()} solution for {domain.lower()} using {project_type.lower()} architecture."
    ]
    
    description = random.choice(desc_patterns)
    
    return {
        "name": project_name,
        "description": description,
        "category": category,
        "type": project_type,
        "domain": domain,
        "feature": feature
    }

def render_idea_generator():
    st.subheader("🎯 Project Idea Generator")
    
    # Get existing entries for context
    entries = ShippingEntry.get_all_entries()
    
    # Add description
    st.markdown("""
    Need inspiration for your next project? This idea generator combines various project types, 
    domains, and features to create unique project suggestions. Click the button below to generate 
    new ideas!
    """)
    
    if st.button("🎲 Generate New Idea"):
        idea = generate_project_idea(entries)
        
        # Display the generated idea in a card-like container
        with st.container():
            st.markdown("### 💡 Generated Project Idea")
            st.markdown(f"**{idea['name']}**")
            
            st.markdown("#### 📝 Description")
            st.write(idea['description'])
            
            # Create three columns for metadata
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Category:**")
                st.info(idea['category'])
            
            with col2:
                st.markdown("**Domain:**")
                st.info(idea['domain'])
            
            with col3:
                st.markdown("**Key Feature:**")
                st.info(idea['feature'])
            
            # Add a quick-start button
            if st.button("📝 Use This Idea"):
                st.session_state['new_project_name'] = idea['name']
                st.session_state['new_project_description'] = idea['description']
                st.session_state['new_project_category'] = idea['category']
                st.success("Great! Head to the 'Add Entry' page to start shipping this idea!")
