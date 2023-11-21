from tkinter import *
from tkinter import Misc
from PIL import Image,ImageTk
from sqlite3 import *
from tkinter.simpledialog import Dialog
from tkinter.messagebox import showinfo




# Cria a janela principal
root = Tk()
root.title("AçaiMania")
root.state("zoomed")

# Cria o primeiro container no topo
top_frame = Frame(root)
top_frame.pack(fill=BOTH, expand=True)

# Adiciona uma label ao primeiro container
label = Label(top_frame, text="AçaiMania", font=("Arial", 24),background="#cc0099",foreground="white")
label.pack(fill="both")

# Cria um frame para conter os containers do meio e de baixo
middle_bottom_frame = Frame(root)
middle_bottom_frame.pack(fill=BOTH, expand=True)

# Cria o segundo container dentro do frame middle_bottom_frame (esquerda)
esquerda = Frame(middle_bottom_frame,background="white")
esquerda.pack(side=LEFT, fill=BOTH, expand=True)

# Cria o terceiro container dentro do frame middle_bottom_frame (direita)
direita = Frame(middle_bottom_frame)
direita.pack(side=RIGHT, fill=BOTH, expand=True)
#seta todas as stringvars
strCodigo = StringVar()
strProd = StringVar()
strPreco = StringVar()
strQuantidade = StringVar()
totalPedido = 0
strTotal = StringVar()
strTotal.set("Total:")
# Cria o quarto container dentro da direita
Label(direita,text="cod").pack(fill=BOTH)
codigo = Entry(direita,textvariable=strCodigo)
codigo.pack(fill=BOTH)

Label(direita,text="produto").pack(fill=BOTH)
prod = Entry(direita,textvariable=strProd,state='disabled')
prod.pack(fill=BOTH)

Label(direita,text="preço").pack(fill=BOTH)
preco = Entry(direita,textvariable=strPreco,state='disabled')
preco.pack(fill=BOTH)

Label(direita,text="Quantidade").pack(fill=BOTH)
quant = Entry(direita,textvariable=strQuantidade)
quant.pack(fill=BOTH)

Label(direita,text="\n\n").pack(fill=BOTH)

#cria uma lista para armazenar o pedido
listaproduto=[]
listbox = Listbox(direita, listvariable=listaproduto, height=6, selectmode=EXTENDED)
listbox.pack(expand=True, fill=BOTH)
listbox.bind('<FocusIn>', lambda event: volta_inicio())


Label(direita,text="Total:",font=("impact",20),textvariable=strTotal).pack(fill=BOTH,side=LEFT)

#adiciona a logo
img = Image.open("LOGO.jpeg")
img = img.resize((500,800))
Logo =ImageTk.PhotoImage(img)
logo = Label(esquerda , image= Logo ) #imagem que vai ser exibida na tela
logo.pack(fill=BOTH,side= LEFT)


def on_tab_press(cod):
    print("procurando item...")
    print(cod)
    con = connect("./database.db")
    cursor =con.cursor()
    try:
        cursor.execute("SELECT * FROM ITEMS WHERE REFERENCIA = "+cod+";")
    except:
        return
    dados = cursor.fetchall()
    print([dados[0][1],dados[0][2]])
    return [dados[0][1],dados[0][2]]
    
class DialogoFinalisaCompra(Dialog):
    def __init__(self, parent: Misc | None, title : str | None = None) -> None:
        self.op = StringVar()
        super().__init__(parent, title)
    def body(self,master):
        Label(master,text="1 - especie\n2-debito\n3-credito\n4 -pix").pack()
        entr =Entry(master,textvariable=self.op).pack()
        return entr
    def apply(self):
        self.opsl=int(self.op.get())
def on_f2_press(totalAPg,root:Tk,NOTA):
    print("F2 pressionado - Finalizar compra")
    print(NOTA)
    perguntafinaliza= DialogoFinalisaCompra(root)
    print(f"Total a pagar:{totalAPg}")
    print(f"opção selecionada:{perguntafinaliza.opsl}")
    arr = [1,2,3,4]
    try :
        a = arr[perguntafinaliza.opsl]
        with open("nota.txt","w") as f:
            f.write(NOTA)
        return 1
    except:
        return None

class DialogoDeleteItem(Dialog):
    def __init__(self, parent, lista, preços):
        self.lista = lista
        self.preços = preços
        self.vartop = StringVar()
        super().__init__(parent)

    def body(self, master):
        buffer = ""
        for i, texto in enumerate(self.lista):
            buffer += str(i) + "-" + texto + "\t\n"
        Label(master,text=buffer).pack()
        entry = Entry(master,textvariable=self.vartop)
        entry.pack(side=BOTTOM)
        return entry


    def apply(self):
        self.result = self.vartop.get()

def on_f3_press(lista:list,preços:list,ROOT:Tk): 
    print("F3 pressionado - Remover itens")
    dialogo = DialogoDeleteItem(ROOT, lista, preços)
    valor_retornado = dialogo.result
    return valor_retornado

    


def on_f4_press(event=None):
    print("F4 pressionado - Verificar pedidos")

def on_f5_press(event=None):
    print("F5 pressionado - Sair do sistema")
    root.quit()
