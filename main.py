from window import Window
from titlescreen import Titlescreen

if __name__ == "__main__":
    w = Window()
    Titlescreen(w)
    w.window.mainloop()