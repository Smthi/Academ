import streamlit as st
from openai import OpenAI
import time

client = OpenAI(
    api_key = st.secrets.get("api", {}).get("OPENAI_API_KEY") if "api" in st.secrets else None,
)

st.set_page_config(page_title="Academ",page_icon='📘',layout='centered')

st.title("Welcome to :blue[*Academ*] 🧙🏻‍♂️📘")
st.write("*Let thy :blue[**Academ**]ic comeback* ***begin***")

if 'messages' not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    name = st.text_input("Display name",placeholder = 'Enter name' ,value=st.session_state.get("name", ""))
    emoji = st.selectbox("How are you feeling?",('😀','😴',"😊","😩","😒","😍","😑",'😎','🥶'))
    join = st.button("Join", type="primary", use_container_width=True)
    if join and name.strip():
        st.session_state["name"] = name.strip()
        st.session_state.messages.append({"role": "system", "content": f"{name} joined the chat.", "sender": "system"})
if "name" not in st.session_state:
    st.info("Enter your name in the sidebar and click **Join** to begin.")
    st.stop()

for m in st.session_state.messages:
    if m["role"] == "system":
        st.markdown(f"> *{m['content']}*")
    elif m["role"] == "user":
        with st.chat_message("user", avatar=emoji):
            st.markdown(f"**{m['sender']}**: {m['content']}")

user_text = st.chat_input("Type your question…")
if user_text:
    # Append user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_text,
        "sender": st.session_state["name"]
    })
    
    # Display user message
    with st.chat_message("user", avatar=emoji):
        st.markdown(f"**{st.session_state['name']}**: {user_text}")
    
    # Display assistant response with streaming
    with st.chat_message("assistant", avatar="🧙🏻‍♂️"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Create the assistant's response stream
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system", 
                    "content": "You're Academ, an intelligent assistant chatbot for Chulalongkorn students. Your main focus is to give concise answers. Ex: teaching topics, desiging study plans, advising through struggles, give motivation, guide directions, etc. If you find the topic irrelevant, reply with 'Sorry, I can't help with that topic.'"
                },
                {
                    "role": "user",
                    "content": user_text,
                },
            ],
            stream=True
        )
        
        # Process the stream
        try:
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    #message_placeholder.markdown(full_response + "▌")

            # Check for '6767' in the complete response
            if "Sorry, I can't help with that topic." in full_response:
                st.error("Sorry, I can't help with that topic.")
            else:
                message_placeholder.markdown(full_response)
            
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_response,
                    "sender": "Assistant"
            })
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

