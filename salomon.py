# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 16:37:40 2022

@author: Ramos
"""

from PIL import Image
import statistics as stat
from preparadorDeArchivos import *
import random
import string
         

def loadDatosDeImagenes(DIRECTORIO_DE_IMAGENES):
    
    with open(DIRECTORIO_DE_IMAGENES + "datosSalomon.txt","r") as file:
        data = file.read()
        
        dictionary = json.loads(data)
    
        return dictionary

def desplazarBox(box,LADO_CAJA,ANCHO_IMAGEN):
    
    leftBound = box[0]
    upperBound = box[1]
    rightBound = box[2]
    lowerBound = box[3]
    
    if ( rightBound <= (ANCHO_IMAGEN - LADO_CAJA  ) ):
        box = (leftBound + LADO_CAJA, upperBound, rightBound + LADO_CAJA, lowerBound)
    else:
        box = (0, upperBound + LADO_CAJA, LADO_CAJA, lowerBound + LADO_CAJA)
    
    return box

def recortarImagenYGuardarTrozos(im,box,CANTIDAD_DE_CUADRADITOS,LADO_CAJA,ANCHO_IMAGEN,ALTO_IMAGEN):

    """ Recorta la imagen seleccionada en pequeñas cajas (box) y guarda cada trozo en una lista """
    
    listaDeTrozos = []
    for i in range(0,CANTIDAD_DE_CUADRADITOS):
        
        trozo = im.crop(box)
        listaDeTrozos.append(trozo)
        box = desplazarBox(box,LADO_CAJA,ANCHO_IMAGEN)
    
    return listaDeTrozos

def obtenerDistancia(dictRGBRepositorio,dictRGBOriginal):
    
    distanciaRoja = abs( dictRGBRepositorio["R"] - dictRGBOriginal["R"] )
    distanciaVerde = abs( dictRGBRepositorio["G"] - dictRGBOriginal["G"] )
    distanciaAzul = abs( dictRGBRepositorio["B"] - dictRGBOriginal["B"] )
        
    return distanciaRoja + distanciaAzul + distanciaVerde

def obtenerValorCaracteristico(dictDePixelesRepositorio,dictDePixelesOriginal,valorOptimo):

    """ el valor característico se calcula sumando los valores absolutos de las diferencias de los colores, esa suma se va acumulando y ese es el valor
     característico """
    
    pixelActual = 1
    valorAcumulado = 0
    for pixel in dictDePixelesRepositorio:
        
        valor = obtenerDistancia(dictDePixelesRepositorio[pixel],dictDePixelesOriginal["pixel"+ str(pixelActual)])
        valorAcumulado += valor
        pixelActual += 1
        if valorAcumulado > valorOptimo:
            return valorAcumulado + 1 #Cualquier valor que descarte la imagen
    
    return valorAcumulado


def obtenerMejorAproximacion(dictDeRGB,dictDeImagenes):

    """ Se recorren cada una de las imagenes del repositorio y se comparan los colores con los de la imagen a editar, se utiliza un valorCaracteristico
     que se calcula en la funcion obtenerValorCaracteristico """
    
    valorCaracteristicoOptimo = len(dictDeRGB)*255*3 #El valor caracteristico siempre va a ser mas chico que esto

    for imagen in dictDeImagenes:
        
        valorCaracteristico = obtenerValorCaracteristico(dictDeImagenes[imagen],dictDeRGB,valorCaracteristicoOptimo)
        
        if (valorCaracteristico < valorCaracteristicoOptimo):
            valorCaracteristicoOptimo = valorCaracteristico
            imagenOptima = imagen
           
    return imagenOptima
    

def ProcesarYCompararTrozos(precision,listaDeTrozos,dictDeImagenes,DIRECTORIO_DE_IMAGENES,CANTIDAD_DE_CUADRADITOS,LADO_CAJA):

    """ Esta es la función principal del programa. Recorre cada uno de los trozos en los que fue dividida la imagen original y compara los colores
     con las imagenes del repositorio. La imagen elegida es "imagenMasCaracteristica" luego se le hace un resize al tamaño correspondiente
      y se la agrega a una lista que se utilizará para reconstruir el mosaico luego. """
    
    listaDeNuevasImagenes = []
    contadorDeImagenesProcesadas = 1
    
    for trozo in listaDeTrozos:
        
        dictDeRGB = obtenerColores(trozo,precision)

        imagenMasCaracteristica = obtenerMejorAproximacion(dictDeRGB,dictDeImagenes)
        numeroDeDichaImagen = imagenMasCaracteristica.split("-")
        
        nuevaImagen = Image.open(DIRECTORIO_DE_IMAGENES + "/" + str(numeroDeDichaImagen[1]) + "-salomon.jpg")
        nuevaImagenResized = nuevaImagen.resize((LADO_CAJA,LADO_CAJA))
        listaDeNuevasImagenes.append( nuevaImagenResized )

        print(str(contadorDeImagenesProcesadas) + "de" + str(CANTIDAD_DE_CUADRADITOS))

        contadorDeImagenesProcesadas += 1
    
    return listaDeNuevasImagenes

def nombre_al_azar(nombre_archivo):
    nombre_con_ext = nombre_archivo.split("/")[-1]
    nombre = nombre_con_ext.split(".")[0]
    caracteres = string.ascii_letters + string.digits
    return nombre + "-" + ''.join(random.choice(caracteres) for _ in range(6))

def guardarImagen(im):
    
    diferenciador = nombre_al_azar(im.filename)
    im = im.save(diferenciador + ".jpg")
        
def crearNuevaImagen(im,box,listaNueva,LADO_CAJA,ANCHO_IMAGEN,ALTO_IMAGEN):

    """ Coloca cada una de las imagenes del repositorio en su posición correspondiente para generar el mosaico """
    
    box = (0,0,LADO_CAJA,LADO_CAJA)
    for trozo in listaNueva:
        
        im.paste(trozo,box)
        box = desplazarBox(box,LADO_CAJA,ANCHO_IMAGEN)
    
    guardarImagen(im)


        







