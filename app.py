import streamlit as st
import sys
from pathlib import Path

# ==========================================
# Project setup
# ==========================================

PROJECT_ROOT = Path(__file__).parent
sys.path.append(str(PROJECT_ROOT / "src"))

from chatbot import chat


# ==========================================
# Page configuration
# ==========================================

st.set_page_config(
    page_title="Fashion Forward Hub",
    page_icon="👗",
    layout="wide"
)


# ==========================================
# Custom styling
# ==========================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #888;
        margin-bottom: 30px;
    }

    .feature-box {
        padding: 18px;
        border-radius: 12px;
        background-color: rgba(128, 128, 128, 0.08);
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# Sidebar
# ==========================================

with st.sidebar:

    st.title("👗 Fashion Forward Hub")

    st.write(
        "AI-powered shopping assistant"
    )

    st.divider()

    st.subheader("What I can help with")

    st.markdown(
        """
        🛍️ **Product Search**

        Find products using natural language.

        💬 **Store FAQ**

        Ask about shipping, returns,
        exchanges, refunds and payments.

        👚 **Outfit Recommendations**

        Get outfits based on occasion,
        style and budget.

        🔎 **Smart Filtering**

        Filter by price, color,
        category, occasion and style.
        """
    )

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# ==========================================
# Header
# ==========================================

st.markdown(
    '<div class="main-title">👗 Fashion Forward Hub</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your AI shopping assistant for products, '
    'store policies and outfit recommendations.'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================
# Example queries
# ==========================================

with st.expander("💡 Try asking something"):

    st.markdown(
        """
        **Products**
        - Tell me about the Black Slim Fit T-Shirt
        - Show me pink tops under ₹1500

        **Store policies**
        - How long does shipping take?
        - What is your return policy?

        **Outfits**
        - Suggest a minimal college outfit
        - Suggest a party outfit
        - Suggest a streetwear outfit for college
        """
    )


# ==========================================
# Chat history
# ==========================================

if "messages" not in st.session_state:

    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ==========================================
# Chat input
# ==========================================

user_query = st.chat_input(
    "Ask about products, policies or outfits..."
)


if user_query:

    # User message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )

    with st.chat_message("user"):

        st.markdown(user_query)


    # Assistant response
    with st.chat_message("assistant"):

        with st.spinner(
            "Thinking..."
        ):

            response = chat(
                user_query
            )

        st.markdown(response)


    # Save response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )