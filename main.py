import streamlit as st
from scrape import (scrape_website, split_dom_content, extract_body_content, clean_body_content)
from parse import parse_with_ollama

st.set_page_config(page_title="AI Web Scraper", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stTextInput > div > div > input {
        background-color: #2D2D2D;
        color: #FFFFFF;
        border: 1px solid #4A4A4A;
    }
    .stTextArea > div > div > textarea {
        background-color: #2D2D2D;
        color: #FFFFFF;
        border: 1px solid #4A4A4A;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stExpander {
        border-color: #4A4A4A;
    }
    .stExpander > div > div > div > div {
        background-color: #2D2D2D;
        color: #FFFFFF;
    }
    .stJson {
        background-color: #2D2D2D;
        color: #FFFFFF;
    }
    .loading-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.7);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        backdrop-filter: blur(5px);
    }
    .loading-spinner {
        border: 16px solid #4A4A4A;
        border-top: 16px solid #3498db;
        border-radius: 50%;
        width: 120px;
        height: 120px;
        animation: spin 2s linear infinite;
        margin-bottom: 20px;
    }
    .loading-text {
        color: #FFFFFF;
        font-size: 18px;
        text-align: center;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .title {
        color: #3498db;
        font-weight: bold;
    }
    .stTextInput > label {
        color: #FF9800; /* Nice orange color */
    }
    .stTextArea > label {
        color: #FF9800; /* Nice orange color */
    }
    .stAlert > div {
        background-color: #444444 !important;
        border-left: 5px solid #FF9800 !important;
        color: #FFFFFF !important;
    }
    .stAlert > div[data-baseweb="notification-success"] {
        border-left: 5px solid #00FF00 !important; /* Bright green */
    }
    .stAlert > div[data-baseweb="notification-error"] {
        border-left: 5px solid #FF0000 !important; /* Bright red */
    }
    </style>
    """, unsafe_allow_html=True)

# Function to show loading overlay
def show_loading_overlay(message):
    with st.spinner(message):
        loading_placeholder = st.empty()
        loading_placeholder.markdown(f"""
            <div class="loading-overlay">
                <div class="loading-spinner"></div>
                <div class="loading-text">{message}</div>
            </div>
        """, unsafe_allow_html=True)
        return loading_placeholder

st.markdown('<div style="padding: 1rem 0;"></div>', unsafe_allow_html=True)
st.markdown('<h1 class="title">🌐 AI Web Scraper</h1>', unsafe_allow_html=True)

url = st.text_input("🔗 Enter a Website URL:")

if st.button("🚀 Scrape Site"):
    loading_overlay = show_loading_overlay("Scraping website...")
    
    try:
        result = scrape_website(url)
        body_content = extract_body_content(result)
        cleaned_content = clean_body_content(body_content)

        st.session_state.dom_content = cleaned_content

        with st.expander("🔍 View DOM Content"):
            st.text_area("DOM Content", cleaned_content, height=300)
        
        st.success("Website scraped successfully!")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    finally:
        loading_overlay.empty()

if "dom_content" in st.session_state:
    parse_description = st.text_area("📝 Describe what you want to parse:")

    if st.button("🧠 Parse Content"):
        if parse_description:
            loading_overlay = show_loading_overlay("Parsing content...")
            
            try:
                dom_chunks = split_dom_content(st.session_state.dom_content)
                result = parse_with_ollama(dom_chunks, parse_description)
                
                st.subheader("📊 Parsing Results")
                # Extract only the keys (e.g., "Tutorials", "Courses") from parsed JSON and display them as plain text
                plain_text_result = "\n".join(
                    key for item in result if isinstance(item, dict) for key in item.keys()
                )
                
                st.text(plain_text_result)  # Display the headings as plain text
            except Exception as e:
                st.error(f"An error occurred during parsing: {str(e)}")
            finally:
                loading_overlay.empty()
        else:
            st.warning("Please provide a description of what you want to parse.")

# Add a footer
st.markdown("---")
st.markdown("Created with ❤️ by Arjun | [GitHub](https://github.com/ArjunAmbavane01)")
