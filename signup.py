from tkinter import ttk, Entry
from validate import *
from menu import Menu
from hashlib import sha3_256

class Signup():
    def __init__(self,titlescreen,window):
        self.titlescreen = titlescreen
        self.window = window
        self.connection = window.connection
        self.frame = ttk.Frame(self.window.window)
        self.menu = Menu(titlescreen,window)
        self.fieldStatus = [False for _ in range(6)]

        self.frame.grid(sticky="nsew")
        x,y = self.window.window.minsize(None)
        window.split(self.frame,20,50,x//20,y//50)

        self.setWidgets()
        self.frame.grid_remove()

    def setWidgets(self):
        matLabel = ttk.Label(self.frame,text="Matrícula",style="signin.TLabel")
        matricula = Entry(self.frame,exportselection=False,validate='key',
                              justify="center")
        senLabel = ttk.Label(self.frame,text="Senha",style="signin.TLabel")
        password = Entry(self.frame,exportselection=False,justify="center",
                             validate='key',show='*')
        emailLabel = ttk.Label(self.frame,text="Email",style="signin.TLabel")
        email = Entry(self.frame,validate='key',exportselection=False,
                              justify="center")
        curLabel = ttk.Label(self.frame,text="Curso",style="signin.TLabel")
        curso = Entry(self.frame,exportselection=False,validate='key',
                      justify="center")
        nomLabel = ttk.Label(self.frame,text="Nome",style="signin.TLabel")
        nome = Entry(self.frame,exportselection=False,validate='key',
                              justify="center")
        sobreL = ttk.Label(self.frame,text="Sobrenome",style="signin.TLabel")
        sobren = Entry(self.frame,exportselection=False,validate='key',
                       justify="center")
        self.doneB = ttk.Button(self.frame,command=self.done,text="Pronto",
                           style="options.TButton")
        backB = ttk.Button(self.frame,command=self.back,text="Voltar",
                           style="options.TButton")
        labels = [matLabel,senLabel,nomLabel,sobreL,emailLabel,curLabel]
        self.fields = [matricula,password,nome,sobren,email,curso]
        manage = [self.manageMat,self.managePass,self.manageNom,self.manageSob,
                  self.manageEma,self.manageCur]
        r = 1
        for l, f, func in zip(labels,self.fields,manage):
            l.grid(row=r,column=7,rowspan=3,columnspan=6,sticky="nsew")
            f.grid(row=r + 3,column=6,rowspan=4,columnspan=8,sticky="nsew")
            r += 8
            f.event_add('<<entryFont>>','<Configure>','<Visibility>')
            f.bind("<<entryFont>>",self.window.entryFont,add=True)
        matricula.configure(validatecommand=(matricula.register(
                            lambda t:self.manageMat(matricula,t)),'%P'))
        password.configure(validatecommand=(matricula.register(
                            lambda t:self.managePass(password,t)),'%P'))
        email.configure(validatecommand=(email.register(
                            lambda t:self.manageEma(email,t)),'%P'))
        curso.configure(validatecommand=(curso.register(
                            lambda t:self.manageCur(curso,t)),'%P'))
        nome.configure(validatecommand=(nome.register(
                            lambda t:self.manageNom(nome,t)),'%P'))
        sobren.configure(validatecommand=(sobren.register(
                            lambda t:self.manageSob(sobren,t)),'%P'))
        self.doneB.grid(row=45,column=1,rowspan=4,columnspan=4,sticky="nsew")
        backB.grid(row=45,column=15,rowspan=4,columnspan=4,sticky="nsew")
        self.doneB.bind('<Configure>',lambda e:self.allRight)

    def allRight(self):
        status = self.fieldStatus[0]
        for s in self.fieldStatus:
            status = status and s
        if status:
            self.doneB.state(['!disabled'])
        else:
            self.doneB.state(['disabled'])

    def display(self):
        self.frame.grid()
        self.fields[0].focus()
        self.doneB.bind_all('<KeyPress>',lambda e:self.allRight())
        self.doneB.bind_all('<KeyRelease>',lambda e:self.allRight())
    
    def done(self):
        args = [entry.get() for entry in self.fields]
        args[1] = sha3_256(args[1].encode('utf8')).digest().hex()
        args.append(self.connection.userRegister(args))
        for entry in self.fields:
            entry.delete(0,'end')
            entry.configure(background='#FFFFFF')
        self.doneB.unbind_all('<KeyPress>')
        self.doneB.unbind_all('<KeyRelease>')
        self.frame.grid_remove()
        self.menu.display(args)

    def manageMat(self,mat,t):
        if usuMatricula(t) and not self.connection.matExists(t):
            self.fieldStatus[0] = True
            mat.configure(background='#AAFFAA')
        else:
            self.fieldStatus[0] = False
            mat.configure(background='#FFAAAA')
        return True

    def managePass(self,password,t):
        if usuSenha(t):
            self.fieldStatus[1] = True
            password.configure(background='#AAFFAA')
        else:
            self.fieldStatus[1] = False
            password.configure(background='#FFAAAA')
        return True

    def manageNom(self,nome,t):
        if primNome(t):
            self.fieldStatus[2] = True
            nome.configure(background='#AAFFAA')
        else:
            self.fieldStatus[2] = False
            nome.configure(background='#FFAAAA')
        return True

    def manageSob(self,sobren,t):
        if sobrenome(t):
            self.fieldStatus[3] = True
            sobren.configure(background='#AAFFAA')
        else:
            self.fieldStatus[3] = False
            sobren.configure(background='#FFAAAA')
        return True

    def manageEma(self,email,t):
        if usuEmail(t) and not self.connection.emailExists(t):
            self.fieldStatus[4] = True
            email.configure(background='#AAFFAA')
        else:
            self.fieldStatus[4] = False
            email.configure(background='#FFAAAA')
        return True

    def manageCur(self,curso,t):
        if usuCurso(t):
            self.fieldStatus[5] = True
            curso.configure(background='#AAFFAA')
        else:
            self.fieldStatus[5] = False
            curso.configure(background='#FFAAAA')
        return True

    def back(self):
        for entry in self.fields:
            entry.delete(0,'end')
            entry.configure(background='#FFFFFF')
        self.doneB.unbind_all('<KeyPress>')
        self.doneB.unbind_all('<KeyRelease>')
        self.frame.grid_remove()
        self.titlescreen.display()