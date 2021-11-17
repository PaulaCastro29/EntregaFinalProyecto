#-----------------------------------------
#ENTREGA FINAL PROYECTO: DETECCIÓN DEL PARÁSITO CAUSANTE DE LA MALARIA MEDIANTE PROCESAMIENTO DE IMÁGENES DIGITALES
#PRESENTADO POR: PAULA CASTRO Y MICHAEL CONTRERAS
#-----------------------------------------

# Importación de librerias requeridas
import tkinter
import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Desarrollo de una aplicación que procesa imágenes microscopicas de frotis grueso e identifica glóbulos blancos y el parásito de la malaria.
if __name__ == '__main__':

# Creación de pantalla principal (menú) de la interfaz gráfica
    root = tkinter.Tk()
    root.geometry("400x380")
    root.title("Detección del parásito de la Malaria")
    img = tkinter.PhotoImage(file="mosquito3.png")
    img = img.subsample(2,2)
    labemalaria=tkinter.Label(root, text="Proceso de detección",font=('Arial', 18, 'bold'))
    labemalaria.place(x=10, y=10, relwidth=1.0, relheight=1.0)
    labemalaria.pack()
    labemalaria1=tkinter.Label(root, text="del parásito de la Malaria",font=('Arial', 18,'bold'))
    labemalaria1.place(x=10, y=15, relwidth=1.0, relheight=1.0)
    labemalaria1.pack()
    labelimg=tkinter.Label(image=img)
    labelimg.pack()

