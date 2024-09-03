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

class Dilutions():
    """Class is used to generate the dilution volumes and masking for the input
    dilution factors."""
    def __init__(self, samples):
        """initialization that takes as an input a dictionary with the key as the sample name and the 
        value is a tuple of the dilution factor and lot number for the samples. The reqired dilutions will generate
        another dictionary with the ln+sample name as the key and the value as a tuple of each possible dilution step"""
        self.samples_dict = samples
        # samplename: (df, lot number)
        self.samples_dilutions = None
        # ln+sample name : (total df, diluent3, sample3, diluent2, sample2, diluent1, sample1, diluent0, sample0)
        self.dilution_table = None

    def get_sample_names(self):
        """Returns the keys or sample names"""
        return self.samples_dict.keys()

    def get_sample_details(self):
        """Returns alist of the sample name + df + lot number of the sample"""
        sample_and_ln = []
        for i in self.samples_dict:
            sample_and_ln.append(self.samples_dict[i] + "_df = "+ self.sample_dict[i][0]+" _ln_" + self.samples_dict[i][1])
        return sample_and_ln
    
    def generate_dilutions(self):
        """Function is used to generate the dilutions required for each sample based on the dilution factor.
        d3 = 901-540,000, d2 = 151-900, d1 = 21-150, d0 = 2-20
        equation 
        dilution rational										
		Pre -3		Pre -2		Pre -1		prep x2 inc spike		
df		diluent -3	sample -3	diluent-2	sample-2	diluent-1	sample-1	diluent	sample	sample required
<20	2-20							190	10	200-20
>20	20-30					270	30	100	100	30
>30	30-150					280	20	100	100	20
>150	150-900			280	20	180	120	150	50	20
>900	900-13500	280	20	222.5	77.5	222.5	77.5	150	50	20
>13500	13500-160000	285	15	255.2	44.8	255.2	44.8	190	10	15
>160,000	160000-540000	290	10	281.6	18.4	281.6	18.4	190	10	10
or max 540,000		285	10	290	10	290	10	190	10	10

        """
        return







app = App()
app.mainloop()