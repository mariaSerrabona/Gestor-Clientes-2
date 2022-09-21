from ast import Delete
from tkinter import *
from tkinter import ttk
import database as db
from tkinter.messagebox import askokcancel, WARNING
import helpers


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
        # Entries and validations
        dni = Entry(frame)
        dni.grid(row=1, column=0)
        dni.bind("<KeyRelease>", lambda event: self.validate(event, 0))
        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda event: self.validate(event, 1))
        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda event: self.validate(event, 2))

        # Bottom frame
        frame = Frame(self)
        frame.pack(pady=10)

        # Buttons
        crear = Button(frame, text="Crear",command=self.create_client)
        crear.configure(state=DISABLED)
        crear.grid(row=0, column=0)
        Button(frame, text="Cancelar", command=self.close).grid(row=0,column=1)


        # Create button activation
        self.validaciones = [0, 0, 0] # False, False, False
        self.crear = crear
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido


    def create_client(self):
        self.master.treeview.insert(
            parent='', index='end', iid=self.dni.get(), values=(self.dni.get(), self.nombre.get(),
        self.apellido.get()))
        db.Clientes.crear(self.dni.get(), self.nombre.get(),self.apellido.get())
        self.close()

    def close(self):
        self.destroy()
        self.update()


    def validate(self, event, index):
        valor = event.widget.get()
        # Validar el dni si es el primer campo o textual para los otrosdos
        valido = helpers.dni_valido(valor, db.Clientes.lista) if index == 0\
            else (valor.isalpha() and len(valor) >= 2 and len(valor) <=30)
        event.widget.configure({"bg": "Green" if valido else "Red"})
        # Cambiar estado del botón en base a las validaciones
        self.validaciones[index] = valido
        self.crear.config(state=NORMAL if self.validaciones == [1, 1, 1]
                                else DISABLED)


class EditClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Actualizar cliente')
        self.build()
        self.center()
        self.transient(parent)
        # Obligar al usuario a interactuar con la subventana self.transient(parent)
        self.grab_set()


    def build(self):
        # Top frame
        frame = Frame(self)
        frame.pack(padx=20, pady=10)
        # Labels
        Label(frame, text="DNI (no editable)").grid(row=0, column=0)
        Label(frame, text="Nombre (2 a 30 chars)").grid(row=0, column=1)
        Label(frame, text="Apellido (2 a 30 chars)").grid(row=0, column=2)

        # Entries
        dni = Entry(frame)
        dni.grid(row=1, column=0)
        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda event: self.validate(event, 0))
        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda event: self.validate(event, 1))

        # Set entries initial values
        cliente = self.master.treeview.focus()
        campos = self.master.treeview.item(cliente, 'values')
        dni.insert(0, campos[0])
        dni.config(state=DISABLED)
        nombre.insert(0, campos[1])
        apellido.insert(0, campos[2])

        # Bottom frame
        frame = Frame(self)
        frame.pack(pady=10)
        treeview = ttk.Treeview(frame)
        treeview['columns'] = ('DNI', 'Nombre', 'Apellido')

        # Buttons
        actualizar = Button(frame, text="Actualizar", command=self.update_client)
        actualizar.grid(row=0, column=0)
        Button(frame, text="Cancelar", command=self.close).grid(row=0, column=1)

        # Update button activation
        self.validaciones = [1, 1]  # True, True
        # Class exports
        self.actualizar = actualizar
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.treeview = treeview

    def validate(self, event, index):
        valor = event.widget.get()
        valido = (valor.isalpha() and len(valor) >= 2 and len(valor) <=30)
        event.widget.configure({"bg": "Green" if self.valido else "Red"})
        # Cambiar estado del botón en
        self.validaciones[index] = valido
        self.actualizar.config(state=NORMAL if self.validaciones ==[1, 1] else DISABLED)

    def update_client(self):
        cliente = self.master.treeview.focus()
        # Sobreescribimos los datos de la fila seleccionada
        self.master.treeview.item(cliente, values=(self.dni.get(), self.nombre.get(), self.apellido.get()))
        db.Clientes.modificar(self.dni.get(), self.nombre.get(), self.apellido.get())
        self.close()

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


        for cliente in db.Clientes.lista:
            treeview.insert(parent='', index='end', iid=cliente.dni, values=(cliente.dni, cliente.nombre, cliente.apellido))

        treeview.pack()

        frame = Frame(self)
        frame.pack(pady=20)
        # Buttons
        Button(frame, text="Modificar", command=self.create_edit_window).grid(row=1, column=1)
        Button(frame, text="Borrar", command=self.delete).grid(row=1, column=2)
        Button(frame, text="Crear", command=self.create_client_window).grid(row=1, column=0)

        self.treeview = treeview

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
            db.Clientes.borrar(campos[0])



    def create_client_window(self):
        CreateClientWindow(self)

    def create_edit_window(self):
        EditClientWindow(self)



if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()