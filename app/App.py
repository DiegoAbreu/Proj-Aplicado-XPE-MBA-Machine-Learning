import streamlit as st
from PIL import Image

st.set_page_config(page_title='Detector de DeepFakes', page_icon='🔍️', layout="wide", 
                   initial_sidebar_state="auto", menu_items=None)
st.title("Projeto Aplicado XPE | MBA em Machine Learning")
st.write('Autor: Diego Abreu')

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)

#image = Image.open('https://raw.githubusercontent.com/DiegoAbreu/Proj-Aplicado-XPE-MBA-Machine-Learning/main/references/images/Arquitetura.png')

st.image('https://raw.githubusercontent.com/DiegoAbreu/Proj-Aplicado-XPE-MBA-Machine-Learning/main/references/images/Arquitetura.png', 
          caption='Sunrise by the mountains')