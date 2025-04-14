import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the OpenAI API key from the environment
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is None:
    st.error("Error: OpenAI API key is not set in the environment variables!")

# Set up the OpenAI API key
openai.api_key = openai_api_key

# Function to generate assistant's reply
def generate_follow_up_questions(messages):
    response = openai.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=messages,
        max_tokens=150
    )
    assistant_reply = response.choices[0].message.content.strip()
    return assistant_reply

# Streamlit app
def main():
    st.set_page_config(page_title="Emergency Response Assistant", page_icon="🚑")
    st.title("🚑 Emergency Response Assistant")

    if "messages" not in st.session_state:
        # Initialize conversation history
        st.session_state.messages = [
            {"role": "system", "content": """
            You are an emergency response assistant. The user has provided an emergency description.
            Your task is to identify the missing critical information (like age, gender, location, remoteness of location, number of people involved, nature of the emergency, allergies, pre-existing health conditions).
            If the user starts talking about something unrelated to an emergency, politely guide them back to describing the emergency.
            Always assume a user needs help getting to the nearest facility. So after all relevant info is gathered then give a summary of the emergency to the user.
            """}
        ]

    # Show chat history
    for msg in st.session_state.messages[1:]:  # Skip system prompt
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])
        elif msg["role"] == "assistant":
            with st.chat_message("assistant"):
                st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("Describe the emergency situation...")
    
    if user_input:
        # Save user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate assistant's reply
        assistant_reply = generate_follow_up_questions(st.session_state.messages)

        # Save assistant message
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

        with st.chat_message("assistant"):
            st.markdown(assistant_reply)

if __name__ == "__main__":
    main()
