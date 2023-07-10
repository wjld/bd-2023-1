from tkinter import ttk
from ranking import Ranking

class Titlescreen():
    def __init__(self,window):
        self.window = window
        self.titleframe = ttk.Frame(self.window.window)
        self.ranking = Ranking(self,window)

        self.titleframe.grid(sticky="nsew")
        x,y = self.window.window.minsize(None)
        self.window.split(self.titleframe,20,50,x//20,y//50)
        self.setWidgets()

    def setWidgets(self):
        title1 = ttk.Label(self.titleframe,text="Avaliação de",
                          style="title.TLabel")
        title2 = ttk.Label(self.titleframe,text="Professores",
                          style="title.TLabel")
        title3 = ttk.Label(self.titleframe,text="e Disciplinas",
                          style="title.TLabel")
        signUpB = ttk.Button(self.titleframe,command=lambda:None,
                              text="Cadastro",style="options.TButton")
        signInB = ttk.Button(self.titleframe,command=lambda:None,
                               text="Entrar",style="options.TButton")
        rankingB = ttk.Button(self.titleframe,command=self.rankingScreen,
                                  text="Ranking geral",style="options.TButton")
        quitB = ttk.Button(self.titleframe,command=self.quit,text="Sair",
                           style="options.TButton")

        title1.grid(row=2,column=1,rowspan=5,columnspan=18)
        title2.grid(row=7,column=1,rowspan=5,columnspan=18)
        title3.grid(row=12,column=1,rowspan=5,columnspan=18)
        signUpB.grid(row=25,column=5,rowspan=4,columnspan=10,sticky="nsew")
        signInB.grid(row=30,column=5,rowspan=4,columnspan=10,sticky="nsew")
        rankingB.grid(row=35,column=5,rowspan=4,columnspan=10,sticky="nsew")
        quitB.grid(row=40,column=5,rowspan=4,columnspan=10,sticky="nsew")

        signInB.bind("<Visibility>",self.hasAdmins)

    def hasAdmins(self, event):
        if self.window.connection.hasAdmins():
            event.widget.state(["!disabled"])
        else:
            event.widget.state(["disabled"])

    def display(self):
        self.titleframe.grid()

    def rankingScreen(self):
        self.titleframe.grid_remove()
        self.ranking.display()

    def quit(self):
        self.window.destroy()