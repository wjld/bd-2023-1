from tkinter import ttk, Toplevel, StringVar, Text
from validate import avaTexto

class Dialog():
    def __init__(self,window,matricula,info):
        self.window = window
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
        self.gradeVal = StringVar(frame,'5')
        self.lastText = ''
        self.info = info
        self.matricula = matricula
        frame.grid(sticky="nsew")
        self.window.split(frame,30,45,int(1.5*size)//30,size//45)

        self.setWidgets(info,frame)

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

    def widFont(self,event):
        comboBox = event.widget
        x,y = self.window.proportionalSize
        comboBox.configure(font=("Roboto",int(-y*0.032)))

    def limitInput(self,event):
        if not avaTexto(event.widget.get('1.0','end-1c')):
            event.widget.delete('insert-1c')

    def recordRating(self):
        self.window.connection.recordRating(self.matricula,self.info,
                                            int(self.gradeVal.get()),
                                            self.text.get('1.0','end-1c'))
        self.dialog.destroy()