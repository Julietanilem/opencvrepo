import cv2 as cv
import numpy as np
upperColor = np.array([10,10, 10])
lowerColor = np.array([0, 0, 0])

# Tomar imagen-- idealmente será transmitida de un tópico en vivo cada que se renueve la imagen completamente 
#(no se repitan los 3 caracteres)

# Procesar la imagen
img = cv.imread(cv.samples.findFile("braille.png"))
grises    = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
blur     = cv.GaussianBlur(grises,(3,3),0)
thres    = cv.adaptiveThreshold(blur,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,5,4)
erosion_size = 4
erosion_shape = cv.MORPH_RECT
element = cv.getStructuringElement(erosion_shape, (2 * erosion_size + 1, 2 * erosion_size + 1),
                            (erosion_size, erosion_size))
erosion= cv.erode(thres, element)
# colorNegro = cv.inRange(erosion, lowerColor, upperColor)
# cv.imshow("Display window", colorNegro)
# for  x in range(erosion.shape[0]):
#     for y in range(erosion.shape[1]):  
#         print(erosion[x,y])

cv.imshow("COLOR", erosion)
k = cv.waitKey(0)

#Convertir la imagen en arreglos
letraDetectada={1,1}
##comparar con los siguientes
h={{1,0},{1,1},{0,0}}
o={{1,0},{0,1},{1,0}}
l={{1,0},{1,0},{1,0}}
letras={h,o,l}
for letra in letras:
    if letraDetectada==letra:
        print(letra)
