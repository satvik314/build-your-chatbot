import streamlit as st
from openai import OpenAI

# Page config
st.set_page_config(page_title="OpenAI Chatbot with System Prompt", page_icon="💬")

# Header
st.title("💬 OpenAI Chatbot")
st.caption("Customize the chatbot's behavior using the system prompt in the sidebar")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Sidebar for system prompt
st.sidebar.title("⚙️ Custom Instructions")
st.sidebar.write("Modify the system prompt below to change how the chatbot responds.")

system_prompt = st.sidebar.text_area(
    "System Prompt",
    value="You are a helpful assistant.",
    height=150,
    help="The system prompt sets the behavior and personality of the AI assistant."
)

st.sidebar.info("💡 **Tip:** Try prompts like:\n- 'You are a friendly pirate'\n- 'Respond only in haikus'\n- 'You are a coding tutor'")

# Reset chat when system prompt changes
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = system_prompt
    st.session_state.messages = []

if st.session_state.system_prompt != system_prompt:
    st.session_state.system_prompt = system_prompt
    st.session_state.messages = []
    st.rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build messages with system prompt
    messages_to_send = [{"role": "system", "content": system_prompt}] + st.session_state.messages

    # Get response from OpenAI
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_to_send
        )
        reply = response.choices[0].message.content
        st.markdown(reply)

    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": reply})

st.sidebar.markdown("---")
st.sidebar.markdown("❤️ Made by [Build Fast with AI](https://buildfastwithai.com)")
