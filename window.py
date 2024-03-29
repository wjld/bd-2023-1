from tkinter import Tk, ttk, Toplevel
from dbConnect import DbConnect

class Window:

    def __init__(self):
        self.window: Tk = Tk()
        self.size = None
        self.proportionalSize: tuple[int, int] = (0,0)
        self.style: ttk.Style = ttk.Style(self.window)
        self.height: int = self.window.winfo_screenheight()
        self.connection = DbConnect()
        self.window.title("Sistema de Avaliação")
        self.window.rowconfigure(0,weight=1)
        self.window.columnconfigure(0,weight=1)
        self.window.bind("<Configure>",self.manageSize)
        self.window.protocol("WM_DELETE_WINDOW",self.destroy)

        self.window.minsize(3*self.height//4, 9*self.height//16)
        self.proportionalSize = self.window.minsize(None)

    def manageSize(self,event):
        if isinstance(event.widget,Tk) and self.isResizing(event):
            self.size = (event.width,event.height)
            aspectRatio = 3/4
            maxY = int(event.width/aspectRatio)

            if maxY < event.height:
                self.proportionalSize = (event.width,maxY)
            else:
                self.proportionalSize = self.size

            self.styleConfig(self.window,self.style,*self.proportionalSize)

    def styleConfig(self, w: Tk, s: ttk.Style, x: int, y: int) -> None:
        s.configure("title.TLabel",anchor="center",
                    font=("Roboto",int(-y*0.085)))
        s.configure("ratings.TLabel",anchor="w",font=("Roboto",int(-y*0.042)))
        s.configure("grade.TLabel",anchor="e",font=("Roboto",int(-y*0.038)))
        s.configure("dialog.TLabel",anchor="w",font=("Roboto",int(-y*0.032)))
        s.configure("signin.TLabel",anchor="center",
                    font=("Roboto",int(-y*0.04)))
        s.configure("options.TButton",font=("Roboto",int(-y*0.042)))
        s.configure("admin.TCheckbutton",font=("Roboto",int(-y*0.038)))
        s.configure("smallOptions.TButton",font=("Roboto",int(-y*0.032)))
        w.option_add("*TCombobox*Listbox.font",("Roboto",int(-y*0.04)))
        w.option_add("*TCombobox*Listbox.justify","center")

    def comboFont(self,event):
        comboBox = event.widget
        x,y = self.proportionalSize
        comboBox.configure(font=("Roboto",int(-y*0.04)))

    def entryFont(self,event):
        entry = event.widget
        x,y = self.proportionalSize
        entry.configure(font=("Roboto",int(-y*0.038)))

    def isResizing(self,event):
        return (event.width,event.height) != self.size

    def split(self,frame,xLength,yLength,xSize,ySize,i=0):
        if i < xLength or i < yLength:
            if i < xLength:
                frame.columnconfigure(i,minsize=xSize,weight=1)
            if i < yLength:
                frame.rowconfigure(i,minsize=ySize,weight=1)
            self.split(frame,xLength,yLength,xSize,ySize,i+1)

    def destroy(self):
        self.connection.close()
        self.window.destroy()