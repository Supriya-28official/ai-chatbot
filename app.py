import os
import streamlit as st
from openai import OpenAI

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(
    page_title="Supriya AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# -----------------------------
# CUSTOM DESIGN
# -----------------------------
st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown(
    '<div class="main-title">🤖 Supriya AI Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your smart AI customer support assistant</div>',
    unsafe_allow_html=True
)

# -----------------------------
# OPENROUTER API
# -----------------------------
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    st.error("OpenRouter API key nahi mili.")
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

# -----------------------------
# CHAT HISTORY
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Previous messages show karo
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# USER INPUT
# -----------------------------
user_message = st.chat_input("Ask me anything...")

if user_message:

    # User message save karo
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    # User message display
    with st.chat_message("user"):
        st.markdown(user_message)

    # AI response
    with st.chat_message("assistant"):

        with st.spinner("Thinking... 🤔"):

            try:

                response = client.chat.completions.create(

                    model="openrouter/free",

                    messages=[
                        {
                            "role": "system",
                            "content": """
You are Supriya AI Assistant, a helpful and friendly
customer support chatbot.

Your job is to:
- Answer questions clearly.
- Be polite and professional.
- Keep answers easy to understand.
- Help customers with general questions.
- If you don't know something, honestly say you don't have that information.
"""
                        },

                        *st.session_state.messages
                    ]
                )

                answer = response.choices[0].message.content

                # AI answer display
                st.markdown(answer)

                # AI answer save
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:

                st.error(f"Something went wrong: {e}")