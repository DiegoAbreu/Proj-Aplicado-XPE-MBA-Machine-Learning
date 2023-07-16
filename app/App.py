import streamlit as st
from PIL import Image
from glob import glob
import os

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

def save_uploadedvideo(uploadedfile):
    try:
        with open(os.path.join("data/external/",uploadedfile.name),"wb") as f:
            f.write(uploadedfile.getbuffer())
    except: 
       with open(os.path.join("../data/external/",uploadedfile.name),"wb") as f:
            f.write(uploadedfile.getbuffer())

## Caixa de Upload
with st.form("my-form", clear_on_submit=True):
  uploaded_files = st.file_uploader("Envie um arquivo .ZIP com todas as planilhas de funcionários + o arquivo de consolidação do parceiro em xlsx.", accept_multiple_files=True)
  submitted = st.form_submit_button("Processar")
  if submitted and uploaded_files is not None:
    st.write("Leitura concluída.")
    for i in uploaded_files:
      if i.name.split('.')[1] == 'mp4' or i.split('.')[1] == 'mpg4':
        save_uploadedvideo(i)
        video_file = open(glob('../data/external/*.mp4')[0], 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)
        st.write('Autor: Diego Abreu')
      else:
          st.write('Arquivo não compatível. Por favor refaça o upload de um arquivo de vídeo em .mp4.')

