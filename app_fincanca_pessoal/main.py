from tkinter import *
from tkinter import Tk,ttk
from tkinter import messagebox

#importando pillow e trabalhando com image
from PIL import Image,ImageTk

#importando barra de progresso do tkinter(utilizar no projeto de banco de horas)
from tkinter.ttk import Progressbar

#importando Matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure



#tkcalendar (calendario do tkinter)
from tkcalendar import Calendar,DateEntry
from datetime import date

#importando funcoes da view.py
from view import bar_valores,porcentagem_valor,pie_valores,inserir_categoria,inserir_receita,inserir_gastos,ver_categoria,deletar_gastos,deletar_receitas,tabela


################# cores ###############
co0 = "#2e2d2b"  # Preta
co1 = "#feffff"  # branca
co2 = "#4fa882"  # verde
co3 = "#38576b"  # valor
co4 = "#403d3d"   # letra
co5 = "#e06636"  
co6 = "#038cfc"   
co7 = "#3fbfb9"   
co8 = "#263238"   
co9 = "#e9edf5"   

colors = ['#5588bb', '#66bbbb','#99bb55', '#ee9944', '#444466', '#bb5555']


#criando janela
janela = Tk()
janela.title('Orçamento pessoal')
janela.geometry('900x650')
janela.configure(background=co9)
janela.resizable(width=FALSE,height=FALSE)

style = ttk.Style(janela)
style.theme_use("clam")


#criando frames para divisao da tela
frameCima = Frame(janela, width=1043, height=50, bg=co1,relief="flat")
frameCima.grid(row=0,column=0)

frameMeio = Frame(janela, width=1043, height=361, bg=co1,pady=20,relief="raised")
frameMeio.grid(row=1,column=0,pady=1,padx=0,sticky=NSEW)

frameBaixo = Frame(janela, width=1043, height=300, bg=co1,pady=20,relief="flat")
frameBaixo.grid(row=2,column=0,pady=0,padx=10,sticky=NSEW)

frame_gra_pie = Frame(frameMeio, width=580, height=250,bg=co2)
frame_gra_pie.place(x=415,y=5)


# Trabalhando no frame Cima

# acessando a imagem
app_img = Image.open('log.png')
app_img = app_img.resize((45,45))
app_img = ImageTk.PhotoImage(app_img)


app_logo = Label(frameCima, image=app_img, text="Orçamento Pessoal", width=900, compound=LEFT, padx= 5, relief=RAISED,anchor=NW, font=('Verdana 20 bold'), bg=co1, fg=co4)
app_logo.place(x=0,y=0)


# definindo tree como global
global tree

# funcao inserir categoria

def inserir_categoria_b():

    nome = entrada_valor_categoria.get()

    lista_inserir = [nome]

    for i in lista_inserir:
        if i == '':
            messagebox.showerror('Erro','Preencha todos os campos')
            return
    #passando para a funcao inserir gastos presente na view
    inserir_categoria(lista_inserir)

    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

    entrada_valor_categoria.delete(0,'end')

    #PEGANDO OS VALORES DA CATEGORIA
    categorias_funcao = ver_categoria()
    categoria = []

    for i in categorias_funcao:
        categoria.append(i[1])

    # atualizando a lista de categorias
    combo_categoria_despesa['values'] = (categoria)


# funcao inserir receitas
def inserir_receitas_b():
    nome = 'Receita'
    data = e_cal_receitas.get_date()
    quantia = e_valor_receitas.get()

    lista_inserir = [nome, data, quantia]

    for i in lista_inserir:
        if i == '':
            messagebox.showerror('Erro','Preencha todos os campos')
            return    
        
    # chamando a funcao inserir receitas presente na view
    inserir_receita(lista_inserir)
    
    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

    e_cal_receitas.delete(0,'end')
    e_valor_receitas.delete(0,'end')

    #atualizando dados 
    mostrar_renda()
    porcentagem()
    grafico_bar()
    resumo()
    grafico_pie()


