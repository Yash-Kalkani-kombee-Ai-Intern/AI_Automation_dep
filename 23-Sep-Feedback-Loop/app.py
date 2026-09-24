import os
import time
import uuid

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

from feedback_db import (
    get_active_prompt,
    get_all_feedback,
    get_negative_feedback,
    get_negative_feedback_count,
    init_db,
    save_feedback,
    set_active_prompt,
)


# ============================================================
# Configuration
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash",
)

if not GEMINI_API_KEY:
    st.error(
        "Gemini API key is missing. "
        "Add GEMINI_API_KEY or GOOGLE_API_KEY to your .env file."
    )
    st.stop()


client = genai.Client(
    api_key=GEMINI_API_KEY
)

init_db()


# ============================================================
# Streamlit page
# ============================================================

st.set_page_config(
    page_title="AI Feedback Loop",
    page_icon="🤖",
    layout="wide",
)


st.title("🤖 AI Feedback Loop")
st.caption(
    "Gemini chatbot with automatic feedback-based prompt improvement"
)


# ============================================================
# Session state
# ============================================================

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "response_meta" not in st.session_state:
    st.session_state.response_meta = {}

if "feedback_saved" not in st.session_state:
    st.session_state.feedback_saved = set()

if "last_improvement" not in st.session_state:
    st.session_state.last_improvement = False


# ============================================================
# Gemini response
# ============================================================

def call_gemini_api(contents, config=None, max_retries=3, initial_delay=2.0):
    """
    Call Gemini API with automatic retry and exponential backoff
    for transient errors (such as 503 UNAVAILABLE or high demand).
    """
    delay = initial_delay
    last_error = None
    models_to_try = [GEMINI_MODEL, "gemini-3.5-flash", "gemini-3.7-flash"]
    
    for attempt in range(1, max_retries + 1):
        model_name = models_to_try[(attempt - 1) % len(models_to_try)]
        try:
            return client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config,
            )
        except Exception as exc:
            last_error = exc
            err_str = str(exc)
            # If rate limit or 503 temporary overload, wait and retry
            if "503" in err_str or "429" in err_str or "UNAVAILABLE" in err_str or "high demand" in err_str:
                if attempt < max_retries:
                    time.sleep(delay)
                    delay *= 2
                    continue
            raise last_error


def generate_response(user_prompt):
    """
    Generate a Gemini response using the currently active
    system prompt with proper multi-turn conversation structure
    and automatic retry for transient overloads.
    """

    system_prompt = get_active_prompt()

    # Build structured multi-turn conversation history
    contents = []

    # Prior turns (excluding the newly appended prompt and excluding error responses)
    for message in st.session_state.messages[:-1][-10:]:
        role = "user" if message.get("role") == "user" else "model"
        content = message.get("content", "")

        # Skip any previous error messages so history is clean
        if message.get("role") == "assistant" and content.startswith("Gemini API error:"):
            continue

        if content:
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=content)],
                )
            )

    # Current user turn
    contents.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_prompt)],
        )
    )

    try:
        response = call_gemini_api(
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.7,
            ),
        )

        if not response.text:
            return "Gemini returned an empty response."

        return response.text

    except Exception as exc:
        return f"Gemini API error: {exc}"


# ============================================================
# Automatic prompt improvement
# ============================================================

