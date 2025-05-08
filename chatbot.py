import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import streamlit as st
import time

# Load Data
df_project = pd.read_csv(r"C:\Users\santh\OneDrive\Desktop\finale\Project.csv")
df_dev = pd.read_csv(r"C:\Users\santh\OneDrive\Desktop\finale\developers.csv")
df_lead = pd.read_csv(r"C:\Users\santh\OneDrive\Desktop\finale\Lead.csv")
df_scrum = pd.read_csv(r"C:\Users\santh\OneDrive\Desktop\finale\Scrummaster.csv")

# Preprocess text
nltk.download("punkt")
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

def preprocess_text(text):
    words = word_tokenize(text.lower())
    return [word for word in words if word.isalnum() and word not in stop_words]

def search_info(query):
    query_tokens = preprocess_text(query)
    results = {"Project": None, "Developer": None, "Lead": None, "Scrum Master": None}
    datasets = {"Project": df_project, "Developer": df_dev, "Lead": df_lead, "Scrum Master": df_scrum}
    
    for category, df in datasets.items():
        for _, row in df.iterrows():
            row_text = " ".join(str(value) for value in row)
            row_tokens = preprocess_text(row_text)
            if any(token in row_tokens for token in query_tokens):
                results[category] = row.to_dict()
                break  # Stop searching after the first match
    return results

# Streamlit Page Config
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

# Sidebar with chatbot details
st.sidebar.image("https://source.unsplash.com/400x400/?robot,ai", use_container_width=True)  # updated to use_container_width
st.sidebar.title("🤖 Chatbot Info")
st.sidebar.write("This chatbot helps you find details about projects, developers, leads, and Scrum Masters.")

# Custom CSS for Styling
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://source.unsplash.com/1600x900/?technology,abstract");
        background-size: cover;
        background-position: center;
    }
    .chat-container {
        width: 60%;
        margin: auto;
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 5px 5px 20px rgba(0,0,0,0.2);
    }
    .chat-header {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        color: #0078ff;
    }
    .chat-bubble {
        background: #0078ff;
        color: white;
        padding: 10px;
        border-radius: 15px;
        max-width: 80%;
        margin-bottom: 10px;
    }
    .user-bubble {
        background: #e6e6e6;
        color: black;
        padding: 10px;
        border-radius: 15px;
        max-width: 80%;
        margin-bottom: 10px;
        text-align: right;
        margin-left: auto;
    }
    .typing-animation::after {
        content: " .";
        animation: dots 1.5s steps(3, end) infinite;
    }
    @keyframes dots {
        0% { content: " ."; }
        33% { content: " .."; }
        66% { content: " ..."; }
        100% { content: " ."; }
    }
    </style>
""", unsafe_allow_html=True)

# Chatbot UI
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
st.markdown("<div class='chat-header'>🤖 AI Chatbot</div>", unsafe_allow_html=True)

# User Input
user_input = st.text_input("🔍 Ask me about projects, developers, or teams...", key="user_query")

# Search Button
if st.button("Chat 💬"):
    if user_input:
        st.markdown(f"<div class='user-bubble'>{user_input}</div>", unsafe_allow_html=True)
        
        # Show typing animation
        typing_placeholder = st.empty()
        typing_placeholder.markdown("<div class='chat-bubble typing-animation'>AI is typing...</div>", unsafe_allow_html=True)
        
        # Simulate AI response delay
        time.sleep(1.5)
        
        # Stop typing animation and show the answer
        typing_placeholder.empty()
        
        # Search and Display Results
        results = search_info(user_input)
        for category, data in results.items():
            if data:
                response = f"✅ {category} Found:<br>"
                for key, value in data.items():
                    response += f"<strong>{key}:</strong> {value}<br>"
                st.markdown(f"<div class='chat-bubble'>{response}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

