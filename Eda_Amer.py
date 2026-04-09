# Developer: Amer Aizam | I SETEL SOLUTIONS
# Version: 1.0.1
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

# ============================================================
# STREAMLIT EDA APPLICATION - Complete Data Explorer
# ============================================================

# Page configuration
st.set_page_config(
    page_title="Complete EDA App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2196F3;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .info-text {
        font-size: 1rem;
        color: #666;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown('<p class="main-header">📊 Complete EDA Application</p>', unsafe_allow_html=True)
st.markdown("""
    <p style="text-align: center; color: #666;">
        Upload your CSV or Excel file to explore and visualize your data interactively.
    </p>
""", unsafe_allow_html=True)

st.divider()

# ============================================================
# TASK 1a: FILE UPLOAD WITH CSV/EXCEL SUPPORT
# ============================================================
st.sidebar.header("📁 File Upload")

uploaded_file = st.sidebar.file_uploader(
    "Choose a file",
    type=["csv", "xlsx", "xls"],
    help="Upload a CSV or Excel file to begin analysis"
)

# Initialize data variable
data = None

if uploaded_file is not None:
    # Get file name and extension
    file_name = uploaded_file.name
    file_extension = file_name.split(".")[-1].lower()
    
    # Show file info
    st.sidebar.success(f"✅ Uploaded: {file_name}")
    
    # ============================================================
    # IF-ELSE LOGIC BASED ON FILE EXTENSION
    # ============================================================
    try:
        if file_extension in ["xlsx", "xls"]:
            # Excel file: use pd.read_excel()
            st.sidebar.info("📗 Detected: Excel file")
            data = pd.read_excel(uploaded_file)
            
        elif file_extension == "csv":
            # CSV file: use pd.read_csv()
            st.sidebar.info("📄 Detected: CSV file")
            data = pd.read_csv(uploaded_file)
            
        else:
            st.sidebar.error("❌ Unsupported file format!")
            st.stop()
            
    except Exception as e:
        st.sidebar.error(f"❌ Error reading file: {str(e)}")
        st.stop()

else:
    # Show instructions when no file is uploaded
    st.info("👈 Please upload a file from the sidebar to get started!")
    
    # Sample data option for demo
    if st.button("🎲 Load Sample Data (for demo)"):
        np.random.seed(42)
        n_samples = 500
        
        data = pd.DataFrame({
            'Age': np.random.randint(18, 80, n_samples),
            'Salary': np.random.normal(50000, 15000, n_samples).astype(int),
            'Experience': np.random.randint(0, 40, n_samples),
            'Department': np.random.choice(['IT', 'HR', 'Sales', 'Marketing', 'Finance'], n_samples),
            'Satisfaction': np.random.uniform(1, 10, n_samples).round(2),
            'Promoted': np.random.choice([True, False], n_samples, p=[0.3, 0.7])
        })
        
        st.success("✅ Sample data loaded! Upload your own file to analyze real data.")
        st.balloons()

# ============================================================
# MAIN ANALYSIS SECTION
# ============================================================
if data is not None:
    
    # --------------------------------------------------------
    # BASIC DATA INFO
    # --------------------------------------------------------
    st.markdown('<p class="sub-header">📋 Dataset Overview</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Rows", f"{data.shape[0]:,}")
    with col2:
        st.metric("Total Columns", data.shape[1])
    with col3:
        st.metric("Missing Values", f"{data.isnull().sum().sum():,}")
    with col4:
        st.metric("Duplicate Rows", data.duplicated().sum())
    
    # Data preview with tabs
    tab1, tab2, tab3 = st.tabs(["📄 Data Preview", "📊 Column Info", "🔍 Sample Data"])
    
    with tab1:
        st.dataframe(data, use_container_width=True, height=300)
    
    with tab2:
        # Create column info dataframe
        col_info = pd.DataFrame({
            'Column': data.columns,
            'Data Type': data.dtypes.values,
            'Non-Null Count': data.count().values,
            'Null Count': data.isnull().sum().values,
            'Unique Values': [data[col].nunique() for col in data.columns]
        })
        st.dataframe(col_info, use_container_width=True)
    
    with tab3:
        st.write("**Random Sample (10 rows):**")
        st.dataframe(data.sample(min(10, len(data))), use_container_width=True)
    
    st.divider()
    
    # --------------------------------------------------------
    # TASK 1b: HANDLING SUMMARIES WITH CATEGORICAL CHECK
    # --------------------------------------------------------
    st.markdown('<p class="sub-header">📈 Statistical Summaries</p>', unsafe_allow_html=True)
    
    # Numerical Summary (always show)
    st.subheader("🔢 Numerical Features Summary")
    numerical_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    
    if numerical_cols:
        st.dataframe(data[numerical_cols].describe().T, use_container_width=True)
    else:
        st.info("ℹ️ No numerical columns found in the dataset.")
    
    # Categorical Summary (with existence check)
    st.subheader("🏷️ Categorical Features Summary")
    
    # Check if categorical/non-numerical columns exist
    categorical_cols = data.select_dtypes(include=['object', 'bool', 'category']).columns.tolist()
    
    if len(categorical_cols) > 0:
        # Safe to generate summary - categorical columns exist
        try:
            cat_summary = data[categorical_cols].describe(include=['object', 'bool', 'category']).T
            st.dataframe(cat_summary, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not generate categorical summary: {str(e)}")
    else:
        # No categorical columns - skip gracefully without errors
        st.info("ℹ️ No categorical/non-numerical columns found. Skipping categorical summary.")
    
    st.divider()
    
    # ============================================================
    # TASK 1c: INTERACTIVE VISUALIZATIONS
    # ============================================================
    st.markdown('<p class="sub-header">📊 Interactive Visualizations</p>', unsafe_allow_html=True)
    
    # Sidebar controls for visualizations
    st.sidebar.markdown("---")
    st.sidebar.header("🎨 Visualization Settings")
    
    # Select only numerical columns for certain plots
    num_cols_for_viz = data.select_dtypes(include=[np.number]).columns.tolist()
    
    # --------------------------------------------------------
    # VISUALIZATION 1: CORRELATION HEATMAP
    # --------------------------------------------------------
    if len(num_cols_for_viz) >= 2:
        st.subheader("🌡️ Correlation Heatmap")
        
        with st.expander("⚙️ Heatmap Settings", expanded=True):
            col_h1, col_h2 = st.columns(2)
            with col_h1:
                heatmap_method = st.selectbox(
                    "Correlation Method",
                    ["pearson", "spearman", "kendall"],
                    help="Pearson: linear correlation, Spearman: rank-based, Kendall: ordinal"
                )
            with col_h2:
                annot_heatmap = st.checkbox("Show Values on Heatmap", value=True)
        
        # Create correlation matrix
        corr_matrix = data[num_cols_for_viz].corr(method=heatmap_method)
        
        # Create heatmap using Seaborn
        fig, ax = plt.subplots(figsize=(10, 8))
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        
        sns.heatmap(
            corr_matrix,
            mask=mask,
            annot=annot_heatmap,
            fmt='.2f',
            cmap='RdYlBu_r',
            center=0,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.8},
            ax=ax
        )
        plt.title(f'{heatmap_method.capitalize()} Correlation Heatmap', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        st.pyplot(fig)
        
        # Show correlation values as table
        with st.expander("📋 View Correlation Matrix Data"):
            st.dataframe(corr_matrix.style.background_gradient(cmap='RdYlBu_r', axis=None), 
                        use_container_width=True)
    else:
        st.info("ℹ️ Need at least 2 numerical columns to generate correlation heatmap.")
    
    st.divider()
    
    # --------------------------------------------------------
    # VISUALIZATION 2: HISTOGRAM
    # --------------------------------------------------------
    if num_cols_for_viz:
        st.subheader("📊 Histogram Distribution")
        
        with st.expander("⚙️ Histogram Settings", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                hist_column = st.selectbox(
                    "Select Column for Histogram",
                    num_cols_for_viz,
                    help="Choose a numerical column to visualize its distribution"
                )
            
            with col2:
                bins = st.slider("Number of Bins", min_value=5, max_value=100, value=30)
            
            with col3:
                hist_color = st.color_picker("Histogram Color", "#4CAF50")
        
        # Create histogram
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot histogram with KDE
        sns.histplot(
            data=data,
            x=hist_column,
            bins=bins,
            kde=True,
            color=hist_color,
            alpha=0.7,
            ax=ax
        )
        
        plt.title(f'Distribution of {hist_column}', fontsize=14, fontweight='bold')
        plt.xlabel(hist_column, fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        st.pyplot(fig)
        
        # Show statistics for the selected column
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        with col_stat1:
            st.metric("Mean", f"{data[hist_column].mean():.2f}")
        with col_stat2:
            st.metric("Median", f"{data[hist_column].median():.2f}")
        with col_stat3:
            st.metric("Std Dev", f"{data[hist_column].std():.2f}")
        with col_stat4:
            st.metric("Skewness", f"{data[hist_column].skew():.2f}")
    else:
        st.info("ℹ️ No numerical columns available for histogram.")
    
    st.divider()
    
    # --------------------------------------------------------
    # VISUALIZATION 3: SCATTER PLOT
    # --------------------------------------------------------
    if len(num_cols_for_viz) >= 2:
        st.subheader("⚡ Scatter Plot")
        
        with st.expander("⚙️ Scatter Plot Settings", expanded=True):
            col_s1, col_s2, col_s3 = st.columns(3)
            
            with col_s1:
                x_column = st.selectbox(
                    "X-Axis",
                    num_cols_for_viz,
                    index=0,
                    help="Select column for X-axis"
                )
            
            with col_s2:
                # Default to second column, different from first
                default_y_index = 1 if len(num_cols_for_viz) > 1 else 0
                y_column = st.selectbox(
                    "Y-Axis",
                    num_cols_for_viz,
                    index=default_y_index,
                    help="Select column for Y-axis"
                )
            
            with col_s3:
                # Optional color by categorical column
                color_options = ["None"] + categorical_cols
                color_by = st.selectbox(
                    "Color By (Optional)",
                    color_options,
                    help="Color points by a categorical variable"
                )
        
        # Create scatter plot
        fig, ax = plt.subplots(figsize=(10, 7))
        
        if color_by != "None" and color_by in data.columns:
            # Scatter with color coding
            scatter = sns.scatterplot(
                data=data,
                x=x_column,
                y=y_column,
                hue=color_by,
                alpha=0.6,
                s=60,
                ax=ax
            )
            plt.legend(title=color_by, bbox_to_anchor=(1.05, 1), loc='upper left')
        else:
            # Simple scatter plot
            sns.scatterplot(
                data=data,
                x=x_column,
                y=y_column,
                color='#2196F3',
                alpha=0.6,
                s=60,
                ax=ax
            )
        
        # Add trend line
        try:
            z = np.polyfit(data[x_column].dropna(), 
                          data[y_column].dropna(), 1)
            p = np.poly1d(z)
            plt.plot(data[x_column].sort_values(), 
                    p(data[x_column].sort_values()), 
                    "r--", alpha=0.8, linewidth=2, label='Trend')
        except:
            pass
        
        plt.title(f'{y_column} vs {x_column}', fontsize=14, fontweight='bold')
        plt.xlabel(x_column, fontsize=12)
        plt.ylabel(y_column, fontsize=12)
        plt.grid(alpha=0.3)
        plt.tight_layout()
        
        st.pyplot(fig)
        
        # Calculate and display correlation
        correlation = data[[x_column, y_column]].corr().iloc[0, 1]
        st.info(f"📊 **Correlation between {x_column} and {y_column}:** `{correlation:.4f}`")
        
    else:
        st.info("ℹ️ Need at least 2 numerical columns to generate scatter plot.")
    
    st.divider()
    
    # --------------------------------------------------------
    # ADDITIONAL VISUALIZATIONS
    # --------------------------------------------------------
    st.markdown('<p class="sub-header">🎁 Bonus Visualizations</p>', unsafe_allow_html=True)
    
    viz_tab1, viz_tab2 = st.tabs(["📊 Bar Chart (Categorical)", "📈 Box Plot"])
    
    # Bar Chart for Categorical Data
    with viz_tab1:
        if categorical_cols:
            cat_col = st.selectbox("Select Categorical Column", categorical_cols, key="bar_cat")
            
            value_counts = data[cat_col].value_counts().head(15)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(value_counts.index.astype(str), value_counts.values, 
                         color=plt.cm.Set3(np.linspace(0, 1, len(value_counts))))
            
            plt.title(f'Value Counts: {cat_col}', fontsize=14, fontweight='bold')
            plt.xlabel(cat_col, fontsize=12)
            plt.ylabel('Count', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=9)
            
            plt.tight_layout()
            st.pyplot(fig)
            
            st.dataframe(value_counts.reset_index().rename(
                columns={'index': cat_col, cat_col: 'Count'}
            ), use_container_width=True)
        else:
            st.info("ℹ️ No categorical columns available for bar chart.")
    
    # Box Plot
    with viz_tab2:
        if num_cols_for_viz:
            box_col = st.selectbox("Select Numerical Column", num_cols_for_viz, key="box_num")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            bp = ax.boxplot(data[box_col].dropna(), patch_artist=True,
                           labels=[box_col])
            
            # Style the boxplot
            for patch in bp['boxes']:
                patch.set_facecolor('#87CEEB')
            for whisker in bp['whiskers']:
                whisker.set(color='#7570b3', linewidth=2)
            for cap in bp['caps']:
                cap.set(color='#7570b3', linewidth=2)
            for median in bp['medians']:
                median.set(color='#b2df8a', linewidth=2)
            
            plt.title(f'Box Plot: {box_col}', fontsize=14, fontweight='bold')
            plt.ylabel('Value', fontsize=12)
            plt.grid(axis='y', alpha=0.3)
            
            st.pyplot(fig)
            
            # Show outlier info
            Q1 = data[box_col].quantile(0.25)
            Q3 = data[box_col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = data[(data[box_col] < Q1 - 1.5*IQR) | 
                          (data[box_col] > Q3 + 1.5*IQR)][box_col]
            
            st.info(f"📊 **Outliers detected:** {len(outliers)} points outside 1.5×IQR range")
        else:
            st.info("ℹ️ No numerical columns available for box plot.")
    
    # ============================================================
    # DATA EXPORT SECTION
    # ============================================================
    st.divider()
    st.markdown('<p class="sub-header">💾 Export Data</p>', unsafe_allow_html=True)
    
    col_exp1, col_exp2 = st.columns(2)
    
    with col_exp1:
        # Export to CSV
        csv_buffer = BytesIO()
        data.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        st.download_button(
            label="⬇️ Download as CSV",
            data=csv_buffer.getvalue(),
            file_name="processed_data.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col_exp2:
        # Export to Excel
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            data.to_excel(writer, index=False, sheet_name='Data')
        excel_buffer.seek(0)
        
        st.download_button(
            label="⬇️ Download as Excel",
            data=excel_buffer.getvalue(),
            file_name="processed_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.markdown("""
    <p style="text-align: center; color: #888; font-size: 0.9rem;">
        📊 Complete EDA Application | Built with Streamlit | 
        <a href="https://docs.streamlit.io" target="_blank">Streamlit Docs</a>
    </p>
""", unsafe_allow_html=True)
