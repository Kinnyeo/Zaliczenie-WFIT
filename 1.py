import math as np
import schedule
import time
import tkinter
import sched

G = 6.67e-11
m1 = [0]
m2 = [0]

# lista, dwa pierwsze to wspolrzedne x i y pierwszej planety, dwa ostatnie to x i y drugiej planety
xy = [0, 0, 0, 0]
dxy = [0.0, 0.0, 0.0, 0.0]
vxy = [1, 1, -1, -1]

# wartosci start i restart potrzebne do guzikow
start = [0]
restart = [0]
wystart1 = [0]
wystart2 = [0]
pierwszewlaczeniesymulacji = [1]

# szerekosc okna
animation_window_width = 1800
# wysokosc okna
animation_window_height = 1000
# promien planety
animation_planet_radius = 5
# opoznienie miedzy klatkami
animation_refresh_seconds = 0.01


# funkcja wyliczajaca polozenie i predkosc
def calculateNewPosition():
    grav = G * m1[0] * m2[0]

    dt = 0.75

    rx = xy[2] - xy[0]  # odleglosc pomiedzy planetami w x
    ry = xy[3] - xy[1]  # odleglosc pomiedzy planetami w y

    modr = np.sqrt(rx ** 2 + ry ** 2)  # dl wektora r
    wektorx = rx / modr  # wektor jednostkowy
    wektory = ry / modr  # wektor jednostkowy

    fx = -grav / modr ** 2 * wektorx
    fy = -grav / modr ** 2 * wektory

    scale = 1e-18  # przeskalowanie zeby miescilo sie na ekranie

    vxy[0] += -fx * dt / m1[0] * scale
    vxy[1] += -fy * dt / m1[0] * scale
    vxy[2] += fx * dt / m2[0] * scale
    vxy[3] += fy * dt / m2[0] * scale

    dxy[0] = vxy[0] * dt
    dxy[1] = vxy[1] * dt
    dxy[2] = vxy[2] * dt
    dxy[3] = vxy[3] * dt

    xy[2] += dxy[2]
    xy[3] += dxy[3]
    xy[0] += dxy[0]
    xy[1] += dxy[1]


# funkcja tworzaca okno
def create_animation_window():
    window = tkinter.Tk()
    window.title("Animation")
    window.geometry(f'{animation_window_width}x{animation_window_height}')
    return window


# funkcja tworzaca canvas, przyciski i pola do wpisywania wartosci. Wstawia wszystko do okna
def create_animation_canvas(window):
    canvas = tkinter.Canvas(window)
    canvas.configure(bg="black")
    canvas.pack(fill="both", expand=True)
    canvas.create_window(1720, 45, window=entry_fields2(Window))
    canvas.create_window(1720, 15, window=entry_fields3(Window))
    canvas.create_window(1720, 75, window=entry_fields4(Window))
    canvas.create_window(1720, 105, window=entry_fields5(Window))
    canvas.create_window(1720, 135, window=entry_fields6(Window))
    canvas.create_window(1720, 165, window=entry_fields7(Window))
    name_label2 = tkinter.Label(window, text='M1', font=('calibre', 10, 'bold'))
    name_label3 = tkinter.Label(window, text='M2', font=('calibre', 10, 'bold'))
    name_label4 = tkinter.Label(window, text='X1', font=('calibre', 10, 'bold'))
    name_label5 = tkinter.Label(window, text='Y1', font=('calibre', 10, 'bold'))
    name_label6 = tkinter.Label(window, text='X2', font=('calibre', 10, 'bold'))
    name_label7 = tkinter.Label(window, text='Y2', font=('calibre', 10, 'bold'))
    button = tkinter.Button(window, text='Start', font=('calibre', 12, 'bold'), command=getstart)
    button3 = tkinter.Button(window, text='Restart', font=('calibre', 12, 'bold'), command=getrestart)
    canvas.create_window(1630, 45, window=name_label2)
    canvas.create_window(1630, 15, window=name_label3)
    canvas.create_window(1630, 75, window=name_label4)
    canvas.create_window(1630, 105, window=name_label5)
    canvas.create_window(1630, 135, window=name_label6)
    canvas.create_window(1630, 165, window=name_label7)
    canvas.create_window(1680, 195, window=button)
    canvas.create_window(1750, 195, window=button3)

    return canvas


# funkcje tworzace pola do wpisywania

def entry_fields2(window):
    entry2 = tkinter.Entry(window, textvariable=namem2, font=('calibre', 10, 'normal'))
    return entry2


