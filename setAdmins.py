from tkinter import ttk, Canvas, BooleanVar

class SetAdmins():
    def __init__(self,titlescreen,window):
        self.titlescreen = titlescreen
        self.window = window
        self.connection = window.connection
        self.rootframe = ttk.Frame(self.window.window)
        self.searchArea = Canvas(self.rootframe)

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

        self.setWidgets()
        self.rootframe.grid_remove()

    def setWidgets(self):
        backB = ttk.Button(self.rootframe,command=self.back,text="Voltar",
                           style="options.TButton")

        self.searchTerm.grid(row=2,column=1,rowspan=4,columnspan=20,
                             sticky="nsew")
        self.searchB.grid(row=2,column=22,rowspan=4,columnspan=9,sticky="nsew")
        backB.grid(row=55,column=35,rowspan=4,columnspan=9,sticky="nsew")
        self.searchTerm.event_add('<<entryFont>>','<Configure>','<Visibility>')
        self.searchTerm.bind("<<entryFont>>",self.window.entryFont,add=True)
        self.searchTerm.bind('<Return>',lambda e:self.setSResults())

    def setSResults(self,results=None,level=0):
        if results is None:
            for frame in self.searchFrame.winfo_children():
                frame.destroy()
            results = self.connection.searchUsers(self.searchTerm.get()[:75])
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
            userId = f'{info[0]}, {info[1]}'
            userInfo = f'{info[2]}, {info[3]}'
            current = BooleanVar(result,bool(info[4]))
            result.update()
            setB = ttk.Checkbutton(result,text="Admin",variable=current,
                                   style="admin.TCheckbutton",
                                   command=lambda:self.toggle(info[1],current))
            userIdL = ttk.Label(result,text=userId,style="ratings.TLabel")
            userInfoL = ttk.Label(result,text=userInfo,style="ratings.TLabel")
            setB.grid(row=0,column=0,rowspan=2,sticky='nsew')
            if not self.window.connection.otherAdmins(info[0]):
                setB.state(['disabled'])
            userIdL.grid(row=0,column=1,sticky='nsw')
            userInfoL.grid(row=1,column=1,sticky='nsw')
            result.pack(anchor='w')
            self.setSResults(results,level=level+1) if results else None

    def scroll(self,event):
        if event.state == 0:
            self.searchArea.yview_scroll(-(event.delta//120),'units')
        elif event.state == 1:
            self.searchArea.xview_scroll(-(event.delta//120),'units')

    def toggle(self,matricula,current):
        self.connection.toggleAdmin(matricula,current.get())

    def display(self,fromS):
        self.fromS = fromS
        self.rootframe.grid()
        self.setSResults()

    def back(self):
        self.searchTerm.delete(0,'end')
        for frame in self.searchFrame.winfo_children():
            frame.destroy()
        self.rootframe.grid_remove()
        self.fromS.display()