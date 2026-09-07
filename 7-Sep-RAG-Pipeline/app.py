import os
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from google import genai


# --------------------------------------------------
# Configuration
# --------------------------------------------------

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY not found in .env file")
    st.stop()

client = genai.Client(api_key=GEMINI_API_KEY)


# --------------------------------------------------
# Streamlit UI
# --------------------------------------------------

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="📚",
    layout="wide"
)

st.title("📚 RAG Chatbot")
st.write("Upload a PDF and ask questions based on its content.")


# --------------------------------------------------
# Upload PDF
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"]
)


if uploaded_file:

    # --------------------------------------------------
    # 1. Document Ingestion
    # --------------------------------------------------

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    st.success("PDF loaded successfully!")

    st.write(f"**Total characters:** {len(text):,}")


    # --------------------------------------------------
    # 2. Chunking
    # --------------------------------------------------

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_text(text)

    st.write(f"**Total chunks:** {len(chunks)}")


    # --------------------------------------------------
    # 3. Embeddings
    # --------------------------------------------------

    with st.spinner("Creating embeddings..."):

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )


    # --------------------------------------------------
    # 4. Store in ChromaDB
    # --------------------------------------------------

    with st.spinner("Storing documents in ChromaDB..."):

        vectorstore = Chroma.from_texts(
            texts=chunks,
            embedding=embeddings,
            persist_directory="./chroma_db"
        )

    st.success("Documents stored in ChromaDB!")


    # --------------------------------------------------
    # 5. User Question
    # --------------------------------------------------

    st.divider()

    st.subheader("💬 Ask a Question")

    question = st.text_input(
        "Enter your question about the document:"
    )


    if question:

        # --------------------------------------------------
        # 6. Retrieval
        # --------------------------------------------------

        with st.spinner("Searching relevant information..."):

            results = vectorstore.similarity_search(
                question,
                k=3
            )


        # --------------------------------------------------
        # 7. Create Context
        # --------------------------------------------------

        context = "\n\n".join(
            result.page_content
            for result in results
        )


        # --------------------------------------------------
        # 8. Gemini Generation
        # --------------------------------------------------

        prompt = f"""
You are a helpful document-based assistant.

Answer the user's question using ONLY the information
provided in the context.

Do not use outside knowledge.

If the answer is not available in the context,
say exactly:

"I could not find this information in the document."

Keep the answer clear and concise.

Context:
{context}

Question:
{question}

Answer:
"""


        with st.spinner("Generating answer..."):

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )


        # --------------------------------------------------
        # 9. Display Answer
        # --------------------------------------------------

        st.subheader("🤖 Answer")

        st.write(response.text)


        # --------------------------------------------------
        # 10. Display Retrieved Sources
        # --------------------------------------------------

        with st.expander("🔎 View Retrieved Chunks"):

            for i, result in enumerate(results):

                st.markdown(f"### Chunk {i + 1}")

                st.write(result.page_content)

                st.divider()