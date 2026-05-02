import streamlit as st
from agent import create_tourism_agent

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Serendib AI 🇱🇰",
    page_icon="🇱🇰",
    layout="wide"
)

# ---------------- CLEAN MODERN UI ----------------
st.markdown(
    """
    <style>

    .stApp {
        background-color: #f4f6f9;
    }

    .block-container {
        padding: 2rem;
    }

    /* HEADER CARD */
    .header {
        background: linear-gradient(90deg, #0a3d62, #1e90ff);
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
    }

    .header h1 {
        font-size: 38px;
        margin: 0;
    }

    .header p {
        margin: 5px 0 0 0;
        font-size: 16px;
        opacity: 0.9;
    }

    /* CHAT BUBBLES */
    .stChatMessage {
        border-radius: 12px;
        padding: 12px;
        background-color: white !important;
        border: 1px solid #e6e6e6;
    }

    /* SIDEBAR CLEAN */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- HEADER ----------------
st.markdown("""
<div class="header">
    <h1>🇱🇰 Serendib AI</h1>
    <p>Explore Sri Lanka • Beaches • Wildlife • Culture • Nature</p>
</div>
""", unsafe_allow_html=True)

# ---------------- AGENT ----------------
if "agent" not in st.session_state:
    st.session_state.agent = create_tourism_agent()

if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------- SIDEBAR QUICK ACTIONS ----------------
with st.sidebar:
    st.title("⚡ Quick Explore")

    if st.button("🏝️ Beaches"):
        st.session_state.quick = "best beaches in Sri Lanka"

    if st.button("🐘 Safari"):
        st.session_state.quick = "best wildlife safari Sri Lanka"

    if st.button("⛰️ Nature"):
        st.session_state.quick = "best hiking places in Sri Lanka"

    if st.button("🏛️ Heritage"):
        st.session_state.quick = "best cultural heritage sites Sri Lanka"

    if st.button("🧹 Clear Chat"):
        st.session_state.chat = []

# ---------------- INPUT ----------------
user_input = st.chat_input("Ask about Sri Lanka travel...")

# auto-fill from sidebar buttons
if "quick" in st.session_state:
    user_input = st.session_state.quick
    del st.session_state.quick

# ---------------- CHAT HISTORY ----------------
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- PROCESS INPUT ----------------
if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Finding Sri Lanka destinations... 🌴"):
            response = st.session_state.agent.invoke({"input": user_input})
            answer = response["output"]

            # CLEAN OUTPUT (IMPORTANT)
            answer = answer.replace("**", "")

            st.markdown(answer)

    st.session_state.chat.append({"role": "assistant", "content": answer})