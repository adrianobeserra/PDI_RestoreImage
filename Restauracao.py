import cv2
import numpy as np
import time
import sys
import os
import random
import matplotlib.pyplot as plt


def histogram(imgName, title):
    histogramFolder = sys.path[0] + '\\' + 'histogram'

    if not os.path.exists(histogramFolder):
        os.makedirs(histogramFolder)

    img = cv2.imread(imgName, cv2.IMREAD_GRAYSCALE)
    plt.hist(img, bins=10, range=None, normed=None, weights=None, density=None)
    plt.legend()
    plt.title(title, fontsize=20)
    plt.savefig(histogramFolder + '\\' + title + ".png")

'''Implementação do filtro de mediana.'''
def get_median(list):
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
    filtro = np.zeros((tamanhoJanela, tamanhoJanela), int)
    return filtro

def get_gaussian(x,x0,sigma):
    return np.exp(-np.power((x - x0)/sigma, 2.)/2.)

def impulsivo_unipolar(img):
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
    start_time = time.time()
    desImgName = imgName
    imgName = sys.path[0] + '\\' + imgName
    processedFolder = sys.path[0] + '\\' + 'processed'

    if not os.path.exists(processedFolder):
        os.makedirs(processedFolder)

    img = cv2.imread(imgName, cv2.IMREAD_GRAYSCALE)
    print("Processing image '{0}'...".format(imgName))

    imgDest = impulsivo_unipolar(img)
    imgPath = processedFolder + "\\" + "unipolar_" + desImgName

    cv2.imwrite(imgPath, imgDest)
    histogram(imgPath, "Histograma Ruído Unipolar")

    imgDest = impulsivo_bipolar(img)
    imgPath = processedFolder + "\\" + "bipolar_" + desImgName
    cv2.imwrite(imgPath, imgDest)

    imgDest = gaussiano(img)
    imgPath = processedFolder + "\\" + "gaussiano_" + desImgName
    cv2.imwrite(imgPath, imgDest)

    elapsed_time = time.time() - start_time
    print("Done.")
    print("Done! Elapsed Time: {0}".format(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))

    ''' Caso queira exibir a imagem na tela 
    cv2.imshow(imgName, imgDest)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
def process_restore_image(imgName):
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

def gerar_histogramas():
    histogram("image_(1).jpg", "image_(1)");
    histogram("image_(2).jpg", "image_(2)");
    histogram("image_(3).jpg", "image_(3)");
    histogram("image_(4).jpg", "image_(4)");

    processedFolder = sys.path[0] + '\\' + 'processed'
    histogram(processedFolder + "\\unipolar_image_(1).jpg", "unipolar_image_(1)");
    histogram(processedFolder + "\\bipolar_image_(1).jpg", "bipolar_image_(1)");
    histogram(processedFolder + "\\gaussiano_image_(1).jpg", "gaussiano_image_(1)");

    histogram(processedFolder + "\\image_(2).jpg", "filtred_image_(2)");
    histogram(processedFolder + "\\image_(3).jpg", "filtred_image_(3)");
    histogram(processedFolder + "\\image_(4).jpg", "filtred_image_(4)");

    image1 = cv2.imread("image_(2).jpg")
    image2 = cv2.imread(processedFolder + "\\image_(2).jpg")
    subtract = image1 - image2
    cv2.imwrite(processedFolder + "\\sub_image_(2).jpg", subtract)
    histogram(processedFolder + "\\sub_image_(2).jpg", "sub_image_(2)");

    image1 = cv2.imread("image_(3).jpg")
    image2 = cv2.imread(processedFolder + "\\image_(3).jpg")
    subtract = image1 - image2
    cv2.imwrite(processedFolder + "\\sub_image_(3).jpg", subtract)
    histogram(processedFolder + "\\sub_image_(3).jpg", "sub_image_(3)");

    image1 = cv2.imread("image_(4).jpg")
    image2 = cv2.imread(processedFolder + "\\image_(4).jpg")
    subtract = image1 - image2
    cv2.imwrite(processedFolder + "\\sub_image_(4).jpg", subtract)
    histogram(processedFolder + "\\sub_image_(4).jpg", "sub_image_(4)");

'''Programa Principal'''
process_image("image_(1).jpg")
process_restore_image("image_(2).jpg")
process_restore_image("image_(3).jpg")
process_restore_image("image_(4).jpg")

gerar_histogramas()
