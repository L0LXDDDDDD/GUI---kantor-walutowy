###################
# KONWERTER WALUT # Autor: Michał Wiktorowski
###################

# Zaimportowane moduły
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import sys
import requests
import json
import pickle
import urllib.request

# Zmienne pomocnicze (globalne)
chosen1 = ''
chosen2 = ''

# Funkcja sprawdzająca połączenie z internetem
def connect():
    try:
        urllib.request.urlopen('http://google.com') #Python 3.x
        return True
    except:
        return False

# Pobranie danych z internetu. W przypadku braku internetu, otwarza te zapisane w pamięci
rates2 = requests.get('http://api.nbp.pl/api/exchangerates/tables/A/')
rates2 = rates2.json()[0]

storefile = 'store.json'
fw = open(storefile, 'wb')
pickle.dump(rates2, fw)
fw.close()

if connect():
    rates = requests.get('http://api.nbp.pl/api/exchangerates/tables/A/')
    rates = rates.json()[0]
else:
    fd = open(storefile, 'rb')
    rates = pickle.load(fd)
    rates = rates.json()[0]

# Stworzenie listy walut wraz z ich kursem
cur_dict = {}
cur_names = []
cur_rates = []

for dicts in range(len(rates['rates'])):
    currency = rates['rates'][dicts]['currency']
    code = rates['rates'][dicts]['code']
    full_name = code + ' - ' + currency
    mid = rates['rates'][dicts]['mid']
    cur_names.append(full_name)
    cur_rates.append(mid)
cur_names.append('PLN - polski złoty')
cur_rates.append(1.0)

# Stworzenie słownika z powstałych list
for key in cur_names:
   for value in cur_rates:
      cur_dict[key] = value
      cur_rates.remove(value)
      break

# Funkcja konwertująca waluty
def converter(value1, currency_rate1, currency_rate2):
    value2 = value1*currency_rate1/currency_rate2
    return value2

def create_img(frame, png_file):
    width = 1000
    height = 600

    img = Image.open(png_file)
    img = img.resize((width,height), Image.ANTIALIAS)
    photoImg =  ImageTk.PhotoImage(img)

    img_label = Label(frame, image=photoImg, width=width)
    img_label.image = photoImg
    return img_label

# Klasa Window
class Window(Frame):
    def __init__(self, master = None):

        # Inicjalizacja okna
        Frame.__init__(self, master)
        self.master = master

        self.pack(fill = BOTH, expand = True)

        # Inicjalizacja tła
        img = create_img(self, 'background.png')
        img.place(x = 0, y = 0)

        # Inicjalizacja tytułu
        titlelabel = Label(self, text = 'Currency converter', height = 2, width = 16, font = ("Calibri", 45), fg = 'blue')
        titlelabel.place(x = 0, y = 0)

        # Inicjalizacja list rozwijanych
        global chosen1
        options = cur_names
        combo = ttk.Combobox(self, value = options)
        self.combo = combo
        combo.current(0)
        combo.place(x = 600, y = 20)
        combo.bind("<<ComboboxSelected>>", lambda _: self.checkcombo(chosen1, self.combo))
        
        fromlabel = Label(self, text = 'From')
        fromlabel.place(x = 600, y = 0)

        global chosen2
        options2 = cur_names
        combo2 = ttk.Combobox(self, value = options2)
        self.combo2 = combo2
        combo2.current(0)
        combo2.place(x = 800, y = 20)
        combo2.bind("<<ComboboxSelected>>", lambda _: self.checkcombo(chosen2, self.combo2))

        tolabel = Label(self, text = 'To')
        tolabel.place(x = 800, y = 0)

        # Inicjalizacja pola tekstowego
        typetext = Entry(self, font = ("Calibri", 25), bg = 'white smoke')
        self.typetext = typetext
        self.typetext.place(x = 17, y = 302, width = 600, height = 80)

        currencylabel = Label(self, text = 'Amount', height = 2, width = 30, font = ("Calibri", 15))
        currencylabel.place(x = 17, y = 248)

        # Inicjalizacja pola wynikowego
        display_text = StringVar()
        self.display_text = display_text
        resultlabel = Label(self, textvariable = display_text, height = 3, width = 60, borderwidth = 1, relief = 'sunken', font = ("Calibri", 15))
        resultlabel.place(x = 17, y = 500)

        result2label = Label(self, text = 'Result', height = 2, width = 30, font = ("Calibri", 15))
        result2label.place(x = 17, y = 446)

        # Inicjalizacja przycisków
        exitButton = Button(self, text = 'Exit', command = self.clickexitButton, height = 4, width = 12, bg = 'Red')
        exitButton.place(x = 850, y = 500)

        convertButton = Button(self, text = 'Convert', command = self.clickconvertButton, width = 12, height = 4)
        convertButton.place(x = 850, y = 302)


    # Funkcje przycisków

    # Przycisk wyjścia
    def clickexitButton(self):
        exit()

    # Listy rozwijane
    def checkcombo(self, chosen, combobox):
        for names in cur_names:
            if combobox.get() == names:
                chosen = combobox.get()
                chosen_rate = cur_dict[chosen]
        return chosen_rate

    # Skróty nazw wybranych walut
    def shortform(self, chosen, combobox):
        for names in cur_names:
            if combobox.get() == names:
                chosen = combobox.get()[0:3]
        return chosen

    # Pole do wpisania tekstu
    # def checkentry(self, text):
    #     return text.get()

    # Przycisk konwersji
    def clickconvertButton(self):
        try:
            text = self.typetext.get()
            text = text.replace(',', '.')
            result = round(converter(float(text), self.checkcombo(chosen1, self.combo), self.checkcombo(chosen2, self.combo2)), 3)
            final_result = str(float(text)) + ' ' + self.shortform(chosen1, self.combo) + ' = ' + str(result) + ' ' + self.shortform(chosen2, self.combo2)
            self.display_text.set(final_result)
            return final_result
        except:
            self.display_text.set('Wrong value, please enter a real number!')

        
# Stwórz okno
root = Tk()
app = Window(root)
root.wm_title("Currency converter")
root.geometry("1000x600")
root.mainloop()