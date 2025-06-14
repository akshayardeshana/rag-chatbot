import streamlit as st
import requests
from rag_engine import get_response

st.title("RAG Chatbot – Complaint Assistant")

if 'session' not in st.session_state:
    st.session_state.session = {
        'step': 'start',
        'name': None,
        'email': None,
        'phone': None,
        'details': None,
        'complaint_id': None
    }

msg = st.chat_input("Type your message")
if msg:
    st.chat_message("user").write(msg)
    session = st.session_state.session

    if session['step'] == 'start':
        if "register" in msg.lower() or "file" in msg.lower():
            session['step'] = 'ask_name'
            st.chat_message("assistant").write("Sure, I can help. What's your name?")
        elif "status" in msg.lower() or "find" in msg.lower() or "show details" in msg.lower():
            if session['complaint_id']:
                res = requests.get(f"http://localhost:8000/complaints/{session['complaint_id']}")
                if res.status_code == 200:
                    data = res.json()
                    st.chat_message("assistant").write(
                        f"Complaint ID: {data['complaint_id']}\nStatus: {data['status']}\nDetails: {data['complaint_details']}\nCreated: {data['created_at']}"
                    )
                else:
                    st.chat_message("assistant").write("❌ No complaint found for your number.")
            else:
                session['step'] = 'ask_status_complaint_id'
                st.chat_message("assistant").write("Please enter your complaint_id to check your complaint status.")
        else:
            rag_reply = get_response(msg)
            st.chat_message("assistant").write(rag_reply)

    elif session['step'] == 'ask_name':
        session['name'] = msg.strip().title()
        session['step'] = 'ask_email'
        st.chat_message("assistant").write("Thanks. Can I have your email?")


    elif session['step'] == 'ask_email':
        session['email'] = msg.strip().title()
        session['step'] = 'ask_phone'
        st.chat_message("assistant").write("Thanks. Can I have your 10-digit phone number?")

    elif session['step'] == 'ask_phone':
        if len(msg.strip()) == 10 and msg.strip().isdigit():
            session['phone'] = msg.strip()
            session['step'] = 'ask_details'
            st.chat_message("assistant").write("Got it. Please describe your complaint.")
        else:
            st.chat_message("assistant").write("That doesn't look like a valid 10-digit number. Please re-enter.")

    elif session['step'] == 'ask_details':
        session['details'] = msg.strip()
        res = requests.post("http://localhost:8000/complaints", json={
            "name": session['name'],
            "email": session['email'],
            "phone_number": session['phone'],
            "complaint_details": session['details']
        })
        if res.status_code == 200:
            session['complaint_id'] = res.json()['complaint_id']
            st.chat_message("assistant").write(f"✅ Complaint registered! Your ID is: {session['complaint_id']}")
        else:
            st.chat_message("assistant").write("❌ Failed to register complaint.")
        session['step'] = 'start'
        session['name'] = session['phone'] = session['details'] = None

    elif session['step'] == 'ask_status_complaint_id':
        session['complaint_id'] = msg.strip()
        res = requests.get(f"http://localhost:8000/complaints/{session['complaint_id']}")
        if res.status_code == 200:
            data = res.json()
            st.chat_message("assistant").write(
                f"Complaint ID: {data['complaint_id']}\nStatus: {data['status']}\nDetails: {data['complaint_details']}\nCreated: {data['created_at']}"
            )
        else:
            st.chat_message("assistant").write("❌ No complaint found for your complaint_id.")
        session['step'] = 'start'
        
    else:
        rag_reply = get_response(msg)
        st.chat_message("assistant").write(rag_reply)
