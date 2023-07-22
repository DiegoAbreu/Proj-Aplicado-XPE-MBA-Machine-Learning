import os
import cv2
from glob import glob
from PIL import Image
import time

# Salva vídeo
def save_uploaded_video(uploadedfile):
    with open(os.path.join("data/external/","video_upload.mp4"),"wb") as f:
            f.write(uploadedfile.getbuffer())

# Caminho do vídeo
def caminho_video():
    return glob('data/external/*.mp4')[0]

# Visualiza vídeo
def play_video():
    return open(glob('data/external/*.mp4')[0], 'rb')

# Caminho das faces
def caminho_faces():
    return glob('data/interim/faces/*.jpg')

# Exclusão de arquivos importados
def limpar():
    filelist = [ f for f in os.listdir('data/external/') if (f.endswith(".mp4") or f.endswith(".mpg4"))]
    for f in filelist:
        os.remove(os.path.join('data/external/', f))
    filelist = [ f for f in os.listdir('data/interim/faces/') if (f.endswith(".jpg"))]
    for f in filelist:
        os.remove(os.path.join('data/interim/faces/', f))
    filelist = [ f for f in os.listdir('data/interim/') if (f.endswith(".gif"))]
    for f in filelist:
        os.remove(os.path.join('data/interim/', f))

# Captura de face:
face_cascade = cv2.CascadeClassifier('src/features/haarcascades/haarcascade_frontalface_default.xml')

def ROI(img):
    offset = 30 
    face_img = img.copy()
    face_rects = face_cascade.detectMultiScale(face_img,scaleFactor=1.3, minNeighbors=5) 
    for (x,y,w,h) in face_rects: 
        roi = face_img[y-offset:y+h+offset,x-offset:x+w+offset] 
    return roi

def save_faces(arquivo_video):
    cap = cv2.VideoCapture(arquivo_video)
    ret,frame = cap.read()
    count = 0
    try:
        while count < 10:
            cap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))   
            ret,frame = cap.read()
            image0 = frame
            image0 = ROI(image0)
            arquivo = arquivo_video.replace("data/external","").replace(".mp4","")
            arquivo_nome = "data/interim/faces/"+ arquivo + "_" + str(count) + ".jpg"
            cv2.imwrite(arquivo_nome,image0)
            count = count + 1
    except:
        pass


def gera_gif():
    frames = [Image.open(image) for image in glob('data/interim/faces/*jpg')]
    frame_one = frames[0]
    frame_one.save("data/interim/analise.gif", format="GIF", append_images=frames,
               save_all=True, duration=300, loop=0)