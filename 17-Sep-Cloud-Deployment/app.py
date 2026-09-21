from google.genai._gaos.types import security

import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError


# ============================================================
# 1. LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Use one confirmed model for stable deployment.
MODEL_NAME = "gemini-3.6-flash"


# ============================================================
# 2. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Gemini AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 3. CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
        .chat-header {
            font-size: 2.3rem;
            font-weight: 800;
            background: linear-gradient(
                135deg,
                #3B82F6 0%,
                #8B5CF6 50%,
                #EC4899 100%
            );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.1rem;
            letter-spacing: -0.5px;
        }

        .chat-subtitle {
            color: #94A3B8;
            font-size: 1rem;
            font-weight: 400;
            margin-bottom: 1.5rem;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin: 6px 0 16px 0;
        }

        .status-connected {
            background-color: rgba(16, 185, 129, 0.15);
            color: #10B981;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }

        .status-disconnected {
            background-color: rgba(239, 68, 68, 0.15);
            color: #EF4444;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }

        .starter-header {
            font-size: 1.15rem;
            font-weight: 600;
            color: #E2E8F0;
            margin-bottom: 12px;
        }

        .msg-meta {
            font-size: 0.72rem;
            color: #64748B;
            margin-top: 4px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 4. SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )


# ============================================================
# 5. SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("### ⚙️ Assistant Settings")

    # --------------------------------------------------------
    # API STATUS
    # --------------------------------------------------------

    st.markdown("##### 🔑 Gemini API")

    if GEMINI_API_KEY:

        st.markdown(
            """
            <div class="status-badge status-connected">
                ● API Connected
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            """
            <div class="status-badge status-disconnected">
                ● API Key Not Found
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.warning(
            "Gemini API key was not found. "
            "Set GEMINI_API_KEY in your .env file."
        )

    st.markdown("---")

    # --------------------------------------------------------
    # MODEL
    # --------------------------------------------------------

    st.markdown("##### 🧠 Model")

    st.info(MODEL_NAME)

    # --------------------------------------------------------
    # PERSONA
    # --------------------------------------------------------

    st.markdown("##### 🎭 AI Persona")

    persona_options = {
        "💡 Helpful Assistant": (
            "You are a helpful, versatile, and articulate AI assistant. "
            "Use structured markdown, clear explanations, and code blocks "
            "where helpful."
        ),
        "🐍 Senior Python Engineer": (
            "You are a senior Python engineer. "
            "Provide clean, readable, PEP-8 compliant code "
            "with concise explanations."
        ),
        "☁️ Cloud & DevOps Architect": (
            "You are a senior Cloud and DevOps architect. "
            "Explain concepts around cloud infrastructure, "
            "Docker, Kubernetes, CI/CD, scalability, and security."
        ),
        "✍️ Creative Writer": (
            "You are a creative writer and copywriting assistant. "
            "Create engaging and clear content."
        ),
        "⚡ Concise Assistant": (
            "You are an ultra-concise expert. "
            "Answer directly using short paragraphs or bullet points."
        ),
    }

    selected_persona = st.selectbox(
        "Select Persona",
        options=list(persona_options.keys()),
        label_visibility="collapsed",
    )

    system_prompt = persona_options[selected_persona]

    # --------------------------------------------------------
    # GENERATION PARAMETERS
    # --------------------------------------------------------

    with st.expander("🎛️ Generation Parameters"):

        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.05,
        )

        top_p = st.slider(
            "Top-P",
            min_value=0.0,
            max_value=1.0,
            value=0.95,
            step=0.05,
        )

        max_output_tokens = st.number_input(
            "Max Output Tokens",
            min_value=128,
            max_value=8192,
            value=4096,
            step=256,
        )

    st.markdown("---")

    # --------------------------------------------------------
    # CONVERSATION CONTROLS
    # --------------------------------------------------------

    st.markdown("##### 📁 Conversation Controls")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🗑️ Clear Chat",
            use_container_width=True,
        ):

            st.session_state.messages = []
            st.rerun()

    with col2:

        if st.session_state.messages:

            md_text = (
                f"# Gemini Chat History "
                f"({st.session_state.session_id})\n\n"
            )

            for message in st.session_state.messages:

                speaker = (
                    "User"
                    if message["role"] == "user"
                    else "Gemini"
                )

                timestamp = message.get("timestamp", "")

                md_text += (
                    f"### {speaker} ({timestamp})\n"
                    f"{message['content']}\n\n"
                )

            st.download_button(
                label="📥 Export",
                data=md_text,
                file_name=(
                    f"gemini_chat_"
                    f"{st.session_state.session_id}.md"
                ),
                mime="text/markdown",
                use_container_width=True,
            )

    st.markdown("---")

    st.caption(
        "Powered by Google GenAI SDK & Streamlit"
    )


# ============================================================
# 6. MAIN HEADER
# ============================================================

st.markdown(
    '<div class="chat-header">'
    '🤖 Google Gemini Chatbot'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="chat-subtitle">
        Active Model: <code>{MODEL_NAME}</code>
        &nbsp;|&nbsp;
        Persona: <b>{selected_persona}</b>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 7. STARTER PROMPTS
# ============================================================

if not st.session_state.messages:

    st.markdown(
        '<div class="starter-header">'
        '💡 Choose a starter or ask anything below:'
        '</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    starter_prompts = [
        (
            "🚀 Explain Quantum Computing",
            "Explain quantum computing and superposition "
            "simply using an everyday analogy.",
        ),
        (
            "🐍 Build a FastAPI Service",
            "Explain how to build a FastAPI service "
            "with Pydantic validation.",
        ),
        (
            "☁️ Modern Cloud Architecture",
            "Explain best practices for deploying "
            "containerized Python applications to the cloud.",
        ),
        (
            "⚡ Clean Code Guidelines",
            "What are the top 7 clean code principles "
            "every software developer should follow?",
        ),
    ]

    for index, (title, prompt_text) in enumerate(
        starter_prompts
    ):

        target_col = (
            col1
            if index % 2 == 0
            else col2
        )

        with target_col:

            if st.button(
                title,
                key=f"starter_{index}",
                use_container_width=True,
            ):

                st.session_state.messages.append(
                    {
                        "role": "user",
                        "content": prompt_text,
                        "timestamp": datetime.now().strftime(
                            "%H:%M"
                        ),
                    }
                )

                st.rerun()


# ============================================================
# 8. DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    role = message["role"]

    avatar = (
        "👤"
        if role == "user"
        else "🤖"
    )

    with st.chat_message(
        role,
        avatar=avatar,
    ):

        st.markdown(message["content"])

        if "timestamp" in message:

            st.markdown(
                f"""
                <div class="msg-meta">
                    {message["timestamp"]}
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# 9. GEMINI STREAMING FUNCTION
# ============================================================

def stream_gemini_chat(
    api_key: str,
    model_name: str,
    messages: list,
    system_instr: str,
    temperature_value: float,
    top_p_value: float,
    max_tokens: int,
):
    """
    Send the conversation to Gemini and
    stream the response token-by-token.
    """

    client = genai.Client(
        api_key=api_key
    )

    # Build Gemini conversation history.
    history_contents = []

    for message in messages[:-1]:

        role = (
            "user"
            if message["role"] == "user"
            else "model"
        )

        history_contents.append(
            types.Content(
                role=role,
                parts=[
                    types.Part.from_text(
                        text=message["content"]
                    )
                ],
            )
        )

    config = types.GenerateContentConfig(
        system_instruction=(
            system_instr
            if system_instr
            else None
        ),
        temperature=temperature_value,
        top_p=top_p_value,
        max_output_tokens=max_tokens,
    )

    chat = client.chats.create(
        model=model_name,
        history=history_contents,
        config=config,
    )

    latest_user_message = messages[-1]["content"]

    stream = chat.send_message_stream(
        latest_user_message
    )

    for chunk in stream:

        if chunk.text:

            yield chunk.text


# ============================================================
# 10. CHAT INPUT
# ============================================================

user_prompt = st.chat_input(
    "Type your message here..."
)


# ============================================================
# 11. PROCESS USER MESSAGE
# ============================================================

is_new_prompt = False

if user_prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt,
            "timestamp": datetime.now().strftime(
                "%H:%M"
            ),
        }
    )

    is_new_prompt = True


# ============================================================
# 12. GENERATE GEMINI RESPONSE
# ============================================================

if (
    is_new_prompt
    or (
        st.session_state.messages
        and st.session_state.messages[-1]["role"]
        == "user"
    )
):

    if not GEMINI_API_KEY:

        st.error(
            "⚠️ GEMINI_API_KEY was not found. "
            "Please configure it in the .env file."
        )

    else:

        if is_new_prompt:

            with st.chat_message(
                "user",
                avatar="👤",
            ):

                st.markdown(user_prompt)

                st.markdown(
                    f"""
                    <div class="msg-meta">
                        {datetime.now().strftime("%H:%M")}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with st.chat_message(
            "assistant",
            avatar="🤖",
        ):

            try:

                response_placeholder = st.empty()

                accumulated_text = ""

                with st.spinner(
                    "Gemini is thinking..."
                ):

                    stream_generator = (
                        stream_gemini_chat(
                            api_key=GEMINI_API_KEY,
                            model_name=MODEL_NAME,
                            messages=(
                                st.session_state.messages
                            ),
                            system_instr=system_prompt,
                            temperature_value=temperature,
                            top_p_value=top_p,
                            max_tokens=int(
                                max_output_tokens
                            ),
                        )
                    )

                    for chunk in stream_generator:

                        accumulated_text += chunk

                        response_placeholder.markdown(
                            accumulated_text + "▌"
                        )

                response_placeholder.markdown(
                    accumulated_text
                )

                st.markdown(
                    f"""
                    <div class="msg-meta">
                        {datetime.now().strftime("%H:%M")}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": accumulated_text,
                        "timestamp": datetime.now().strftime(
                            "%H:%M"
                        ),
                    }
                )

            except APIError as error:

                st.error(
                    f"❌ Google GenAI API Error: {error}"
                )

            except Exception as error:

                st.error(
                    f"❌ An error occurred: {error}"
                )
