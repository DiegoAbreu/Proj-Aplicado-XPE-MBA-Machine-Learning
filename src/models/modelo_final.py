import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Input, Dense, Flatten, Conv2D, MaxPooling2D, BatchNormalization, Dropout, Reshape, Concatenate, LeakyReLU
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model
import pickle
from scipy.interpolate import griddata
from glob import glob
import cv2

# Tamanho a imagem e canais
image_dimensions = {'height':256, 'width':256, 'channels':3}

# Classe do classificador
class Classifier:
    def __init__():
        self.model = 0 
    def predict(self, x):
        return self.model.predict(x)  
    def fit(self, x, y):
        return self.model.train_on_batch(x, y)
    def get_accuracy(self, x, y):
        return self.model.test_on_batch(x, y)
    def load(self, path):
        self.model.load_weights(path)

# Rede Mesonet usando o Classificador
class Meso4(Classifier):
    def __init__(self, learning_rate = 0.001):
        self.model = self.init_model()
        optimizer = Adam(lr = learning_rate)
        self.model.compile(optimizer = optimizer,
                           loss = 'mean_squared_error',
                           metrics = ['accuracy'])
    
    def init_model(self): 
        x = Input(shape = (image_dimensions['height'],
                           image_dimensions['width'],
                           image_dimensions['channels']))
        
        x1 = Conv2D(8, (3, 3), padding='same', activation = 'relu')(x)
        x1 = BatchNormalization()(x1)
        x1 = MaxPooling2D(pool_size=(2, 2), padding='same')(x1)
        
        x2 = Conv2D(8, (5, 5), padding='same', activation = 'relu')(x1)
        x2 = BatchNormalization()(x2)
        x2 = MaxPooling2D(pool_size=(2, 2), padding='same')(x2)
        
        x3 = Conv2D(16, (5, 5), padding='same', activation = 'relu')(x2)
        x3 = BatchNormalization()(x3)
        x3 = MaxPooling2D(pool_size=(2, 2), padding='same')(x3)
        
        x4 = Conv2D(16, (5, 5), padding='same', activation = 'relu')(x3)
        x4 = BatchNormalization()(x4)
        x4 = MaxPooling2D(pool_size=(4, 4), padding='same')(x4)
        
        y = Flatten()(x4)
        y = Dropout(0.5)(y)
        y = Dense(16)(y)
        y = LeakyReLU(alpha=0.1)(y)
        y = Dropout(0.5)(y)
        y = Dense(1, activation = 'sigmoid')(y)

        return Model(inputs = x, outputs = y)
    
# Utilização de pesos já treinados
meso = Meso4()
meso.load('src/models/Meso4_DF.h5')

def modelo_meso4():
    # Preparação da imagem
    # Rescaling pixel values (between 1 and 255) to a range between 0 and 1
    dataGenerator = ImageDataGenerator(rescale=1./255)
    directory = 'data/interim/'
    # Instantiating generator to feed images through the network
    generator = dataGenerator.flow_from_directory(
        directory,
        target_size=(256, 256),
        class_mode=None,
        batch_size=1,
        shuffle=False
    )

    frame = []
    real = []
    fake = []
    for i in range(10):
        X = generator.next()
        pred = meso.predict(X)[0][0]
        frame.append(i)
        real.append(pred)
        fake.append(1-pred)
    resultado_real = sum(real)/len(real)
    resultado_fake = 1 - resultado_real
    return (frame,real,fake,resultado_real,resultado_fake)


# Modelo de análise de Espectro:

def azimuthalAverage(image, center=None):
    """
    Calculate the azimuthally averaged radial profile.

    image - The 2D image
    center - The [x,y] pixel coordinates used as the center. The default is 
             None, which then uses the center of the image (including 
             fracitonal pixels).
    
    """
    # Calculate the indices from the image
    y, x = np.indices(image.shape)

    if not center:
        center = np.array([(x.max()-x.min())/2.0, (y.max()-y.min())/2.0])

    r = np.hypot(x - center[0], y - center[1])

    # Get sorted radii
    ind = np.argsort(r.flat)
    r_sorted = r.flat[ind]
    i_sorted = image.flat[ind]

    # Get the integer part of the radii (bin size = 1)
    r_int = r_sorted.astype(int)

    # Find all pixels that fall within each radial bin.
    deltar = r_int[1:] - r_int[:-1]  # Assumes all radii represented
    rind = np.where(deltar)[0]       # location of changed radius
    nr = rind[1:] - rind[:-1]        # number of radius bin
    
    # Cumulative sum to figure out sums for each radius bin
    csim = np.cumsum(i_sorted, dtype=float)
    tbin = csim[rind[1:]] - csim[rind[:-1]]

    radial_prof = tbin / nr

    return radial_prof

def modelo_analise_de_espectro():
    # Importação do Modelo:
    modelo = pickle.load(open('src/models/model_espectro.pkl','rb'))
    epsilon = 1e-8
    N = 300
    number_iter = 10
    psd1D_total = np.zeros([number_iter, N])
    label_total = np.zeros([number_iter])
    cont = 0
    real = []
    fake = []
    for face in glob('data/interim/faces/*jpg'):
        img = cv2.imread(face,0)
        f = np.fft.fft2(img)
        fshift = np.fft.fftshift(f)
        fshift += epsilon
        magnitude_spectrum = 20*np.log(np.abs(fshift))
        psd1D = azimuthalAverage(magnitude_spectrum)
        # Calculate the azimuthally averaged 1D power spectrum
        points = np.linspace(0,N,num=psd1D.size) # coordinates of a
        xi = np.linspace(0,N,num=N) # coordinates for interpolation
        interpolated = griddata(points,psd1D,xi,method='cubic')
        interpolated /= interpolated[0]
        psd1D_total[cont,:] = interpolated             
        label_total[cont] = 1
        cont+=1     
    pred = modelo.predict(psd1D_total)
    real = list(pred)
    fake = list(1-pred)
    resultado_real = sum(real)/len(real)
    resultado_fake = 1 - resultado_real
    return (real,fake,resultado_real,resultado_fake)

def roda_modelo():
    modelo1 = modelo_meso4()
    frame = modelo1[0]
    modelo2 = modelo_analise_de_espectro()
    peso1 = 0.616
    peso2 = 0.707
    peso_total = peso1+peso2
    real_modelo1 =[]
    real_modelo2 =[]
    fake_modelo1 =[]
    fake_modelo2 =[]
    real = []
    fake = []
    for i in modelo1[1]: real_modelo1.append(i*peso1)
    for i in modelo2[0]: real_modelo2.append(i*peso2)
    for i in modelo1[2]: fake_modelo1.append(i*peso1)
    for i in modelo2[1]: fake_modelo2.append(i*peso2)
    for i in [x + y for x, y in zip(real_modelo1, real_modelo2)]: real.append(i/peso_total)
    for i in [x + y for x, y in zip(fake_modelo1, fake_modelo2)]: fake.append(i/peso_total)
    resultado_real = sum(real)/len(real)
    resultado_fake = 1 - resultado_real
    return (frame,real,fake,resultado_real,resultado_fake)
 
