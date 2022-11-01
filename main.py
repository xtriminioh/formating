from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from lazyhuman import LazyHand

root = Tk()
root.title('Formating')
#root.geometry('300x200')
root.resizable(0,0)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

message = StringVar()
filepath = StringVar()

def openfile() :
    file = filedialog.askopenfile()
    message.set(file.name.split('/')[-1])
    filepath.set(file.name)

def formating():
    message.set(f'Formating {message.get()}')
    LazyHand(filepath.get()).guardar
    message.set('Ready...')

class MainFrameButtons(ttk.Frame):
    def __init__(self, master, col:int, row:int):
        super().__init__(master)
        self.pos_col=col
        self.pos_row=row
        self.configure(padding="12 12 12 12")
        self.grid(column=self.pos_col, row=self.pos_row, sticky=(N,S))

        upload_btn = ttk.Button(self, text='UploadFile')
        upload_btn.config(command=openfile)

        format_btn = ttk.Button(self, text='Formating')
        format_btn.config(command=formating)

        close_btn = ttk.Button(self, text='Close')
        close_btn.config(command=master.destroy)
    
        for i, child in enumerate(self.winfo_children()):
            child.grid_configure(column=i, row=1, padx=5, pady=5)

class StatusBar(ttk.Label):
    def __init__(self, master, message:StringVar):
        super().__init__(master)
        self.message = message 
        self.configure(textvariable=self.message, relief=SUNKEN, anchor=W)
        self.grid_configure(column=1, row=2, sticky=(N, W, E, S))

if __name__ == '__main__':
    MainFrameButtons(root,col=1,row=1)
    StatusBar(root,message=message)
    root.mainloop()