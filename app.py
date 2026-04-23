# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------–- Session state initialization -----------------–-
if "df" not in st.session_state:
    st.session_state.df = None

st.set_page_config(page_title="CSV Data Analysis Studio", layout="wide")
st.title("📊 CSV Data Analysis Studio")
st.markdown("Upload a CSV file and explore its contents with built‑in tools.")

# -----------------–- File uploader -----------------–-
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        st.success(f"✅ File loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        st.session_state.df = None

# -----------------–- Main interface (only if data exists) -----------------–-
if st.session_state.df is not None:
    df = st.session_state.df

    # Action selector
    action = st.selectbox(
        "Select an action",
        [
            "Show First 5 Rows",
            "Show Last 5 Rows",
            "Show Column Names",
            "Show Shape",
            "Show Summary Statistics (describe)",
            "Plot First Two Columns (Line Chart)",
        ],
    )

    # Execute the chosen action
    if action == "Show First 5 Rows":
        st.subheader("First 5 rows")
        st.dataframe(df.head())

    elif action == "Show Last 5 Rows":
        st.subheader("Last 5 rows")
        st.dataframe(df.tail())

    elif action == "Show Column Names":
        st.subheader("Column names")
        st.write(list(df.columns))

    elif action == "Show Shape":
        st.subheader("Dataset shape")
        st.write(f"Rows: {df.shape[0]}")
        st.write(f"Columns: {df.shape[1]}")

    elif action == "Show Summary Statistics (describe)":
        st.subheader("Summary statistics (numeric columns)")
        st.dataframe(df.describe())

    elif action == "Plot First Two Columns (Line Chart)":
        if df.shape[1] < 2:
            st.warning("Need at least 2 columns to plot.")
        else:
            col1, col2 = df.columns[0], df.columns[1]
            st.subheader(f"Line plot: {col1} vs {col2}")

            # Drop rows with missing values in the two columns
            plot_df = df[[col1, col2]].dropna()
            if plot_df.empty:
                st.error("No valid numeric data for plotting.")
            else:
                # Try to convert second column to numeric (coerce errors)
                plot_df[col2] = pd.to_numeric(plot_df[col2], errors="coerce")
                plot_df = plot_df.dropna(subset=[col2])

                if plot_df.empty:
                    st.error("Second column contains no numeric values after conversion.")
                else:
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.plot(plot_df[col1], plot_df[col2], marker="o", linestyle="-", color="#f39c12")
                    ax.set_xlabel(col1)
                    ax.set_ylabel(col2)
                    ax.set_title(f"{col2} vs {col1}")
                    ax.grid(True, linestyle="--", alpha=0.6)
                    st.pyplot(fig)

else:
    st.info("👈 Please upload a CSV file to begin.")

# Optional footer
st.markdown("---")
st.caption("Built with Streamlit · CSV analysis · pandas · matplotlib")