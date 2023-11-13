# ---- Import Zone ----

import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import pandas as pd
import numpy as np
import os as os
import csv

# ---- Global Variable Zone ----
# Fil path selection storage location


# Used in FileSet() function to store the file path of the selected file.
file_path = None


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
            input("Please press any key to continue...\n")

            root = tk.Tk()
            root.withdraw()

            file_path = filedialog.askopenfilename()
            file_extension = file_path[-3:]
            print("---- File has been selected, analyzing for file type.---- \n")

            if Path(file_path).suffix == ".csv":  # Checks if selected file is a csv extension.
                print("---File Type is CSV---\n")
                break
            else:
                print("A CSV file was not selected. Please select a csv file for analysis.\n")
                request_pause = input("Please press any key to continue or type end to go to main menu.\n\n").lower()
                if request_pause == "end":
                    pass
    else:
        # Needed during analysis. File path selection is run automatically, because users...
        while True:
            print("Is this the correct file for data analysis?\n", file_path)
            request2 = input("Please press enter Yes or No. \n").lower()

            if request2 == "yes":
                break

            if request2 == "no":
                root = tk.Tk()
                root.withdraw()

                file_path = filedialog.askopenfilename()
                file_extension = file_path[-3:]
                print("---- File has been selected, analyzing for file type.---- \n")

            if Path(file_path).suffix == ".csv":  # Checks if selected file is a csv extension.
                print("----File is a csv extension. Accepting file path.----\n")
                break
            else:
                print("----A CSV file was not selected. Please select a csv file for analysis.----\n")
                request_pause = input("Please press any key to continue or type \"END\" to go to the main menu.\n\n").lower()
                if request_pause == "end":
                    break
    return file_path


# Function determines if the current filepath contains the data of interest, if not it requests
# a direct filepath from the user to use for analysis.


def directorychange():
    """Function runs the FileSet function, in case the use goes to data analysis without setting the csv file."""
    global file_path
    if file_path is None:
        FileSet()
    else:
        pass


# Initializes the data frame. Returns the dataframe.
def init_dataframe():
    """Initalizes the data frame that will be used later on in the analysis."""
    global file_path
    print('\n\n Initializing Dataframe... Using filepath: \n')
    print(file_path, "\n")
    initdframe = pd.read_csv(file_path, encoding='cp1252')
    print("Dataframe created and loaded. Displaying full dataframe...\n", initdframe)
    return initdframe


def sort_dataframe(dframe):
    """Performs an initial sort of the dataframe into the core and required columns."""
    #TODO write an exception block for this range in case the user does not use dilution factors in the template
    print("\n\n Loaded Dataframe: \n")
    df_sorted = dframe[["Well", "Sample", "Normalized Intensity (Cnt/s)", "Dilution Factor", "Diameter (nm)",
                        "Amplitude", "Baseline", "SOS", "%PD",
                        "Range1 Diameter (I) (nm)", "Range1 %Pd (I)", "Range1 %Number (I)",
                        "Range2 Diameter (I) (nm)", "Range2 %Pd (I)", "Range2 %Number (I)",
                        "Range3 Diameter (I) (nm)", "Range3 %Pd (I)", "Range3 %Number (I)",
                        "Range4 Diameter (I) (nm)", "Range4 %Pd (I)", "Range4 %Number (I)",
                        "Range5 Diameter (I) (nm)", "Range5 %Pd (I)", "Range5 %Number (I)",
                        "Number Acqs", "% Acqs Unmarked", "Number Acqs", "Number Marked Acqs", "Item"
                        ]].copy()
    print("df_sorted Printed:", df_sorted)
    return df_sorted

def filter_parameters():
    """place holder function that will be used o ask and store filter parameter variables during analysis"""
    #TODO complete this function and a new menu selection for data analysis, probably make into a class.
    baseline_lower = 0.99
    baseline_upper = 1.01
    sos = 25
    amplitude_limit = 0.1
    percent_acqs_unmarked = 70
    relative_std = 5
    replicate_size = 3