def automatically_improve_prompt():
    """
    Analyze recent negative feedback and automatically
    generate an improved system prompt.

    Improvement is triggered after every 3 negative
    feedback records.
    """

    negative_count = get_negative_feedback_count()

    # No improvement before 3 negative feedbacks
    if negative_count < 3:
        return False

    # Only improve at 3, 6, 9, 12, ...
    if negative_count % 3 != 0:
        return False

    feedback_rows = get_negative_feedback()

    if not feedback_rows:
        return False

    current_prompt = get_active_prompt()

    feedback_text = ""

    for row in feedback_rows:
        (
            user_prompt,
            model_response,
            comment,
            latency,
            created_at,
        ) = row

        feedback_text += f"""
USER QUESTION:
{user_prompt}

AI RESPONSE:
{model_response}

USER FEEDBACK:
{comment or "No written comment"}

RESPONSE LATENCY:
{latency:.3f} seconds

CREATED AT:
{created_at}

--------------------------------
"""

    optimizer_prompt = f"""
You are an AI system-prompt optimizer.

CURRENT SYSTEM PROMPT:
{current_prompt}

RECENT NEGATIVE USER FEEDBACK:
{feedback_text}

Analyze the recurring problems in the negative feedback.

Your job is to create an improved system prompt.

Rules:

1. Keep useful existing behavior.
2. Fix only problems supported by the feedback.
3. Make technical explanations simple when users struggle.
4. Add examples when feedback indicates examples are needed.
5. Avoid unnecessary verbosity.
6. Do not invent user requirements.
7. Do not change the AI's core purpose.
8. Return ONLY the new system prompt.
"""

    try:
        with st.spinner(
            "🔄 Gemini is analyzing feedback and improving the prompt..."
        ):
            response = call_gemini_api(
                contents=optimizer_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                ),
            )

        improved_prompt = (
            response.text.strip()
            if response.text
            else ""
        )

        if not improved_prompt:
            return False

        set_active_prompt(
            improved_prompt,
            "Automatically improved from recurring negative user feedback",
        )

        return True

    except Exception as exc:
        st.error(
            f"Automatic prompt improvement failed: {exc}"
        )
        return False


# ============================================================
# Save feedback
# ============================================================

def save_user_feedback(response_id):
    """
    Save explicit feedback and trigger the automatic
    improvement cycle when the threshold is reached.
    """

    rating = st.session_state.get(
        f"feedback_{response_id}"
    )

    if rating is None:
        st.warning(
            "Please select 👍 or 👎 first."
        )
        return

    if response_id in st.session_state.feedback_saved:
        st.info(
            "Feedback for this response was already saved."
        )
        return

    metadata = st.session_state.response_meta.get(
        response_id
    )

    if not metadata:
        st.error(
            "Response information was not found."
        )
        return

    comment = st.session_state.get(
        f"comment_{response_id}",
        "",
    )

    # Save feedback
    save_feedback(
        session_id=st.session_state.session_id,
        response_id=response_id,
        user_prompt=metadata["prompt"],
        model_response=metadata["response"],
        rating=int(rating),
        comment=comment.strip(),
        response_latency=metadata["latency"],
        turn_number=metadata["turn_number"],
    )

    st.session_state.feedback_saved.add(
        response_id
    )

    metadata["saved"] = True

    # Automatically improve only when negative feedback
    # reaches 3, 6, 9, 12...
    if int(rating) == 0:
        improved = automatically_improve_prompt()

        if improved:
            st.session_state.last_improvement = True


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.header("⚙️ Feedback Loop")

    st.write(
        """
        **Explicit feedback**

        👍 Helpful  
        👎 Not helpful  
        + optional comment

        **Automatic improvement**

        Every 3 negative feedback records,
        Gemini analyzes the feedback and
        creates an improved system prompt.
        """
    )

    st.divider()

    st.subheader("Current Model")

    st.code(
        GEMINI_MODEL
    )

    st.subheader("Active System Prompt")

    st.code(
        get_active_prompt(),
        language="text",
    )


# ============================================================
# Show previous messages
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        # Feedback only for assistant responses
        if message["role"] == "assistant":

            response_id = message["response_id"]

            metadata = st.session_state.response_meta.get(
                response_id,
                {},
            )

            st.caption(
                f"Response latency: "
                f"{metadata.get('latency', 0):.3f} sec"
            )

            # Feedback widget
            st.feedback(
                "thumbs",
                key=f"feedback_{response_id}",
                disabled=metadata.get(
                    "saved",
                    False,
                ),
            )

            # Optional comment
            st.text_input(
                "Optional feedback comment",
                key=f"comment_{response_id}",
                disabled=metadata.get(
                    "saved",
                    False,
                ),
                placeholder=(
                    "Tell us what was good or what should improve..."
                ),
            )

            # Submit feedback
            if not metadata.get(
                "saved",
                False,
            ):

                if st.button(
                    "Submit Feedback",
                    key=f"submit_{response_id}",
                ):
                    save_user_feedback(
                        response_id
                    )
                    st.rerun()

            else:
                st.success(
                    "Feedback saved ✅"
                )


