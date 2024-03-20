# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 12:34:37 2022

@author: Ramos
"""

import os
import glob
from PIL import Image
from math import floor
import json
import pprint



def obtenerUltimoSalomon(lista):
    
    """ Obtiene el numero más grande del grupo de imagenes llamadas XX-salomon.jpg """
    
    numeroMax = 0
    for name in lista:
        
        if ("salomon" in name):
            numeroYNombre = name.split("-")

            if ( int(numeroYNombre[0]) > numeroMax ):
                numeroMax = int(numeroYNombre[0])
            
    return numeroMax


def prepararImagenesLocales(DIRECTORIO_DE_IMAGENES):

    """ La funcion cambia el nombre de todos los archivos en el repositorio de imagenes a n-salomon.jpg, donde n va variando. """
    
    listadoDeNombresDeImagenes = os.listdir(DIRECTORIO_DE_IMAGENES)
    ultimoSalomon = obtenerUltimoSalomon(listadoDeNombresDeImagenes)
    cantidadDeArchivosProcesados = 0
    
    for name in listadoDeNombresDeImagenes:
        
        if not ("salomon" in name):
            cantidadDeArchivosProcesados += 1
            nameNuevo = str(ultimoSalomon + cantidadDeArchivosProcesados) + "-salomon.jpg"
            os.rename(DIRECTORIO_DE_IMAGENES + name,DIRECTORIO_DE_IMAGENES + nameNuevo)
            
def obtenerColores(imLocal,precision):
    
    """ Recibe una imagen .jpg y devuelve una lista de todos los pixeles de la imagen en formato (R,G,B)"""
    
    dictDeTuplasRGB = {}
    pixelesCargados = 0
    anchoPartidoEnPrecisionPartes = floor(imLocal.width/precision)
    altoPartidoEnPrecisionPartes = floor(imLocal.height/precision)
    
    for fil in range(0,precision-1):
        for col in range(0,precision - 1):
            pixelesCargados += 1
            pixel = imLocal.getpixel( (col*anchoPartidoEnPrecisionPartes , fil*altoPartidoEnPrecisionPartes) )
            dictDeTuplasRGB["pixel" + str(pixelesCargados)] = {"R":pixel[0],"G":pixel[1],"B":pixel[2] }
            
    return dictDeTuplasRGB
            
def obtenerDatosDeImagenYGuardarEnMemoria(precision,DIRECTORIO_DE_IMAGENES):

    """ Revisa todas las imagenes del repositorio y guarda la informacion de los colores en un diccionario para posteriormente guardar en disco """
    
    dictDatosImagen = {}
    cantidadDeElementosEnCarpeta = len(glob.glob(DIRECTORIO_DE_IMAGENES + "/" + "*.jpg"))
    
    for i in range(1,cantidadDeElementosEnCarpeta):
        
        directory = DIRECTORIO_DE_IMAGENES + "/" + str(i) + "-salomon.jpg"
        imLocal = Image.open(directory)
        dictDatosImagen["imagen-" + str(i)] = obtenerColores(imLocal,precision)
        
    return dictDatosImagen

def guardarDatosEnDisco(dictDatos,DIRECTORIO_DE_IMAGENES):
    
    with open(DIRECTORIO_DE_IMAGENES + "datosSalomon.txt","w") as file:
        file.write(json.dumps(dictDatos))
    

def procesarImagenesLocales(precision,dir_img):

    """ Prepara el repositorio de imágenes, cambia los nombres de los archivos y guarda los colores en un txt """
    
    prepararImagenesLocales(dir_img)
    dictDatosDeImagenes = obtenerDatosDeImagenYGuardarEnMemoria(precision,dir_img)
    guardarDatosEnDisco(dictDatosDeImagenes,dir_img)
    
