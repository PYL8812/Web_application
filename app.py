import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="CSV Data Analysis App", layout="wide")

st.title("CSV Data Analysis App")
st.markdown("Upload a CSV file, choose an option, and view the result in your browser.")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

options = [
    "Show First 5 Rows",
    "Show Last 5 Rows",
    "Show Column Names",
    "Show Shape",
    "Show Summary",
    "Plot First Two Columns"
]

choice = st.selectbox("Choose an option", options)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("CSV file uploaded successfully.")
        st.info(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

        if st.button("Run Option"):
            if choice == "Show First 5 Rows":
                st.subheader("First 5 Rows")
                st.dataframe(df.head())

            elif choice == "Show Last 5 Rows":
                st.subheader("Last 5 Rows")
                st.dataframe(df.tail())

            elif choice == "Show Column Names":
                st.subheader("Column Names")
                st.write(list(df.columns))

            elif choice == "Show Shape":
                st.subheader("Dataset Shape")
                st.write(f"Rows: {df.shape[0]}")
                st.write(f"Columns: {df.shape[1]}")

            elif choice == "Show Summary":
                st.subheader("Summary Statistics")
                st.dataframe(df.describe())

            elif choice == "Plot First Two Columns":
                st.subheader("Simple Plot")

                if df.shape[1] < 2:
                    st.warning("Need at least 2 columns to plot.")
                else:
                    x = df.iloc[:, 0]
                    y = df.iloc[:, 1]

                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.plot(x, y)
                    ax.set_title("Simple Plot")
                    ax.set_xlabel(df.columns[0])
                    ax.set_ylabel(df.columns[1])
                    plt.xticks(rotation=45)
                    st.pyplot(fig)

    except Exception as e:
        st.error(f"Could not read file: {e}")
else:
    st.warning("Please upload a CSV file first.")