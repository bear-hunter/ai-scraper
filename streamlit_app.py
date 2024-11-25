import streamlit as st
import base64

# Helper function to set the background image and text styling
def set_background_and_style():
    # CSS to set the background and style elements
    page_bg = """
    <style>
    .stApp {{
        background: url("data:image/png;base64,{image_file}") no-repeat center fixed;
        background-size: cover;
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
    """.format(image_file=bg_image_encoded)
    st.markdown(page_bg, unsafe_allow_html=True)

# Load and encode the background image
with open("background.png", "rb") as bg_file:
    bg_image_encoded = base64.b64encode(bg_file.read()).decode()

# Initialize session state
if "accounts" not in st.session_state:
    st.session_state["accounts"] = {"user1": "user1"}  # Default account
if "page" not in st.session_state:
    st.session_state["page"] = "Login"

# Function to navigate between pages
def navigate_to(page_name):
    st.session_state["page"] = page_name

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
            # Add the new account
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
    st.write("Enter the URL of the website you want to scrape:")
    
    url = st.text_input("🔗 Website URL")
    
    if st.button("Start Scraping"):
        if url:
            with st.spinner("Scraping the website..."):
                st.success("✅ Scraping complete! (Functionality coming soon.)")
        else:
            st.error("❌ Please enter a valid URL.")

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
        We are the **Scraping Crusaders**, a passionate group of developers specializing in web scraping 
        and data extraction. Our mission is to make data collection seamless, efficient, and actionable.
    </p>
    <p style="font-size: medium; text-align: justify;">
        Whether it's navigating complex DOM structures or solving captchas, we embrace challenges to 
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
