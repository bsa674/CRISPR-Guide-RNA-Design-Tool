'''
Author : Raghvendra Agrawal
Function :
This file displays a thank you message to the user and redirects to the login page after a few seconds
Date of Modified : 17th February, 2025
'''

import streamlit as st
import time

# Center the content using HTML

# Apply custom styles
st.markdown("""
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

/* Animated title with a glow effect */
@keyframes colorChange {
    0% { color: #fff; text-shadow: 2px 2px 10px rgba(255, 154, 158, 0.8); }
    25% { color: #ffeb99; text-shadow: 2px 2px 10px rgba(250, 208, 196, 0.8); }
    50% { color: #a1c4fd; text-shadow: 2px 2px 10px rgba(161, 196, 253, 0.8); }
    75% { color: #c2e9fb; text-shadow: 2px 2px 10px rgba(194, 233, 251, 0.8); }
    100% { color: #fff; text-shadow: 2px 2px 10px rgba(255, 154, 158, 0.8); }
}

.animated-title {
    font-size: 48px;
    font-weight: bold;
    text-align: center;
    animation: colorChange 5s infinite;
    margin-top: 20%;
}

/* General Text Styling */
.centered-text {
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    color: #fff;
    text-shadow: 1px 1px 8px rgba(0, 0, 0, 0.5);
}

/* Countdown timer style */
#countdown {
    font-size: 26px;
    font-weight: bold;
    color: #ffeb99;
}
</style>
""", unsafe_allow_html=True)

# HTML content with countdown
st.markdown("""
<div class="animated-title">Thank You for Visiting! 😊</div>
<p class="centered-text">You have been logged out successfully.</p>
<p class="centered-text">Redirecting to the login page</p>
""", unsafe_allow_html=True)

# Wait for 3 seconds before redirecting
time.sleep(3)

# Redirect to login (refresh page)
st.switch_page("pages/login.py")  # Redirects back to the login page
