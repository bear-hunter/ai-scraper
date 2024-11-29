import streamlit as st
import base64
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
import time

# Helper function to set the background and text styling
def set_background_and_style():
    # CSS to set the background and style elements
    page_bg = """
    <style>
    .stApp {{
        background-color: #0e1117;
        color: white;
    }}
    .stButton>button {{
        background-color: black;
        color: white;
        border: 1px solid white;
        padding: 8px 16px;
        text-align: center;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border-radius: 5px;
    }}
    .stButton>button:hover {{
        background-color: white;
        color: black;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: white;
    }}
    p, li {{
        color: white;
    }}
    .stTextInput > div > input {{
        background-color: black;
        color: white;
        border: 1px solid white;
        border-radius: 5px;
    }}
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

# Initialize session state
if "accounts" not in st.session_state:
    st.session_state["accounts"] = {"user1": "user1"}  # Default account
if "page" not in st.session_state:
    st.session_state["page"] = "Login"

# Function to navigate between pages
def navigate_to(page_name):
    st.session_state["page"] = page_name

def scrape_website(url):
    """Scrape website content using BeautifulSoup."""
    try:
        # Add headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Make the request
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse the content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text and clean it up
        text = soup.get_text(separator='\n', strip=True)
        
        # Clean up extra whitespace and empty lines
        lines = (line.strip() for line in text.splitlines())
        text = '\n'.join(line for line in lines if line)
        
        return text[:15000]  # Limit text length to avoid token limits
        
    except Exception as e:
        return f"Error scraping website: {str(e)}"

def call_gemini_api(api_key, prompt, content):
    """Calls the Gemini API with the scraped content."""
    endpoint = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
    
    # Construct the payload
    payload = {
        "contents": [{
            "parts": [{
                "text": f"{prompt}\n\nContent to analyze:\n{content}"
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.8,
            "maxOutputTokens": 1000,
        }
    }
    
    try:
        response = requests.post(
            f"{endpoint}?key={api_key}",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        
        # Parse the response
        response_data = response.json()
        if 'candidates' in response_data:
            return response_data['candidates'][0]['content']['parts'][0]['text']
        return "No response content found."
    except requests.exceptions.RequestException as e:
        return f"Error calling Gemini API: {str(e)}"
    except KeyError as e:
        return f"Error parsing Gemini API response: {str(e)}"

# Login Page
def login_page():
    set_background_and_style()
    st.title("🔒 Login to Scraping Crusaders")
    st.write("Please enter your credentials to log in.")
    
    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")
    
    if st.button("Login"):
        accounts = st.session_state["accounts"]
        if username in accounts and accounts[username] == password:
            navigate_to("Home")
        else:
            st.error("❌ Invalid username or password.")
    
    st.write("---")
    if st.button("Create Account"):
        navigate_to("Create Account")

# Create Account Page
def create_account_page():
    set_background_and_style()
    st.title("📝 Create an Account")
    st.write("Fill in the details below to create a new account.")
    
    new_username = st.text_input("👤 Choose a Username")
    new_password = st.text_input("🔑 Choose a Password", type="password")
    confirm_password = st.text_input("🔑 Confirm Password", type="password")
    
    if st.button("Create Account"):
        accounts = st.session_state["accounts"]
        
        if new_username in accounts:
            st.error("❌ Username already exists. Please choose a different username.")
        elif new_password != confirm_password:
            st.error("❌ Passwords do not match. Please try again.")
        elif not new_username or not new_password:
            st.error("❌ Username and password cannot be empty.")
        else:
            accounts[new_username] = new_password
            st.success("✅ Account created successfully! You can now log in.")
            st.button("Go to Login", on_click=lambda: navigate_to("Login"))

# Home Page
def home_page():
    set_background_and_style()
    st.sidebar.title("Navigation")
    if st.sidebar.button("Scrape"):
        navigate_to("Scrape")
    if st.sidebar.button("About Us"):
        navigate_to("About Us")
    if st.sidebar.button("Logout"):
        navigate_to("Login")
    
    st.title("🏠 Welcome to Scraping Crusaders")
    st.markdown("""
    <h1 style="text-align: center;">Scraping Crusaders</h1>
    <p style="font-size: large; text-align: center;">
        A team dedicated to extracting the web's hidden treasures.
    </p>
    <p style="font-size: medium; text-align: center; color: white;">
        Join us as we explore the digital landscape with innovation and expertise.
    </p>
    """, unsafe_allow_html=True)

# Scrape Page
def scrape_page():
    set_background_and_style()
    st.sidebar.title("Navigation")
    if st.sidebar.button("Home"):
        navigate_to("Home")
    if st.sidebar.button("About Us"):
        navigate_to("About Us")
    if st.sidebar.button("Logout"):
        navigate_to("Login")
    
    st.title("🌐 Scrape a Website")
    st.write("Enter the URL of the website you want to scrape and analyze:")
    
    # Add API key input
    api_key = st.text_input("🔑 Enter your Gemini API Key", type="password")
    url = st.text_input("🔗 Website URL")
    prompt = st.text_input("💡 Enter your prompt (e.g., 'Summarize this content' or 'What are the main points?'):")
    
    if st.button("Start Scraping and Analysis"):
        if not api_key:
            st.error("❌ Please enter your Gemini API key.")
            return
            
        if url and prompt:
            # Show a progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Validate URL
                parsed_url = urlparse(url)
                if not parsed_url.scheme or not parsed_url.netloc:
                    st.error("❌ Please enter a valid URL including http:// or https://")
                    return
                
                # Step 2: Scrape the website
                status_text.text("🔍 Scraping website content...")
                progress_bar.progress(25)
                scraped_content = scrape_website(url)
                
                if scraped_content.startswith("Error"):
                    st.error(scraped_content)
                    return
                
                # Step 3: Show scraped content (optional)
                with st.expander("Show scraped content"):
                    st.text_area("Raw scraped content:", scraped_content, height=200)
                
                # Step 4: Process with Gemini
                status_text.text("🤖 Analyzing content with Gemini...")
                progress_bar.progress(75)
                analysis = call_gemini_api(api_key, prompt, scraped_content)
                
                # Step 5: Show results
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
                
                st.subheader("Analysis Results:")
                st.write(analysis)
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
            
            finally:
                # Clean up progress indicators
                progress_bar.empty()
                status_text.empty()
        else:
            st.error("❌ Please enter both a URL and a prompt.")

# About Us Page
def about_us_page():
    set_background_and_style()
    st.sidebar.title("Navigation")
    if st.sidebar.button("Home"):
        navigate_to("Home")
    if st.sidebar.button("Scrape"):
        navigate_to("Scrape")
    if st.sidebar.button("Logout"):
        navigate_to("Login")
    
    st.title("📖 About Us")
    st.markdown("""
    <h1 style="text-align: center;">Scraping Crusaders</h1>
    <p style="font-size: large; text-align: justify;">
        We are the Scraping Crusaders, a passionate group of developers specializing in web scraping 
        and data extraction. Our mission is to make data collection seamless, efficient, and actionable.
    </p>
    <p style="font-size: medium; text-align: justify;">
        Whether it's navigating complex DOM structures or analyzing content, we embrace challenges to 
        unlock the full potential of web data. Join us as we continue our quest for knowledge and innovation!
    </p>
    <p style="font-size: small; text-align: center; color: white;">
        Designed with ❤️ by the Scraping Crusaders team.
    </p>
    """, unsafe_allow_html=True)

# Page Routing
if st.session_state["page"] == "Login":
    login_page()
elif st.session_state["page"] == "Create Account":
    create_account_page()
elif st.session_state["page"] == "Home":
    home_page()
elif st.session_state["page"] == "Scrape":
    scrape_page()
elif st.session_state["page"] == "About Us":
    about_us_page()
