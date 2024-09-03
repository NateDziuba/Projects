import customtkinter

class MyTabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        # Class Variables
        # create tabs
        self.add("Experiment Details")
        self.add("Samples")
        self.add("Dilution Table")

        # add widgets on tabs
        self.label1 = customtkinter.CTkLabel(master=self.tab("Experiment Details"), text = "Fill in the experiment details below.")
        self.label1.grid(row=0, column=0, padx=20, pady=(10,0))
        self.label2 = customtkinter.CTkLabel(master=self.tab("Samples"), text = "Test Tab2")
        self.label2.grid(row=0, column=0, padx=20, pady=10)

        # Exerpiment Details Tab
        self._entries = ["Entry test", "Entry Test 2", "Entry Test 3"]
        self._entry = customtkinter.CTkEntry(master=self.tab("Experiment Details"), placeholder_text="Entry Test")
        self._entry.grid(row=1, column=1, padx=(10,5), sticky="ew")
        self.entry_button = customtkinter.CTkButton(
            master=self.tab("Experiment Details"), text="Load Details", command=self.experiment_button,
            state="normal")
        self.entry_button.grid(row=6, column=0, sticky="ew")
        self.label1_1 = customtkinter.CTkLabel(master=self.tab("Experiment Details"), text="Client Code")
        self.label1_1.grid(row=1, column=0, padx=(0,10))

    def experiment_button(self):
        print("Clicked Button")
        entry_data = None
        print("Pre-fill \n", entry_data)
        entry_data = self._entry.get()
        print("Post-fill: ", entry_data)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tab_view = MyTabView(master=self)
        self.tab_view.grid(row=0, column=0, padx=100, pady=100)


        






app = App()
app.mainloop()