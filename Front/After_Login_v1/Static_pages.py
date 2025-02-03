import streamlit as st
from streamlit import session_state as ss
from PIL import Image

img_path = Image.open(ss.dir + "/circular_logo.png")
from functions import footer

def homepage():
    with st.container():
        st.write("---")
        text_column, image_column = st.columns((1, 2))
        with text_column:
            st.subheader("Design the perfect gRNA for your research")
            jtext = st.markdown("""
                    Clustered Regularly Interspaced Short Palindromic Repeats (CRISPR)-associated protein 9 (Cas9)
                    is a powerful genome editing tool utilized across a wide range of organisms,
                    from prokaryotes to humans. A crucial component of this system is the guide RNA (gRNA),
                    which directs the CRISPR complex to its target sequence.

                    Castor—a streamlined tool designed to simplify the gRNA design process for researchers.
                    Castor incorporates established algorithms in an intuitive environment,
                    making the process of designing and evaluating gRNAs both efficient and widely accessible.
                    """)
        with image_column:
            st.image(img_path, width=500)
    footer()

# def user_info():
#     """Provides admin user information
#     """
#     st.title('User Information')
#     folder = '/data'


def change_details():
    """Changes Credentails
    """
    st.title('Change Credentials')

    st.subheader("Currently this feature is under development")
    footer()

def about():
    """Provides Developer Information
    """
    st.title("About")
    st.divider()

    st.header('Developer Information')

    st.markdown('### Backend Devs')
    st.markdown("""
    <ul style="font-size: 18px;">
        <li>Bishal</li>
        <li>Mateo</li>
        <li>Zeynep</li>
    </ul>
    """, unsafe_allow_html=True)

    st.markdown('### Frontend Devs')
    st.markdown("""
    <ul style="font-size: 18px;">
        <li>Pablo</li>
        <li>Raghvendra</li>
    </ul>
    """, unsafe_allow_html=True)

    st.divider()
    st.text("Mail to report issues faced - raghvendra.agrawal@stud-uni.goettingen.de")
    footer()

def logout():
    """Sign out the user"""
    st.title('Logout')
    st.divider()
    st.subheader("Currently this feature is under development")

    footer()


