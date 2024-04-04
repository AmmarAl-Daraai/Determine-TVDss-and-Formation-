#NOTE ⚠️:  I am a learner and not a professional coder,
# so my code may contain mistakes or issues in terms of functionality or calculation methods. 
# If you choose to use my code you can use it but, your own risk and are responsible for any issues that may arise.



# Import libraries
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import streamlit as st

# Streamlit app title
st.title('TVDss Interpolator and Formation Finder for Vertical Well 🛢 ')

# File uploader widgets
uploaded_file_1 = st.file_uploader("Choose the first Excel file (for given ✅  MD,TVDss and formations )", type=['xlsx'])
uploaded_file_2 = st.file_uploader("Choose the second Excel file (For missing⚠️ TVDss and formation???)", type=['xlsx'])

# Function to read uploaded file or return None if no file is selected
def load_excel(uploaded_file):
    if uploaded_file is not None:
        return pd.read_excel(uploaded_file)
    return None

# Function to interpolate and find formations
def process_files(df1, df2):
    if df1 is not None and df2 is not None:
        interpolation_function = interp1d(df1["MD"], df1["TVDss"], fill_value="extrapolate")
        df2["TVDss"] = interpolation_function(df2["MD"])
        
        def find_formation_by_range(md_value, df1):
            if md_value < df1.iloc[0]["MD"]:
                return "Below Range"
            idx = np.searchsorted(df1["MD"], md_value, side='right')
            if idx == len(df1):
                return df1.iloc[-1]["Formation"]
            elif df1.iloc[idx]["MD"] == md_value:
                return df1.iloc[idx]["Formation"]
            else:
                return df1.iloc[idx-1]["Formation"]
        
        df2["Formation"] = df2["MD"].apply(lambda x: find_formation_by_range(x, df1))
        
        return df2
    else:
        return None

# Load the dataframes
df1 = load_excel(uploaded_file_1)
df2 = load_excel(uploaded_file_2)

# Process the files if both are uploaded
if df1 is not None and df2 is not None:
    processed_df = process_files(df1, df2)
    if processed_df is not None:
        st.write("Processed DataFrame Result 🌟:")
        st.dataframe(processed_df)
    else:
        st.error("Error processing the files. Please make sure both files are correctly formatted and uploaded.")
else:
    st.info("Please upload both Excel files to proceed.")