import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import HumanMessage  # for chat-style prompts

# Initialize the ChatOllama model
OLLAMA_MODEL_NAME = "llama3.2:1b"
llm = ChatOllama(model=OLLAMA_MODEL_NAME)

# Prompt template for summarization
summarization_prompt = PromptTemplate(
    input_variables=["text"],
    template="Summarize the following text:\n\n{text}\n\nSummary:"
)

# Cache the transcript to avoid redundant API calls
@st.cache_data(show_spinner=False)
def get_transcript(video_url):
    try:
        # Extract video ID (handles extra URL parameters)
        video_id = video_url.split("v=")[-1].split("&")[0]
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        transcript = " ".join([item['text'] for item in transcript_data])
        return transcript
    except NoTranscriptFound:
        return None
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return None

def split_text(text, chunk_size=1000, overlap=100):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return text_splitter.split_text(text)

def summarize_text(text):
    try:
        prompt = summarization_prompt.format(text=text)
        # Send a chat-style message to ChatOllama
        response = llm([HumanMessage(content=prompt)])
        return response.content.strip()
    except Exception as e:
        st.error(f"Error during summarization: {e}")
        return None

def main():
    # Page configuration and custom styling
    st.set_page_config(page_title="AI-Powered YouTube Summarizer", layout="wide")
    st.markdown(
        """
        <style>
        /* Global body styles */
        body {
            background-color: #1e1e2f;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #f8f8f2;
            font-size: 18px;
        }
        /* Title styling */
        .title {
            text-align: center;
            color: #50fa7b;
            font-size: 48px;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        /* Subtitle and section header styling */
        .subtitle {
            text-align: center;
            color: #ff79c6;
            font-size: 24px;
            margin-bottom: 30px;
        }
        /* Button styling */
        .stButton button {
            background-color: #6272a4;
            color: #f8f8f2;
            font-size: 18px;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            margin: 5px;
        }
        .stButton button:hover {
            background-color: #bd93f9;
            color: #1e1e2f;
        }
        /* Text input styling */
        .stTextInput>div>div>input {
            background-color: #282a36;
            color: #f8f8f2;
            font-size: 18px;
            border: none;
            padding: 10px;
            border-radius: 8px;
        }
        /* Text area styling */
        textarea {
            background-color: #282a36;
            color: #f8f8f2;
            font-size: 18px;
            border-radius: 8px;
            padding: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Page header
    st.markdown("<h1 class='title'>AI-Powered YouTube Summarizer</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='subtitle'>Extract transcripts and generate smart summaries from YouTube videos.</p>",
        unsafe_allow_html=True
    )

    # Input for YouTube video URL
    video_url = st.text_input("YouTube Video URL:", value="", placeholder="https://www.youtube.com/watch?v=XXXX")

    # Two columns for actions
    col1, col2 = st.columns(2)

    # Get Transcript Section
    if col1.button("Get Transcript"):
        if video_url:
            with st.spinner("Fetching transcript..."):
                transcript = get_transcript(video_url)
            if transcript:
                st.markdown("<h2 class='subtitle'>Transcript</h2>", unsafe_allow_html=True)
                st.text_area("", transcript, height=300)
            else:
                st.error("Transcript not found. The video may not have captions or the URL might be invalid.")
        else:
            st.error("Please enter a valid YouTube URL.")

    # Summarize Section
    if col2.button("Summarize"):
        if video_url:
            with st.spinner("Fetching transcript..."):
                transcript = get_transcript(video_url)
            if transcript:
                st.markdown("<h2 class='subtitle'>Transcript</h2>", unsafe_allow_html=True)
                st.text_area("", transcript, height=300)
                with st.spinner("Summarizing transcript..."):
                    # Split transcript into chunks for summarization
                    chunks = split_text(transcript)
                    summaries = []
                    progress_bar = st.progress(0)
                    for i, chunk in enumerate(chunks):
                        summary = summarize_text(chunk)
                        if summary:
                            summaries.append(summary)
                        progress_bar.progress((i + 1) / len(chunks))
                    progress_bar.empty()
                    final_summary = " ".join(summaries)
                    st.markdown("<h2 class='subtitle'>Summary</h2>", unsafe_allow_html=True)
                    st.text_area("", final_summary, height=200)
            else:
                st.error("Failed to extract transcript for summarization.")
        else:
            st.error("Please enter a valid YouTube URL.")

if __name__ == "__main__":
    main()
