from tkinter import StringVar, ttk, Canvas

class Ranking():
    def __init__(self,titlescreen,window):
        self.titlescreen = titlescreen
        self.window = window
        self.connection = window.connection
        self.rootframe = ttk.Frame(self.window.window)
        self.rankingArea = Canvas(self.rootframe)

        self.ratings = []
        self.typeVal = StringVar(self.window.window,"Turmas")
        self.orderVal = StringVar(self.window.window,"Nota ▾")
        self.selectSemesterVal = StringVar(self.window.window,
                                          self.connection.getSemester()[0])

        self.rootframe.grid(sticky="nsew")
        x,y = self.window.window.minsize(None)
        window.split(self.rootframe,20,50,x//20,y//50)

        self.rankingArea.grid(row=12,column=1,rowspan=31,columnspan=17,
                              sticky='nsew')
        self.rankingFrame = ttk.Frame(self.rankingArea)
        self.rankingArea.create_window((0,0),window=self.rankingFrame,anchor='nw')
        vScrollbar = ttk.Scrollbar(self.rootframe,command=self.rankingArea.yview)
        vScrollbar.grid(row=12,column=18,rowspan=32,columnspan=1,sticky="ns")
        hScrollbar = ttk.Scrollbar(self.rootframe,orient='horizontal',
                                   command=self.rankingArea.xview)
        hScrollbar.grid(row=43,column=1,rowspan=1,columnspan=17,sticky='ew')
        self.rankingArea.configure(yscrollcommand=vScrollbar.set,
                                   xscrollcommand=hScrollbar.set)
        self.rankingArea.bind_all("<MouseWheel>",self.scroll)

        self.setWidgets()
        self.rootframe.grid_remove()

    def setWidgets(self):
        title = ttk.Label(self.rootframe,text="Ranking",style="title.TLabel")
        type = ttk.Combobox(self.rootframe,justify="center",state="readonly",
                            values=["Turmas","Professores"],width=5,
                            textvariable=self.typeVal)
        orderScore = ttk.Combobox(self.rootframe,justify="center",
                                  state="readonly",values=["Nota ▴","Nota ▾"],
                                  width=5,textvariable=self.orderVal)
        selectSemester = ttk.Combobox(self.rootframe,justify="center",
                                  state="readonly",width=5,
                                  textvariable=self.selectSemesterVal,
                                  values=self.connection.getSemester())
        backB = ttk.Button(self.rootframe,command=self.back,text="Voltar",
                           style="options.TButton")

        title.grid(row=1,column=3,rowspan=5,columnspan=14)
        type.grid(row=7,column=2,rowspan=4,columnspan=4,sticky="nsew")
        orderScore.grid(row=7,column=8,rowspan=4,columnspan=4,sticky="nsew")
        selectSemester.grid(row=7,column=14,rowspan=4,columnspan=4,
                           sticky="nsew")
        backB.grid(row=45,column=15,rowspan=4,columnspan=4,sticky="nsew")
        type.event_add('<<comboFont>>','<Configure>','<Visibility>')
        orderScore.event_add('<<comboFont>>','<Configure>','<Visibility>')
        selectSemester.event_add('<<comboFont>>','<Configure>','<Visibility>')
        type.bind("<<ComboboxSelected>>",lambda e:self.displayRanking())
        orderScore.bind("<<ComboboxSelected>>",lambda e:self.displayRanking())
        selectSemester.bind("<<ComboboxSelected>>",
                           lambda e:self.displayRanking())
        type.bind("<<ComboboxSelected>>",lambda e:self.window.window.focus(),
                  add=True)
        orderScore.bind("<<ComboboxSelected>>",
                        lambda e:self.window.window.focus(),add=True)
        selectSemester.bind("<<ComboboxSelected>>",
                        lambda e:self.window.window.focus(),add=True)
        type.bind("<<comboFont>>",lambda e:self.comboFont(e.widget,
                        *self.window.proportionalSize),add=True)
        orderScore.bind("<<comboFont>>",lambda e:self.comboFont(e.widget,
                        *self.window.proportionalSize),add=True)
        selectSemester.bind("<<comboFont>>",lambda e:self.comboFont(e.widget,
                        *self.window.proportionalSize),add=True)
        self.setRanking()

    def setRanking(self,ratings=None):
        if ratings is None:
            order = 'desc' if self.orderVal.get() == "Nota ▾" else 'asc'
            ratings = self.connection.avg(order,self.typeVal.get(),
                                          self.selectSemesterVal.get())
        if ratings:
            grade,*name = ratings.pop()
            if len(name) == 2:
                rating = f"{grade:04.2f} - {name[0]} {name[1]}"
            else:
                rating = f"{grade:04.2f} - {name[0]}: {name[1]}, turma {name[2]}"
            rating = ttk.Label(self.rankingFrame,text=rating,
                              style="ratings.TLabel")
            self.ratings.append(rating)
            rating.pack(anchor='w')
            self.setRanking(ratings)

    def displayRanking(self,ratings=None,x=0):
        if ratings is None:
            order = 'desc' if self.orderVal.get() == "Nota ▾" else 'asc'
            ratings = self.connection.avg(order,self.typeVal.get(),
                                          self.selectSemesterVal.get())
        if ratings:
            grade,*name = ratings.pop()
            if len(name) == 2:
                rating = f"{grade:04.2f} - {name[0]} {name[1]}"
            else:
                rating = f"{grade:04.2f} - {name[0]}: {name[1]}, turma {name[2]}"
            self.ratings[x].configure(text=rating)
            self.displayRanking(ratings,x+1)
        if ratings == []:
            self.rankingArea.yview_moveto(0)
            self.rankingArea.xview_moveto(0)
            self.rootframe.update_idletasks()
            self.rankingArea.config(scrollregion=self.rankingArea.bbox("all"))

    def scroll(self,event):
        if event.state == 0:
            self.rankingArea.yview_scroll(-(event.delta//120),'units')
        elif event.state == 1:
            self.rankingArea.xview_scroll(-(event.delta//120),'units')

    def comboFont(self,comboBox,x,y):
        comboBox.configure(font=("Roboto",int(-y*0.04)))

    def display(self,fromS):
        self.fromS = fromS
        self.rootframe.grid()
        self.displayRanking()

    def back(self):
        self.rootframe.grid_remove()
        self.fromS.display()