# Función que permite cargar la imagen que se va analizar desde el computador y ejecuta el procesamiento de la imagen y detección de objetos
    def archivo():
        global fig2, fig, contar, contar1, densidad
        path_image = filedialog.askopenfilename(filetypes=[("image", ".jpg")])
        if len(path_image) > 0:
            global image
            #image = cv2.imread(path_image)
            image = np.array(Image.open(path_image))
        ima = image.copy()
        # Conversión de imagen en escala de grises para identificar itensidad de objetos de interes.
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

       # Aplicación filtro Gaussiano
        gauss = cv2.GaussianBlur(image_gray, (3, 3), 0)

    # HISTOGRAMA para detectar el comportamiento de los pixeles en la imagen

        # Histograma
        #plt.hist(gauss)
        #plt.xlabel("Rango de Tonalidad")
        #plt.ylabel("Numero de Pixeles")
        #plt.title("Histograma")
        #plt.show()

      # Aplicación de metodo Otsu
        ret, Ibw_otsu = cv2.threshold(gauss, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

      # Aplicación método manual global threshold
        threshold = 90.0
        ret, Ibw_manual = cv2.threshold(gauss, threshold, 255, cv2.THRESH_BINARY)

      # Copia de imagen binarizada
        image_bin= np.copy(Ibw_manual)

      # Extracción de tamaño imagen alto y ancho
        h,w = image_bin.shape

      # Creación de mascara y llenado de huecos para extraer objetos de interes y candidatos a posibles parasitos
        mask = np.zeros((h+2,w+2),np.uint8)
        cv2.floodFill(image_bin,mask,(0,0),255)
        imagem = cv2.bitwise_not(image_bin)

      # Detectección de los bordes con Canny
        canny = cv2.Canny(imagem, 50, 150)

      # Dectección de contornos
        contours, hierarchy = cv2.findContours(imagem, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      # Ubicacion de punto central, cáculo de área y perímetro de cada objeto encontrado
        contar = 0
        contar1 = 0
        for i in range(len(contours)):
            if len(contours[i]) > 2:
                cont = contours[i]
                M = cv2.moments(cont)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                area = cv2.contourArea(cont)
                perimetro = cv2.arcLength(cont,True)
                #print('El area es:',area, 'unidad')
                #print('El perimetro es:',perimetro,'unidad')

      # Clasificación de parásitos
                if area > 0 and area < 30 and perimetro > 3 and perimetro < 25:
                    cv2.circle(ima, (cx, cy), 50, (0, 255, 0), 7)
                    print("El objet es parasito:")
                    print("El area del objeto es:", area)
                    print("El Perimetro del objeto es:", perimetro)
                    print("El Punto central del objeto es:", cx, cy)
                    contar=contar+1

      # Clasificación de glóbulos blancos
                elif area > 400 and area < 12000 and perimetro > 105 and perimetro < 700:
                    cv2.circle(ima, (cx, cy), 50, (255, 0, 0), 7)
                    print("El objet es globulo blanco:")
                    print("El area del objeto es:", area)
                    print("El Perimetro del objeto es:", perimetro)
                    print("El Punto central del objeto es:", cx, cy)
                    contar1 = contar1 + 1

        # Cálculo de la densidad o carga parásitaria
        densidad = round((contar * 8000) / contar1)

        print("Se han encontrado {} objetos en la muestra".format(len(contours)))
        print("Se han encontrado {} parasitos en la muestra".format(contar))
        print("Se han encontrado {} globulos blancos en la muestra".format(contar1))
        print("La densidad de parásitos por microlitro de sangre es ", densidad)


      # Gráficas que muestran el proceso para la detección de los elementos
        fig, axs = plt.subplots(2, 3, figsize=(7, 7))
        axs[0, 0].imshow(image)
        axs[0, 0].set_title('Imagen Original', fontweight="bold")
        axs[1, 0].imshow(mask)
        axs[1, 0].set_title('Mascara imagen', fontweight="bold")
        axs[0, 1].imshow(image_gray)
        axs[0, 1].set_title('Imagen escala grises', fontweight="bold")
        axs[1, 1].imshow(canny)
        axs[1, 1].set_title('Deteccion de bordes', fontweight="bold")
        axs[0, 2].imshow(Ibw_otsu)
        axs[0, 2].set_title('Imagen Otsu', fontweight="bold")
        axs[1, 2].imshow(imagem)
        axs[1, 2].set_title('Objetos de interes', fontweight="bold")
        #plt.show()

    # Gráfica de resultados de la detección
        fig2, axs = plt.subplots(figsize=(5, 5))
        plt.imshow(ima)
        plt.title('Detección de glóbulos blancos y parásitos', fontweight="bold")
        #plt.show()

# Función que define la ventana donde se visualizan los resultados de la detección
    def openwindow1():
        new_window1 = Toplevel(root)
        new_window1.geometry("1000x600")
        new_window1.title("Resultados de la detección")
    # Definición de la gráfica en la interfaz
        canvas = FigureCanvasTkAgg(fig2, master=new_window1)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, new_window1)
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    # Información de cantidad de parásitos y globulos asi como carga parasitaria en la interfaz
        label1 = Label(new_window1, text="Cantidad parásitos:", font=('Arial', 12,), bg="white")
        label1.place(x=825, y=160)
        label2 = Label(new_window1, text=contar,font=('Arial', 18), bg="white")
        label2.place(x=885, y=200)
        label3 = Label(new_window1, text="Cantidad glóbulos blancos:", font=('Arial', 12), bg="white")
        label3.place(x=805, y=260)
        label4 = Label(new_window1, text=contar1,font=('Arial', 18), bg="white")
        label4.place(x=880, y=300)
        label5 = Label(new_window1, text="Densidad parasitaria", font=('Arial', 12), bg="white")
        label5.place(x=820, y=360)
        label6 = Label(new_window1, text="[parásitos/uL]:", font=('Arial', 12), bg="white")
        label6.place(x=840, y=380)
        label7 = Label(new_window1, text=densidad,font=('Arial', 18), bg="white")
        label7.place(x=870, y=420)
# Función que define acción del botón 'cerrar'
    def cerrar():
        root.quit()
        root.destroy()
# Función que define la ventana que muestra el proceso de detección
    def openwindow2():
        new_window2 = Toplevel(root)
        new_window2.geometry("1000x600")
        new_window2.title("Visualización del proceso de detección")
       # Definición de la gráfica en la interfaz
        canvas2 = FigureCanvasTkAgg(fig, master=new_window2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

# Creación de botones de la interfaz gráfica

   # Definición del botón 'cerrar'
    button = tkinter.Button(master=root, text="Cerrar", fg = "red",font=('Arial', 11), command=cerrar)
    button.pack(side=tkinter.BOTTOM)
   # Definición del botón 'Visualizar proceso'
    button2 = tkinter.Button(master=root, text="Visualizar proceso", bg = "pink", command=openwindow2)
    button2.place(x=280, y=300)
   # Definición del botón 'Mostrar resultados'
    buttonStart = tkinter.Button(master=root, text="Mostrar resultados",bg = "lightgreen", command=openwindow1)
    buttonStart.place(x=150, y=300)
   # Definición del botón 'Ejecutar detección'
    buttonarchivo = tkinter.Button(master=root, text="Ejecutar detección",bg = "mediumturquoise", command=archivo)
    buttonarchivo.place(x=20, y=300)
   #Permite la ejecución de la interfaz
    tkinter.mainloop()