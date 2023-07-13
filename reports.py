from tkinter import StringVar, ttk, Canvas

class Reports():
    def __init__(self,titlescreen,window):
        self.titlescreen = titlescreen
        self.window = window
        self.connection = window.connection
        self.rootframe = ttk.Frame(self.window.window)
        self.reportsArea = Canvas(self.rootframe)

        self.rootframe.grid(sticky="nsew")
        x,y = self.window.window.minsize(None)
        window.split(self.rootframe,20,50,x//20,y//50)

        self.reportsArea.grid(row=1,column=1,rowspan=42,columnspan=17,
                              sticky='nsew')
        self.reportsFrame = ttk.Frame()
        vScrollbar = ttk.Scrollbar(self.rootframe,command=self.reportsArea.yview)
        vScrollbar.grid(row=7,column=18,rowspan=37,columnspan=1,sticky="ns")
        hScrollbar = ttk.Scrollbar(self.rootframe,orient='horizontal',
                                   command=self.reportsArea.xview)
        hScrollbar.grid(row=43,column=1,rowspan=1,columnspan=17,sticky='ew')
        self.reportsArea.configure(yscrollcommand=vScrollbar.set,
                                   xscrollcommand=hScrollbar.set)
        backB = ttk.Button(self.rootframe,command=self.back,text="Voltar",
                           style="options.TButton")
        backB.grid(row=45,column=15,rowspan=4,columnspan=4,sticky="nsew")

        self.rootframe.grid_remove()

    def setReports(self,ratings=None,level=0):
        if ratings is None:
            if self.reportsFrame:
                self.reportsFrame.destroy()
            self.reportsFrame = ttk.Frame(self.reportsArea)
            self.reportsArea.create_window((0,0),window=self.reportsFrame,
                                           anchor='nw')
            ratings = self.connection.getReports()
        if ratings:
            info = ratings.pop()
            report = ttk.Frame(self.reportsFrame)
            ignoreB = ttk.Button(report,text='Ignorar',
                                 style="smallOptions.TButton",
                                 command=lambda:self.ignore(info))
            deleteB = ttk.Button(report,text='Excluir conta de usuário',
                                 style="smallOptions.TButton",
                                 command=lambda:self.delete(info))
            if self.matricula == info[9]:
                deleteB.state(['disabled'])
            user = f"Usuário {info[0]}, {info[9]}"
            turma = f"{info[1]}: {info[2]}, turma {info[3]}, {info[5]}"
            userL = ttk.Label(report,text=user,style="grade.TLabel")
            turmaL = ttk.Label(report,text=turma,style="grade.TLabel")
            teacherL = ttk.Label(report,text=info[4],style="grade.TLabel")
            maxLen = max(len(user),len(turma),len(info[4]))
            gradeL = ttk.Label(report,text=f'Nota: {info[7]}',
                               style="grade.TLabel")
            i, r = 0, 3
            while i < len(info[1]):
                j = len(info[8]) if len(info[8]) - i <= 15 else i + maxLen
                text = f'{"Descrição: " if i == 0 else ""}{info[8][i:j]}'
                textL = ttk.Label(report,text=text,
                                  style="ratings.TLabel")
                textL.grid(row=r,column=1,sticky='nsw')
                i += maxLen
                r += 1
            userL.grid(row=0,column=0,columnspan=2,sticky='nsw')
            turmaL.grid(row=1,column=0,columnspan=2,sticky='nsw')
            teacherL.grid(row=2,column=0,columnspan=2,sticky='nsw')
            gradeL.grid(row=3,column=0,sticky='nse')
            ignoreB.grid(row=r,column=0,sticky='nse')
            deleteB.grid(row=r,column=1,sticky='nsw')
            report.pack(anchor='w')
            self.setReports(ratings,level=level+1)
        if level == 0:
            self.reportsArea.yview_moveto(0)
            self.reportsArea.xview_moveto(0)
            self.rootframe.update_idletasks()
            self.reportsArea.config(scrollregion=self.reportsArea.bbox("all"))

    def scroll(self,event):
        if event.state == 0:
            self.reportsArea.yview_scroll(-(event.delta//120),'units')
        elif event.state == 1:
            self.reportsArea.xview_scroll(-(event.delta//120),'units')

    def ignore(self,info):
        self.connection.deleteReport(info[9],info[6],info[1],info[3],info[5])
        self.setReports()

    def delete(self,info):
        self.connection.deleteUser(info[9])
        self.setReports()

    def display(self,fromS,matricula):
        self.fromS = fromS
        self.matricula = matricula
        self.rootframe.grid()
        self.setReports()
        c = self.reportsArea
        c.bind("<Enter>",lambda e:c.bind_all("<MouseWheel>",self.scroll))
        c.bind("<Leave>",lambda e:c.unbind_all("<MouseWheel>"))

    def back(self):
        self.rootframe.grid_remove()
        self.fromS.display()