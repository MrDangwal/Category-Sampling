import streamlit as st
import pandas as pd

# Function to sample data by category
def sample_data_by_category(df, category_col, fraction):
    try:
        if category_col not in df.columns:
            st.error(f"Column '{category_col}' not found.")
            return None
        if fraction <= 0 or fraction > 1:
            st.error("Fraction must be between 0 and 1.")
            return None
        sampled_df = df.groupby(category_col, group_keys=False).apply(
            lambda x: x.sample(frac=min(fraction, len(x)/len(x)), random_state=42) if len(x) > 1 else x
        )
        return sampled_df
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Custom HTML and CSS for the background and styling
st.markdown("""
    <style>
        body {
            background-image: url('https://source.unsplash.com/1920x1080/?data,technology');
            background-size: cover;
            color: white;
        }
        .main {
            background-color: rgba(0, 0, 0, 0.8);
            padding: 2rem;
            border-radius: 15px;
        }
        h1 {
            color: #00c4ff;
            text-align: center;
            font-family: 'Arial Black', sans-serif;
        }
        h2, h3 {
            color: #ffaf00;
        }
        .stButton > button {
            background-color: #00c4ff;
            color: white;
            font-size: 16px;
            border-radius: 8px;
            padding: 8px 16px;
        }
    </style>
""", unsafe_allow_html=True)

# Main App Header
st.markdown("<h1>CSV Data Sampler by Category</h1>", unsafe_allow_html=True)

# Sidebar Inputs
st.sidebar.markdown("### Input Controls")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])
sample_percent = st.sidebar.number_input(
    "Percentage of samples per category (1-100)",
    min_value=1, max_value=100, value=1
)

# Main Section
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.markdown("<div class='main'>", unsafe_allow_html=True)
    st.markdown("<h2>Uploaded Data</h2>", unsafe_allow_html=True)
    st.write(f"Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    st.write("Preview of Data", df.head())
    category_col = st.selectbox("Select the category column", df.columns)

    fraction = sample_percent / 100

    if st.button("Sample Data"):
        if len(df) == 0:
            st.error("Uploaded file contains no data.")
        elif category_col:
            sampled_df = sample_data_by_category(df, category_col, fraction)
            if sampled_df is not None and not sampled_df.empty:
                st.markdown("<h3>Sampled Data</h3>", unsafe_allow_html=True)
                st.write(f"Sampled Dataset Shape: {sampled_df.shape[0]} rows")
                st.dataframe(sampled_df)

                st.markdown("<h3>Output Statistics</h3>", unsafe_allow_html=True)
                category_counts = sampled_df[category_col].value_counts()
                category_counts_df = pd.DataFrame({
                    "Category": category_counts.index,
                    "Row Count": category_counts.values
                })
                st.dataframe(category_counts_df)

                st.download_button(
                    label="Download Sampled Data",
                    data=sampled_df.to_csv(index=False),
                    file_name="sampled_data.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No data available for the specified sampling criteria.")
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='main'><h2>Please upload a CSV file to get started.</h2></div>", unsafe_allow_html=True)
