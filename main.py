from tkinter import *
from tkinter import ttk
from tkinter import colorchooser 
from classes import * #Referência ao arquivo onde as classes/subclasses estão guardadas, importando todas

#Adicionando opção de escolher cores
cor_atual = 'black'
background = None

def escolher_cor_borda():
    global cor_atual
    cor = colorchooser.askcolor()[1]
    if cor:
        cor_atual = cor

def escolher_cor_preenchimento():
    global background
    cor = colorchooser.askcolor()[1]
    if cor:
        background = cor

# Quando mouse é pressionado
def iniciar_figura_nova(event):
    global figura_nova

    tipo = tipo_figura_var.get()

    if tipo == 'Linha':
        figura_nova = Linha(event.x, event.y, event.x, event.y, cor_atual)

    elif tipo == 'Retângulo':
        figura_nova = Retangulo(event.x, event.y, event.x, event.y, cor_atual, background)

    elif tipo == 'Oval':
        figura_nova = Oval(event.x, event.y, event.x, event.y, cor_atual, background)

    elif tipo == 'Círculo':
        figura_nova = Circulo(event.x, event.y, event.x, event.y, cor_atual, background)
    else:
        figura_nova =  Rabisco(event.x, event.y, cor_atual)


# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    global figura_nova
    if figura_nova is None:
        return 
    figura_nova.atualizar(event.x, event.y)
    desenhar_figuras()
    figura_nova.desenhar(canvas)

# Quando mouse é solto
def incluir_figura_nova(event):
    # para evitar incluir figuras incompletas,
    # como uma linha sem comprimento ou um rabisco com um único ponto
    global figura_nova
    if figura_nova is None:
        return 
    if not figura_nova.incompleta():
        figuras.append(figura_nova)
    
    figura_nova = None
    desenhar_figuras()

    desenhar_figuras()

def desenhar_figuras(): #aqui a gnt usa o polimorfismo
    canvas.delete("all")
    for figura in figuras:
        figura.desenhar(canvas)

# a função de desenhar figura nova não vai ser mais necessária


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
    'Retângulo',
    'Oval',
    'Círculo'
)

option_menu.grid(column=1, row=0, sticky=W, **paddings)

# Área de desenho
canvas = Canvas(frame, bg='white', width=600, height=600)
canvas.grid(column=0, row=3, columnspan=2, sticky=W, **paddings)

#botão pra escolher cores
botao_cor_borda = Button(frame, text = "Cor da Borda", command = escolher_cor_borda)
botao_cor_borda.grid(column=0, row=1, sticky=W, **paddings)
botao_cor_preenchimento = Button(frame, text = "Preenchimento", command = escolher_cor_preenchimento)
botao_cor_preenchimento.grid(column=1, row=1, sticky=W, **paddings)
frame.pack()

# Eventos de mouse associados ao canvas - com seus callbacks
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

root.attributes('-topmost', 1)
root.mainloop()
