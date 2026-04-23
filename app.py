import streamlit as st
import pandas as pd

# Session state initialization
if "df" not in st.session_state:
    st.session_state.df = None

st.set_page_config(
    page_title="CSV Data Analysis Studio",
    layout="wide"
)

st.title("📊 CSV Data Analysis Studio")
st.markdown("Upload a CSV file and explore its contents.")

# File uploader
uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        st.success(
            f"File loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns"
        )
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        st.session_state.df = None

# Main interface
if st.session_state.df is not None:
    df = st.session_state.df

    action = st.selectbox(
        "Select an action",
        [
            "Show First 5 Rows",
            "Show Last 5 Rows",
            "Show Column Names",
            "Show Shape",
            "Show Summary Statistics",
            "Plot First Two Columns"
        ]
    )

    if action == "Show First 5 Rows":
        st.dataframe(df.head())

    elif action == "Show Last 5 Rows":
        st.dataframe(df.tail())

    elif action == "Show Column Names":
        st.write(df.columns.tolist())

    elif action == "Show Shape":
        st.write(f"Rows: {df.shape[0]}")
        st.write(f"Columns: {df.shape[1]}")

    elif action == "Show Summary Statistics":
        st.dataframe(df.describe())

    elif action == "Plot First Two Columns":
        if df.shape[1] < 2:
            st.warning("Need at least 2 columns to plot.")
        else:
            col1 = df.columns[0]
            col2 = df.columns[1]

            plot_df = df[[col1, col2]].copy()

            # Convert second column to numeric
            plot_df[col2] = pd.to_numeric(
                plot_df[col2],
                errors="coerce"
            )

            plot_df = plot_df.dropna()

            if plot_df.empty:
                st.error("Second column must contain numeric values.")
            else:
                st.line_chart(
                    data=plot_df,
                    x=col1,
                    y=col2
                )

else:
    st.info("Please upload a CSV file to begin.")

st.markdown("---")
st.caption("Built with Streamlit")