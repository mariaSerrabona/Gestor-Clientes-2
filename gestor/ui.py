from ast import Delete
from tkinter import *
from tkinter import ttk
import database as db
from tkinter.messagebox import askokcancel, WARNING


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

class CreateClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Crear cliente')
        self.build()
        self.center()
        # Obligar al usuario a interactuar con la subventana
        self.transient(parent)
        self.grab_set()
    def build(self):
        # Top frame
        frame = Frame(self)
        frame.pack(padx=20, pady=10)
        # Labels
        Label(frame, text="DNI (2 ints y 1 upper char)").grid(row=0, column=0)
        Label(frame, text="Nombre (2 a 30 char)").grid(row=0, column=1)
        Label(frame, text="Apellido (2 a 30 char)").grid(row=0, column=2)
        # Entries
        dni = Entry(frame)
        dni.grid(row=1, column=0)
        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        # Bottom frame
        frame = Frame(self)
        frame.pack(pady=10)
        # Buttons
        crear = Button(frame, text="Crear",command=self.create_client)
        crear.configure(state=DISABLED)
        crear.grid(row=0, column=0)
        Button(frame, text="Cancelar", command=self.close).grid(row=0,column=1)


    def create_client(self):
        pass
    def close(self):
        self.destroy()
        self.update()


class MainWindow(Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title('Gestor de clientes')
        self.build()
        self.center()
        # Export treeview to the class
        #treeview=self.treeview

    def build(self):
        # Top Frame
        frame = Frame(self)
        frame.pack()
        # Treeview
        # Scrollbar
        scrollbar = Scrollbar(frame) # new
        scrollbar.pack(side=RIGHT, fill=Y) # new
        treeview = ttk.Treeview(frame, yscrollcommand=scrollbar.set) # edited
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


        for cliente in db.Clientes.lista:
            treeview.insert(parent='', index='end', iid=cliente.dni, values=(cliente.dni, cliente.nombre, cliente.apellido))

        frame = Frame(self)
        frame.pack(pady=20)
        # Buttons
        Button(frame, text="Modificar", command=None).grid(row=1, column=1)
        Button(frame, text="Borrar", command=self.delete).grid(row=1, column=2)
        Button(frame, text="Crear", command=self.create_client_window).grid(row=1, column=0)


    def delete(self):
        cliente = self.treeview.focus()
        if cliente:
            campos = self.treeview.item(cliente, 'values')
            confirmar = askokcancel(
            title='Confirmación',
            message=f'¿Borrar a {campos[1]} {campos[2]}?', icon=WARNING)
        if confirmar:
            # remove the row
            self.treeview.delete(cliente)



    def create_client_window(self):
        CreateClientWindow(self)



if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()