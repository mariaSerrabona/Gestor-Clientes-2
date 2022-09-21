from tkinter import *
from tkinter import ttk

class MainWindow(Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title('Gestor de clientes')
        self.build()
        self.center()
    def build(self):
        # Top Frame
        frame = Frame(self)
        frame.pack()
        # Treeview
        treeview = ttk.Treeview(frame)
        treeview['columns'] = ('DNI', 'Nombre', 'Apellido')
        treeview.pack()
            # Column format
        treeview.column("#0", width=0, stretch=NO)
        treeview.column("DNI", anchor=CENTER)
        treeview.column("Nombre", anchor=CENTER)
        treeview.column("Apellido", anchor=CENTER)
            # Heading format
        treeview.heading("#0", anchor=CENTER)
        treeview.heading("DNI", text="DNI", anchor=CENTER)
        treeview.heading("Nombre", text="Nombre", anchor=CENTER)
        treeview.heading("Apellido", text="Apellido", anchor=CENTER)
        # Pack
        treeview.pack()
    def hola(self):
        print("¡Hola mundo!")


class CenterWidgetMixin:
    def center(self,):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int((ws/2) - (w/2))
        y = int((hs/2) - (h/2))
        self.geometry(f"{w}x{h}+{x}+{y}")


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()