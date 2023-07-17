import streamlit as st
from PIL import Image
from glob import glob
import os
import funcoes
import numpy as np
import modelo_final

# configuracao da página
st.set_page_config(page_title='Detector de DeepFakes', page_icon='🔍️', layout="wide", 
                   initial_sidebar_state="auto", menu_items=None)
""" # Detector de DeepFake
Projeto de conclusão do curso MBA em Machine Learning. """
""" *** """
if st.button("Nova análise"): 
   uploaded_video = None
   funcoes.limpar()
## Caixa de Upload
with st.form("caixa_upload", clear_on_submit=True):
  uploaded_video = st.file_uploader("Faça o upload de um vídeo em .mp4", accept_multiple_files=False)
  botao_enviar = st.form_submit_button("Enviar vídeo e analisar.")
if uploaded_video is not None:
  if uploaded_video.name.split('.')[1] == 'mp4' or uploaded_video.name.split('.')[1] == 'mpg4':
    funcoes.save_uploaded_video(uploaded_video)
    video_file = funcoes.play_video()
    video_bytes = video_file.read()
    st.write("Upload concluído.")
    st.video(video_bytes)
    """ *** """
    st.write("Análise de frames:")
    funcoes.save_faces(funcoes.caminho_video())
    analise = modelo_final.roda_modelo()
    frames = analise[0]
    real = analise[1]
    fake = analise[2]
    final_real = analise[3]
    final_fake = analise[4]
  if uploaded_video is not None:
    #img_faces = image_select(label="",images= funcoes.caminho_faces(),captions=[0,1,2,3,4,5,6,7,8,9],use_container_width=False)
    #st.image(img_faces)
    faces_list = funcoes.caminho_faces()
    idx = 0 
    for _ in range(len(faces_list)-1): 
        cols = st.columns(5) 
        
        if idx < len(faces_list): 
            cols[0].image(faces_list[idx], width=150, caption=("""_REAL_:"""+str(real[idx].round(4)),"""_FAKE_:"""+str(fake[idx].round(4))))
        idx+=1
        if idx < len(faces_list):
            cols[1].image(faces_list[idx], width=150, caption=("""_REAL_:"""+str(real[idx].round(4)),"""_FAKE_:"""+str(fake[idx].round(4))))
        idx+=1
        if idx < len(faces_list):
            cols[2].image(faces_list[idx], width=150, caption=("""_REAL_:"""+str(real[idx].round(4)),"""_FAKE_:"""+str(fake[idx].round(4))))
        idx+=1 
        if idx < len(faces_list): 
            cols[3].image(faces_list[idx], width=150, caption=("""_REAL_:"""+str(real[idx].round(4)),"""_FAKE_:"""+str(fake[idx].round(4))))
            idx = idx + 1
        if idx < len(faces_list): 
          cols[4].image(faces_list[idx], width=150, caption=("""_REAL_:"""+str(real[idx].round(4)),"""_FAKE_: """+str(fake[idx].round(4))))
          idx = idx + 1
        else:
            break
    """ *** """
    st.write("Resultado final:")
    funcoes.gera_gif()
    col1,col2 = st.columns(2)
    with col1:
      st.image('../data/interim/analise.gif')
    with col2:
      st.write("Probabilidade de ser Real: ",final_real)
      st.write("Probabilidade de ser um Deep Fake: ",final_fake)
      if st.button("Nova análise2"): funcoes.limpar()
  else:
    st.write('Arquivo não compatível. Por favor refaça o upload de um arquivo de vídeo em .mp4.')

