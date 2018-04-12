"""
    Comando para normalizar as imagens:
        mogrify -format jpg *.png
    Comando para melhorar as cores:
        pngcrush -ow -rem allb -reduce * 
"""
import pyqrcode
import cv2
import pandas as pd
import copy as cp
from tqdm import tqdm
from PIL import Image
import os
import glob
import math
import re
import unidecode
from os.path import isfile, join

def removeAccent(src):
    # Verifica também se é "nan" senão retorna em branco.
    if isinstance(src, float) and math.isnan(src):
        return ''
    else:
        # Por algum motivo em alguns casos em específico há geração de '?' nas strings, por isso o replace.
        return unidecode.unidecode(str(src)).replace('?', '')


def insertData(id, data, branch, background):
    color = 0
    font = cv2.FONT_HERSHEY_TRIPLEX
    scale = 3.5
    # Há  a  necessidade  de  se  copiar  o  background  para  não  ficar sobrepondo em camadas do original e alterar os
    # certificados que virão após.
    new_background = cp.deepcopy(background)
    name = data["Nome"]

    cv2.putText(new_background, removeAccent(data['Nome']), (970, 1063), font, scale, color, thickness=2)

    # Salva a imagem do certificado com o nome do membro.
    cv2.imwrite(f"./dist/img/{branch}/{name}.png", new_background)

branches = ["dia_d", "escolas", "infraestrutura", "marketing", "patrocinio", "qualidade", "sacolinhas", "supermercados"]

print("Gerando certificados:")
for branch in branches:
    background = cv2.imread(f"./src/img/{branch}.png")
    df = pd.read_csv(f"./src/data/{branch}.csv")
    
    print(f"Gerando certificados para {branch}:")
    for i in tqdm(range(0, df.shape[0])):
        member = df.ix[i]
        # Isso irá garantir que apenas membros que cumpriram os critérios terão seu certificados gerados.
        if(0 == member["CERTIFICADO: SIM=0  NÃO=1,2,3,4"]):
            insertData(i, df.ix[i], branch, background)