class DialogoCatalogaItem(Dialog):
    def __init__(self,parent):
        self.nome = StringVar()
        self.valorUnitario = StringVar()
        super().__init__(parent)
    def body(self,master):
        Label(master,text="Nome do produto").pack()
        nom =Entry(master,textvariable=self.nome).pack()
        Label(master,text="Valor unitario").pack()
        vl =Entry(master,textvariable=self.valorUnitario).pack()
        return nom
    def apply(self):
        self.listresult = [self.nome.get(),self.valorUnitario.get()]
        
def on_f1_press(root:Tk = root):
    print("F1 pressionado - catalogar item")
    dialogo = DialogoCatalogaItem(root)
    conn = connect("./database.db")
    cursor = conn.cursor()
    sql = f"""INSERT INTO ITEMS(PRODUTO,VALOR) VALUES('{dialogo.listresult[0]}',{dialogo.listresult[1]})"""
    cursor.execute(sql)
    conn.commit()
    print(cursor.fetchall())
    sql = f"""SELECT * FROM ITEMS WHERE PRODUTO = '{dialogo.listresult[0]}' AND VALOR = {dialogo.listresult[1]};"""
    cursor.execute(sql)
    resp = cursor.fetchall()
    conn.close()
    showinfo(f"item adicionado.",f"item adicionado\nREFERENCIA:{resp[0][0]}\nNOME DO PRODUTO:{resp[0][1]}\nPREÇO:{resp[0][2]}\n")
    
    
def volta_inicio():
        print("voltando ao inicio")
        esquerda.selection_clear()
        codigo.focus_force()
        

    
#comecar pelo codigo

volta_inicio()
# Adicionar os manipuladores de eventos 
strCodigo.trace("w", lambda name, index, mode: (rs := on_tab_press(codigo.get()), strProd.set(rs[0]), strPreco.set(rs[1])))
#root.bind("<Enter>", lambda event: (rs := on_tab_press(codigo.get()), strProd.set(rs[0]),strPreco.set(rs[1]),quant.focus_set()))
quant.bind("<Tab>",lambda event:(
    qtd := strQuantidade.get(),None if qtd == "" or strCodigo.get() == "" else (
    listbox.insert("end",str(strProd.get()+"."*10+"...R$"+strPreco.get()+"."*10+"...-> "+strQuantidade.get())+" UN"+"..."*10+" -> R$"+str(float(strPreco.get())*float(strQuantidade.get()))),
    listaproduto.append(float(strPreco.get())*int(strQuantidade.get())),
    tot := sum(listaproduto),strTotal.set("Total:"+str(tot)),
    strProd.set(""),
    strPreco.set(""),
    strCodigo.set(""),
    strQuantidade.set(""),print("produto adicionado")
    
    
    
    )
    
))

def on_f2_press_handler(event = None):
    result = on_f2_press(sum(listaproduto), root=root,NOTA=listbox.get(0, "end"))
    print(result)
    
    if result is not None:
        listbox.delete(0, "end")
        listaproduto.clear()
        strTotal.set("Total:")

root.bind("<F2>", on_f2_press_handler)
root.bind("<F3>", lambda event: (INDEX := on_f3_press(listbox.get(0,"end"),listaproduto,root),
                                 listbox.delete(INDEX),listaproduto.pop(int(INDEX)),tot := sum(listaproduto),strTotal.set("Total:"+str(tot))))
root.bind("<F4>", on_f4_press)
root.bind("<F5>", on_f5_press)
root.bind("<F1>",lambda event:on_f1_press(root=root))
#Label(esquerda,text="F1 - CATALOGAR ITEM\n\nF2 - FINALIZAR COMPRA\n\nF3 - REMOVER ITENS\n\nF4 - VERIFICAR PEDIDOS\n\nF5 - SAIR DO SISTEMA\n",background="#ffffff").pack(side=LEFT,fill=Y)
#espaçamento entre botões
esp=40
#bordas de botões
bd=10
esqbt=Frame(esquerda,background="white")
btn1 = Button(esqbt, text="F1 - CATALOGAR ITEM", command=on_f1_press,foreground="white",background="#cc00cc",bd=bd)

btn1.pack(fill=BOTH,pady=esp)
btn2 = Button(esqbt,text="F2 - FINALIZAR COMPRA",command=on_f2_press_handler,foreground="white",background="#cc00cc",bd=bd).pack(fill=BOTH,pady=esp)
btn3 = Button(esqbt,text="F3 - REMOVER ITENS",command=lambda event=None: (INDEX := on_f3_press(listbox.get(0,"end"),listaproduto,root),
                                 listbox.delete(INDEX),listaproduto.pop(int(INDEX)),tot := sum(listaproduto),strTotal.set("Total:"+str(tot))),foreground="white",background="#cc00cc",bd=bd)
btn3.pack(fill=BOTH,pady=esp)
btn4 = Button(esqbt,text="F4 - VERIFICAR PEDIDOS",command=on_f4_press,foreground="white",background="#cc00cc",bd=bd).pack(fill=BOTH,pady=esp)
btn5 = Button(esqbt,text="F5 - SAIR DO SISTEMA",command=on_f5_press,foreground="white",background="#cc00cc",bd=bd).pack(fill=BOTH,pady=esp)
esqbt.pack(fill=BOTH,expand=True)
root.mainloop()
