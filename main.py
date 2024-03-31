import streamlit as st
import chat
import streamlit.components.v1 as components

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
    st.session_state.input_count = 0  
    st.session_state.conversation = [] 

if st.session_state.input_count == len(questions):
    print(st.session_state.conversation)
    check = True
    print(check)
    if check:
        st.write("Chat Ended")
        res = chat.generate_response(st.session_state.conversation)
        link = chat.get_music(res)
        components.iframe(link, width=700, height=150)
        st.write(res)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
    st.session_state.conversation.append(message)  
    
    
if st.session_state.input_count < len(questions):
    if prompt := st.chat_input(placeholder="Type a message"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.conversation.append({"role": "user", "content": prompt})  
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.input_count += 1  

        
        if st.session_state.input_count < len(questions):
            st.session_state.messages.append({"role": "assistant", "content": questions[st.session_state.input_count]})
            with st.chat_message("assistant"):
                st.write(questions[st.session_state.input_count])
            st.session_state.conversation.append({"role": "assistant", "content": questions[st.session_state.input_count]})  
