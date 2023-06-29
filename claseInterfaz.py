from claseContacto import contacto
import tkinter as tk


class interfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda de Contactos")

        self.contacts = []
        self.selected_index = (
            None
        )

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

        self.edit_button = tk.Button(
            root, text="Editar", command=self.edit_contact
        )  
        self.edit_button.grid(row=2, column=1, pady=10)

        self.delete_button = tk.Button(
            root, text="Eliminar", command=self.delete_contact
        )  
        self.delete_button.grid(row=2, column=2, pady=10)

        self.display_frame = tk.Frame(root)
        self.display_frame.grid(row=3, column=0, columnspan=3)

        self.display_text = tk.Text(self.display_frame, height=10, width=30)
        self.display_text.pack(side=tk.LEFT, fill=tk.Y)

        self.scrollbar = tk.Scrollbar(self.display_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.display_text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.display_text.yview)

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
                    phone = lines[i + 1].strip()

                    contact = contacto(name, phone)
                    self.contacts.append(contact)

                    self.display_text.insert(
                        tk.END, f"Nombre: {name}\nTeléfono: {phone}\n\n"
                    )
        except FileNotFoundError:
            pass

    def save_contacts(self):
        with open("usuarios.txt", "w") as file:
            for contact in self.contacts:
                file.write(contact.nombre + "\n")
                file.write(contact.telefono + "\n")

    def edit_contact(self):
        if self.selected_index is not None:
            name = self.name_entry.get()
            phone = self.phone_entry.get()
            contact = self.contacts[self.selected_index]
            contact.nombre = name
            contact.telefono = phone
            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            data = ""
            for contact in self.contacts:
                data += f"Nombre: {contact.nombre}\nTeléfono: {contact.telefono}\n\n"
            self.display_text.delete(1.0, tk.END)
            self.display_text.insert(tk.END, data)
            self.save_contacts()
        else:
            tk.messagebox.showerror("Error", "No se ha seleccionado ningún contacto")

    def delete_contact(self):
        if self.selected_index is not None:
            contact = self.contacts[self.selected_index]
            self.contacts.remove(contact)
            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            data = ""
            for contact in self.contacts:
                data += f"Nombre: {contact.nombre}\nTeléfono: {contact.telefono}\n\n"
            self.display_text.delete(1.0, tk.END)
            self.display_text.insert(tk.END, data)
            self.save_contacts()
        else:
            tk.messagebox.showerror("Error", "No se ha seleccionado ningún contacto")

    def select_contact(self, event):
        x = event.x
        y = event.y
        index = self.display_text.index(f"@{x},{y}")
        line = int(index.split(".")[0])
        contact_index = (line - 1) // 3
        if 0 <= contact_index < len(self.contacts):
            contact = self.contacts[contact_index]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, contact.nombre)
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, contact.telefono)
            self.selected_index = contact_index
        else:
            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.selected_index = None
