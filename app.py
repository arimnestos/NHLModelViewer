import streamlit as st
import pandas as pd
import os
from datetime import datetime, date, timedelta

# Set page config
st.set_page_config(
    page_title="NHL Model Viewer",
    page_icon="🏒",
    layout="wide"
)

# File path to the Excel model
FILE_PATH = 'NHL Model 2025.xlsx'  # Local file in the same directory
SHEET_NAME = '2026'

@st.cache_data(ttl=300)  # Cache data for 5 minutes
def load_data():
    """Load and process NHL model data from Excel file."""
    if not os.path.exists(FILE_PATH):
        return None
    
    try:
        # Read the file, skipping the first 62 rows (so row 63 is the header)
        df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME, header=0, skiprows=62)
        
        # Select specific columns by index (0-based)
        # C=2 (Date), D=3 (H/A), E=4 (Team), J=9 (Goalie), AR=43 (Adj Fair), AS=44 (Confidence), BB=53 (Model Fair)
        target_indices = [2, 3, 4, 9, 43, 44, 53]
        
        # Verify we have enough columns
        if df.shape[1] <= max(target_indices):
            st.error(f"Error: File has fewer columns ({df.shape[1]}) than expected.")
            return None
            
        final_df = df.iloc[:, target_indices].copy()
        
        # Rename columns to be user-friendly
        final_df.columns = [
            'game_date', 
            'H / A', 
            'Team', 
            'Starting Goalie', 
            'ADJ TO FAIR', 
            'Confidence', 
            'Our Model Fair Values'
        ]
        
        # Filter out rows with no Team or Date (empty rows)
        final_df = final_df.dropna(subset=['Team', 'game_date'])
        
        # Ensure date format
        final_df['game_date'] = pd.to_datetime(final_df['game_date'], errors='coerce')
        
        return final_df
        
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

# --- Main App ---

st.title("🏒 NHL Model Data")

if st.button("Reload Data"):
    st.cache_data.clear()
    st.rerun()

df = load_data()

if df is not None:
    # Get today and tomorrow
    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    # Filter for today and tomorrow
    filtered_df = df[
        (df['game_date'].dt.date == today) | 
        (df['game_date'].dt.date == tomorrow)
    ].copy()
    
    # Sort by date
    filtered_df = filtered_df.sort_values('game_date')
    
    # Display
    st.header(f"Games for Today & Tomorrow")
    st.caption(f"{today.strftime('%b %d, %Y')} and {tomorrow.strftime('%b %d, %Y')}")
    
    if not filtered_df.empty:
        # Group by date for better display
        for game_date in [today, tomorrow]:
            games_on_date = filtered_df[filtered_df['game_date'].dt.date == game_date]
            
            if not games_on_date.empty:
                st.subheader(f"📅 {game_date.strftime('%A, %B %d')}")
                
                st.dataframe(
                    games_on_date,
                    column_config={
                        "game_date": None,  # Hide date column since we're showing it in header
                        "H / A": st.column_config.TextColumn("H/A", width="small"),
                        "Team": st.column_config.TextColumn("Team", width="small"),
                        "Starting Goalie": "Goalie",
                        "ADJ TO FAIR": st.column_config.NumberColumn("Adj Fair", format="%.2f"),
                        "Confidence": st.column_config.NumberColumn("Confidence", format="%.2f"),
                        "Our Model Fair Values": st.column_config.NumberColumn("Model Fair", format="%.0f"),
                    },
                    hide_index=True,
                    use_container_width=True
                )
    else:
        st.info("No games found for today or tomorrow.")
        
    # Show Raw Data option
    with st.expander("See All Games"):
        st.dataframe(df, hide_index=True, use_container_width=True)
else:
    st.warning("Please check if the Excel file exists at the specified path.")
    st.info(f"Looking for: {FILE_PATH}")
