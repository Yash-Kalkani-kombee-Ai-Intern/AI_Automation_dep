import streamlit as st
from llm import generate_text

st.set_page_config(
    page_title="AI Text Generator",
    page_icon="🤖"
)

st.title("🤖 AI Text Generator")
st.write("Generate blogs, emails, and paragraphs using AI.")

topic = st.text_input(
    "Enter your topic",
    placeholder="e.g. Artificial Intelligence in Education"
)

content_type = st.selectbox(
    "Content Type",
    ["Blog", "Email", "Paragraph"]
)

tone = st.selectbox(
    "Tone",
    ["Professional", "Friendly", "Simple", "Creative"]
)

length = st.selectbox(
    "Length",
    ["Short", "Medium", "Long"]
)

if st.button("Generate Text"):

    if topic.strip() == "":
        st.warning("Please enter a topic.")

    else:
        with st.spinner("Generating text..."):

            result = generate_text(
                topic,
                content_type,
                tone,
                length
            )

        st.subheader("Generated Text")
        st.write(result)