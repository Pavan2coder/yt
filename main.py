import streamlit as st
import langchain_helper as lch
import textwrap

st.title("YouTube Assistant")

# Use 'with' notation for the sidebar to keep code clean
with st.sidebar:
    with st.form(key='my_form'):
        # Input for the YouTube link
        youtube_url = st.text_area(
            label="What is the YouTube video URL?",
            max_chars=100
        )
        
        # Input for the user's question
        query = st.text_area(
            label="Ask me about the video:",
            max_chars=100,
            key="query"
        )
        
        # Form submit button
        submit_button = st.form_submit_button(label='Submit')

# When the user clicks submit and both fields are filled:
if submit_button and query and youtube_url:
    # 1. Show a loading spinner so the user knows it's working
    with st.spinner("Downloading transcript and reading video..."):
        # 2. Build the database
        db = lch.create_db_from_youtube_video_url(youtube_url)
        
        # 3. Ask Gemini the question
        response, docs = lch.get_response_from_query(db, query)
        
    # 4. Display the answer!
    st.subheader("Answer:")
    st.text(textwrap.fill(response, width=85))