from tkinter import ttk

class Menu():
    def __init__(self,titlescreen,window):
        self.titlescreen = titlescreen
        self.ranking = self.titlescreen.ranking
        self.window = window
        self.connection = window.connection
        self.frame = ttk.Frame(self.window.window)
        self.userInfo: tuple[str,...]
        self.fields = []

        self.frame.grid(sticky="nsew")
        x,y = self.window.window.minsize(None)
        window.split(self.frame,20,50,x//20,y//50)

        self.setWidgets()
        self.frame.grid_remove()

    def setWidgets(self):
        title1 = ttk.Label(self.frame,text="Bem vindo,",
                          style="title.TLabel")
        self.userLabel = ttk.Label(self.frame,text="",
                          style="title.TLabel")
        rateDisB = ttk.Button(self.frame,command=lambda:None,
                              text="Avaliar Disciplinas",
                              style="options.TButton")
        rateTeaB = ttk.Button(self.frame,command=lambda:None,
                               text="Avaliar Professores",
                               style="options.TButton")
        myRatingsB = ttk.Button(self.frame,command=lambda:None,
                                  text="Minhas avaliações",
                                  style="options.TButton")
        rankingB = ttk.Button(self.frame,command=self.rankingScreen,
                                  text="Ranking geral",style="options.TButton")
        quitB = ttk.Button(self.frame,command=self.quit,text="Sair",
                           style="options.TButton")

        title1.grid(row=2,column=1,rowspan=5,columnspan=18)
        self.userLabel.grid(row=7,column=1,rowspan=5,columnspan=18)
        rateDisB.grid(row=18,column=5,rowspan=4,columnspan=10,sticky="nsew")
        rateTeaB.grid(row=23,column=5,rowspan=4,columnspan=10,sticky="nsew")
        myRatingsB.grid(row=28,column=5,rowspan=4,columnspan=10,sticky="nsew")
        rankingB.grid(row=33,column=5,rowspan=4,columnspan=10,sticky="nsew")
        quitB.grid(row=45,column=1,rowspan=4,columnspan=4,sticky="nsew")

    def rankingScreen(self):
        self.frame.grid_remove()
        self.ranking.display(self)

    def display(self,userInfo=None):
        if userInfo:
            self.userInfo = userInfo
            self.userLabel.config(text=self.userInfo[2])
        self.frame.grid()

    def quit(self):
        self.frame.grid_remove()
        self.titlescreen.display()