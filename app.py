import streamlit as st

st.title("Projeto Aplicado XPE | MBA em Machine Learning")
st.write('Autor: Diego Abreu')

# Using object 
st.sidebar.title("Menu")
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )
