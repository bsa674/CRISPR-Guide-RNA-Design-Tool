'''
Author : Raghvendra Agrawal
Function :
This is the main file for the Castor_gRNA project. It contains the main page of the web application.

Date of Modified : 17th February, 2025
'''

# Libraries
import streamlit as st
from streamlit import session_state as ss
from PIL import Image
import base64

from pages.functions import footer,button_style
# Load image
try:
    img_path = Image.open("images/circular_logo.png")
except FileNotFoundError:
    st.error("Image file not found. Please check the path.")
    img_path = None

# Page config

if 'page_state' not in ss.keys():
    ss.page_state = 'main'

if ss.page_state == 'main':
    st.set_page_config(
        page_title="Castor: A CRISPR Guide RNA Design Tool",
        layout="wide",
        page_icon=img_path,
        initial_sidebar_state="collapsed"
    )

# Custom CSS for animations and styling
custom_css = """
<style>
/* Animated gradient background */
@keyframes gradientBackground {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stApp {
    background: linear-gradient(270deg, #1a2a6c, #b21f1f, #fdbb2d);
    background-size: 600% 600%;
    animation: gradientBackground 15s ease infinite;
    color: white;
}

/* Animated title */
@keyframes colorChange {
    0% { color: #ff9a9e; }
    25% { color: #fad0c4; }
    50% { color: #a1c4fd; }
    75% { color: #c2e9fb; }
    100% { color: #ff9a9e; }
}

.animated-title {
    font-size: 48px;
    font-weight: bold;
    text-align: center;
    animation: colorChange 5s infinite;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
button_style()

# Background image
def set_background(img_background):
    with open(img_background, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

if ss.page_state == 'main':

    # Animated title
    st.markdown('<h1 class="animated-title">Welcome to Castor</h1>', unsafe_allow_html=True)

    # Header
    st.markdown("<h1 style='text-align: center; color: white; font-weight: bold; font-size: 70px;'>A CRISPR Guide RNA Design Tool</h1>", unsafe_allow_html=True)
    st.write("---")

    # Buttons with hover effects
    col1, col2, col3 = st.columns([3, 1, 1])
    with col2:
        if st.button("Sign up", icon=":material/start:", use_container_width=True):
            ss.page_state = 'signup'
            st.switch_page("./pages/signup.py")
    with col3:
        if st.button("Login", icon=":material/login:", use_container_width=True):
            ss.page_state = 'login'
            st.switch_page("./pages/login.py")

    # Main content
    text_column, image_column = st.columns(2, vertical_alignment="center")
    with text_column:
        st.markdown('<p class="animated-text" style="color:white; font-weight: bold; font-size: 40px;">Design the perfect gRNA for your research</p>', unsafe_allow_html=True)
        st.markdown("""
        <p class="animated-text" style="color: white; font-size: 30px;">
        Clustered Regularly Interspaced Short Palindromic Repeats (CRISPR)-associated protein 9 (Cas9)
        is a powerful genome editing tool utilized across a wide range of organisms,
        from prokaryotes to humans. A crucial component of this system is the guide RNA (gRNA),
        which directs the CRISPR complex to its target sequence.
        Castor—a streamlined tool designed to simplify the gRNA design process for researchers.
        Castor incorporates established algorithms in an intuitive environment,
        making the process of designing and evaluating gRNAs both efficient and widely accessible.
        </p>
        """, unsafe_allow_html=True)
    with image_column:
        st.markdown('<div class="image-hover">', unsafe_allow_html=True)
        st.image(img_path, width=400, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        block1,block2,block3,block4,block5,block6,block7,block8,block9 = st.columns(9)
        with block5:
            if st.button("Get Started", icon="🧬", use_container_width=True):
                ss.page_state = 'signup'
                st.switch_page("./pages/signup.py")

else:
#    st.text('Loading...')
    from streamlit.components.v1 import html
    import time

    # Glassmorphism loading screen CSS and HTML
    st.markdown("""
    <style>
    .loading-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    }

    .loading-content {
        background: rgba(255, 255, 255, 0.2);
        padding: 30px 50px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }

    .spinner {
        width: 40px;
        height: 40px;
        border: 4px solid #f3f3f3;
        border-top: 4px solid #3498db;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>

    <div class="loading-overlay" id="loadingOverlay">
        <div class="loading-content">
            <div class="spinner"></div>
            <h3 style="margin-top: 20px; color: #2c3e50;">Loading...</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # JavaScript to hide loading screen after delay
    html("""
    <script>
    setTimeout(function(){
        document.getElementById('loadingOverlay').style.display = 'none';
    }, 3000); // 3 seconds
    </script>
    """, width=0, height=0)
    with st.spinner("Logging in..."):
        time.sleep(2)
# Footer
footer()