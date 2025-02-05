#COVER PAGE CASTOR
#Libraries section
import streamlit as st #main library
from PIL import Image #for add images

#Load section
img_path = Image.open("images/circular_logo.png")
#Tab section
st.set_page_config(page_title="Castor: A CRISPR Guide RNA Design Tool",
                   layout="wide",
                   page_icon=img_path, initial_sidebar_state="auto")

#Top quick buttons
with st.container():
    sp1,sp2,sp3,sp4,sp5,sp6,sp7,sp8,sp9,sp10,sp11,sp12,sp13  = st.columns(13)
    with sp11:
        st.image(img_path, width=100)
    with sp12:
        if st.button("Sign up", icon=":material/start:", use_container_width=True):
            st.switch_page("./pages/signup.py")
    with sp13:
        if st.button("Login", icon=":material/login:",use_container_width=True):
            st.switch_page("./pages/login.py")


#Header section

    st.markdown("<h1 style='text-align: center; color: black;'>Castor: A CRISPR Guide RNA Design Tool</h1>", unsafe_allow_html=True)

    st.write("---")
    text_column, image_column = st.columns(2)
    with text_column:
        st.subheader("Design the perfect :red[gRNA] for your research")
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
        st.image(img_path, width=400)

#Signup page
with st.container():
    st.write("---")
    block1,block2,block3,block4,block5,block6,block7,block8,block9 = st.columns(9)
    with block5:
        if st.button("Get Started", icon="🧬", use_container_width=True):
            st.switch_page("./pages/signup.py")

with st.container():
    st.write("---")
    space1,space2,space3,space4,space5,space6,space7,space8,space9,space10,space11 = st.columns(11)
    with space6:
        st.markdown("<p style='text-align: right; color: black;'>© 2025 Castor<p>", unsafe_allow_html=True)

