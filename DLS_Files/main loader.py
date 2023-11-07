# ---- Import Zone ----

import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
import os as os
import csv

# ---- Global Variable Zone ----
# Fil path selection storage location
file_path = None # Used in FileSet() function to store the file path of the selected file.

def main_menu():
    """Main menu to make selections from."""
    print(
        "Main Menu\n"
        "---------\n"
        "0 - Terminate Script.\n"
        "1 - Template Generation.\n"
        "2 - Data Analysis.\n"
        "3 - Select working file. \n"
        "4 - Printer working file filepath in terminal.\n\n"
    )

def FileSet():
    """Function asks the user for a file path. This filepath is then stored as a global variable for future use."""
    global file_path

    if file_path is None:
        # While function loops until a csv file is selected or end has been input to go to the main menu.
        while True:
            print("Please select a CSV file for data analysis.\n")
            request_pause2 = input("Please press any key to continue...\n")

            root = tk.Tk()
            root.withdraw()

            file_path = filedialog.askopenfilename()
            file_extension = file_path[-3:]
            print("---- File has been selected, analyzing for file type.---- \n")

            if file_extension == "csv": # Checks if selected file is a csv extension.
                break
            else:
                print("A CSV file was not selected. Please select a csv file for analysis.\n")
                request_pause = input("Please press any key to continue or type end to go to main menu.\n\n").lower()
                if request_pause == "end":
                    break
    if file_path is not None: #Needed during analysis. File path selection is run automatically, because users...
        while True:
            print("Is this the correct file for data analysis?\n", file_path)
            request2 = input("Please press enter Yes or No. \n").lower()

            if request2 is yes:
                break

            if request2 is no:
                root = tk.Tk()
                root.withdraw()

                file_path = filedialog.askopenfilename()
                file_extension = file_path[-3:]
                print("---- File has been selected, analyzing for file type.---- \n")

            if file_extension == "csv": # Checks if selected file is a csv extension.
                print("File is a csv extension. Accepting file path.\n")
                break
            else:
                print("A CSV file was not selected. Please select a csv file for analysis.\n")
                request_pause = input("Please press any key to continue or type end to go to main menu.\n\n").lower()
                if request_pause == "end":
                    break

    return(file_path)


class DataAnalysis:

    # initializing the class.
    def __init__(self):

        self.directorychange()
        self.df_load = init_dataframe()

    ### Function determines if the current filepath contains the data of interest, if not it requests
    ### a direct filepath from the user to use for analysis. .
    def directorychange(self):
        FileSet()

    def init_dataframe(self):
        global file_path
        print('\n\n Initializing Dataframe... Using filepath: \n\n')
        print(file_path)
        initframe = pd.read_csv(file_path, encoding = 'cp1252')
        print("\n\n Loaded Dataframe: \n")
        print(self.initframe, "\n\n")
        self.df_sorted = self.initdframe[["Well", "Sample", "Normalized Intensity (Cnt/s)", "Dilution Factor", "Diameter (nm)",
                        "Amplitude", "Baseline", "SOS", "%PD",
                        "Range1 Diameter (I) (nm)", "Range1 %Pd (I)", "Range1 %Number (I)",
                        "Range2 Diameter (I) (nm)", "Range2 %Pd (I)", "Range2 %Number (I)",
                        "Range3 Diameter (I) (nm)", "Range3 %Pd (I)", "Range3 %Number (I)",
                        "Range4 Diameter (I) (nm)", "Range4 %Pd (I)", "Range4 %Number (I)",
                        "Range5 Diameter (I) (nm)", "Range5 %Pd (I)", "Range5 %Number (I)",
                        "Number Acqs", "% Acqs Unmarked", "Number Acqs", "Number Marked Acqs", "Item"
                        ]].copy()

        return (self.df_sorted)


    def FrameFilter(df_sorted):
        df_filtered = df_sorted[(df_sorted['Baseline'] >= 0.99) & (df_sorted['Baseline'] <= 1.01) & (df_sorted['SOS'] <= 10)
                                & (df_sorted['Amplitude'] >= 0.1) & (df_sorted['% Acqs Unmarked'] >= 70)].copy()
        return (df_filtered)

    @staticmethod
    def PRsd(x):
        return (x.std() / x.mean()) * 100


def NormInt():
    # Variable for the filtered data from df_sorted
    df_filtered = df_sorted[(df_sorted['Baseline'] >= 0.99) & (df_sorted['Baseline'] <= 1.01) & (df_sorted['SOS'] <= 25)
                            & (df_sorted['Amplitude'] >= 0.1) & (df_sorted['% Acqs Unmarked'] >= 70)]

    # Sorted results  by sample, then dilution factor and calculated basic statistic values for the described values
    df_NI = df_filtered.groupby(['Sample', 'Dilution Factor']).agg(
        {'Normalized Intensity (Cnt/s)': ['size', 'mean', 'std', PRsd]}).reset_index().copy()

    # %RSD needs to be 5% or lower and the size (the number of grouped dilution factors) needs to be 3.
    df_rsd = df_NI[
        (df_NI['Normalized Intensity (Cnt/s)', "PRsd"] <= 5) & (df_NI['Normalized Intensity (Cnt/s)', 'size'] == 3)]
    print("df_filtered", df_filtered)
    print("df_NI", df_NI)
    print("\n\ndf_rsd", df_rsd)
    return (df_rsd.loc[:, (['Sample', 'Dilution Factor', 'Normalized Intensity (Cnt/s)'], ["", 'mean'])])


# generate a list of non repeating sample names from the normalized intensity data that has been filtered

def SelectSamples():
    df = NormInt()

    sname = df['Sample'].tolist()
    snamer = []
    [snamer.append(i) for i in sname if i not in snamer]

    print(snamer)

    for i in snamer:
        if df['Sample'] is i:
            print("True")
    return (snamer)

def TemplateGenerator():
    print("Template Generator function activated.")


def main():
    """ The main function that prompts the user to make a selection of a task they would like to perform."""


# Initiation of the prompt.
    print("Welcome to the DLS Python script, please select an option below.\n")
    # Loops to allow the user to select an option, and requires only int.
    while True:
        main_menu()

        try:
            request = int(input("Make a selection from the table above.\n\n"))
        except ValueError:
            print("Your input is incorrect. Make a selection from 0-3.\n")
            continue
        if request == 1:
            TemplateGenerator()
        elif request == 2:
            DataAnalysis()
        elif request == 3:
            FileSet()
        elif request == 4:
            print("The filepath is: ", file_path, "\n\n")
        elif request == 0:
            print("Thank-you for using the DLS python script.\n\n")
            break
        else:
            print("Invalid choice. \n")


if __name__ == "__main__":
    main()