# funcao inserir despesas
def inserir_gastos_b():
    nome = combo_categoria_despesa.get()
    data = e_cal_despesas.get_date()
    quantia = e_valor_despesas.get()

    lista_inserir = [nome, data, quantia]

    for i in lista_inserir:
        if i == '':
            messagebox.showerror('Erro','Preencha todos os campos')
            return    
        
    # chamando a funcao inserir despesas presente na view
    inserir_gastos(lista_inserir)
    
    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

    combo_categoria_despesa.delete(0,'end')
    e_cal_despesas.delete(0,'end')
    e_valor_despesas.delete(0,'end')

    #atualizando dados 
    mostrar_renda()
    porcentagem()
    grafico_bar()
    resumo()
    grafico_pie()


# funcao deletar
def deletar_dados():
    try:
        treev_dados = tree.focus()
        treev_dicionario = tree.item(treev_dados)
        treev_lista = treev_dicionario['values']
        valor = treev_lista[0]
        nome = treev_lista[1]


        if nome == 'Receita':
            deletar_receitas([valor])
            messagebox.showinfo('Sucesso', 'Os dados foram deletados com sucesso')
            
            #atualizando dados 
            mostrar_renda()
            porcentagem()
            grafico_bar()
            resumo()
            grafico_pie()
        else:
            deletar_gastos([valor])
            messagebox.showinfo('Sucesso', 'Os dados foram deletados com sucesso')
            
            #atualizando dados 
            mostrar_renda()
            porcentagem()
            grafico_bar()
            resumo()
            grafico_pie()
    except IndexError:
        messagebox.showerror('Erro!', 'Seleciona um dos dados na tabela')
        




# porcentagem-------------------------------------

def porcentagem():
    l_nome = Label(frameMeio, text="Porcentagem de Dinheiro em caixa",height=1, anchor=NW, font=('Verdana'), bg=co1, fg=co4)
    l_nome.place(x=7,y=5)    

    style = ttk.Style()
    style.theme_use('default')
    style.configure("black.Horizontal.TProgressbar", background="#daed6b")  #cor da barra de progresso
    style.configure("TProgressbar", thickness= 25) #largura do progressbar
    bar = Progressbar(frameMeio, length=180, style='black.Horizontal.TProgressbar')

    bar.place(x=10,y=35)
    bar['value'] = porcentagem_valor()
    
    valor= porcentagem_valor()[0]

    l_nome = Label(frameMeio, text="{:,.2f}%".format(valor), anchor=NW, font=('Verdana'), bg=co1, fg=co4)
    l_nome.place(x=200,y=35)    


# funcao para grafico barra-------------------------------------

# Função para gráfico de barras
def grafico_bar():
    lista_categorias = ['Renda', 'Despesas', 'Saldo']
    lista_valores = bar_valores()

    # Crie a figura e atribua objetos de eixo
    figura = Figure(figsize=(4, 3.45), dpi=60)
    ax = figura.add_subplot(111)

    # Crie o gráfico de barras
    ax.bar(lista_categorias, lista_valores, color=colors, width=0.9)

    # Adicione rótulos às barras
    for i, valor in enumerate(lista_valores):
        ax.text(i, valor + 100,  # Ajuste a posição conforme necessário
                str("{:,.0f}".format(valor)), 
                fontsize=17,
                ha='center', 
                fontstyle='italic',  
                verticalalignment='bottom', 
                color='dimgrey')

    # Ajuste os rótulos do eixo x
    ax.set_xticks(range(len(lista_categorias)))
    ax.set_xticklabels(lista_categorias, fontsize=16)

    # Personalize os eixos e o fundo
    ax.patch.set_facecolor('#ffffff')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['left'].set_linewidth(1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(color='#EEEEEE')
    ax.xaxis.grid(False)

    # Exiba o gráfico no Tkinter
    canva = FigureCanvasTkAgg(figura, frameMeio)
    canva.get_tk_widget().place(x=10, y=70)


# funcao de resumo total
def resumo():
    valor = bar_valores()

    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309,y=52)
    l_sumario = Label(frameMeio, text="Total Renda Mensal      ".upper(),anchor=NW, font=('Verdana 12'), bg=co1,fg='#83a9e6')
    l_sumario.place(x=309,y=35)
    l_sumario = Label(frameMeio, text="R$ {:,.2f}".format(valor[0]),anchor=NW, font=('Arial 17'), bg=co1,fg='#545454')
    l_sumario.place(x=309,y=70)
      

    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309,y=132)
    l_sumario = Label(frameMeio, text="Total Despesas Mensais   ".upper(),anchor=NW, font=('Verdana 12'), bg=co1,fg='#83a9e6')
    l_sumario.place(x=309,y=115)
    l_sumario = Label(frameMeio, text="R$ {:,.2f}".format(valor[1]),anchor=NW, font=('Arial 17'), bg=co1,fg='#545454')
    l_sumario.place(x=309,y=150)
    

    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309,y=207)
    l_sumario = Label(frameMeio, text="Total Saldo Mensal      ".upper(),anchor=NW, font=('Verdana 12'), bg=co1,fg='#83a9e6')
    l_sumario.place(x=309,y=190)
    l_sumario = Label(frameMeio, text="R$ {:,.2f}".format(valor[2]),anchor=NW, font=('Arial 17'), bg=co1,fg='#545454')
    l_sumario.place(x=309,y=220)


