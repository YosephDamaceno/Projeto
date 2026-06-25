from tkinter import *
from tkinter import ttk

# Quando mouse é pressionado
def iniciar_figura_nova(event): 
    global figura_nova
    if tipo_figura_var.get() == 'Linha':
        figura_nova = ("linha", (event.x, event.y, event.x, event.y))
    elif tipo_figura_var.get() == 'Rabisco':
        figura_nova = ("rabisco", [(event.x, event.y)])
    elif tipo_figura_var.get() == 'Círculo':
        figura_nova = ('Círculo', (event.x, event.y, event.x, event.y)) # adicionando círculo como figura nova
    elif tipo_figura_var.get() == 'retangulo':
        figura_nova = ("retangulo", ((event.x, event.y, event.x, event.y))) #figura nova: retângulo


# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    global figura_nova
    tipo = figura_nova[0] # atribuí figura_nova[0] a variável tipo para facilitar a nossa visualização do código
    if tipo == "rabisco":
        figura_nova[1].append((event.x, event.y))
    elif tipo == 'linha': 
        figura_nova = (tipo, (figura_nova[1][0], figura_nova[1][1], event.x, event.y))
    elif figura_nova[0] == "retangulo":
        figura_nova = ("retangulo", (figura_nova[1][0], figura_nova[1][1], event.x, event.y))
    elif tipo == 'Círculo':
        x1, y1 = figura_nova[1][0], figura_nova[1][1] 
        dx = event.x - x1
        dy = event.y - y1
        tamanho = max(abs(dx), abs(dy)) #pra que seja realmente  um círculo e não um oval
        x2 = x1 + tamanho if dx >= 0 else x1 - tamanho
        y2 = y1 + tamanho if dx >= 0 else y1 - tamanho
        figura_nova = (tipo, (x1, y1, x2, y2) )
    desenhar_figuras()
    desenhar_figura_nova()

# Quando mouse é solto
def incluir_figura_nova(event): 
    if not incompleta(figura_nova): # para evitar incluir figuras incompletas, como uma linha sem comprimento ou um rabisco com um único ponto
        figuras.append(figura_nova) 
    desenhar_figuras()

def desenhar_figuras():
    canvas.delete("all")
    for fig, values in figuras:
        if fig == "linha":
            canvas.create_line(values[0], values[1], values[2], values[3])
        elif fig == "Círculo":
            canvas.create_oval(values[0], values[1], values[2], values[3])
        elif fig == "retangulo":
            canvas.create_rectangle(values[0], values[1], values[2], values[3])
        else : # fig == "rabisco"
            canvas.create_line(values)

def desenhar_figura_nova():
    fig, values = figura_nova
    if fig == "linha":
        canvas.create_line(values[0], values[1], values[2], values[3], dash=(4, 2))
    elif fig == 'Círculo':
        canvas.create_oval(values[0], values[1], values[2], values[3], dash = (4,2))
    elif fig == "retangulo":
        canvas.create_rectangle(values[0], values[1], values[2], values[3], dash=(4, 2))
    else : # fig == "rabisco"
        canvas.create_line(values, dash=(4, 2))

def incompleta(figura):
    fig, values = figura
    if fig in ["linha", "Círculo", "retangulo"]:
        return (values[0], values[1]) == (values[2], values[3])
    else : # fig == "rabisco"
        return len(values) <= 1




#******* MAIN *******#

figuras = []       # Todas as figuras desenhadas
figura_nova = None # Figura que está sendo desenhada, mas ainda não foi incluída em figuras

root = Tk()
root.title('Exemplo de aplicação')
frame = Frame(root)

# Widgets arranjados com Layout grid dentro de frame
paddings = {'padx': 5, 'pady': 5} 

# label
label = ttk.Label(frame,  text='Escolha se vai desenhar linha, Rabisco, Círculo ou retangulo:')
label.grid(column=0, row=0, sticky=W, **paddings)

# option menu
tipo_figura_var = StringVar(root) # Guarda o tipo de figura selecionado no option menu (linha ou rabisco)
option_menu = ttk.OptionMenu(frame, tipo_figura_var,
                             'Linha', 'Linha', 'Rabisco','Círculo', 'retangulo')
option_menu.grid(column=1, row=0, sticky=W, **paddings)

# Área de desenho
canvas = Canvas(frame, bg='white', width=600, height=600)
canvas.grid(column=0, row=1, columnspan=2, sticky=W, **paddings)

frame.pack()

# Eventos de mouse associados ao canvas - com seus callbacks
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

root.mainloop()

