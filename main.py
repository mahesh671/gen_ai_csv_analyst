import streamlit as st
from app.main import call_agent
import uuid
# from main import customer_transaction_agent

# Set page configuration
st.set_page_config(page_title="Chat with AI", layout="wide")

# Title
st.title("💬 AI Chat Assistant")

# Initialize session state to store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id=str(uuid.uuid4())



# Function to simulate AI reply (replace with real model call)
def get_ai_reply(session_id,user_input):
    # Simulate logic — replace with call to your model or API
    # return f"You said: '{user_input}'. Here's a response from your AI assistant."
    # return remove_think_tag(react_agent.invoke({'messages':user_input})['messages'][-1].content)
    return call_agent(session_id,user_input)
    # answer= customer_transaction_agent(user_input)
    print(type(answer))
    return answer

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box for user
user_input = st.chat_input("Type your message here...")

# Process user input
if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get AI response
    ai_reply = get_ai_reply(st.session_state.session_id,user_input)
    
    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    
    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(ai_reply)
