import streamlit as st
from services.agent import run_agent

st.set_page_config(page_title="AI Agent Tool Caller", layout="centered")

st.title("🤖 AI Agent with Tool Calling")
st.markdown("I can calculate, search docs, create tasks, and actually save email drafts to your Gmail!")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "json" in msg:
            st.json(msg["json"])

user_input = st.chat_input("E.g., Calculate 45 * 150 and draft an email to Ali about it.")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Process Agent
    with st.chat_message("assistant"):
        with st.spinner("Thinking and calling tools..."):
            try:
                final_response = run_agent(user_input)
                
                # Show readable text
                st.markdown(final_response["readable_response"])
                # Show the Lead's requested JSON format
                st.json(final_response["structured_json"])
                
                # Save to state
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": final_response["readable_response"],
                    "json": final_response["structured_json"]
                })
            except Exception as e:
                st.error(f"An error occurred: {e}")