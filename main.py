from tkinter import *
from tkinter import ttk
from tkinter import colorchooser 

#Adicionando opção de escolher cores
cor_atual = 'black'
background = None

def escolher_cor():
    global cor_atual
    global background
    cor = colorchooser.askcolor()[1]
    if cor:
        cor_atual = cor
        background = cor

# Quando mouse é pressionado
def iniciar_figura_nova(event):
    global figura_nova

    if tipo_figura_var.get() == 'Linha':
        figura_nova = ("linha", (event.x, event.y, event.x, event.y))

    elif tipo_figura_var.get() == 'retangulo':
        figura_nova = ("retangulo", (event.x, event.y, event.x, event.y))

    elif tipo_figura_var.get() == 'oval':
        figura_nova = ("oval", (event.x, event.y, event.x, event.y)) ### novo ###

    elif tipo_figura_var.get() == 'Círculo':
        figura_nova = ('Círculo', (event.x, event.y, event.x, event.y))
    else:
        figura_nova = ("rabisco", [(event.x, event.y)])

# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    global figura_nova
    tipo = figura_nova[0]
    if tipo == "rabisco":
        figura_nova[1].append((event.x, event.y))

    elif tipo == "retangulo":
        figura_nova = (
            "retangulo",
            (figura_nova[1][0], figura_nova[1][1], event.x, event.y)
        )
    elif tipo == "oval": ### novo ###
        figura_nova = (
            "oval",
            (figura_nova[1][0], figura_nova[1][1], event.x, event.y)
        )
    elif tipo == 'Círculo':
        x1 = figura_nova[1][0]
        y1 = figura_nova[1][1]
        dx = event.x - x1
        dy = event.y - y1

        tamanho = max(abs(dx), abs(dy))

        x2 = tamanho + x1 if dx >= 0 else x1 - tamanho
        y2 = tamanho + y1 if dy >= 0 else y1 - tamanho

        figura_nova = ('Círculo', (x1, y1, x2, y2) )
    else:  # figura_nova[0] == "linha"
        figura_nova = (
            "linha",
            (figura_nova[1][0], figura_nova[1][1], event.x, event.y)
        )

    desenhar_figuras()
    desenhar_figura_nova()

# Quando mouse é solto
def incluir_figura_nova(event):
    # para evitar incluir figuras incompletas,
    # como uma linha sem comprimento ou um rabisco com um único ponto
    if not incompleta(figura_nova):
        figuras.append(figura_nova)

    desenhar_figuras()

def desenhar_figuras():
    canvas.delete("all")

    for fig, values in figuras:

        if fig == "linha":
            canvas.create_line(
                values[0],
                values[1],
                values[2],
                values[3],
                fill = cor_atual
            )

        elif fig == "retangulo":
            canvas.create_rectangle(
                values[0],
                values[1],
                values[2],
                values[3],
                outline=cor_atual,
                fill=background
            )

        elif fig in ["oval", 'Círculo']: 
            canvas.create_oval(
                values[0],
                values[1],
                values[2],
                values[3],
                outline=cor_atual,
                fill=background
            )

        else:  # fig == "rabisco"
            canvas.create_line(values, fill= cor_atual)

def desenhar_figura_nova():
    fig, values = figura_nova

    if fig == "linha":
        canvas.create_line(
            values[0],
            values[1],
            values[2],
            values[3],
            dash=(4, 2)
        )

    elif fig == "retangulo":
        canvas.create_rectangle(
            values[0],
            values[1],
            values[2],
            values[3],
            dash=(4, 2),
            fill=background
        )

    elif fig in ["oval", 'Círculo']:
        canvas.create_oval(
            values[0],
            values[1],
            values[2],
            values[3],
            dash=(4, 2),
            fill=background
        )

    else:  # fig == "rabisco"
        canvas.create_line(values, dash=(4, 2))

def incompleta(figura):
    fig, values = figura

    if fig == "linha":
        return (values[0], values[1]) == (values[2], values[3])

    elif fig == "retangulo":
        return (values[0], values[1]) == (values[2], values[3])

    elif fig in ["oval", 'Círculo']: ### novo ###
        return (values[0], values[1]) == (values[2], values[3])

    else:  # fig == "rabisco"
        return len(values) <= 1


# ******* MAIN ******* #

figuras = []       # Todas as figuras desenhadas
figura_nova = None # Figura que está sendo desenhada, mas ainda não foi incluída em figuras

root = Tk()
root.title('Primeira entrega do Projeto POO')

frame = Frame(root)

# Widgets arranjados com Layout grid dentro de frame
paddings = {'padx': 5, 'pady': 5}

# label
label = ttk.Label(
    frame,
    text='Escolha se vai desenhar linha, Rabisco, retangulo ou oval:'
)
label.grid(column=0, row=0, sticky=W, **paddings)

# option menu
# Guarda o tipo de figura selecionado no option menu
tipo_figura_var = StringVar(root)

option_menu = ttk.OptionMenu(
    frame,
    tipo_figura_var,
    'Linha',
    'Linha',
    'Rabisco',
    'retangulo',
    'oval',
    'Círculo'
)

option_menu.grid(column=1, row=0, sticky=W, **paddings)

# Área de desenho
canvas = Canvas(frame, bg='white', width=600, height=600)
canvas.grid(column=0, row=2, columnspan=2, sticky=W, **paddings)
#botão pra escolher cores
botao_cor = Button(root, text = "Escolher cor", command = escolher_cor)
botao_cor.pack()
frame.pack()

# Eventos de mouse associados ao canvas - com seus callbacks
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

root.attributes('-topmost', 1)
root.mainloop()
