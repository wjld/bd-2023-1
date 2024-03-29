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

        self.rankingArea.grid(row=7,column=1,rowspan=36,columnspan=17,
                              sticky='nsew')
        self.rankingFrame = ttk.Frame()
        vScrollbar = ttk.Scrollbar(self.rootframe,command=self.rankingArea.yview)
        vScrollbar.grid(row=7,column=18,rowspan=37,columnspan=1,sticky="ns")
        hScrollbar = ttk.Scrollbar(self.rootframe,orient='horizontal',
                                   command=self.rankingArea.xview)
        hScrollbar.grid(row=43,column=1,rowspan=1,columnspan=17,sticky='ew')
        self.rankingArea.configure(yscrollcommand=vScrollbar.set,
                                   xscrollcommand=hScrollbar.set)

        self.setWidgets()
        self.rootframe.grid_remove()

    def setWidgets(self):
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

        type.grid(row=2,column=2,rowspan=4,columnspan=4,sticky="nsew")
        orderScore.grid(row=2,column=8,rowspan=4,columnspan=4,sticky="nsew")
        selectSemester.grid(row=2,column=14,rowspan=4,columnspan=4,
                           sticky="nsew")
        backB.grid(row=45,column=15,rowspan=4,columnspan=4,sticky="nsew")
        type.event_add('<<comboFont>>','<Configure>','<Visibility>')
        orderScore.event_add('<<comboFont>>','<Configure>','<Visibility>')
        selectSemester.event_add('<<comboFont>>','<Configure>','<Visibility>')
        type.bind("<<ComboboxSelected>>",lambda e:self.setRanking())
        orderScore.bind("<<ComboboxSelected>>",lambda e:self.setRanking())
        selectSemester.bind("<<ComboboxSelected>>",lambda e:self.setRanking())
        type.bind("<<ComboboxSelected>>",lambda e:self.window.window.focus(),
                  add=True)
        orderScore.bind("<<ComboboxSelected>>",
                        lambda e:self.window.window.focus(),add=True)
        selectSemester.bind("<<ComboboxSelected>>",
                        lambda e:self.window.window.focus(),add=True)
        type.bind("<<comboFont>>",self.window.comboFont,add=True)
        orderScore.bind("<<comboFont>>",self.window.comboFont,add=True)
        selectSemester.bind("<<comboFont>>",self.window.comboFont,add=True)

    def setRanking(self,ratings=None,level=0):
        if ratings is None:
            if self.rankingFrame:
                self.rankingFrame.destroy()
            self.rankingFrame = ttk.Frame(self.rankingArea)
            self.rankingArea.create_window((0,0),window=self.rankingFrame,
                                           anchor='nw')
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
            self.setRanking(ratings,level=level+1)
        if level == 0:
            self.rankingArea.yview_moveto(0)
            self.rankingArea.xview_moveto(0)
            self.rootframe.update_idletasks()
            self.rankingArea.config(scrollregion=self.rankingArea.bbox("all"))

    def scroll(self,event):
        if event.state == 0:
            self.rankingArea.yview_scroll(-(event.delta//120),'units')
        elif event.state == 1:
            self.rankingArea.xview_scroll(-(event.delta//120),'units')

    def display(self,fromS):
        self.fromS = fromS
        self.rootframe.grid()
        self.setRanking()
        c = self.rankingArea
        c.bind("<Enter>",lambda e:c.bind_all("<MouseWheel>",self.scroll))
        c.bind("<Leave>",lambda e:c.unbind_all("<MouseWheel>"))

    def back(self):
        self.rootframe.grid_remove()
        self.fromS.display()