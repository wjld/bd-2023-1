from tkinter import ttk, Toplevel, StringVar, Text, Canvas
from validate import avaTexto

class Dialog():
    def __init__(self,searchS,info,format):
        self.searchS = searchS
        self.window = searchS.window
        self.connection = self.window.connection
        self.dialog = Toplevel()
        self.dialog.grab_set()
        x = self.window.window.winfo_width()
        y = self.window.window.winfo_height()
        size = self.window.proportionalSize[1]//2
        xOffset = self.window.window.winfo_x()+(x//2)-(int(1.5*size)//2)
        yOffset = self.window.window.winfo_y()+(y//2)-(size//2)
        self.dialog.minsize(int(1.5*size),size)
        self.dialog.geometry(f"+{xOffset}+{yOffset}")
        self.dialog.rowconfigure(0,weight=1)
        self.dialog.columnconfigure(0,weight=1)

        frame = ttk.Frame(self.dialog)
        self.info = info
        self.matricula = searchS.fromS.userInfo[0]
        self.op = searchS.operation
        frame.grid(sticky="nsew")
        self.window.split(frame,30,45,int(1.5*size)//30,size//45)
        if format == 'single':
            initGrade = '5' if self.op == 'search' else str(info[6])
            self.gradeVal = StringVar(frame,initGrade)
            self.setWidgets(info,frame)
        else:
            self.setRatings(info,frame)

    def setWidgets(self,info,frame):
        self.dialog.focus()
        title1 = f'Avaliando {info[0]}, turma {info[2]}, {info[4]}'
        title1L = ttk.Label(frame,text=title1,style='dialog.TLabel')
        title2L = ttk.Label(frame,text=info[3],style='dialog.TLabel')
        gradeL = ttk.Label(frame,text='Nota:',style='dialog.TLabel')
        grade = ttk.Combobox(frame,justify="center",state="readonly",width=3,
                             textvariable=self.gradeVal,
                             values=['5','4','3','2','1','0'])
        textL = ttk.Label(frame,text='Descrição: ',style='dialog.TLabel')
        self.text = Text(frame,height=1,width=1,wrap='char',
                         exportselection=False)
        if self.op == 'view':
            self.text.insert('1.0',info[7])
        doneB = ttk.Button(frame,command=self.recordRating,text="Pronto",
                           style="smallOptions.TButton")
        backB = ttk.Button(frame,command=self.dialog.destroy,
                           text="Voltar",style="smallOptions.TButton")

        title1L.grid(row=2,column=1,rowspan=4,columnspan=28,sticky="nsew")
        title2L.grid(row=7,column=1,rowspan=4,columnspan=28,sticky="nsew")
        gradeL.grid(row=12,column=1,rowspan=4,columnspan=6,sticky="nsew")
        grade.grid(row=12,column=8,rowspan=4,columnspan=6,sticky="nsew")
        textL.grid(row=17,column=1,rowspan=4,columnspan=28,sticky="nsew")
        self.text.grid(row=22,column=1,rowspan=16,columnspan=28,sticky="nsew")
        doneB.grid(row=39,column=6,rowspan=5,columnspan=8,sticky="nsew")
        backB.grid(row=39,column=16,rowspan=5,columnspan=8,sticky="nsew")
        fontEvent = '<<font>>','<Configure>','<Visibility>'
        self.text.event_add(*fontEvent)
        grade.event_add(*fontEvent)
        self.text.bind("<<font>>",self.widFont,add=True)
        self.text.bind('<KeyPress>',self.limitInput)
        self.text.bind('<KeyRelease>',self.limitInput)
        grade.bind("<<font>>",self.widFont,add=True)
        grade.bind("<<ComboboxSelected>>",lambda e:self.dialog.focus())

    def setRatings(self,info,frame):
        self.dialog.focus()
        title1 = f'Visualizando {info[0]}, turma {info[2]}, {info[4]}'
        title1L = ttk.Label(frame,text=title1,style='dialog.TLabel')
        title2L = ttk.Label(frame,text=info[3],style='dialog.TLabel')
        self.maxLen = max(len(title1),len(info[3]))
        backB = ttk.Button(frame,command=self.dialog.destroy,
                           text="Voltar",style="smallOptions.TButton")
        ratingsArea = Canvas(frame)
        avalFrame = ttk.Frame(ratingsArea)
        ratingsArea.create_window((0,0),window=avalFrame,anchor='nw')
        vScrollbar = ttk.Scrollbar(frame,command=ratingsArea.yview)
        hScrollbar = ttk.Scrollbar(frame,orient='horizontal',
                                   command=ratingsArea.xview)
        ratingsArea.configure(yscrollcommand=vScrollbar.set,
                                   xscrollcommand=hScrollbar.set)

        title1L.grid(row=2,column=1,rowspan=4,columnspan=28,sticky="nsew")
        title2L.grid(row=7,column=1,rowspan=4,columnspan=28,sticky="nsew")
        ratingsArea.grid(row=12,column=1,rowspan=24,columnspan=27,sticky='nsew')
        vScrollbar.grid(row=12,column=28,rowspan=26,columnspan=1,sticky="ns")
        hScrollbar.grid(row=36,column=1,rowspan=2,columnspan=27,sticky='ew')
        backB.grid(row=39,column=16,rowspan=5,columnspan=8,sticky="nsew")

        self.displayRankings(self.connection.getAval(info),avalFrame)

        ratingsArea.yview_moveto(0)
        ratingsArea.xview_moveto(0)
        frame.update_idletasks()
        ratingsArea.config(scrollregion=ratingsArea.bbox("all"))
        self.c = ratingsArea
        self.c.bind("<Enter>",lambda e:self.c.bind_all("<MouseWheel>",
                                                       self.scroll))
        self.c.bind("<Leave>",lambda e:self.c.unbind_all("<MouseWheel>"))
    
    def displayRankings(self,results,avalFrame):
        if results:
            info = results.pop()
            result = ttk.Frame(avalFrame)
            reportB = ttk.Button(result,text='Denunciar',
                                 style="smallOptions.TButton",
                                 command=lambda:self.report(info,reportB))
            userN = ttk.Label(result,text=f'{info[2]}:',style="ratings.TLabel")
            if self.connection.reported(self.matricula,self.info,info[3]):
                reportB.state(['disabled'])
            gradeL = ttk.Label(result,text=f'Nota: {info[0]}',
                               style="grade.TLabel")
            i, r = 0, 1
            while i < len(info[1]):
                j = len(info[1]) if len(info[1]) - i <= 15 else i + self.maxLen
                text = f'{"Descrição: " if i == 0 else ""}{info[1][i:j]}'
                textL = ttk.Label(result,text=text,style="ratings.TLabel")
                textL.grid(row=r,column=1,sticky='nsw')
                i += self.maxLen
                r += 1
            userN.grid(row=0,column=0,columnspan=2,sticky='nsw')
            gradeL.grid(row=1,column=0,sticky='nse')
            reportB.grid(row=2,column=0,sticky='nse')
            result.pack(anchor='w')
            self.displayRankings(results,avalFrame) if results else None
        elif results is not None:
            result = ttk.Frame(avalFrame)
            empty = f'Ainda não há avaliações.'
            emptyL = ttk.Label(result,text=empty,style="ratings.TLabel")
            emptyL.pack()
            result.pack(anchor='w')

    def scroll(self,event):
        if event.state == 0:
            self.c.yview_scroll(-(event.delta//120),'units')
        elif event.state == 1:
            self.c.xview_scroll(-(event.delta//120),'units')

    def widFont(self,event):
        comboBox = event.widget
        x,y = self.window.proportionalSize
        comboBox.configure(font=("Roboto",int(-y*0.032)))

    def limitInput(self,event):
        if event.keysym == 'Return':
            self.recordRating()
        elif not avaTexto(event.widget.get('1.0','end-1c')):
            event.widget.delete('insert-1c')

    def recordRating(self):
        if self.op == 'view':
            self.connection.updateRating(self.matricula,self.info,
                                         int(self.gradeVal.get()),
                                         self.text.get('1.0','end-1c'))
        elif self.op == 'search':
            self.connection.recordRating(self.matricula,self.info,
                                         int(self.gradeVal.get()),
                                         self.text.get('1.0','end-1c'))
        self.searchS.setSResults()
        self.dialog.destroy()

    def report(self,info,button):
        self.connection.report(self.matricula,self.info,info[3])
        button.state(['disabled'])