def entry_fields3(window):
    entry3 = tkinter.Entry(window, textvariable=namem1, font=('calibre', 10, 'normal'))
    return entry3


def entry_fields5(window):
    entry5 = tkinter.Entry(window, textvariable=pol2, font=('calibre', 10, 'normal'))
    return entry5


def entry_fields4(window):
    entry4 = tkinter.Entry(window, textvariable=pol1, font=('calibre', 10, 'normal'))
    return entry4


def entry_fields6(window):
    entry6 = tkinter.Entry(window, textvariable=pol3, font=('calibre', 10, 'normal'))
    return entry6


def entry_fields7(window):
    entry7 = tkinter.Entry(window, textvariable=pol4, font=('calibre', 10, 'normal'))
    return entry7


# funkcja powiazana z przyciskiem start, obsluguje wartosic wpisywane do pól
def getstart():
    name1 = namem1.get()
    name1conv = float(name1)
    m1[0] = name1conv * 1e30
    name2 = namem2.get()
    name2conv = float(name2)
    m2[0] = name2conv * 1e30
    polx1 = pol1.get()
    poly1 = pol2.get()
    polx2 = pol3.get()
    poly2 = pol4.get()
    polx1conv = int(polx1)
    poly1conv = int(poly1)
    polx2conv = int(polx2)
    poly2conv = int(poly2)
    xy[0] = polx1conv
    xy[1] = poly1conv
    xy[2] = polx2conv
    xy[3] = poly2conv

    if start[0] == 0:
        start[0] = 1
        if restart[0] == 1 or pierwszewlaczeniesymulacji[0] == 1:
            wystart1[0] = 1
        restart[0] = 0
        pierwszewlaczeniesymulacji[0] = 0

#funckja obslugujaca przycisk restart
def getrestart():
    restart[0] = 1
    start[0] = 0
    wystart1[0] = 0
    pierwszewlaczeniesymulacji[0] = 1


# funkcje tworzace planety
def animate_planet(canvas):
    planet = canvas.create_oval(xy[0] - animation_planet_radius,
                                xy[1] - animation_planet_radius,
                                xy[0] + animation_planet_radius,
                                xy[1] + animation_planet_radius,
                                fill="blue", tag="planet1", outline="blue", width=4)

    return planet


def animate_planet2(canvas):
    planet = canvas.create_oval(xy[2] - animation_planet_radius,
                                xy[3] - animation_planet_radius,
                                xy[2] + animation_planet_radius,
                                xy[3] + animation_planet_radius,
                                fill="red", tag="planet2", outline="red", width=4)

    return planet


# ustawienie wykonywania co sekunde funkcji obliczajacej pozycje i metody numerycznej
schedule.every(int(animation_refresh_seconds)).seconds.do(calculateNewPosition)
while True:

    # stworzenie okna, canvas i zmienne przechowujace dane z pol w ktorych mozna pisac
    Window = create_animation_window()
    namem1 = tkinter.StringVar()
    namem2 = tkinter.StringVar()
    pol1 = tkinter.StringVar()
    pol2 = tkinter.StringVar()
    pol3 = tkinter.StringVar()
    pol4 = tkinter.StringVar()
    Canvas1 = create_animation_canvas(Window)

    while True:
        # Jesli doszlo do restartu lub uruchamiamy pierwszy raz
        if wystart1[0] == 1:
            #planety
            Planet1 = animate_planet(Canvas1)
            Planet2 = animate_planet2(Canvas1)
            wystart2[0] = 1
            wystart1[0] = 0
        # jesli nie wpisalismy mas i nie kliknelismy start
        if start[0] == 0:
            Window.update()
        # jesli kliknelismy nastepuje restart
        if restart[0] == 1:
            Window.destroy()
            vxy[0] = 0
            vxy[1] = 0
            vxy[2] = 0
            vxy[3] = 0
            restart[0] = 0
            wystart2[0] = 0
            schedule.clear('calculateNewPosition')
            break


        # anmiacja dziala
        elif wystart2[0] == 1:
            schedule.run_pending()
            time.sleep(animation_refresh_seconds)

            print(xy[0], xy[1], vxy[0], vxy[1])
            print(xy[2], xy[3], vxy[2], vxy[3])

            Canvas1.create_oval(xy[2], xy[3], xy[2], xy[3], width=0, fill='red')
            Canvas1.create_oval(xy[0], xy[1], xy[0], xy[1], width=0, fill='blue')

            Canvas1.move(Planet1, dxy[0], dxy[1])
            Canvas1.move(Planet2, dxy[2], dxy[3])
            Window.update()
