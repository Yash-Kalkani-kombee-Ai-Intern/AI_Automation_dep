import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Data Dashboard",
    page_icon="📊",
    layout="wide"
)


# -----------------------------
# Backend function
# -----------------------------
def analyze_data(df):
    numeric_columns = df.select_dtypes(include="number").columns

    if len(numeric_columns) == 0:
        return None

    return df[numeric_columns].mean()


# -----------------------------
# Session State
# -----------------------------
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "result" not in st.session_state:
    st.session_state.result = None


# -----------------------------
# UI
# -----------------------------
st.title("📊 Interactive Data Dashboard")

st.write(
    "Upload a CSV file and analyze its numeric data."
)

# File uploader
uploaded_file = st.file_uploader(
    "Upload CSV file",
    type=["csv"]
)


# -----------------------------
# Process uploaded file
# -----------------------------
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.success("CSV uploaded successfully!")

    # Dataset preview
    st.subheader("📋 Dataset Preview")
    st.dataframe(df, use_container_width=True)

    # Metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    with col3:
        st.metric(
            "Numeric Columns",
            len(df.select_dtypes(include="number").columns)
        )

    # Analyze button
    if st.button("🔍 Analyze Data"):

        result = analyze_data(df)

        if result is None:

            st.warning("No numeric columns found.")

        else:

            st.session_state.result = result
            st.session_state.analysis_done = True


# -----------------------------
# Display analysis
# -----------------------------
if st.session_state.analysis_done:

    st.subheader("📈 Analysis Result")

    st.dataframe(
        st.session_state.result,
        use_container_width=True
    )

    # Chart
    st.subheader("📊 Average Values")

    fig, ax = plt.subplots()

    st.session_state.result.plot(
        kind="bar",
        ax=ax
    )

    ax.set_ylabel("Average")
    ax.set_xlabel("Columns")

    st.pyplot(fig)