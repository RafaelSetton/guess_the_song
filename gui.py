from tkinter import messagebox
from tkinter import filedialog
from tkinter import Tk, Label, Button, Text, Checkbutton, END, BooleanVar
from typing import Callable
import sys
from PIL import Image, ImageTk


class StdoutRedirector:
    def __init__(self, text_widget: Text, text_color: str):
        self.text_widget = text_widget
        self.tag = text_color

    def write(self, message):
        # Insert the message into the Text widget
        self.text_widget.insert(END, message, self.tag)
        # Automatically scroll to the end
        self.text_widget.see(END)

    def flush(self):
        # This method is required for Python 3 compatibility.
        pass


class App(Tk):
    def __init__(self, callback: Callable[[map, str, bool], None]):
        Tk.__init__(self)
        img = Image.open("./icon.png")
        icon = ImageTk.PhotoImage(img)
        self.iconphoto(False, icon)
        self.callback = callback
        self.directory = None

    def pick_directory(self):
        directory = filedialog.askdirectory(title="Select a Directory")
        if directory:
            self.directory_label.config(text=f"Selected Directory:\n{directory}")
            self.directory = directory
        else:
            self.directory_label.config(text="No directory selected.")
        return directory

    def submit(self):
        if self.directory == None:
            self.error("Escolha um diretório")
        
        try:
            usernames = {}
            lines = self.text_widget.get("1.0", END).strip().split('\n')
            self.text_widget.delete("1.0", END)
            for line in lines:
                _id, name = line.split(":")
                _id = _id.strip()
                name = name.strip()
                usernames[_id] = name
        except ValueError:
            self.error("A formatação dos nomes está errada")
        else:
            self.callback(usernames, self.directory, self.use_cache)
            self.text_widget.insert(END, "Arquivos gerados com sucesso", "green")

    def add_components(self):
        # Basic Window Info
        x = self.winfo_screenwidth() // 2 - 175
        y = self.winfo_screenheight() // 2 - 250
        self.title("Guess The Song Assistant")
        self.geometry(f"500x500+{x}+{y}")
        self.resizable(False, False)

        # Label and Text Widget

        Label(self, text="Usernames (1 per line)\n(user_id: display_name)").pack(pady=10)
        self.text_widget: Text = Text(self, height=10, width=50)
        self.text_widget.pack(pady=10)

        # Pick Directory Button and Label

        Button(self, text="Pick Directory", command=self.pick_directory, font=("Arial", 12)).pack(pady=20)

        self.directory_label = Label(self, text="No directory selected.", font=("Arial", 10), wraplength=350, justify="left")
        self.directory_label.pack(pady=10)

        # Use Cache?

        self.use_cache = BooleanVar(value=True)
        Checkbutton(self, text="Usar cache", variable=self.use_cache, onvalue=True, offvalue=False).pack(pady=10)

        # Submit Button

        Button(self, text="Submit", command=self.submit, font=("Arial", 12)).pack(pady=10)

        # Credits

        Label(self, text="2024 © Created by Rafael Setton").place(x=300, y=480)

        # Configura Output

        self.text_widget.tag_configure("red", foreground="red")      # Red text
        self.text_widget.tag_configure("blue", foreground="blue")    # Blue text
        self.text_widget.tag_configure("green", foreground="green")

        sys.stdout = StdoutRedirector(self.text_widget, "blue")
        sys.stderr = StdoutRedirector(self.text_widget, "red")



    def error(self, msg: str):
        """Display a message box with the entered text."""
        messagebox.showinfo("ERRO", msg)