# funcao grafico pie
def grafico_pie():
    #faça figura e atribua objetos de eixo
    figura = plt.Figure(figsize=(5, 3), dpi=90)
    ax = figura.add_subplot(111)

    lista_valores = pie_valores()[1]
    lista_categorias = pie_valores()[0]

    #only "explode" the 2nd slice (i.e. 'Hogs')

    explode = []
    for i in lista_categorias:
        explode.append(0.05)

    ax.pie(lista_valores, explode=explode, wedgeprops=dict(width=0.2), autopct='%1.1f%%', colors=colors,shadow=True, startangle=90)
    ax.legend(lista_categorias, loc="center right", bbox_to_anchor=(1.55, 0.50))

    canva_categoria = FigureCanvasTkAgg(figura, frame_gra_pie)
    canva_categoria.get_tk_widget().grid(row=0,column=0)
    
    


porcentagem()
grafico_bar()
resumo()
grafico_pie()

# criando frames dentro do frame baixo
frame_renda = Frame(frameBaixo, width=300, height=250, bg=co1)
frame_renda.grid(row=0,column=0)

frame_operacoes = Frame(frameBaixo, width=220, height=250, bg=co1)
frame_operacoes.grid(row=0,column=1, padx=5)

frame_configuracao = Frame(frameBaixo, width=220, height=250, bg=co1)
frame_configuracao.grid(row=0,column=2, padx=5)

# Tabela renda mensal---------------------------------------

app_tabela = Label(frameMeio, text="Tabela Receitas e Despesas", anchor=NW, font=('Verdana 12'), bg=co1, fg=co4)
app_tabela.place(x=5,y=309)


