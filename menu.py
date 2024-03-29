from tkinter import ttk
from rate import RateScreen
from reports import Reports
from setAdmins import SetAdmins

class Menu():
    def __init__(self,titlescreen,window):
        self.titlescreen = titlescreen
        self.ranking = self.titlescreen.ranking
        self.rate = RateScreen(titlescreen,window)
        self.reportsScreen = Reports(titlescreen,window)
        self.setAdminsScreen = SetAdmins(titlescreen,window)
        self.window = window
        self.connection = window.connection
        self.frame = ttk.Frame(self.window.window)
        self.userInfo: tuple[str,...]
        self.commonOptions = []
        self.adminOptions = []

        self.frame.grid(sticky="nsew")
        x,y = self.window.window.minsize(None)
        window.split(self.frame,20,50,x//20,y//50)

        self.setWidgets()
        self.frame.grid_remove()

    def setWidgets(self):
        title = ttk.Label(self.frame,text="Bem vindo,",style="title.TLabel")
        self.userLabel = ttk.Label(self.frame,text="",style="title.TLabel")
        rateClassB = ttk.Button(self.frame,command=lambda:self.rateScreen(0),
                                text="Fazer avaliação",style="options.TButton")
        myRatingsB = ttk.Button(self.frame,command=lambda:self.rateScreen(1),
                                text="Minhas avaliações",
                                style="options.TButton")
        rankingB = ttk.Button(self.frame,command=self.rankingScreen,
                                  text="Ranking geral",style="options.TButton")
        viewRatB = ttk.Button(self.frame,command=lambda:self.rateScreen(2),
                                  text="Ver avaliações",
                                  style="options.TButton")
        adminOptB = ttk.Button(self.frame,command=self.showAdminOpt,
                                  text="Opções de administrador",
                                  style="options.TButton")
        addTeaB = ttk.Button(self.frame,command=lambda:None,
                                   text="Adicionar professores",
                                   style="options.TButton")
        addClassB = ttk.Button(self.frame,command=lambda:None,
                                   text="Adicionar turmas",
                                   style="options.TButton")
        reviewRepB = ttk.Button(self.frame,command=self.reviewReports,
                                   text="Analisar denúncias",
                                   style="options.TButton")
        setAdminsB = ttk.Button(self.frame,command=self.setAdmins,
                                   text="Configurar administradores",
                                   style="options.TButton")
        quitB = ttk.Button(self.frame,command=self.quit,text="Sair",
                           style="options.TButton")
        self.commonOptions = [rateClassB,myRatingsB,rankingB,viewRatB]
        self.adminOptions = [adminOptB,addTeaB,addClassB,reviewRepB,setAdminsB]

        title.grid(row=2,column=1,rowspan=5,columnspan=18)
        self.userLabel.grid(row=7,column=1,rowspan=5,columnspan=18)
        rateClassB.grid(row=15,column=3,rowspan=4,columnspan=14,sticky="nsew")
        myRatingsB.grid(row=20,column=3,rowspan=4,columnspan=14,sticky="nsew")
        rankingB.grid(row=25,column=3,rowspan=4,columnspan=14,sticky="nsew")
        viewRatB.grid(row=30,column=3,rowspan=4,columnspan=14,sticky="nsew")
        adminOptB.grid(row=35,column=3,rowspan=4,columnspan=14,sticky="nsew")
        addTeaB.grid(row=15,column=3,rowspan=4,columnspan=14,sticky="nsew")
        addClassB.grid(row=20,column=3,rowspan=4,columnspan=14,sticky="nsew")
        reviewRepB.grid(row=25,column=3,rowspan=4,columnspan=14,sticky="nsew")
        setAdminsB.grid(row=30,column=3,rowspan=4,columnspan=14,sticky="nsew")
        quitB.grid(row=45,column=1,rowspan=4,columnspan=4,sticky="nsew")
        for option in self.adminOptions:
            option.grid_remove()

    def rankingScreen(self):
        self.frame.grid_remove()
        self.ranking.display(self)

    def rateScreen(self,n):
        self.frame.grid_remove()
        if n == 0:
            self.rate.display(self,'search')
        elif n == 1:
            self.rate.display(self,'view')
        elif n == 2:
            self.rate.display(self,'view others')

    def reviewReports(self):
        self.frame.grid_remove()
        self.reportsScreen.display(self,self.userInfo[0])

    def setAdmins(self):
        self.frame.grid_remove()
        self.setAdminsScreen.display(self)

    def display(self,userInfo=None):
        if userInfo:
            self.userInfo = userInfo
            self.userLabel.config(text=userInfo[2])
            if userInfo[6]:
                self.adminOptions[0].grid()
        self.frame.grid()
    
    def showAdminOpt(self):
        self.adminOptions : list[ttk.Button]
        if self.adminOptions[1].winfo_viewable():
            for option in self.adminOptions[1:]:
                option.grid_remove()
            for option in self.commonOptions:
                option.grid()
            self.adminOptions[0].configure(text='Opções de administrador')
        else:
            for option in self.commonOptions:
                option.grid_remove()
            for option in self.adminOptions:
                option.grid()
            self.adminOptions[0].configure(text='Opções comuns')

    def quit(self):
        self.frame.grid_remove()
        self.titlescreen.display()