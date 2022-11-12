#####################
# RYSOWANIE FUNKCJI # Autor: Michał Wiktorowski
#####################

# Zaimporotowane moduły
from tkinter import *
import tkinter as ttk
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import math
import numpy as np
from numpy import sin
from numpy import cos
from numpy import tan
from numpy import sqrt
from numpy import log
from numpy import exp
from numpy import pi
from numpy import e

# Funkcja dodająca tło
def create_img(frame, png_file):
    """Funkcja create_img dodająca tło. Argumenty: frame (okno aplikacji), oraz png_file (plik z obrazkiem)."""
    width = 2000
    height = 1000

    img = Image.open(png_file)
    img = img.resize((width,height), Image.ANTIALIAS)
    photoImg =  ImageTk.PhotoImage(img)

    img_label = Label(frame, image=photoImg, width=width)
    img_label.image = photoImg
    return img_label



# Klasa Window
class Window(Frame):
    """Klasa Window."""
    # FUNKCJA INICJALIZACJI
    def __init__(self, master = None):
        """Funkcja __init__ inicjalizująca klasę Window."""
        
        # Inicjalizacja okna
        Frame.__init__(self, master)
        self.master = master

        self.pack(fill = BOTH, expand = True)

        # Inicjalizacja tła
        img = create_img(self, 'galactic.jpg')
        img.place(x = -2, y = 0)

        # POLA TEKSTOWE
        
        # Pole tekstowe "Wpisz wzór funkcji"
        funclabel = Label(self, text = 'Wprowadź wzór funkcji:', height = 1, width = 20, font = ("Calibri", 13))
        funclabel.place(x = 20, y = 300)

        enterfunc = Entry(self, font = ("Calibri", 13))
        self.enterfunc = enterfunc
        self.enterfunc.place(x = 250, y = 300, width = 400, height = 30)

        # Pole tekstowe "Tytuł wykresu"
        plot_titlelabel = Label(self, text = 'Wprowadź tytuł wykresu:', height = 1, width = 20, font = ("Calibri", 13))
        plot_titlelabel.place(x = 20, y = 650)

        enterplot_title = Entry(self, font = ("Calibri", 13))
        self.enterplot_title = enterplot_title
        self.enterplot_title.place(x = 250, y = 650, width = 400, height = 30)

        # Pole tekstowe "Tytuł osi x"
        xaxis_titlelabel = Label(self, text = 'Wprowadź nazwę osi x:', height = 1, width = 20, font = ("Calibri", 13))
        xaxis_titlelabel.place(x = 20, y = 700)

        enterxaxis_title = Entry(self, font = ("Calibri", 13))
        self.enterxaxis_title = enterxaxis_title
        self.enterxaxis_title.place(x = 250, y = 700, width = 400, height = 30)

        # Zakres x
        xfromlabel = Label(self, text = 'Zakres x: od', height = 1, width = 10, font = ("Calibri", 13))
        xfromlabel.place(x = 500, y = 870)

        enterxfrom = Entry(self, font = ("Calibri", 13))
        self.enterxfrom = enterxfrom
        self.enterxfrom.place(x = 600, y = 870, width = 50, height = 30)

        xtolabel = Label(self, text = 'do', height = 1, width = 3, font = ("Calibri", 13))
        xtolabel.place(x = 660, y = 870)

        enterxto = Entry(self, font = ("Calibri", 13))
        self.enterxto = enterxto
        self.enterxto.place(x = 700, y = 870, width = 50, height = 30)

        # Pole tekstowe "Tytuł osi y"
        yaxis_titlelabel = Label(self, text = 'Wprowadź nazwę osi y:', height = 1, width = 20, font = ("Calibri", 13))
        yaxis_titlelabel.place(x = 20, y = 750)

        enteryaxis_title = Entry(self, font = ("Calibri", 13))
        self.enteryaxis_title = enteryaxis_title
        self.enteryaxis_title.place(x = 250, y = 750, width = 400, height = 30)

        # PRZYCISKI RADIOWE
   
        # Wybór siatki
        gridlabel = Label(self, text = 'Siatka', height = 1, width = 4, font = ("Calibri", 13))
        gridlabel.place(x = 200, y = 870)

        grid = IntVar()
        self.grid = grid
        Radiobutton(self, text = "Włącz", variable = self.grid, value = 1, command = self.checkgrid).place(x = 200, y = 900)
        Radiobutton(self, text = "Wyłącz", variable = self.grid, value = 2, command = self.checkgrid).place(x = 200, y = 930)
        
        # #Wybór legendy
        legendlabel = Label(self, text = 'Legenda', height = 1, width = 6, font = ("Calibri", 13))
        legendlabel.place(x = 300, y = 870)

        legend = IntVar()
        self.legend = legend
        Radiobutton(self, text = "Włącz", variable = self.legend, value = 1, command = self.checklegend).place(x = 300, y = 900)
        Radiobutton(self, text = "Wyłącz", variable = self.legend, value = 2, command = self.checklegend).place(x = 300, y = 930)

        # PRZYCISKI

        # Przycisk rysowania
        drawButton = Button(self, text = 'Rysuj', command = self.drawaplot, height = 4, width = 12)
        drawButton.place(x = 750, y = 280)

        # Przycisk wyjścia
        exitButton = Button(self, text = 'Wyjście', command = self.clickexitButton, height = 4, width = 12, bg = 'Red')
        exitButton.place(x = 1850, y = 900)

        # 1
        oneButton = Button(self, text = '1', command = lambda: self.calculatorButton(1), height = 2, width = 4)
        oneButton.place(x = 200, y = 400)

        # 2
        twoButton = Button(self, text = '2', command = lambda: self.calculatorButton(2), height = 2, width = 4)
        twoButton.place(x = 237, y = 400)

        # 3
        threeButton = Button(self, text = '3', command = lambda: self.calculatorButton(3), height = 2, width = 4)
        threeButton.place(x = 274, y = 400)

        # 4
        fourButton = Button(self, text = '4', command = lambda: self.calculatorButton(4), height = 2, width = 4)
        fourButton.place(x = 200, y = 440)

        # 5
        fiveButton = Button(self, text = '5', command = lambda: self.calculatorButton(5), height = 2, width = 4)
        fiveButton.place(x = 237, y = 440)

        # 6
        sixButton = Button(self, text = '6', command = lambda: self.calculatorButton(6), height = 2, width = 4)
        sixButton.place(x = 274, y = 440)

        # 7
        sevenButton = Button(self, text = '7', command = lambda: self.calculatorButton(7), height = 2, width = 4)
        sevenButton.place(x = 200, y = 480)

        # 8
        eightButton = Button(self, text = '8', command = lambda: self.calculatorButton(8), height = 2, width = 4)
        eightButton.place(x = 237, y = 480)

        # 9
        nineButton = Button(self, text = '9', command = lambda: self.calculatorButton(9), height = 2, width = 4)
        nineButton.place(x = 274, y = 480)

        # 0
        zeroButton = Button(self, text = '0', command = lambda: self.calculatorButton(0), height = 2, width = 4)
        zeroButton.place(x = 200, y = 520)

        # .
        dotButton = Button(self, text = '.', command = lambda: self.calculatorButton('.'), height = 2, width = 4)
        dotButton.place(x = 237, y = 520)

        # ;
        delimiterButton = Button(self, text = ';', command = lambda: self.calculatorButton(';'), height = 2, width = 4)
        delimiterButton.place(x = 274, y = 520)

        #pi
        ctgButton = Button(self, text = '\u03C0', command = lambda: self.calculatorButton('\u03C0'), height = 2, width = 4)
        ctgButton.place(x = 200, y = 560)

        #e
        ctgButton = Button(self, text = 'e', command = lambda: self.calculatorButton('e'), height = 2, width = 4)
        ctgButton.place(x = 237, y = 560)

        # (
        leftbraceButton = Button(self, text = '(', command = lambda: self.calculatorButton('('), height = 2, width = 4)
        leftbraceButton.place(x = 274, y = 560)

        # +
        plusButton = Button(self, text = '+', command = lambda: self.calculatorButton('+'), height = 2, width = 4)
        plusButton.place(x = 311, y = 400)

        # -
        minusButton = Button(self, text = '-', command = lambda: self.calculatorButton('-'), height = 2, width = 4)
        minusButton.place(x = 311, y = 440)

        # *
        prodButton = Button(self, text = '*', command = lambda: self.calculatorButton('*'), height = 2, width = 4)
        prodButton.place(x = 311, y = 480)

        # /
        divButton = Button(self, text = '/', command = lambda: self.calculatorButton('/'), height = 2, width = 4)
        divButton.place(x = 311, y = 520)

        # )
        rightbraceButton = Button(self, text = ')', command = lambda: self.calculatorButton(')'), height = 2, width = 4)
        rightbraceButton.place(x = 311, y = 560)

        # sin
        sinButton = Button(self, text = 'sin(x)', command = lambda: self.calculatorButton('sin('), height = 2, width = 6)
        sinButton.place(x = 348, y = 400)

        # cos
        cosButton = Button(self, text = 'cos(x)', command = lambda: self.calculatorButton('cos('), height = 2, width = 6)
        cosButton.place(x = 348, y = 440)

        # tan
        tanButton = Button(self, text = 'tan(x)', command = lambda: self.calculatorButton('tan('), height = 2, width = 6)
        tanButton.place(x = 348, y = 480)

        # abs
        absButton = Button(self, text = 'abs(x)', command = lambda: self.calculatorButton('abs('), height = 2, width = 6)
        absButton.place(x = 348, y = 520)

        #sqrt
        sqrtButton = Button(self, text = 'sqrt(x)', command = lambda: self.calculatorButton('sqrt('), height = 2, width = 6)
        sqrtButton.place(x = 399, y = 400)

        #log
        logButton = Button(self, text = 'log(x)', command = lambda: self.calculatorButton('log('), height = 2, width = 6)
        logButton.place(x = 399, y = 440)

        #exp
        expButton = Button(self, text = 'exp(x)', command = lambda: self.calculatorButton('exp('), height = 2, width = 6)
        expButton.place(x = 399, y = 480)


    # FUNKCJE KLASY 

    # Przycisk wyjścia
    def clickexitButton(self):
        """Funkcja clickexitButton. Zaprogramowany przycisk zamyka aplikacje."""
        exit()

    # Przyciski kalkulatora
    def calculatorButton(self, button):
        """Funkcja calculatorButton. Zaprogramowany przycisk powoduje wypisanie się tekstu w polu do wpisywania tekstu. Argument button to tekst, który ma zostać wypisany."""
        click = self.enterfunc.get()
        self.enterfunc.delete(0, END)
        self.enterfunc.insert(0, str(click) + str(button))

    # Sprawdzanie siatki
    def checkgrid(self, plot):
        """Funkcja checkgrid. Zaprogramowane nią przyciski radiowe odpowiadają za pojawienie się siatki na wykresie. Argument plot odpowiada za wykres."""
        choise = self.grid.get()
        if choise == 1:
            plot.grid()
        elif choise == 2:
            pass
        else:
            pass
    
    # Sprawdzanie legendy
    def checklegend(self, plot):
        """Funkcja checklegend. Zaprogramowane nią przyciski radiowe odpowiadają za pojawienie się legendy na wykresie. Argument plot odpowiada za wykres."""
        choise = self.legend.get()
        if choise == 1:
            plot.legend()
        elif choise == 2:
            pass
        else:
            plot.legend()
        
    # Przycisk rysowania
    def drawaplot(self):
        """Funkcja drawaplot. Zaprogramowany nią przycisk odpowiada za wyrysowanie podanej funkcji."""
        formula = self.enterfunc.get()
        formula = formula.split(';')
        title = self.enterplot_title.get()
        x_axis_title = self.enterxaxis_title.get()
        y_axis_title = self.enteryaxis_title.get()
        x_from = self.enterxfrom.get()
        x_to = self.enterxto.get()
        fig = Figure(figsize = (6,6))           
        plot_canvas = FigureCanvasTkAgg(fig, root)
        try:
            for i in formula: 
                i = i.replace('^', '**')                     
                subplot = fig.add_subplot()
                self.subplot = subplot
                if x_from=='' or x_to=='':
                    x = np.linspace(-10, 10, 1000)
                else:
                    x = np.linspace(eval(x_from), eval(x_to), 1000)

                y = eval(i)
                if type(y) == float or type(y) == int:
                    table = []
                    for i in range(1000):
                        table.append(y)
                    y = table
                else:
                    pass
  
                self.subplot.plot(x,y, label = i)
                self.checklegend(subplot)
            self.subplot.title.set_text(title)
            self.subplot.set_xlabel(x_axis_title)
            self.subplot.set_ylabel(y_axis_title)
            self.checkgrid(subplot)
            plot_canvas.get_tk_widget().place(relx = 0.55, rely = 0.25, relwidth = 0.4, relheight = 0.5)
            plot_canvas.draw()
        except:
            canvas = ttk.Canvas(self, width=800, height=500)
            canvas.place(relx = 0.55, rely = 0.25, relwidth = 0.4, relheight = 0.5)
            canvas_id = canvas.create_text(400, 200, anchor="center", font = ("Calibri 20 bold"))
            canvas.itemconfig(canvas_id, text="Źle określona funkcja!!!")
            canvas.insert(canvas_id, 12)



# Stwórz okno
root = Tk()
app = Window(root)
root.wm_title("Plot drawer")
root.geometry("2000x1000")
root.mainloop()