# ============================================================
# Chat input
# ============================================================

prompt = st.chat_input(
    "Ask Gemini something..."
)


if prompt:

    # --------------------------------------------------------
    # Save user message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # --------------------------------------------------------
    # Generate Gemini response
    # --------------------------------------------------------

    start_time = time.perf_counter()

    response = generate_response(
        prompt
    )

    latency = (
        time.perf_counter()
        - start_time
    )

    response_id = str(
        uuid.uuid4()
    )

    turn_number = len(
        [
            message
            for message in st.session_state.messages
            if message["role"] == "user"
        ]
    )

    # --------------------------------------------------------
    # Store metadata
    # --------------------------------------------------------

    st.session_state.response_meta[
        response_id
    ] = {
        "prompt": prompt,
        "response": response,
        "latency": latency,
        "turn_number": turn_number,
        "saved": False,
    }

    # --------------------------------------------------------
    # Save assistant message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
            "response_id": response_id,
        }
    )

    st.rerun()


# ============================================================
# Improvement notification
# ============================================================

if st.session_state.last_improvement:

    st.success(
        """
        🔄 **Feedback loop completed!**

        Gemini analyzed the recent negative feedback
        and automatically improved the active system prompt.

        Future responses will use the improved prompt.
        """
    )

    st.session_state.last_improvement = False


# ============================================================
# Dashboard
# ============================================================

st.divider()

st.header("📊 Feedback Dashboard")

rows = get_all_feedback()

if not rows:

    st.info(
        "No feedback collected yet. "
        "Ask Gemini a question and submit feedback."
    )

else:

    columns = [
        "id",
        "session_id",
        "response_id",
        "user_prompt",
        "model_response",
        "rating",
        "comment",
        "response_latency",
        "turn_number",
        "created_at",
    ]

    df = pd.DataFrame(
        rows,
        columns=columns,
    )

    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    total = len(df)

    positive = int(
        (df["rating"] == 1).sum()
    )

    negative = int(
        (df["rating"] == 0).sum()
    )

    positive_rate = (
        positive / total * 100
        if total > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Feedback",
        total,
    )

    col2.metric(
        "👍 Positive",
        positive,
    )

    col3.metric(
        "👎 Negative",
        negative,
    )

    col4.metric(
        "Positive Rate",
        f"{positive_rate:.1f}%",
    )

    # --------------------------------------------------------
    # Feedback distribution
    # --------------------------------------------------------

    st.subheader(
        "Feedback Distribution"
    )

    chart_df = (
        df["rating"]
        .map(
            {
                0: "Negative",
                1: "Positive",
            }
        )
        .value_counts()
    )

    st.bar_chart(
        chart_df
    )

    # --------------------------------------------------------
    # Average latency
    # --------------------------------------------------------

    st.subheader(
        "Response Performance"
    )

    average_latency = df[
        "response_latency"
    ].mean()

    st.write(
        f"Average response latency: "
        f"**{average_latency:.3f} seconds**"
    )

    # --------------------------------------------------------
    # Negative feedback analysis
    # --------------------------------------------------------

    st.subheader(
        "🔎 Negative Feedback Analysis"
    )

    negative_df = df[
        df["rating"] == 0
    ][
        [
            "user_prompt",
            "comment",
            "response_latency",
            "created_at",
        ]
    ]

    if negative_df.empty:

        st.success(
            "No negative feedback yet."
        )

    else:

        st.dataframe(
            negative_df,
            use_container_width=True,
        )

    # --------------------------------------------------------
    # User comments
    # --------------------------------------------------------

    st.subheader(
        "💬 User Comments"
    )

    comments_df = df[
        df["comment"]
        .fillna("")
        .str.strip()
        != ""
    ][
        [
            "rating",
            "comment",
            "user_prompt",
            "created_at",
        ]
    ]

    if comments_df.empty:

        st.info(
            "No written comments submitted yet."
        )

    else:

        st.dataframe(
            comments_df,
            use_container_width=True,
        )

    # --------------------------------------------------------
    # Complete dataset
    # --------------------------------------------------------

    st.subheader(
        "📋 Complete Feedback Data"
    )

    st.dataframe(
        df,
        use_container_width=True,
    )