from tkinter import ttk, Canvas, StringVar
from dialog import Dialog

class RateScreen:
    def __init__(self,titlescreen,window):
        self.titlescreen = titlescreen
        self.window = window
        self.connection = window.connection
        self.rootframe = ttk.Frame(self.window.window)
        self.searchArea = Canvas(self.rootframe)

        self.selectSemesterVal = StringVar(self.window.window,
                                           self.connection.getSemester()[0])

        self.rootframe.grid(sticky="nsew")
        x,y = self.window.window.minsize(None)
        window.split(self.rootframe,45,60,x//45,y//60)

        self.searchTerm = ttk.Entry(self.rootframe,exportselection=False,
                               justify="center")
        self.searchB = ttk.Button(self.rootframe,command=self.setSResults,
                                  text="Buscar",style="options.TButton")
        self.searchArea.grid(row=7,column=1,rowspan=45,columnspan=42,
                              sticky='nsew')
        self.searchFrame = ttk.Frame(self.searchArea)
        self.searchArea.create_window((0,0),window=self.searchFrame,anchor='nw')
        vScrollbar = ttk.Scrollbar(self.rootframe,command=self.searchArea.yview)
        vScrollbar.grid(row=7,column=43,rowspan=47,columnspan=1,sticky="ns")
        hScrollbar = ttk.Scrollbar(self.rootframe,orient='horizontal',
                                   command=self.searchArea.xview)
        hScrollbar.grid(row=52,column=1,rowspan=2,columnspan=42,sticky='ew')
        self.searchArea.configure(yscrollcommand=vScrollbar.set,
                                   xscrollcommand=hScrollbar.set)
        self.searchArea.bind_all("<MouseWheel>",self.scroll)

        self.setWidgets()
        self.rootframe.grid_remove()

    def setWidgets(self):
        selectSemester = ttk.Combobox(self.rootframe,justify="center",
                                  state="readonly",width=5,
                                  textvariable=self.selectSemesterVal,
                                  values=self.connection.getSemester())
        backB = ttk.Button(self.rootframe,command=self.back,text="Voltar",
                           style="options.TButton")

        self.searchTerm.grid(row=2,column=1,rowspan=4,columnspan=20,
                             sticky="nsew")
        self.searchB.grid(row=2,column=22,rowspan=4,columnspan=9,sticky="nsew")
        selectSemester.grid(row=2,column=35,rowspan=4,columnspan=9,
                            sticky="nsew")
        backB.grid(row=55,column=35,rowspan=4,columnspan=9,sticky="nsew")
        self.searchTerm.event_add('<<entryFont>>','<Configure>','<Visibility>')
        self.searchTerm.bind("<<entryFont>>",self.window.entryFont,add=True)
        self.searchTerm.bind('<Return>',lambda e:self.setSResults())
        selectSemester.event_add('<<comboFont>>','<Configure>','<Visibility>')
        selectSemester.bind("<<ComboboxSelected>>",lambda e:self.setSResults())
        selectSemester.bind("<<comboFont>>",self.window.comboFont,add=True)

    def setSResults(self,results=None,level=0):
        if results is None:
            for frame in self.searchFrame.winfo_children():
                frame.destroy()
            if self.operation == 'search':
                self.searchTerm.grid()
                self.searchB.grid()
                results = self.connection.search(self.searchTerm.get()[:150],
                                                 self.selectSemesterVal.get())
            elif self.operation == 'view':
                self.searchTerm.grid_remove()
                self.searchB.grid_remove()
                results = self.connection.viewOwn(self.fromS.userInfo[0],
                                                  self.selectSemesterVal.get())
        self.manageResults(results,level)
        if level == 0:
            self.searchArea.yview_moveto(0)
            self.searchArea.xview_moveto(0)
            self.rootframe.update_idletasks()
            self.searchArea.config(scrollregion=self.searchArea.bbox("all"))
            c = self.searchArea
            c.bind("<Enter>",lambda e:c.bind_all("<MouseWheel>",self.scroll))
            c.bind("<Leave>",lambda e:c.unbind_all("<MouseWheel>"))

    def manageResults(self,results,level):
        if results:
            info = results.pop()
            result = ttk.Frame(self.searchFrame)
            classText = f'{info[0]}: {info[1]}, turma {info[2]}'
            action = 'Avaliar' if self.operation == 'search' else 'Editar'
            rateB = ttk.Button(result,command=lambda:self.rateDialog(info),
                               text=action,style="smallOptions.TButton")
            classL = ttk.Label(result,text=classText,style="ratings.TLabel")
            teacherL = ttk.Label(result,text=info[3],style="ratings.TLabel")
            rateB.grid(row=0,column=0,rowspan=2)
            if (self.operation == 'search'
                and self.window.connection.rated(self.fromS.userInfo[0],info)):
                rateB.state(['disabled'])
            if self.operation == 'view':
                gradeL = ttk.Label(result,text=f'Nota: {info[6]}',
                                   style="grade.TLabel")
                gradeL.grid(row=2,column=0,sticky='nse')
                maxLen = max(len(classText),len(info[3]))
                i, r = 0, 2
                while i < len(info[7]):
                    j = len(info[7]) if len(info[7]) - i <= 15 else i + maxLen
                    text = f'{"Descrição: " if i == 0 else ""}{info[7][i:j]}'
                    textL = ttk.Label(result,text=text,style="ratings.TLabel")
                    textL.grid(row=r,column=1,sticky='nsw')
                    i += maxLen
                    r += 1
            classL.grid(row=0,column=1,sticky='nsw')
            teacherL.grid(row=1,column=1,sticky='nsw')
            result.pack(anchor='w')
            self.setSResults(results,level=level+1) if results else None
        elif results is not None:
            result = ttk.Frame(self.searchFrame)
            empty = ''
            if self.operation == 'search':
                empty = f'Sem resultados para "{self.searchTerm.get()}".'
            elif self.operation == 'view':
                empty = f'Ainda não há avaliações.'
            emptyL = ttk.Label(result,text=empty,style="ratings.TLabel")
            emptyL.pack()
            result.pack(anchor='w')

    def rateDialog(self,info):
        if self.operation == 'search':
            self.searchTerm.focus()
        elif self.operation == 'view':
            self.window.window.focus()
        Dialog(self,info)

    def scroll(self,event):
        if event.state == 0:
            self.searchArea.yview_scroll(-(event.delta//120),'units')
        elif event.state == 1:
            self.searchArea.xview_scroll(-(event.delta//120),'units')

    def display(self,fromS,op):
        self.fromS = fromS
        self.operation = op
        self.rootframe.grid()
        self.setSResults()

    def back(self):
        self.searchTerm.delete(0,'end')
        for frame in self.searchFrame.winfo_children():
            frame.destroy()
        self.rootframe.grid_remove()
        self.fromS.display()