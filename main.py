import streamlit as st
import dotenv
import chat
import upload
dotenv.load_dotenv()

st.title("MusicMATE")

questions = [
    "How are you feeling today?",
    "What was the best part of your day so far?",
    "Did anything make you sad today?",
    "Were you able to accomplish your goals for today?",
    "How would you describe your overall mood right now?"
]

check = False

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": questions[0]}]
    st.session_state.input_count = 0  # Add a new session state variable to keep track of the input count
    st.session_state.conversation = []  # Add a new session state variable to store the complete conversation

if st.session_state.input_count == len(questions):
    print(st.session_state.conversation)
    check = not check
    print(check)
    if check:
        st.write("Chat Ended")
        res = chat.generate_response(st.session_state.conversation)
        st.write(res)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
    st.session_state.conversation.append(message)  # Append the message to the conversation

# Only show the chat input if the user hasn't answered all 5 questions
if st.session_state.input_count < len(questions):
    if prompt := st.chat_input(placeholder="Type a message"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.input_count += 1  # Increment the input count
        st.session_state.conversation.append({"role": "user", "content": prompt})  # Append the message to the conversation

        # If there are more questions, ask the next one
        if st.session_state.input_count < len(questions):
            st.session_state.messages.append({"role": "assistant", "content": questions[st.session_state.input_count]})
            with st.chat_message("assistant"):
                st.write(questions[st.session_state.input_count])
            st.session_state.conversation.append({"role": "assistant", "content": questions[st.session_state.input_count]})  # Append the message to the conversation
