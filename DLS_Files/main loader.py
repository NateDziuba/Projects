# ---- Import Zone ----

import tkinter as tk
from tkinter import filedialog

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
    return(file_path)

def DataAnalysis():
    print("Data Analysis function activated.")

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
