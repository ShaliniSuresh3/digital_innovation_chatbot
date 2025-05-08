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

# Download NLTK Resources
nltk.download("punkt")
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

# Preprocess Text
def preprocess_text(text):
    words = word_tokenize(text.lower())
    return [word for word in words if word.isalnum() and word not in stop_words]

# Define Keywords for Dataset Matching
keywords = {
    "Lead": ["lead", "leader", "team lead", "head", "management"],
    "Scrum Master": ["scrum", "scrum master", "agile", "sprint"],
    "Developer": ["developer", "engineer", "programmer", "coder"],
    "Project": ["project", "timeline", "budget", "progress", "metrics"]
}

# Function to Detect Question Category
def detect_category(query):
    query_tokens = preprocess_text(query)
    for category, words in keywords.items():
        if any(word in query_tokens for word in words):
            return category
    return None

# Function to Search Relevant Data in a Specific Dataset
def search_info(query, category):
    dataset_mapping = {
        "Lead": df_lead,
        "Scrum Master": df_scrum,
        "Developer": df_dev,
        "Project": df_project
    }
    
    df = dataset_mapping.get(category)
    if df is None:
        return "Sorry, I couldn't find relevant information."

    query_tokens = preprocess_text(query)
    for _, row in df.iterrows():
        row_text = " ".join(str(value) for value in row)
        row_tokens = preprocess_text(row_text)
        if any(token in row_tokens for token in query_tokens):
            return row.to_dict()
    
    return f"Sorry, no matching {category} data found."

# Streamlit Page Configuration
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

# Sidebar with Chatbot Details
st.sidebar.title("🤖 Chatbot Info")
st.sidebar.write("This chatbot provides precise answers based on Leads, Scrum Masters, Developers, and Project Metrics.")

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

# Initialize session state for chat history and input field
if 'history' not in st.session_state:
    st.session_state.history = []

if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# Chatbot UI
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
st.markdown("<div class='chat-header'>🤖 AI Chatbot</div>", unsafe_allow_html=True)

# User Input Field
user_input = st.text_input("🔍 Ask me about projects, developers, or teams...", value=st.session_state.user_input, key="user_query")

# Search Button
if st.button("Search 💬"):
    if user_input.strip():  # Ensure input isn't empty
        # Add user input to history
        st.session_state.history.append(f"User: {user_input}")
        
        # Show typing animation
        typing_placeholder = st.empty()
        typing_placeholder.markdown("<div class='chat-bubble typing-animation'>AI is typing...</div>", unsafe_allow_html=True)
        
        # Simulate AI response delay
        time.sleep(1.5)
        
        # Stop typing animation
        typing_placeholder.empty()
        
        # Detect Category
        category = detect_category(user_input)
        if category:
            # Search and Display Results
            result = search_info(user_input, category)
            if isinstance(result, dict):
                ai_response = f"✅ {category} Data Found:<br>"
                for key, value in result.items():
                    ai_response += f"<strong>{key}:</strong> {value}<br>"
            else:
                ai_response = result
        else:
            ai_response = "Sorry, I couldn't determine what category your question belongs to. Try using terms like 'Lead', 'Scrum Master', 'Developer', or 'Project'."
        
        # Add AI response to history
        st.session_state.history.append(f"AI: {ai_response}")
        
        # Clear input field in session state
        st.session_state.user_input = ""

# Display conversation history
for message in st.session_state.history:
    if message.startswith("User:"):
        st.markdown(f"<div class='user-bubble'>{message[6:]}</div>", unsafe_allow_html=True)
    elif message.startswith("AI:"):
        st.markdown(f"<div class='chat-bubble'>{message[4:]}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
