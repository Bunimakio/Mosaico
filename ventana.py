import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from salomon import *
from preparadorDeArchivos import *




def buscar_imagen():
    ruta_archivo = filedialog.askopenfilename()
    if ruta_archivo:
        input_imagen.delete(0,tk.END)
        input_imagen.insert(0,ruta_archivo)
        
        im = Image.open(input_imagen.get())
        ancho_imagen.set(im.width)
        alto_imagen.set(im.height)
        opt_size = tamanios_cuadrados(ancho_imagen.get(),alto_imagen.get())
        opt_size.sort()
        dropdown_size['values'] = opt_size
        

def buscar_repositorio():
    ruta_archivo = filedialog.askdirectory()
    if ruta_archivo:
        input_repository.delete(0,tk.END)
        input_repository.insert(0,ruta_archivo)

def divide(num,div):
    if num % div == 0:
        return div
    return 1

def obtener_divisores(num):

    return [divide(num,i) for i in range(1,int(num//2))]

def tamanios_cuadrados(ancho,alto):
    
    divisores_ancho = set(obtener_divisores(ancho))
    divisores_alto = set(obtener_divisores(alto))
    divisores_comunes = divisores_ancho.intersection(divisores_alto)

    return list(divisores_comunes)

def actualizar_img_url(*args):
    img_url.set(input_imagen.get())

def actualizar_repository_url(*args):
    repository_url.set(input_repository.get())

def actualizar_sel_quality(self):
    sel_quality.set(dropdown_quality.get())
    if sel_quality.get() == "baja":
        precision.set(10)
    elif sel_quality.get() == "media":
        precision.set(20)
    else:
        precision.set(30)

def actualizar_sel_size(self):
    sel_size.set(dropdown_size.get())
    


def generar():

    RUTA_IMAGEN_A_CAMBIAR = img_url.get()
    DIRECTORIO_DE_IMAGENES = repository_url.get()
    PRECISION = precision.get()
    ANCHO_IMAGEN = ancho_imagen.get()
    ALTO_IMAGEN = alto_imagen.get()
    LADO_CAJA = int(sel_size.get())
    CANTIDAD_DE_CUADRADITOS = (ANCHO_IMAGEN * ALTO_IMAGEN)//(LADO_CAJA**2)
    box = (0,0,LADO_CAJA,LADO_CAJA)

    im = Image.open(RUTA_IMAGEN_A_CAMBIAR)
    estimated_time = "El proceso tardará unos " + str(4*CANTIDAD_DE_CUADRADITOS//100) + " segundos"
    label_estimated.config(text=estimated_time)
    root.update_idletasks()

    procesarImagenesLocales(PRECISION,DIRECTORIO_DE_IMAGENES)
    dictDeImagenes = loadDatosDeImagenes(DIRECTORIO_DE_IMAGENES)
    listaDeTrozos = recortarImagenYGuardarTrozos(im,box,CANTIDAD_DE_CUADRADITOS,LADO_CAJA,ANCHO_IMAGEN,ALTO_IMAGEN)
    listaDeNuevosTrozos = ProcesarYCompararTrozos(PRECISION,listaDeTrozos,dictDeImagenes,DIRECTORIO_DE_IMAGENES,CANTIDAD_DE_CUADRADITOS,LADO_CAJA)
    crearNuevaImagen(im,box,listaDeNuevosTrozos,LADO_CAJA,ANCHO_IMAGEN,ALTO_IMAGEN)
    im.show()

    label_estimated.config(text="")
    root.update_idletasks()



root = tk.Tk() #Crea la ventana principal

#Variables tipo settings ---------------------------------

bgcolor = "#1f1f1f"
fontcolor = "#7abfff"
btn_bgcolor = "#3d67ff"
btn_fgcolor = "white"
border_color = "#4f4f4f"

precision = tk.IntVar()
ancho_imagen = tk.IntVar()
alto_imagen = tk.IntVar()

root.resizable(False, False)
root.title("Mosaico")
root.geometry("600x400")
root.configure(background=bgcolor)
#---------------------------------------------------------

""" 
Los frames son contenedores de los elementos visuales. He creado los siguientes:
    - frame_principal: contenedor de toda la ventana
    - frame_titulo: contiene el título
    - frame_componentes: contiene a todas las columnas donde se dispondran los items en pantalla
        -frame_columna_i: son las columnas que tienen los labels, inputs y botones. Hay 3 columnas
    - frame_generar: contiene al botón de generar

Verás que el código es pesado, eso es debido a que Tkinter no permite una buena reutilización de código. Con lo cual la lógica que he utilizado
es la siguiente. En cada frame columna encontrarás:

    - frame_columna_1: todos los labels
    - frame_columna_2: todos los inputs y combobox, con sus respectivas variables para obtener las entradas
    - frame_columna_3: todos los botones

"""


frame_principal = tk.Frame(root,bg=bgcolor) 
frame_principal.pack(fill=tk.BOTH,padx=16,pady=16)

frame_titulo = tk.Frame(frame_principal,bg=bgcolor)
frame_titulo.pack(fill=tk.X)

font_title = ("arial",24,"bold")
font_text = ("Verdana",12)
titulo = tk.Label(frame_titulo,text="Mosaico",font=font_title,fg=fontcolor,bg=bgcolor)
titulo.pack(anchor="center")

frame_componentes = tk.Frame(frame_principal,bg=bgcolor)
frame_componentes.pack(fill=tk.X,pady=16)

frame_column_1 = tk.Frame(frame_componentes,bg=bgcolor)
frame_column_1.pack(fill=tk.Y,side=tk.LEFT)
label_info_img = tk.Label(frame_column_1, text="Ruta Imagen principal:",fg=fontcolor,font=font_text,bg=bgcolor)
label_info_img.pack(pady=8,anchor="w")
label_repository = tk.Label(frame_column_1,text="Ruta del repositorio:",fg=fontcolor,font=font_text,bg=bgcolor)
label_repository.pack(pady=8,anchor="w")
label_quality = tk.Label(frame_column_1,text="Calidad:",fg=fontcolor,font=font_text,bg=bgcolor)
label_quality.pack(pady=8,anchor="w")
label_size = tk.Label(frame_column_1,text="Tamaño de cada división:",fg=fontcolor,font=font_text,bg=bgcolor)
label_size.pack(pady=8,anchor="w")

frame_column_2 = tk.Frame(frame_componentes,bg=bgcolor)
frame_column_2.pack(fill=tk.Y,side=tk.LEFT,padx=20)
img_url = tk.StringVar()
input_imagen = tk.Entry(frame_column_2,textvariable=img_url)
input_imagen.pack(pady=10,anchor="w",fill=tk.X)
img_url.trace_add("write",actualizar_img_url)
repository_url = tk.StringVar()
input_repository = tk.Entry(frame_column_2,textvariable=repository_url)
input_repository.pack(pady=9,anchor="w",fill=tk.X)
repository_url.trace_add("write",actualizar_repository_url)
opt_quality= ["","baja","media","alta"]
sel_quality = tk.StringVar(value=opt_quality[0])
dropdown_quality = ttk.Combobox(frame_column_2,textvariable=sel_quality,values=opt_quality)
dropdown_quality.pack(pady=10,anchor="w")
dropdown_quality.bind("<<ComboboxSelected>>", actualizar_sel_quality)
sel_size = tk.StringVar(value=1)
opt_size = [1]
dropdown_size = ttk.Combobox(frame_column_2,textvariable=sel_size,values=opt_size)
dropdown_size.pack(pady=10,anchor="w")
dropdown_size.bind("<<ComboboxSelected>>", actualizar_sel_size)

frame_column_3 = tk.Frame(frame_componentes,bg=bgcolor)
frame_column_3.pack(fill=tk.Y)
btn_image = tk.Button(frame_column_3,text="Cargar Archivo",command=buscar_imagen,bg=btn_bgcolor,fg=btn_fgcolor,relief="flat",font=("Verdana",10,"bold"))
btn_image.pack(pady=6,anchor="w")
btn_repository = tk.Button(frame_column_3,text="Cargar Repositorio",command=buscar_repositorio,bg=btn_bgcolor,fg=btn_fgcolor,relief="flat",font=("Verdana",10,"bold"))
btn_repository.pack(pady=6,anchor="w")

frame_generar = tk.Frame(frame_principal,bg=bgcolor)
frame_generar.pack(fill=tk.X)

btn_start = tk.Button(frame_generar,command=generar,bg=btn_bgcolor,fg=btn_fgcolor,relief="flat",font=("Verdana",10,"bold"),text="Generar")
btn_start.pack()
label_estimated = tk.Label(frame_generar, text="",fg=fontcolor,font=font_text,bg=bgcolor)
label_estimated.pack()

root.mainloop()