def norm_init(dframe):
    """Generates the data filtered dataframe"""

    def PRsd(x):
        return (x.std() / x.mean()) * 100

    # Variable for the filtered data from df_sorted
    df_filtered = dframe[(dframe['Baseline'] >= 0.99) & (dframe['Baseline'] <= 1.01) & (dframe['SOS'] <= 25)
                         & (dframe['Amplitude'] >= 0.1) & (dframe['% Acqs Unmarked'] >= 70)]

    # Sorted results  by sample, then dilution factor and calculated basic statistic values for the described values
    df_NI = df_filtered.groupby(['Sample', 'Dilution Factor']).agg(
        {'Normalized Intensity (Cnt/s)': ['size', 'mean', 'std', PRsd]}).reset_index().copy()

    # %RSD is set and needs to be at or lower than the provided value
    # and the size (the number of grouped dilution factors) needs to be 3.
    df_rsd = df_NI[
        (df_NI['Normalized Intensity (Cnt/s)', "PRsd"] <= 20) & (df_NI['Normalized Intensity (Cnt/s)', 'size'] == 3)]
    #print("df_filtered", df_filtered)
    #print("df_NI", df_NI)
    print("\n\ndf_rsd", df_rsd)
    #return df_rsd.loc[:, (['Sample', 'Dilution Factor', 'Normalized Intensity (Cnt/s)'], ["", 'mean'])]


    return df_rsd

def select_samples(dframe):
    """ This function uses the sorted data frame and the list of selected samples. The list is used to iterate through
    the sorted dataframe and the selected samples are evaluated accordingly. The dataframe that should be used as an
    argument should be the norm int """
    # Makes a list of lists of sample names and dilution factors that pass the above tests.
    snamer = []
    num_rsd = dframe.to_numpy()
    [snamer.append([i[0], i[1]]) for i in num_rsd if [i[0], i[1]] not in snamer]
    print(num_rsd)
    print(snamer)

    a = snamer
    df = dframe
    df_index = df.set_index(["Sample", "Dilution Factor"])
    print ("Printing df_index: ", df_index)
    verified_list = []
    output_list = []
    list_len = len(a)

    pos1 = 0
    pos2 = 1

    # for loop initiates iteration over list length.
    for i in range(list_len):
        if pos2 < list_len:  # Check to prevent an index error.
            if a[pos1][0] == a[pos2][0]:  # checks it the sample names are the same
                fold = a[pos1][1] / a[pos2][1]
                if fold == 0.5 or fold == 2:  # Confirms if the dilution factor fold difference are correct and begins extracting normalized intensity counts.
                    comparison1 = df_index.loc[(a[pos1][0], a[pos1][1])][("Normalized Intensity (Cnts/s)", "mean")]
                    print("Comparison 1 printing: ", comparison1)
                    #The above line of code returns the sample and dilution factor index values, and then the position of the remaining column.
                    #excluding a column value for norm. Int. appears to be syntactic sugar to including a ':'(splice value).
                    comparison2 = df_index.loc[(a[pos2][0], a[pos2][1])][0]
                    comp_fold = comparison1/comparison2
                    if 1.5 <= comp_fold <= 2.5:  # if norm intensity fold difference is within 2 +/- 25%, append to a new list
                        verified_list.append([a[pos1][0], a[pos1][1], comparison1])
                        verified_list.append([a[pos2][0], a[pos2][1], comparison2])
            pos1 += 1
            pos2 += 1
        else:
            print("\nList scan finished, generating master list.")
            # A new list is generated without repeats.
            [output_list.append(i) for i in verified_list if i not in output_list]


    print('\n Printing Output List: ', output_list)
    print("\n Printing initial list: ", a)
    print("\n Prining verified list: ", verified_list, "\n\n")
    return output_list

def TemplateGenerator():
    print("Template Generator function activated.")


def main():
    """ The main function that prompts the user to make a selection of a task they would like to perform."""
    global file_path
    file_path = "/Users/natedziuba/Library/Mobile Documents/com~apple~CloudDocs/Computer Science/Python/Repos/DLS_Files/DLSTrainingRAW 2.csv"

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
            directorychange()
            df = init_dataframe()
            df_sort = sort_dataframe(df)
            filtered = norm_init(df_sort)
            select_samples(filtered)


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
