# Developer: Amer Aizam | I SETEL SOLUTIONS
# Version: 1.0.1
"""
Amer Aizam - Data Cleaner Pro
A Professional Data Cleaning Application using Streamlit
"""

import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Amer Aizam - Data Cleaner Pro",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS STYLING
# ============================================================
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #1E88E5;
    }
    .success-msg {
        padding: 10px;
        border-radius: 5px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .section-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #1E88E5;
    }
    .cleaning-btn {
        margin: 5px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER SECTION
# ============================================================
st.markdown('<p class="main-header">🧹 Amer Aizam - Data Cleaner Pro</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Professional Data Cleaning & Preprocessing Tool</p>', unsafe_allow_html=True)

st.divider()

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
if 'df' not in st.session_state:
    st.session_state.df = None
if 'df_cleaned' not in st.session_state:
    st.session_state.df_cleaned = None
if 'original_file_name' not in st.session_state:
    st.session_state.original_file_name = None

# ============================================================
# SIDEBAR - FILE UPLOAD SECTION
# ============================================================
st.sidebar.header("📁 Upload Your Data")

uploaded_file = st.sidebar.file_uploader(
    "Choose a file (CSV or Excel)",
    type=["csv", "xlsx", "xls"],
    help="Upload CSV or Excel files for cleaning"
)

# ============================================================
# FILE LOADING LOGIC (CSV & EXCEL SUPPORT)
# ============================================================
if uploaded_file is not None:
    file_name = uploaded_file.name
    file_extension = file_name.split(".")[-1].lower()
    st.session_state.original_file_name = file_name.replace(f".{file_extension}", "")
    
    st.sidebar.success(f"✅ Uploaded: {file_name}")
    
    try:
        # Load file based on extension
        if file_extension in ["xlsx", "xls"]:
            st.sidebar.info("📗 Reading Excel file...")
            st.session_state.df = pd.read_excel(uploaded_file)
        elif file_extension == "csv":
            st.sidebar.info("📄 Reading CSV file...")
            st.session_state.df = pd.read_csv(uploaded_file)
        else:
            st.sidebar.error("❌ Unsupported file format!")
            st.stop()
        
        # Initialize cleaned dataframe
        st.session_state.df_cleaned = st.session_state.df.copy()
        
    except Exception as e:
        st.sidebar.error(f"❌ Error reading file: {str(e)}")
        st.stop()

# ============================================================
# MAIN APPLICATION CONTENT
# ============================================================
if st.session_state.df is not None:
    
    df = st.session_state.df_cleaned
    
    # --------------------------------------------------------
    # SECTION 1: INITIAL DIAGNOSTICS
    # --------------------------------------------------------
    st.markdown('<p class="section-title">📊 Data Diagnostics</p>', unsafe_allow_html=True)
    
    # Calculate metrics
    total_rows = len(df)
    total_cols = len(df.columns)
    missing_values = df.isnull().sum().sum()
    duplicate_records = df.duplicated().sum()
    
    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📋 Total Rows", f"{total_rows:,}")
    with col2:
        st.metric("📊 Total Columns", total_cols)
    with col3:
        st.metric("❌ Missing Values", f"{missing_values:,}", 
                 delta=f"{missing_values}" if missing_values > 0 else None,
                 delta_color="inverse")
    with col4:
        st.metric("🔄 Duplicate Records", f"{duplicate_records:,}",
                 delta=f"{duplicate_records}" if duplicate_records > 0 else None,
                 delta_color="inverse")
    
    # Show detailed missing values by column
    if missing_values > 0:
        with st.expander("📋 View Missing Values by Column"):
            missing_by_col = df.isnull().sum()
            missing_by_col = missing_by_col[missing_by_col > 0].sort_values(ascending=False)
            st.dataframe(
                missing_by_col.reset_index().rename(
                    columns={'index': 'Column', 0: 'Missing Count'}
                ),
                use_container_width=True
            )
    
    st.divider()
    
    # --------------------------------------------------------
    # SECTION 2: CLEANING ACTIONS (BUTTONS)
    # --------------------------------------------------------
    st.markdown('<p class="section-title">🛠️ Cleaning Actions</p>', unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    # Button 1: Remove Missing Values (Drop NA)
    with col_btn1:
        if st.button("🗑️ Remove Missing Values", use_container_width=True, 
                    help="Drop all rows with any missing values"):
            if df.isnull().sum().sum() > 0:
                rows_before = len(df)
                st.session_state.df_cleaned = df.dropna()
                rows_after = len(st.session_state.df_cleaned)
                rows_removed = rows_before - rows_after
                
                st.success(f"✅ Removed {rows_removed} rows with missing values!")
                st.balloons()
            else:
                st.info("ℹ️ No missing values found in the dataset.")
            st.rerun()
    
    # Button 2: Handle Missing Values (Fill with Mean for Numerical Columns)
    with col_btn2:
        if st.button("🔧 Fill Missing (Mean)", use_container_width=True,
                    help="Fill missing values in numerical columns with their mean"):
            numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numerical_cols) == 0:
                st.warning("⚠️ No numerical columns found to fill.")
            else:
                filled_count = 0
                for col in numerical_cols:
                    if df[col].isnull().sum() > 0:
                        mean_value = df[col].mean()
                        st.session_state.df_cleaned[col].fillna(mean_value, inplace=True)
                        filled_count += df[col].isnull().sum()
                
                if filled_count > 0:
                    st.success(f"✅ Filled missing values in numerical columns with mean!")
                else:
                    st.info("ℹ️ No missing values found in numerical columns.")
                st.rerun()
    
    # Button 3: Remove Duplicate Records
    with col_btn3:
        if st.button("🔄 Remove Duplicates", use_container_width=True,
                    help="Remove all duplicate records from the dataset"):
            if df.duplicated().sum() > 0:
                rows_before = len(df)
                st.session_state.df_cleaned = df.drop_duplicates()
                rows_after = len(st.session_state.df_cleaned)
                rows_removed = rows_before - rows_after
                
                st.success(f"✅ Removed {rows_removed} duplicate records!")
                st.balloons()
            else:
                st.info("ℹ️ No duplicate records found in the dataset.")
            st.rerun()
    
    st.divider()
    
    # --------------------------------------------------------
    # SECTION 3: DATA PREVIEW
    # --------------------------------------------------------
    st.markdown('<p class="section-title">👁️ Data Preview</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📄 Cleaned Data", "📊 Data Info", "🔍 Sample Rows"])
    
    with tab1:
        st.write(f"**Showing {len(st.session_state.df_cleaned):,} rows × {len(st.session_state.df_cleaned.columns)} columns**")
        st.dataframe(st.session_state.df_cleaned, use_container_width=True, height=400)
    
    with tab2:
        # Data type information
        col_info = pd.DataFrame({
            'Column': st.session_state.df_cleaned.columns,
            'Data Type': st.session_state.df_cleaned.dtypes.values,
            'Non-Null Count': st.session_state.df_cleaned.count().values,
            'Null Count': st.session_state.df_cleaned.isnull().sum().values,
            'Unique Values': [st.session_state.df_cleaned[col].nunique() for col in st.session_state.df_cleaned.columns]
        })
        st.dataframe(col_info, use_container_width=True)
    
    with tab3:
        sample_size = min(10, len(st.session_state.df_cleaned))
        st.write(f"**Random Sample ({sample_size} rows):**")
        st.dataframe(st.session_state.df_cleaned.sample(sample_size), use_container_width=True)
    
    st.divider()
    
    # --------------------------------------------------------
    # SECTION 4: DOWNLOAD CLEANED DATA
    # --------------------------------------------------------
    st.markdown('<p class="section-title">💾 Export Cleaned Data</p>', unsafe_allow_html=True)
    
    # Convert dataframe to CSV for download
    csv_buffer = BytesIO()
    st.session_state.df_cleaned.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
    # Generate download filename
    download_filename = f"{st.session_state.original_file_name}_cleaned.csv"
    
    col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
    
    with col_dl2:
        st.download_button(
            label="⬇️ Download Cleaned Data (CSV)",
            data=csv_buffer.getvalue(),
            file_name=download_filename,
            mime="text/csv",
            use_container_width=True,
            help="Download the cleaned dataset as a CSV file"
        )
    
    # Summary of cleaning performed
    original_rows = len(st.session_state.df)
    cleaned_rows = len(st.session_state.df_cleaned)
    rows_difference = original_rows - cleaned_rows
    
    if rows_difference > 0:
        st.info(f"📊 **Cleaning Summary:** Removed {rows_difference} rows ({rows_difference/original_rows*100:.1f}%) from original dataset.")

else:
    # --------------------------------------------------------
    # WELCOME SCREEN (NO FILE UPLOADED)
    # --------------------------------------------------------
    st.info("👈 **Get Started:** Upload a CSV or Excel file from the sidebar to begin cleaning your data!")
    
    # Feature highlights
    st.markdown("""
    ### ✨ Features:
    - 📁 **Support for CSV & Excel files**
    - 📊 **Automatic diagnostics** (missing values & duplicates detection)
    - 🛠️ **One-click cleaning actions**:
        - Remove missing values
        - Fill missing values with mean (numerical columns)
        - Remove duplicate records
    - 💾 **Download cleaned data** as CSV
    - 🎨 **Clean, professional UI**
    """)
    
    # Demo image placeholder
    col_demo1, col_demo2, col_demo3 = st.columns(3)
    with col_demo1:
        st.metric("📁 Supported Formats", "CSV, Excel")
    with col_demo2:
        st.metric("⚡ Cleaning Speed", "Instant")
    with col_demo3:
        st.metric("💯 Free to Use", "Always")

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.markdown("""
    <p style="text-align: center; color: #888; font-size: 0.9rem;">
        🧹 <b>Amer Aizam - Data Cleaner Pro</b> | Built with ❤️ using Streamlit<br>
        Professional Data Cleaning Made Simple
    </p>
""", unsafe_allow_html=True)
