import cv2
import numpy as np
import time
import sys
import os
import random

def get_median(list):
    '''Implementação do filtro de mediana.'''
    list = sorted(list)
    tamanhoLista = len(list)
    meio = int(tamanhoLista / 2)
    if tamanhoLista % 2 == 0:
        medianA = list[meio]
        medianB = list[meio-1]
        median = (medianA + medianB) / 2
    else:
        median = list[meio + 1]
    return median


def getFiltro(tamanhoJanela):
    '''Obtém um array de tamanho = @tamanhoJanela que será usado em filtros de convolução.'''
    filtro = np.zeros((tamanhoJanela, tamanhoJanela), int)
    return filtro

def get_gaussian(x,x0,sigma):
    '''Obtém a gaussiana de média @x0 e desvio padrão @sigma.'''
    return np.exp(-np.power((x - x0)/sigma, 2.)/2.)

def impulsivo_unipolar(img):
    '''Degrada a imagem utilizando o método impulsivo unipolar.'''
    imgDest = np.zeros_like(img)
    height, width = img.shape[0], img.shape[1]

    for y in range(height):
        for x in range(width):
            if random.random() <= 0.15:
                imgDest[y,x] = 0
            else:
                imgDest[y,x] = img[y,x]
    return imgDest

def impulsivo_bipolar(img):
    '''Degrada a imagem utilizando o método impulsivo bipolar.'''
    imgDest = np.zeros_like(img)
    height, width = img.shape[0], img.shape[1]

    for y in range(height):
        for x in range(width):
            prob = random.random()
            if prob <= 0.10:
                probIntensity = random.random()
                if probIntensity > 0.5:
                    intensity = 0
                else:
                    intensity = 255
                imgDest[y,x] = intensity
            else:
                imgDest[y,x] = img[y,x]
    return imgDest

def gaussiano(img):
    '''Degrada a imagem utilizando o método gaussiano.'''
    imgDest = np.zeros_like(img)
    height, width = img.shape[0], img.shape[1]
    mean = 10.0
    std = 30.0
    ruido = img + np.random.normal(mean, std, img.shape)
    ruido_normalizado = np.clip(ruido, 0, 255)
    for y in range(height):
        for x in range(width):

            imgDest[y,x] = ruido_normalizado[y,x]

    return imgDest

def median_filter(img, tamFiltro):
    '''Aplica a filtragem espacial utilizando o filtro de mediana.'''
    imgDest = np.zeros_like(img)
    filtro = getFiltro(tamFiltro)
    width, height = img.shape[1], img.shape[0]
    filter_width, filter_height = filtro.shape[0], filtro.shape[1]
    intensidades = []

    for y in range(height):
        for x in range(width):

            for filterY in range(int(-(filter_height / 2)), filter_height - 1):
                for filterX in range(int(-(filter_width / 2)), filter_width - 1):

                    pixel_y = y - filterY
                    pixel_x = x - filterX
                    pixel = img[filterY, filterX]

                    if (pixel_y >= 0) and (pixel_y < height) and (pixel_x >= 0) and (pixel_x < width):
                        pixel = img[pixel_y, pixel_x]

                    intensidades.append(pixel)

            mediana = get_median(intensidades)
            imgDest[y, x] = mediana
            intensidades = []
    return imgDest

def process_image(imgName):
    '''Método que chama as funções de degradação de imagens.'''
    start_time = time.time()
    desImgName = imgName
    imgName = sys.path[0] + '\\' + imgName
    processedFolder = sys.path[0] + '\\' + 'processed'

    if not os.path.exists(processedFolder):
        os.makedirs(processedFolder)

    img = cv2.imread(imgName, cv2.IMREAD_GRAYSCALE)
    print("Processing image '{0}'...".format(imgName))

    imgDest = impulsivo_unipolar(img)
    cv2.imwrite(processedFolder + "\\" + "unipolar_" + desImgName, imgDest)

    imgDest = impulsivo_bipolar(img)
    cv2.imwrite(processedFolder + "\\" + "bipolar_" + desImgName, imgDest)

    imgDest = gaussiano(img)
    cv2.imwrite(processedFolder + "\\" + "gaussiano_" + desImgName, imgDest)

    elapsed_time = time.time() - start_time
    print("Done.")
    print("Done! Elapsed Time: {0}".format(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))

    ''' Caso queira exibir a imagem na tela 
    cv2.imshow(imgName, imgDest)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
def process_restore_image(imgName):
    '''Método que chama as funções de restauração de imagens.'''
    start_time = time.time()
    desImgName = imgName
    imgName = sys.path[0] + '\\' + imgName
    processedFolder = sys.path[0] + '\\' + 'processed'

    if not os.path.exists(processedFolder):
        os.makedirs(processedFolder)

    img = cv2.imread(imgName, cv2.IMREAD_GRAYSCALE)
    print("Processing image '{0}'...".format(imgName))

    imgDest = median_filter(img, 7)
    cv2.imwrite(processedFolder + "\\" + desImgName, imgDest)

    elapsed_time = time.time() - start_time
    print("Done.")
    print("Done! Elapsed Time: {0}".format(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))

'''Programa Principal'''
process_image("image_(1).jpg")
process_restore_image("image_(2).jpg")
process_restore_image("image_(3).jpg")
process_restore_image("image_(4).jpg")