from tkinter import ttk
from menu import Menu
from hashlib import sha3_256

class Signin():
    def __init__(self,titlescreen,window):
        self.titlescreen = titlescreen
        self.window = window
        self.connection = window.connection
        self.frame = ttk.Frame(self.window.window)
        self.menu = Menu(titlescreen,window)
        self.fields = []

        self.frame.grid(sticky="nsew")
        x,y = self.window.window.minsize(None)
        window.split(self.frame,20,50,x//20,y//50)

        self.setWidgets()
        self.frame.grid_remove()

    def setWidgets(self):
        fail = ttk.Label(self.frame,text="Usuário ou senha incorretos",
                         style="signin.TLabel",background='#D06060')
        usuLabel = ttk.Label(self.frame,text="Usuário",style="signin.TLabel")
        username = ttk.Entry(self.frame,exportselection=False,justify="center")
        senLabel = ttk.Label(self.frame,text="Senha",style="signin.TLabel")
        password = ttk.Entry(self.frame,exportselection=False,justify="center",
                             show='*')
        doneB = ttk.Button(self.frame,command=self.done,text="Pronto",
                           style="options.TButton")
        backB = ttk.Button(self.frame,command=self.back,text="Voltar",
                           style="options.TButton")
        self.fields = [username,password,fail]

        usuLabel.grid(row=18,column=7,rowspan=3,columnspan=6,sticky="nsew")
        username.grid(row=21,column=6,rowspan=4,columnspan=8,sticky="nsew")
        senLabel.grid(row=26,column=7,rowspan=3,columnspan=6,sticky="nsew")
        password.grid(row=29,column=6,rowspan=4,columnspan=8,sticky="nsew")
        doneB.grid(row=35,column=8,rowspan=4,columnspan=4,sticky="nsew")
        backB.grid(row=45,column=15,rowspan=4,columnspan=4,sticky="nsew")
        username.event_add('<<entryFont>>','<Configure>','<Visibility>')
        username.bind("<<comboFont>>",self.window.entryFont,add=True)
        username.bind('<Key>',lambda e:self.manageKey(e))
        password.event_add('<<entryFont>>','<Configure>','<Visibility>')
        password.bind("<<comboFont>>",self.window.entryFont,add=True)
        password.bind('<Key>',lambda e:self.manageKey(e))

    def display(self):
        self.frame.grid()
        self.fields[0].focus()
    
    def done(self):
        username, password = self.fields[:2]
        passW = sha3_256(password.get().encode('utf8')).digest().hex()
        userInfo = self.connection.signin(username.get(),passW)
        if userInfo == []:
            self.fields[2].grid(row=13,column=6,rowspan=3,columnspan=8,
                                sticky="nsew")
        else:
            for entry in self.fields[:2]:
                entry.delete(0,'end')
            self.fields[2].grid_forget()
            self.frame.grid_remove()
            self.menu.display(userInfo[0])

    def manageKey(self,event):
        if event.keysym == 'Return':
            self.done()
        else:
            self.fields[2].grid_forget()

    def back(self):
        for entry in self.fields[:2]:
            entry.delete(0,'end')
        self.fields[2].grid_forget()
        self.frame.grid_remove()
        self.titlescreen.display()