import tkinter as tk
from PIL import Image, ImageTk
import os
import re


def segmentar(cadena, diccionario, imagenes):
    n = len(cadena)
    dp = [0] * (n + 1)
    dp[n] = 1
    segmentos = [''] * (n + 1)

    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n + 1):
            if cadena[i:j] in diccionario or cadena[i:j] in imagenes and dp[j] == 1:
                dp[i] = 1
                segmentos[i] = cadena[i:j] if segmentos[j] == '' else cadena[i:j] + ' ' + segmentos[j]

    return segmentos[0].split() if dp[0] == 1 else []

def analizador_lexicografico(cadena, diccionario):
    elementos = re.findall(r'[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+|[:;][-^]?[DOoP()]|\(y\)|\(n\)|<3|:3|E3|\\m/|:O|:-\||:\||:\*|>\:\(|\^\^|:-\]|:-D|:-P|xD|:-\]|:\]|:\[|:-\[', cadena)
    palabras_espanol = [elemento.lower() for elemento in elementos if elemento.lower() in diccionario]
    emoticones = [elemento for elemento in elementos if elemento in imagenes]

    return palabras_espanol, emoticones

def cargar_diccionario(ruta_diccionario):
    diccionario = set()
    for filename in os.listdir(ruta_diccionario):
        if filename.endswith('.txt'):
            with open(os.path.join(ruta_diccionario, filename), 'r', encoding='utf-8') as f:
                diccionario.update(f.read().splitlines())
    return diccionario

def cargar_imagenes(carpeta_imagenes):
    imagenes = {}
    correspondencias = {
        'xD': '010-risa',
        ':)': '003-feliz',
        ':D': '005-sonriente',
        ':O': '004-conmocionado',
        ':P': '023-cabeza-alienigena-1',
        ':|': '008-confuso',
        ':*': '019-entusiasta',
        '>:(': '011-enojado',
        '^^': '019-entusiasta',
        ':-]': '003-feliz',
        ':-D': '005-sonriente',
        ':-P': '023-cabeza-alienigena-1',
        'xD': '010-risa',
        ':-|': '013-preocuparse',
        ':]': '014-sonrisa',
        ':[': '009-triste',
        ':-[': '009-triste',
        ':3': '066-perro-6',
        'E3': '022-gato',
        # Agrega aquí las correspondencias para los demás emojis en el BNF
    }

    for filename in os.listdir(carpeta_imagenes):
        if filename.endswith('.png'):
            imagen = Image.open(os.path.join(carpeta_imagenes, filename))
            imagen = imagen.resize((20, 20))  # Cambia el tamaño de la imagen a 20x20 píxeles
            for emoji, nombre_archivo in correspondencias.items():
                if nombre_archivo == filename[:-4]:
                    imagenes[emoji] = ImageTk.PhotoImage(imagen)
    return imagenes
def procesar_cadena():
    # Limpiar el frame de salida
    for widget in frame_salida.winfo_children():
        widget.destroy()

    cadena = entrada.get()
    if ' ' not in cadena:
        cadena = ' '.join(segmentar(cadena, diccionario, imagenes))
    palabras_espanol, emoticones = analizador_lexicografico(cadena, diccionario)

    elementos = re.findall(r'[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+|[:;][-^]?[DOoP()]|\(y\)|\(n\)|<3|:3|\\m/|:O|:-\||:\||:\*|>\:\(|\^\^|:-\]|:-D|:-P|xD|:-\]|:\]|:\[|:-\[', cadena)

    for elemento in elementos:
        if elemento in emoticones and elemento in imagenes:
            label_imagen = tk.Label(frame_salida, image=imagenes[elemento])
            label_imagen.pack(side=tk.LEFT)
        else:
            label_palabra = tk.Label(frame_salida, text=elemento + ' ', fg='blue')
            label_palabra.pack(side=tk.LEFT)

    texto_palabras.set(f'Palabras en español: {len(palabras_espanol)}')
    texto_emoticones.set(f'Emoticones: {len(emoticones)}')

# Crear la interfaz gráfica
ventana = tk.Tk()
ventana.title("Entrega Final - Lenguajes de Programación")

# Imagen y título
ruta_logo = 'C:\\Users\\Miguel\\Desktop\\emojicshd\\png\\logo_eafit_completo.png'
imagen_titulo = Image.open(ruta_logo)
imagen_titulo = ImageTk.PhotoImage(imagen_titulo)
label_imagen_titulo = tk.Label(ventana, image=imagen_titulo)
label_imagen_titulo.image = imagen_titulo
label_imagen_titulo.grid(row=0, column=0, padx=10, pady=10, sticky="w")

label_titulo = tk.Label(ventana, text="Entrega Final - Lenguajes de Programación", font=("Arial", 16))
label_titulo.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# Entrada de texto y botón
label_frase = tk.Label(ventana, text="Ingrese una frase:")
label_frase.grid(row=2, column=0, padx=10, pady=5, sticky="w")

entrada = tk.Entry(ventana, width=67)
entrada.grid(row=2, column=0, padx=125, pady=5, sticky="w")

boton = tk.Button(ventana, text='Procesar', command=procesar_cadena)
boton.grid(row=3, column=0, padx=275, pady=10, sticky="w")

# Salida con emojis
label_salida = tk.Label(ventana, text="Salida con emojis:")
label_salida.grid(row=4, column=0, padx=10, pady=5, sticky="w")

frame_salida = tk.Frame(ventana)
frame_salida.grid(row=4, column=0, padx=125, pady=5, sticky="w")

# Información adicional
texto_palabras = tk.StringVar()
label_palabras = tk.Label(ventana, textvariable=texto_palabras)
label_palabras.grid(row=5, column=0, columnspan=2, pady=10, sticky="w")

texto_emoticones = tk.StringVar()
label_emoticones = tk.Label(ventana, textvariable=texto_emoticones)
label_emoticones.grid(row=6, column=0, columnspan=2, pady=0, sticky="w")

# Cargar diccionario e imágenes
ruta_diccionario = 'C:\\Users\\Miguel\\Desktop\\dics'
carpeta_imagenes = 'C:\\Users\\Miguel\\Desktop\\emojicshd\\png'

diccionario = cargar_diccionario(ruta_diccionario)
imagenes = cargar_imagenes(carpeta_imagenes)

ventana.mainloop()
