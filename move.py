import getopt, sys
from DNAStrand import DNAStrand
from tkinter import *
from tkinter import messagebox as msgBox

##
# Instancia um objeto da classe Tk , responsável por criar
# a janela principal . Aceita , na linha de comando ,
# quatro argumentos :

# @param h help
# @param n tamanho do DNA1
# @param m tamanho do DNA2
# @param v modo verboso

# Uso:
# - move.py -n6 -m7 -v or
# - move.py --dna1 = 6 --dna2 = 7 -v or
# - move.py --help

def main(argv=None):
    if argv is None:
        argv = sys.argv
        n1 = n2 = 0
        debug = True
        try:
            try:
            # Opções , que requeiram um argumento , devem ser
            # seguidas por dois pontos (:).
            # Opções longas , que requeiram um argumento ,
            # devem ser seguidas por um sinal de igual ( '=').
                opts, args=getopt.getopt(argv[1:],"h:n:m:v",\
                    ["help","dna1 = " ,"dna2 = " ,"verbose"])
            except getopt.GetoptError as msg:
                raise ValueError(str(msg))
            # opts é uma lista de opções com pares [( option1 , argument1 ),
            # ( option2 , argument2 )]
            # args é a lista de argumentos de programa que sobra
            # após a lista de opções ser removida ,
            # por exemplo , " move .py -h --help 1 2",
            # faz opts e args serem :
            # [('-h', ''), ('--help ', '')] ['1', '2']
            for opt, arg in opts:   # alguma coisa como [('-h', '')] or
                                    # [('--help ', '')]
                if opt in ( "-h", "--help" ):
                    print("Usage move.py -n1 <DNA1_length>\
                        -n2 <DNA2_length > -v")
                    return 1
                elif opt in ("-n", "--dna1 "):
                    n1 = int(arg)

                elif opt in ("-m", "--dna2 "):
                    n2 = int(arg)

                elif opt in ( "-v", "--verbose " ):
                    debug = True
        except ValueError as err:
            print (str(err) + "\nFor help , type : %s --help " % argv[0])
            return 2

    class GFG(object):
        def __init__(self, master=None, n1=None, n2=None, debug=True):
            self.master = master
            self.master.geometry('600x300+50+50')
            self.master.minsize(600,250)
            self.canvas = Canvas(self.master, bg='lightgray')
            self.canvas.pack()

            self.fonte = 'courier 25 bold'
            self.unid = 20
            self.moveX = int(0)
            self.moveY = int(0)
            self.count = None

            self.barrademenu = Menu(self.master)
            self.btnArquivo = Menu(self.barrademenu, tearoff=0)
            self.btnAjuda = Menu(self.barrademenu, tearoff=0)
            self.barrademenu.add_cascade(label='Arquivo', menu=self.btnArquivo)

            self.barrademenu.add_command(label='Ajuda', command=self.Ajuda)
            self.btnArquivo.add_command(label='Fechar', command=self.Quit)
            
            self.master.config(menu=self.barrademenu)

            self.dna1Texto = 'tcatcgata'
            self.dna2Texto = 'agagcat'

            if n1 or n2:
                self.dna1Texto = self.dna1Texto[:n1]
                self.dna2Texto = self.dna2Texto[:n2]

            if debug:
                self.reset(self)
            
            self.frame = Frame(self.master, width=self.master.winfo_width())
            self.frame.pack()

            self.controleRemoto()
        
        def Quit(self):
            self.master.destroy()
            
        def Ajuda(self):
            msgTexto='Lista de comandos\n\n    1) Você pode usar as setas (diretamente em seu teclado como na barra inferior do aplicativo) para movimentar a fita em todos os lados (cima, baixo, direita, esquerda)\n\n    2) SHIFT + Setas (direita e esquerda) para embaralhar os termos que compõe a fita.\n\n    3) Botão ESC - Encerra a aplicação assim como o botão "Fechar" dentro do botão "Arquivo" na barra de menus.\n\n    4) Ajuda pode ser acionado tanto pelo botão "Ajuda" na barra de menu como tambem pressionando "H" em seu teclado.\n\n    5) Botão "TAB" em seu teclado você reinicia a fita em seu local de origem.\n\n    6) Caso arraste a fita após os limites da janela, automaticamente a fita voltará para seu local de origem.\n\n    7) Ao pressionar o botão "M" em seu teclado ou na parte inferior do aplicativo moverá a fita para o local onde encontrará maior número de casamentos entre seus termos automaticamente.\n\n    8) Na barra inferior você poderá alterar as fitas padrões (ambas ou unitariamente) facilmente escrevendo na barra inferior ( Nesta barra só é permitido a confirmação de caracteres A-T-C-G ) e confirmando com o botão "Confirmar alteração" na parte inferior do aplicativo.'
            msgBox.showinfo(title='Ajuda', message=msgTexto)

        def movimentStrand(self, dna1: str, dna2: str, event: str = 'Right', moveX: int = 0):
            if event == 'Right':
                self.count = DNAStrand(dna1).countMatchesWithRightShift(DNAStrand(dna2), moveX)
                return DNAStrand(dna1).findMatchesWithRightShift(DNAStrand(dna2), moveX)[1], DNAStrand(dna2).findMatchesWithLeftShift(DNAStrand(dna1), moveX)[1]
            if event == 'Left':
                self.count = DNAStrand(dna1).countMatchesWithLeftShift(DNAStrand(dna2), moveX*-1)
                return DNAStrand(dna1).findMatchesWithLeftShift(DNAStrand(dna2), moveX*-1)[1], DNAStrand(dna2).findMatchesWithRightShift(DNAStrand(dna1), moveX*-1)[1]

        def resize(self, event):
            self.canvas.configure(width=self.master.winfo_width(), height=self.master.winfo_height()-60)
            self.canvas.delete('dna', 'limite')
            self.moveX = 0
            self.dna1 = self.canvas.create_text(self.master.winfo_width()//2, self.master.winfo_height()//2, text=self.movimentStrand(self.dna1Texto, self.dna2Texto)[0], font=self.fonte, fill='black', tag='dna')
            self.dna2 = self.canvas.create_text(self.master.winfo_width()//2+self.unid*(len(self.dna2Texto)-len(self.dna1Texto))//2, self.master.winfo_height()//2+32, text=self.movimentStrand(self.dna1Texto, self.dna2Texto)[1], font=self.fonte, fill='black', tag='dna')
            self.coordenada = self.canvas.bbox(self.dna2)
            self.pos_initial = self.canvas.coords(self.dna2)

        def maxMatchesMemory(self, event=None):

            maxCountMatches = None

            loop = max(len(self.dna1Texto), len(self.dna2Texto))
            maxCountMatches = DNAStrand(self.dna1Texto).findMaxPossibleMatches(DNAStrand(self.dna2Texto), loop)
            self.count = maxCountMatches[0]

            if maxCountMatches[2] == 'Left':
                
                self.canvas.coords(self.dna2, self.pos_initial[0]+(self.unid*-maxCountMatches[1]), self.pos_initial[1])
                self.canvas.itemconfig(self.dna1, text=self.movimentStrand(self.dna1Texto, self.dna2Texto, maxCountMatches[2], maxCountMatches[1])[0])
                self.canvas.itemconfig(self.dna2, text=self.movimentStrand(self.dna1Texto, self.dna2Texto, maxCountMatches[2], maxCountMatches[1])[1])
                self.moveX = maxCountMatches[1]
                print(maxCountMatches)

            else:
                
                self.canvas.coords(self.dna2, self.pos_initial[0]+(self.unid*maxCountMatches[1]), self.pos_initial[1])
                self.canvas.itemconfig(self.dna1, text=self.movimentStrand(self.dna1Texto, self.dna2Texto, maxCountMatches[2], maxCountMatches[1])[0])
                self.canvas.itemconfig(self.dna2, text=self.movimentStrand(self.dna1Texto, self.dna2Texto, maxCountMatches[2], maxCountMatches[1])[1])
                self.moveX = maxCountMatches[1]
                print(maxCountMatches)
            
            if debug:
                print('Pressionado "M" para máximo de pareamento')
                self.verbosaMode()

        def verifyClashReset(self):
            x = self.coordenada[2]-self.coordenada[0]-(self.unid*2)
            y = self.coordenada[3]-self.coordenada[1]

            #colisão a esquerda
            if self.canvas.coords(self.dna2)[0] <= (x*-1) or self.canvas.coords(self.dna2)[0] >= self.master.winfo_width()+x:
                self.reset(self)

            #colisão a direita
            if self.canvas.coords(self.dna2)[1] <= (y*-1) or self.canvas.coords(self.dna2)[1] >= self.master.winfo_height()+y:
                self.reset(self)

            if debug:
                self.verbosaMode()

        def verbosaMode(self):
            print('    posx, posy - ({}, {})'.format(self.moveX , self.moveY))
            print('    matches = %d' %self.count)

        # for motion in negative x direction 
        def left(self, event=None):
            self.moveX -= 1
            self.canvas.move(self.dna2, self.unid*-1, 0)
            if self.moveX < 0:
                self.canvas.itemconfig(self.dna1, text=self.movimentStrand(self.dna1Texto, self.dna2Texto, 'Left', self.moveX)[0])
                self.canvas.itemconfig(self.dna2, text=self.movimentStrand(self.dna1Texto, self.dna2Texto, 'Left', self.moveX)[1])
            else:
                self.canvas.itemconfig(self.dna1, text=self.movimentStrand(self.dna1Texto, self.dna2Texto, 'Right', self.moveX)[0])
                self.canvas.itemconfig(self.dna2, text=self.movimentStrand(self.dna1Texto, self.dna2Texto, 'Right', self.moveX)[1])
            
            if debug:
                if event:
                    print(event.keysym)
                else:
                    print('Left')
            self.verifyClashReset()
                
        # for motion in positive x direction 
        def right(self, event=None):
            self.moveX += 1
            self.canvas.move(self.dna2, self.unid, 0)

            if self.moveX > 0:
                self.canvas.itemconfig(self.dna1, text=self.movimentStrand(self.dna1Texto, self.dna2Texto, 'Right', self.moveX)[0])
                self.canvas.itemconfig(self.dna2, text=self.movimentStrand(self.dna1Texto, self.dna2Texto, 'Right', self.moveX)[1])
            else:
                self.canvas.itemconfig(self.dna1, text=self.movimentStrand(self.dna1Texto, self.dna2Texto, 'Left', self.moveX)[0])
                self.canvas.itemconfig(self.dna2, text=self.movimentStrand(self.dna1Texto, self.dna2Texto, 'Left', self.moveX)[1])

            if debug:
                if event:
                    print(event.keysym)
                else:
                    print('Right')
            self.verifyClashReset()

        def shuffler_Right(self, event=None):
            self.resize(self)
            self.dna2Texto = self.dna2Texto[len(self.dna2Texto)-1:] + self.dna2Texto[:len(self.dna2Texto)-1]
            self.canvas.itemconfig(self.dna1, text=self.movimentStrand(self.dna1Texto, self.dna2Texto)[0])
            self.canvas.itemconfig(self.dna2, text=self.movimentStrand(self.dna1Texto, self.dna2Texto)[1])
            if debug:
                print('Shift_R')
            self.reset(self)
        
        def shuffler_Left(self, event=None):
            self.resize(self)
            self.dna2Texto = self.dna2Texto[1:] + self.dna2Texto[0]
            self.canvas.itemconfig(self.dna1, text=self.movimentStrand(self.dna1Texto, self.dna2Texto)[0])
            self.canvas.itemconfig(self.dna2, text=self.movimentStrand(self.dna1Texto, self.dna2Texto)[1])
            if debug:
                print('Shift_L')
            self.reset(self)

        # for motion in positive y direction 
        def up(self, event=None):
            self.moveY -= 1 
            self.canvas.move(self.dna2, 0, self.unid*-3)
            if debug:
                if event:
                    print(event.keysym)
                else:
                    print('Up')
            self.verifyClashReset()

        # for motion in negative y direction 
        def down(self, event=None):
            self.moveY += 1 
            self.canvas.move(self.dna2, 0, self.unid*3)
            if debug:
                if event:
                    print(event.keysym)
                else:
                    print('Down')
            self.verifyClashReset()

        def reset(self, event=None):
            self.resize(self)
            if debug:
                print('reset')
                print('    text box: ', self.canvas.bbox(self.dna1))
                print('    text2 box: ', self.canvas.bbox(self.dna2))

        def controleRemoto(self):
            self.frameLeft = Frame(self.frame,width=self.frame.winfo_width())
            self.frameLeft.pack(side='left')

            self.labelAlteraDNA1 = Label(self.frameLeft, text='Insira a fita (DNA1) desejada: ')
            self.labelAlteraDNA2 = Label(self.frameLeft, text='Insira a fita (DNA2) desejada: ')
            
            self.labelAlteraDNA1.pack()
            self.labelAlteraDNA2.pack()

            self.frameRight = Frame(self.frame, width=self.frame.winfo_width())
            self.frameRight.pack(side='left')

            self.alteraDNA1 = Entry(self.frameRight, width=30)
            self.alteraDNA2 = Entry(self.frameRight, width=30)
            
            self.alteraDNA1.pack()
            self.alteraDNA2.pack()

            def verifyErrorImputText(tempVerifica):
                permitido = set(DNAStrand.symbols)
                tempVerifica = set(self.alteraDNA1.get())
                return tempVerifica.issubset(permitido)

            def btn_confirmado():
                try:
                    if self.alteraDNA1.get() and not self.alteraDNA2.get() and verifyErrorImputText(self.alteraDNA1.get()):
                            self.dna1Texto = self.alteraDNA1.get()
                            self.alteraDNA1.delete(0, 'end')
                    else:
                        raise ValueError
                except ValueError:
                            msgBox.showerror(title='Item inserido não é permitido!', message='Foi inserido o(s) caracteres(s) {} não permitido(s)'.format(tempVerifica.difference(permitido)))
                            self.alteraDNA1.delete(0, 'end')
                            self.alteraDNA2.delete(0, 'end')
                try:
                    if self.alteraDNA2.get() and not self.alteraDNA1.get() and verifyErrorImputText(self.alteraDNA2.get()):
                        self.dna2Texto = self.alteraDNA2.get()
                        self.alteraDNA2.delete(0, 'end')
                    else:
                        raise ValueError
                except ValueError:
                            msgBox.showerror(title='Item inserido não é permitido!', message='Foi inserido o(s) caracteres(s) {} não permitido(s)'.format(tempVerifica.difference(permitido)))
                            self.alteraDNA1.delete(0, 'end')
                            self.alteraDNA2.delete(0, 'end')
                try:
                    if self.alteraDNA1.get() and self.alteraDNA2.get() and verifyErrorImputText(self.alteraDNA1.get()) and verifyErrorImputText(self.alteraDNA2.get()):
                        self.dna1Texto = self.alteraDNA1.get()
                        self.dna2Texto = self.alteraDNA2.get()
                        self.alteraDNA1.delete(0, 'end')
                        self.alteraDNA2.delete(0, 'end')
                    else:
                        raise ValueError
                except ValueError:
                            msgBox.showerror(title='Item inserido não é permitido!', message='Foi inserido o(s) caracteres(s) {} não permitido(s)'.format(tempVerifica.difference(permitido)))
                            self.alteraDNA1.delete(0, 'end')
                            self.alteraDNA2.delete(0, 'end')
                
                self.canvas.itemconfig(self.dna1, text=self.movimentStrand(self.dna1Texto, self.dna2Texto)[0])
                self.canvas.itemconfig(self.dna2, text=self.movimentStrand(self.dna1Texto, self.dna2Texto)[1])

            self.frameBTN = Frame(self.frame)
            self.frameBTN.pack(side='left')

            self.btnConfirmar = Button(self.frameBTN, text='Confirmar alteração', command=btn_confirmado)
            self.btnConfirmar.pack()
            self.btnConfirmar.configure(relief='groove', border='3', font='Times 8 bold')

            self.frameDKeyBTN = Frame(self.frame)
            self.frameDKeyBTN.pack(side='right')

            self.frameDKeyBTNTop = Frame(self.frameDKeyBTN)
            self.frameDKeyBTNTop.pack(side='top')
            
            self.frameDKeyBTNBot = Frame(self.frameDKeyBTN)
            self.frameDKeyBTNBot.pack(side='bottom')

            self.btnShufflerLeft = Button(self.frameDKeyBTNTop, text='◄', command=self.shuffler_Left)
            self.btnShufflerLeft.pack(side='left')
            self.btnTop = Button(self.frameDKeyBTNTop, text='⇧', command=self.up)
            self.btnTop.pack(side='left')
            self.btnShufflerRight = Button(self.frameDKeyBTNTop, text='►', command=self.shuffler_Right)
            self.btnShufflerRight.pack(side='right')
            self.btnRight = Button(self.frameDKeyBTNBot, text='⇨', command=self.right)
            self.btnRight.pack(side='right')
            self.btnLeft = Button(self.frameDKeyBTNBot, text='⇦', command=self.left)
            self.btnLeft.pack(side='left')
            self.btnDown = Button(self.frameDKeyBTNBot, text='⇩', command=self.down)
            self.btnDown.pack(side='bottom')

            self.frameAlternativeBTN = Frame(self.frame)
            self.frameAlternativeBTN.pack(side='right')

            self.btnTAB = Button(self.frameAlternativeBTN, text='TAB', command=self.reset)
            self.btnTAB.pack(side='top',fill='x')
            self.btnMemory = Button(self.frameAlternativeBTN, text='M', command=self.maxMatchesMemory)
            self.btnMemory.pack(side='bottom', fill='x')

            for widget in (self.btnDown, self.btnLeft, self.btnRight, self.btnTop, self.btnShufflerLeft, self.btnShufflerRight, self.btnTAB, self.btnMemory):
                widget.configure(relief='groove', border='3', font='Times 8 bold')

    master = Tk()
    master.title('DNA Strand')
    gfg = GFG(master, n1, n2, debug)
    master.bind('<Configure>', lambda e: gfg.resize(e))
    master.bind('<Up>', lambda e: gfg.up(e))
    master.bind('<Down>', lambda e: gfg.down(e))
    master.bind('<Left>', lambda e: gfg.left(e))
    master.bind('<Right>', lambda e: gfg.right(e))
    master.bind('<Shift-Left>', lambda e: gfg.shuffler_Left(e))
    master.bind('<Shift-Right>', lambda e: gfg.shuffler_Right(e))
    master.bind('<Key-m>', lambda e: gfg.maxMatchesMemory(e))
    master.bind('<Key-h>', lambda e: gfg.Ajuda())
    master.bind('<Escape>', lambda e: gfg.Quit())
    master.bind('<Tab>', lambda e: gfg.reset(e))
    master.mainloop()

if __name__ == "__main__":
    main()
