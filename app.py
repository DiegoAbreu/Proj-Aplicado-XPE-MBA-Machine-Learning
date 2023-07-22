import os
import sys
import streamlit as st
from PIL import Image
from glob import glob
path_funcoes = os.path.abspath("src/app")
sys.path.append(path_funcoes)
import funcoes
path_modelo = os.path.abspath("src/models")
sys.path.append(path_modelo)
import modelo_final

# configuracao da página
st.set_page_config(page_title='Detector de DeepFakes', page_icon='🔍️', layout="wide", 
                   initial_sidebar_state="auto", menu_items=None)
""" # Detector de DeepFake
Projeto de conclusão do curso MBA em Machine Learning. """
tab1, tab2= st.tabs(["Aplicação", "Sobre"])
with tab1:
  if st.button("Nova análise"): 
    funcoes.limpar()
    uploaded_video = None
  ## Caixa de Upload
  with st.form("caixa_upload", clear_on_submit=True):
    uploaded_video = st.file_uploader("Faça o upload de um vídeo em .mp4", accept_multiple_files=False)
    botao_enviar = st.form_submit_button("Enviar vídeo e analisar.")
    if botao_enviar and uploaded_video is not None:
      if uploaded_video.name.split('.')[1] == 'mp4' or uploaded_video.name.split('.')[1] == 'mpg4':
        funcoes.save_uploaded_video(uploaded_video)

  total_arquivos_mp4 = len(glob("data/external/*.mp4"))
  if total_arquivos_mp4 > 0:
    if uploaded_video.name.split('.')[1] == 'mp4' or uploaded_video.name.split('.')[1] == 'mpg4':
      funcoes.save_uploaded_video(uploaded_video)
      video_file = funcoes.play_video()
      video_bytes = video_file.read()
      st.write("Upload concluído.")
      st.video(video_bytes)
      """ *** """
      """ ### Análise de Frames: """
      funcoes.save_faces(funcoes.caminho_video())
      analise = modelo_final.roda_modelo()
      frames = analise[0]
      real = analise[1]
      fake = analise[2]
      final_real = analise[3]
      final_fake = analise[4]
    if uploaded_video is not None:
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
      """ ### Resultado Final: """
      funcoes.gera_gif()
      col1,col2 = st.columns(2)
      with col1:
        st.image('data/interim/analise.gif')
      with col2:
        """\n"""   
        """\n"""   
        """\n"""   
        """\n"""   
        #final_real = 5
        #final_fake = 10
        subcol1,subcol2= st.columns([1,4])
        if final_real > final_fake:
            with subcol1:
              st.image('references/images/resultado_real.png')
            with subcol2:
              """\n""" 
              """ #### REAL"""
        elif final_real == final_fake:
            """ #### INCONCLUSIVO """
        else:
            with subcol1:
              st.image('references/images/resultado_fake.png')
            with subcol2:
              """\n""" 
              """ #### DEEP FAKE """
        """\n"""   
        st.write("Probabilidade de ser Real: ",round((final_real*100),4))
        st.write("Probabilidade de ser um Deep Fake: ",round((final_fake*100),4))
    else:
      st.write('Arquivo não compatível. Por favor refaça o upload de um arquivo de vídeo em .mp4.')

with tab2:
  st.write('tal tala tal')
