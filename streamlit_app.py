import streamlit as st
import base64
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os

# Hardcoded Gemini API key (replace 'your-api-key' with the actual key)
GEMINI_API_KEY = "AIzaSyCnm5q9bI4D1Y8TmrjVHO7UvLOIfkFsVec"


# Helper function to set the background and text styling
def set_background_and_style():
    # Ensure the background image is available
    image_path = "./background.png"  # Update this if the file is in a subdirectory, e.g., "static/background.png"
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()
        page_bg = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: white;
        }}
        .stButton>button {{
            background-color: black !important;
            color: white !important;
            border: 1px solid white !important;
            padding: 8px 16px !important;
            font-size: 16px !important;
            margin: 4px 2px !important;
            cursor: pointer !important;
            border-radius: 5px !important;
        }}
        .stButton>button:hover {{
            background-color: white !important;
            color: black !important;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: white !important;
        }}
        p, li {{
            color: white !important;
        }}
        .stTextInput > div > input {{
            background-color: black !important;
            color: white !important;
            border: 1px solid white !important;
            border-radius: 5px !important;
        }}
        </style>
        """
        st.markdown(page_bg, unsafe_allow_html=True)
    else:
        st.error("❌ Background image not found. Please ensure 'background.png' is in the correct directory.")


# Initialize session state
if "accounts" not in st.session_state:
    st.session_state["accounts"] = {"user1": "user1"}
if "page" not in st.session_state:
    st.session_state["page"] = "Login"

# Function to navigate between pages
def navigate_to(page_name):
    st.session_state["page"] = page_name

def scrape_website(url):
    """Scrape website content using BeautifulSoup."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator='\n', strip=True)
        lines = (line.strip() for line in text.splitlines())
        return '\n'.join(line for line in lines if line)[:15000]
    except Exception as e:
        return f"Error scraping website: {str(e)}"

def call_gemini_api(prompt, content):
    """Calls the Gemini API with the scraped content."""
    endpoint = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
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
            f"{endpoint}?key={GEMINI_API_KEY}",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        response_data = response.json()
        if 'candidates' in response_data:
            return response_data['candidates'][0]['content']['parts'][0]['text']
        return "No response content found."
    except requests.exceptions.RequestException as e:
        return f"Error calling Gemini API: {str(e)}"
    except KeyError as e:
        return f"Error parsing Gemini API response: {str(e)}"

# Pages (Login, Create Account, Home, Scrape, About Us)
# Each function is unchanged except for API key input removed from scrape_page.
def login_page():
    set_background_and_style()
    st.title("🔒 Login to Scraping Crusaders")
    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")
    if st.button("Login"):
        accounts = st.session_state["accounts"]
        if username in accounts and accounts[username] == password:
            navigate_to("Home")
        else:
            st.error("❌ Invalid username or password.")
    if st.button("Create Account"):
        navigate_to("Create Account")

def create_account_page():
    set_background_and_style()
    st.title("📝 Create an Account")
    new_username = st.text_input("👤 Choose a Username")
    new_password = st.text_input("🔑 Choose a Password", type="password")
    confirm_password = st.text_input("🔑 Confirm Password", type="password")
    if st.button("Create Account"):
        accounts = st.session_state["accounts"]
        if new_username in accounts:
            st.error("❌ Username already exists.")
        elif new_password != confirm_password:
            st.error("❌ Passwords do not match.")
        elif not new_username or not new_password:
            st.error("❌ Username and password cannot be empty.")
        else:
            accounts[new_username] = new_password
            st.success("✅ Account created successfully!")
            navigate_to("Login")

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
    **Unleash the Power of Web Data: Conquer Information Overload with Scraping Crusaders**

    Drowning in a sea of data? Struggling to extract meaningful insights from the endless stream of online content? You're not alone. In today's digital age, information overload is a real challenge. But what if you could harness the power of the web, effortlessly gathering and filtering information to uncover hidden gems of knowledge? Scraping Crusaders is your AI-powered ally in this data-driven crusade.

    Imagine: effortlessly summarizing complex articles, instantly extracting key product details from multiple websites, and uncovering hidden trends in customer reviews. No more tedious manual research, no more wasted time sifting through endless pages. Scraping Crusaders does the heavy lifting, delivering concise, accurate summaries directly to you.

    **Experience the freedom of knowledge at your fingertips. Join the Scraping Crusaders and transform information chaos into actionable insights.**

    **(Limited-time offer – don't miss out!)  ➡️  [Sign Up/Get Started Button Here]**  <--  Add a button/link here!
    """)

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
    url = st.text_input("🔗 Website URL")
    prompt = st.text_input("💡 Enter your prompt:")
    if st.button("Start Scraping and Analysis"):
        if url and prompt:
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                st.error("❌ Invalid URL.")
                return
            scraped_content = scrape_website(url)
            if scraped_content.startswith("Error"):
                st.error(scraped_content)
                return
            with st.expander("Show scraped content"):
                st.text_area("Scraped content:", scraped_content, height=200)
            analysis = call_gemini_api(prompt, scraped_content)
            st.subheader("Analysis Results:")
            st.write(analysis)
        else:
            st.error("❌ URL and prompt are required.")

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
    **Meet the Knights of Knowledge: The Story Behind Scraping Crusaders**

    We're not just another tech company; we're a team of passionate problem-solvers, driven by a shared belief in the transformative power of information. At Scraping Crusaders, we understand the frustration of information overload. We've been there, battling the endless scroll, struggling to keep up with the ever-expanding digital universe. That's why we embarked on a mission: to forge a powerful tool that could cut through the noise and empower individuals and organizations to conquer data chaos.

    We're more than just developers; we're architects of efficiency, crafting intelligent algorithms and intuitive interfaces to simplify your life. Our AI-powered engine, fueled by cutting-edge Natural Language Processing (NLP), acts as your personal research assistant, tirelessly gathering, filtering, and summarizing information so you can focus on what matters most.

    **Join our community of knowledge seekers. Together, let's unlock the full potential of the web and transform information overload into opportunity.** 

    [Learn More About Our Mission]  <-- Add a link here!
    """, unsafe_allow_html=True)  # No need for unsafe_allow_html now

# Page routing
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
