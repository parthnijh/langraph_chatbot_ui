

import streamlit as st 
from langraph_backend_database import chatbot
from langchain_core.messages import HumanMessage
import uuid
def generate_thread():
    thread_id=uuid.uuid4()
    return thread_id

def new_chat():
    thread_id=generate_thread()
    st.session_state['thread_id']=thread_id
    add_thread(thread_id)
    st.session_state['message_history']=[]

def add_thread(thread_id):
    if thread_id not in st.session_state['threads']:
        st.session_state['threads'].append(thread_id)

def get_messages(thread_id):
    if(chatbot.get_state(config={'configurable':{'thread_id':thread_id}}).values=={}):
        return []
       
    return chatbot.get_state(config={'configurable':{'thread_id':thread_id}}).values['messages']
def add_threads_set():
    thread_set=set()
    for checkpoint in checkpoint.list(None):
        thread_set.add(checkpoint[0]['configurable']['thread_id'])
    return list(thread_set)

if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]
if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=generate_thread()
if 'threads' not in st.session_state:
    st.session_state['threads']=add_threads_set()
add_thread(st.session_state['thread_id'])

st.sidebar.title('Langraph chatbot')
if st.sidebar.button('New Chat'):
    new_chat()

st.sidebar.header("My conversations")
for thread_id in st.session_state['threads']:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id']=thread_id
        messages=get_messages(thread_id)
        temp=[]
        for message in messages:
            if isinstance(message,HumanMessage):
                role='user'
            else:
                role='assistant'
            temp.append({'role':role,'content':message.content})
        st.session_state['message_history']=temp
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])
user_input=st.chat_input("Type here")
config={'configurable':{'thread_id':st.session_state['thread_id']}}

if user_input:
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message("user"):
        st.text(user_input)
    
   
    with st.chat_message("assistant"):
       ai_message=st.write_stream(
           message_chunk.content for message_chunk,meta_deta in chatbot.stream(
               {'messages':[HumanMessage(content=user_input)]},
               config=config,
               stream_mode='messages'
           )
       )
   
    st.session_state['message_history'].append({'role':'assistant','content':ai_message})

        