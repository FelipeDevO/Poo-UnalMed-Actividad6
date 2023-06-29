from claseContacto import contacto
import tkinter as tk



class interfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda de Contactos")

        self.contacts = []
        self.selected_index = None # Variable para guardar el índice del contacto seleccionado

        self.name_label = tk.Label(root, text="Nombre:")
        self.name_label.grid(row=0, column=0)

        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1)

        self.phone_label = tk.Label(root, text="Teléfono:")
        self.phone_label.grid(row=1, column=0)

        self.phone_entry = tk.Entry(root)
        self.phone_entry.grid(row=1, column=1)

        self.add_button = tk.Button(root, text="Agregar", command=self.add_contact)
        self.add_button.grid(row=2, column=0, pady=10)

        self.edit_button = tk.Button(root, text="Editar", command=self.edit_contact) # Botón para editar
        self.edit_button.grid(row=2, column=1, pady=10)

        self.delete_button = tk.Button(root, text="Eliminar", command=self.delete_contact) # Botón para eliminar
        self.delete_button.grid(row=2, column=2, pady=10)

        self.display_frame = tk.Frame(root)
        self.display_frame.grid(row=3, column=0, columnspan=3)

        self.display_text = tk.Text(self.display_frame, height=10, width=30)
        self.display_text.pack(side=tk.LEFT, fill=tk.Y)

        self.scrollbar = tk.Scrollbar(self.display_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.display_text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.display_text.yview)

        # Agregar un evento para detectar cuando se hace clic en el texto de la ventana
        self.display_text.bind("<Button-1>", self.select_contact)

        self.load_contacts()

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()

        contact = contacto(name, phone)
        self.contacts.append(contact)

        self.display_text.insert(tk.END, f"Nombre: {name}\nTeléfono: {phone}\n\n")

        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

        self.save_contacts()

    def load_contacts(self):
        try:
            with open("usuarios.txt", "r") as file:
                lines = file.readlines()

                for i in range(0, len(lines), 2):
                    name = lines[i].strip()
                    phone = lines[i+1].strip()

                    contact = contacto(name, phone)
                    self.contacts.append(contact)

                    self.display_text.insert(tk.END, f"Nombre: {name}\nTeléfono: {phone}\n\n")
        except FileNotFoundError:
            pass

    def save_contacts(self):
        with open("usuarios.txt", "w") as file:
            for contact in self.contacts:
                file.write(contact.nombre + "\n")
                file.write(contact.telefono + "\n")

    # Método para editar un contacto de la lista
    def edit_contact(self):
        # Si hay un contacto seleccionado
        if self.selected_index is not None:
            # Obtener los datos de los campos de entrada
            name = self.name_entry.get()
            phone = self.phone_entry.get()
            # Obtener el objeto del contacto seleccionado
            contact = self.contacts[self.selected_index]
            # Actualizar los atributos del objeto con los datos
            contact.nombre = name
            contact.telefono = phone
            # Limpiar los campos de entrada
            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            # Actualizar el texto de la ventana con los datos modificados
            data = ""
            for contact in self.contacts:
                data += f"Nombre: {contact.nombre}\nTeléfono: {contact.telefono}\n\n"
            self.display_text.delete(1.0, tk.END)
            self.display_text.insert(tk.END, data)
            # Guardar los cambios en el archivo
            self.save_contacts()
        else:
            # Si no hay un contacto seleccionado, mostrar un mensaje de error
            tk.messagebox.showerror("Error", "No se ha seleccionado ningún contacto")

    # Método para eliminar un contacto de la lista
    def delete_contact(self):
        # Si hay un contacto seleccionado
        if self.selected_index is not None:
            # Obtener el objeto del contacto seleccionado
            contact = self.contacts[self.selected_index]
            # Eliminar el objeto de la lista de contactos
            self.contacts.remove(contact)
            # Limpiar los campos de entrada
            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            # Actualizar el texto de la ventana con los datos modificados
            data = ""
            for contact in self.contacts:
                data += f"Nombre: {contact.nombre}\nTeléfono: {contact.telefono}\n\n"
            self.display_text.delete(1.0, tk.END)
            self.display_text.insert(tk.END, data)
            # Guardar los cambios en el archivo
            self.save_contacts()
        else:
            # Si no hay un contacto seleccionado, mostrar un mensaje de error
            tk.messagebox.showerror("Error", "No se ha seleccionado ningún contacto")

    # Método para seleccionar un contacto al hacer clic en el texto de la ventana
    def select_contact(self, event):
        # Obtener la posición del clic
        x = event.x
        y = event.y
        # Obtener el índice del texto donde se hizo clic
        index = self.display_text.index(f"@{x},{y}")
        # Obtener el número de línea donde se hizo clic
        line = int(index.split(".")[0])
        # Calcular el índice del contacto en la lista de contactos según el número de línea
        contact_index = (line - 1) // 3
        # Si el índice es válido
        if 0 <= contact_index < len(self.contacts):
            # Obtener el objeto del contacto según el índice
            contact = self.contacts[contact_index]
            # Mostrar los datos del contacto en los campos de entrada
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, contact.nombre)
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, contact.telefono)
            # Guardar el índice del contacto seleccionado en la variable
            self.selected_index = contact_index
        else:
            # Si el índice no es válido, limpiar los campos de entrada y la variable
            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.selected_index = None
