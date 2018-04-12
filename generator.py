"""
    Comando para normalizar as imagens:
        mogrify -format jpg *.png
"""
import pyqrcode
import cv2
import pandas as pd
import copy as cp
from tqdm import tqdm
from PIL import Image
import os
import math
import re
import unidecode

background = cv2.imread('./src/img/_Certificado 2018 - Dia D.png')
df = pd.read_csv('./src/data/data.csv')

def removeAccent(src):
    # Verifica também se é "nan" senão retorna em branco
    if isinstance(src, float) and math.isnan(src):
        return ''
    else:
        # Por algum motivo em alguns casos em específico há geração de '?' nas strings, por isso o replace
        return unidecode.unidecode(str(src)).replace('?', '')

def insertData(id, data):
    color = 0
    font = cv2.FONT_HERSHEY_TRIPLEX
    scale = 3.5
    new_background = cp.deepcopy(background)

    cv2.putText(new_background, removeAccent(data['Nome']), (970, 1063), font, scale, color, thickness=2)

    # Salva a imagem do cartão
    cv2.imwrite(f"./dist/img/OPN-{i}.png", new_background)

print('\n\nCriando as imagens de certificado:\n')
for i in tqdm(range(0, df.shape[0])):
   insertData(i, df.ix[i])