# funcao para mostrar_renda
def mostrar_renda():

    # creating a treeview with dual scrollbars
    tabela_head = ['#Id','Categoria','Data','Quantia']

    lista_itens = tabela()
    
    global tree

    tree = ttk.Treeview(frame_renda, selectmode="extended",columns=tabela_head, show="headings")
    # vertical scrollbar
    vsb = ttk.Scrollbar(frame_renda, orient="vertical", command=tree.yview)
    # horizontal scrollbar
    hsb = ttk.Scrollbar(frame_renda, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    hd=["center","center","center", "center"]
    h=[30,100,100,100]
    n=0

    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        # adjust the column's width to the header string
        tree.column(col, width=h[n],anchor=hd[n])
        
        n+=1

    for item in lista_itens:
        tree.insert('', 'end', values=item)



# Configuracoes Despesas----------------------------------------------
l_info = Label(frame_operacoes, text="Insira novas despesas",height=1, anchor=NW, font=('Verdana 10 bold'), bg=co1,fg=co4)
l_info.place(x=10,y=10)

#categoria
l_categoria = Label(frame_operacoes, text="Categoria",height=1, anchor=NW, font=('Ivy 10'), bg=co1,fg=co4)
l_categoria.place(x=10,y=40)

# Pegando categorias(caixa de selecao)
categoria_funcao = ver_categoria()
categoria = []

for i in categoria_funcao:
    categoria.append(i[1])

combo_categoria_despesa = ttk.Combobox(frame_operacoes, width=10,font=('Ivy 10'))
combo_categoria_despesa['values'] = (categoria)
combo_categoria_despesa.place(x=110,y=41)


#despesas(fomato calendario)---------------------------------
l_cal_despesas = Label(frame_operacoes, text="Data",height=1, anchor=NW, font=('Ivy 10'), bg=co1,fg=co4)
l_cal_despesas.place(x=10,y=70)
e_cal_despesas = DateEntry(frame_operacoes, width=12,background='darkblue',foreground='white', borderwidth=2,year=2024)
e_cal_despesas.place(x=110,y=71)


# Valor (input) ------------------------------
l_valor_despesas = Label(frame_operacoes, text="Quantia Total",height=1, anchor=NW, font=('Ivy 10'), bg=co1,fg=co4)
l_valor_despesas.place(x=10,y=100)
e_valor_despesas = Entry(frame_operacoes, width=14, justify='left',relief='solid')
e_valor_despesas.place(x=110, y=101)




# botao de adicionar (despesas)
app_add_despesas = Image.open('icon-add.png')
app_add_despesas = app_add_despesas.resize((17,17))
app_add_despesas = ImageTk.PhotoImage(app_add_despesas)

botao_inserir_despesas = Button(frame_operacoes,command=inserir_gastos_b, image=app_add_despesas, text="Adicionar".upper(), width=80, compound=LEFT,anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0,overrelief=RIDGE)
botao_inserir_despesas.place(x=110,y=131)


# botao de deletar(despesas)

l_excluir = Label(frame_operacoes, text="Excluir ação",height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1,fg=co4)
l_excluir.place(x=10,y=190)

img_deletar = Image.open('icon-delete.png')
img_deletar = img_deletar.resize((17,17))
img_deletar = ImageTk.PhotoImage(img_deletar)


botao_deletar = Button(frame_operacoes,command=deletar_dados ,image=img_deletar, text="Deletar".upper(), width=80, compound=LEFT,anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0,overrelief=RIDGE)
botao_deletar.place(x=110,y=190)

# Configuracoes Receitas--------------------------------

l_info = Label(frame_configuracao, text="Insira novas receitas",height=1, anchor=NW, font=('Verdana 10 bold'), bg=co1,fg=co4)
l_info.place(x=10,y=10)

#receitas(fomato calendario)---------------------------------
l_cal_receitas = Label(frame_configuracao, text="Data",height=1, anchor=NW, font=('Ivy 10'), bg=co1,fg=co4)
l_cal_receitas.place(x=10,y=40)
e_cal_receitas = DateEntry(frame_configuracao, width=12,background='darkblue',foreground='white', borderwidth=2,year=2024)
e_cal_receitas.place(x=110,y=41)


# Valor (input) ------------------------------
l_valor_receitas = Label(frame_configuracao, text="Quantia Total",height=1, anchor=NW, font=('Ivy 10'), bg=co1,fg=co4)
l_valor_receitas.place(x=10,y=70)
e_valor_receitas = Entry(frame_configuracao, width=14, justify='left',relief='solid')
e_valor_receitas.place(x=110, y=71)


# botao de adicionar(receitas)
app_add_receitas = Image.open('icon-add.png')
app_add_receitas = app_add_receitas.resize((17,17))
app_add_receitas = ImageTk.PhotoImage(app_add_receitas)

botao_inserir_receitas = Button(frame_configuracao, image=app_add_receitas,command=inserir_receitas_b, text="Adicionar".upper(), width=80, compound=LEFT,anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0,overrelief=RIDGE)
botao_inserir_receitas.place(x=110,y=111)

# Operacao nova categoria --------------------------------

l_info = Label(frame_configuracao, text="Categoria",height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1,fg=co4)
l_info.place(x=10,y=160)

entrada_valor_categoria = Entry(frame_configuracao, width=14, justify='left',relief='solid')
entrada_valor_categoria.place(x=110, y=160)

# botao de adicionar(receitas)
app_add_categorias = Image.open('icon-add.png')
app_add_categorias = app_add_categorias.resize((17,17))
app_add_categorias = ImageTk.PhotoImage(app_add_categorias)

botao_inserir_categoriasapp_add_categorias = Button(frame_configuracao,command=inserir_categoria_b, image=app_add_categorias, text="Adicionar".upper(), width=80, compound=LEFT,anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0,overrelief=RIDGE)
botao_inserir_categoriasapp_add_categorias.place(x=110,y=190)



mostrar_renda()
janela.mainloop()


