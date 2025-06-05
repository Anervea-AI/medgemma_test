import streamlit as st
import requests

st.set_page_config(page_title="MedGemma Chatbot")
st.title("MedGemma Chatbot")

# Sidebar for settings
st.sidebar.header("Chat Settings")
role = st.sidebar.text_input(
    "Role (e.g., medical expert, radiologist, etc.)",
    value="medical expert"
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Custom CSS to fix chatbox at bottom center
st.markdown("""
<style>
.fixed-bottom-center {
    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 600px;
    background: #fff;
    padding: 12px 16px 12px 16px;
    border-top: 1px solid #eee;
    z-index: 9999;
    box-shadow: 0 -2px 8px rgba(0,0,0,0.04);
    display: flex;
    justify-content: center;
    align-items: center;
}
.fixed-bottom-center .stTextInput, .fixed-bottom-center .stFileUploader {
    flex: 1 1 auto;
}
</style>
""", unsafe_allow_html=True)

# Main chat input at bottom center
with st.container():
    st.markdown('<div class="fixed-bottom-center">', unsafe_allow_html=True)
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            prompt = st.text_input(
                "Type your message:",
                label_visibility="collapsed",
                placeholder="Ask your medical question..."
            )
        with col2:
            submitted = st.form_submit_button("🚀 Send")
    st.markdown('</div>', unsafe_allow_html=True)

# Handle submissions (same logic as before)
if 'submitted' in locals() and submitted:
    if not prompt.strip():
        st.error("Please provide a text prompt.")
    else:
        url = "http://98.81.79.124:8000/chat/"
        data = {
            "prompt": prompt,
            "model_variant": "27b-text-it",
            "role": role
        }
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        try:
            with st.spinner("Analyzing your query..."):
                response = requests.post(
                    url,
                    data=data,
                    headers={"accept": "application/json"}
                )
            if response.status_code == 200:
                result = response.json()
                st.session_state.messages.append({"role": "assistant", "content": result["response"]})
                st.rerun()
            else:
                st.error(f"API Error: {response.text}")
        except Exception as e:
            st.error(f"Connection failed: {str(e)}")
