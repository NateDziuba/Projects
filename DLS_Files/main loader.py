# ---- Import Zone ----

import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import pandas as pd
import numpy as np
import datetime
import os


# ---- Global Variable Zone ----
# File path selection storage location
# Used in FileSet() function to store the file path of the selected file.
file_path = None
folder_path = None


def main_menu():
    """Main menu to make selections from."""
    print(
        "Main Menu\n"
        "---------\n"
        "0 - Terminate Program.\n"
        "1 - Template Generation.\n"
        "2 - Data Analysis.\n"
        "3 - Select working directory filepath. \n"
        "4 - Print working file-filepath in terminal.\n\n"
    )

def folderset():
    """Function will ask the user for the working folder directory and then stores it as a global variable.
    The working file path and folder directory must be manually set prior to using."""
    global folder_path

    if folder_path is None:
        while True:
            print("Please select the working folder directory filepath for data storage.\n")
            input("Please  input any to continue...\n ")
            root = tk.Tk()
            root.withdraw()

            folder_path = filedialog.askdirectory()
            print("---- The Folder Path has been selected. ----\n")
            os.chdir(folder_path)
            print("The working directory folder path is: ", folder_path, "\n\n")
            break
    else:
        print("Is the following working directory correct?: ", folder_path, "\n\n")
        request_pause = input("Please input Yes or No.\n").lower()
        #TODO add a check if the input is empty or not. If nothing is input it crashes the program. 
        if request_pause == "yes":
            pass
        else: 
            request_pause == "no"
            root = tk.Tk()
            root.withdraw()

            folder_path = filedialog.askdirectory()
            print("---- The  working directory folder path has been selected. ----\n")
            os.chdir(folder_path)
            print("The folder path is: ", folder_path, "\n\n")

def fileset():
    """Function asks the user for a file path. This filepath is then stored as a global variable for future use."""
    global file_path

    if file_path is None:
        # While function loops until a csv file is selected or end has been input to go to the main menu.
        while True:
            print("Please select a CSV file for data analysis.\n")
            input("A selection window will popup, hit enter for the window to appear...\n")

            root = tk.Tk()
            root.withdraw()

            file_path = filedialog.askopenfilename()
            print("---- File has been selected, analyzing for file type.---- \n")

            if Path(file_path).suffix == ".csv":  # Checks if selected file is a csv extension incase user selects incorrect file. 
                print("---File Type is CSV---\n")
                break
            else:
                print("A CSV file was not selected. Please select a csv file for analysis.\n")
                request_pause = input("Please press any key to continue or type end to go to main menu.\n\n").lower()
                if request_pause == "end":
                    break
    else:
        # Needed during analysis. File path selection is run automatically incase alternative files are analyzed
        while True:
            print("Is this the correct file for data analysis?\n", file_path)
            request2 = input("Please enter Yes or No. \n").lower()

            if request2 == "yes":
                break

            else: 
                request2 == "no"
                root = tk.Tk()
                root.withdraw()

                file_path = filedialog.askopenfilename()
                print("---- File has been selected, analyzing for file type.---- \n")

            if Path(file_path).suffix == ".csv":  # Checks if selected file is a csv extension.
                print("----File is a csv extension. Accepting file path.----\n")
                break
            else:
                print("----A CSV file was not selected. Please select a csv file for analysis.----\n")
                request_pause = input("Press any key to continue or type \"END\" to go to the main menu.\n\n").lower()
                if request_pause == "end":
                    break
    return file_path

def directorychange():
    """Function runs the fileset function, in case the use goes to data analysis without setting the csv file."""
    global filepath_path
    if file_path is None:
        fileset()
    else:
        pass


# Initializes the data frame. Returns the dataframe.
def init_dataframe():
    """Initalizes the data frame that will be used later on in the analysis."""
    global file_path
    print('\n\n Initializing Dataframe... Using filepath: \n', file_path, "\n")
    initdframe = pd.read_csv(file_path, encoding='cp1252')
    print("\nDataframe created and loaded. Displaying full dataframe...\n", initdframe)
    return initdframe


class Col_Header:
    """Class is uesd to standardize the headers utilized in this program. Base headers are used for initial processing
    and the cume, and reg, num_reg are used for different aspects of reporting depending on the outcome of the analysis.
    For instance: if %PD is >15% reg headers are used and if PD <15% cume headers are used."""
    def __init__(self, dframe):
        self.df = dframe
        self.heading_list = None
        self.all_headers = self.list_make()

    def list_make(self):
        self.heading_list = list(self.df)

    def numeric_only(self):
        numeric_list = ["Normalized Intensity (Cnt/s)", "Dilution Factor","Amplitude", "Baseline", "SOS",
                             'D10 (nm)', 'D50 (nm)', 'D90 (nm)', 'Span (D90 - D10)/D50',
                             "Number Acqs", "% Acqs Unmarked", "Number Acqs", "Number Marked Acqs"]
        reg_list = self.reg()

        [self.numeric_list.append(i) for i in reg_list]

        return self.numeric_list

    def base(self):
        #TODO add  "Lot Number", back to base when finished.
        base_list = ["Well", "Sample", "Sample Name", "Normalized Intensity (Cnt/s)", "Dilution Factor", "%PD",
                     'D10 (nm)', 'D50 (nm)', 'D90 (nm)', 'Span (D90 - D10)/D50', "Diameter (nm)",
                        "Amplitude", "Baseline", "SOS",  "Number Acqs", "% Acqs Unmarked", "Number Acqs",
                        "Number Marked Acqs", "Item", "Date", "Time Stamp"]
        return base_list

    def cume(self):
        self.cume_list = ["Well", "Sample", "Sample Name", "Normalized Intensity (Cnt/s)", "Dilution Factor", "Diameter (nm)",
                                "Amplitude", "Baseline", "SOS", "%PD", 'D10 (nm)', 'D50 (nm)', 'D90 (nm)', 'Span (D90 - D10)/D50',
                                "Number Acqs", "% Acqs Unmarked", "Number Acqs", "Number Marked Acqs", "Item",
                                "Date", "Time Stamp"]
        return self.cume_list

    def num_reg(self):
        self.reg_list = ["Baseline", "SOS", "Amplitude","Normalized Intensity (Cnt/s)", "%PD", 'D10 (nm)', 'D50 (nm)',
                         'D90 (nm)', 'Span (D90 - D10)/D50',"Diameter (nm)"]
        ranges = ["Range1", "Range2", "Range3", "Range4", "Range5"]
        range_list =[]
        [range_list.append(j) for i in ranges for j in self.heading_list if j.startswith(i) ]
        [self.reg_list.append(i) for i in range_list]

        return self.reg_list

    def reg(self):
        reg_list = []
        ranges = ["Range1", "Range2", "Range3", "Range4", "Range5"]
        range_list =[]
        [range_list.append(j) for i in ranges for j in self.heading_list if j.startswith(i) ]
        base = self.base()
        [reg_list.append(i) for i in base]
        [reg_list.append(i) for i in range_list]

        return reg_list

    def help(self):
        print("Help method...\nThe available methods are:\n"
              "1. numeric_only\n"
              "2. reg\n"
              "3. num_reg\n"
              "4. cume\n"
              "5. base")


def sort_dataframe(dframe):
    """Performs an initial sort of the dataframe into the core and required columns."""
    #TODO write an exception block for this range in case the user does not use dilution factors in the template
    print("\n\n Sort Dataframe initiated...\n")
    main_list = Col_Header(dframe)
    #print("Printing main_list   :   ", main_list.reg())

    df_sorted = dframe[main_list.reg()].replace("--", np.NaN, regex=False).replace("", np.NaN, regex=False)
    df_sorted[["%PD"]] = df_sorted[["%PD"]].replace("Multimodal", 999, regex=False)
    #The %PD list has to be changed to a float otherwise the analysis gets difficult. 
    #The Dynamics software (where the data originates) uses floats and strings, we want to convert the string 'multimodal'
    #into a float, so we set that value as a floating number of 999. %PD is not calculated anywhere. 
    df_sorted[main_list.num_reg()] = df_sorted[main_list.num_reg()].astype("float")
    
    #print("df_sorted :    \n", df_sorted.dtypes)
    #print("%pd type:  ", df_sorted["%PD"].dtypes)
    print("Dataframe has been sorted, displaying: \n", df_sorted)
    return df_sorted


def filter_parameters():
    """place holder function that will be used to ask and store filter parameter variables during analysis"""
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
    print("\n Initiatiing parameter filter:...\n\n")
    # Variable for the filtered data from df_sorted
    df_filtered = dframe[(dframe['Baseline'] >= 0.99) & (dframe['Baseline'] <= 1.01) & (dframe['SOS'] <= 25)
                         & (dframe['Amplitude'] >= 0.1) & (dframe['% Acqs Unmarked'] >= 70)]

    # Sorted results  by sample, then dilution factor and calculated basic statistic values for the described values
    df_NI = df_filtered.groupby(["Sample Name", 'Dilution Factor']).agg(
        {'Normalized Intensity (Cnt/s)': ['size', 'mean', 'std', PRsd]}).reset_index().copy()

    # %RSD is set and needs to be at or lower than the provided value
    # and the size (the number of grouped dilution factors) needs to be 3.
    df_rsd = df_NI[
        (df_NI['Normalized Intensity (Cnt/s)', "PRsd"] <= 30) & (df_NI['Normalized Intensity (Cnt/s)', 'size'] >= 3)]
    print("df_filtered", df_filtered)
    print("df_NI", df_NI)
    print("\n\n Filtered and grouped dataset finished, loading df_rsd: ....\n\n", df_rsd)
    #return df_rsd.loc[:, (['Sample', 'Dilution Factor', 'Normalized Intensity (Cnt/s)'], ["", 'mean'])]


    return df_rsd


def select_samples(dframe):
    """ This function uses the sorted data frame and the list of selected samples. The list is used to iterate through
    the sorted dataframe and the selected samples are evaluated accordingly. The dataframe that should be used as an
    argument should be from the norm int """
    # Makes a list of lists of sample names and dilution factors that pass the above tests, exports into numpy.
    snamer = []
    num_rsd = dframe.to_numpy()
    [snamer.append([i[0], i[1]]) for i in num_rsd if [i[0], i[1]] not in snamer]
    print(num_rsd)
    print(snamer)

    a = snamer
    df = dframe
    df_index = df.set_index(["Sample Name", "Dilution Factor"], drop=True)
    print("Printing df_index: ", df_index)
    verified_list = []
    output_list = []
    list_len = len(a)

    pos1 = 0
    pos2 = 1

    for i in range(list_len):
        if pos2 < list_len:  # Check to prevent an index error.
            if a[pos1][0] == a[pos2][0]:  # checks if the sample names are the same
                fold = a[pos1][1] / a[pos2][1]
                # Confirms if the dilution factor fold difference are correct and extracts normalized intensity counts.
                if fold == 0.5 or fold == 2:
                    comparison1 = df_index.loc[(a[pos1][0], a[pos1][1]), ('Normalized Intensity (Cnt/s)', 'mean')]
                    #print("Printing Comp1: ", comparison1)
                    # The above line returns the sample and df index values, then the position of the remaining column.
                    # excluding a col.value for norm. Int. appears to be syntac sugar to including a ':'(splice value)
                    comparison2 = df_index.loc[(a[pos2][0], a[pos2][1]), ('Normalized Intensity (Cnt/s)', 'mean')]
                    comp_fold = comparison1/comparison2
                    if 1.4 <= comp_fold <= 2.6:  # if norm intensity fold dif is within 2 +/- 30%, append to a new list
                        verified_list.append([a[pos1][0], a[pos1][1], comparison1])
                        verified_list.append([a[pos2][0], a[pos2][1], comparison2])
            pos1 += 1
            pos2 += 1
        else:
            print("\nList scan finished, generating master list.\n\n")
            # A new list is generated without repeats.
            [output_list.append(i) for i in verified_list if i not in output_list]

    #print('\n Printing Output List: ', output_list)
    #print("\n Printing initial list: ", a)
    #print("\n Printing verified list: ", verified_list, "\n\n")
    print("--------------------------------------")
    return output_list


def cum_reg_report(list, dframe):
    """Function takes a list of lists that contain the sample name, dilution factor, and normalized intensity
    that have passed assay acceptance criteria. This list is used to pull cummulant or regularization values and
    generates basic statistics on it.The second arg is the sorted dataframe. Use the verified list from the 
    select samples function. Use the sorted data frame from sort_dataframe function."""
    global file_path
    print("printing file path: ", file_path)
    foldersave = ""
    header_list = Col_Header(dframe)
    excel_report_date = datetime.datetime.now().strftime('DLS_Report_%d%b%y_%H%M.xlsx')

    for i in range(len(file_path)):
        if file_path[-(i+1):len(file_path)-i] == '/':
            foldersave = file_path[:-i]
            print('File Path if statement passed...')
            print("Folder Save:   ", foldersave)
            break
    print("printing folder save path: ", foldersave)
    accepted_values = list
    df_sorted = dframe
    df_index = df_sorted.set_index(["Sample Name", "Dilution Factor"], drop=False)
    dfidx_sort = df_index.sort_index()
    
    writer = pd.ExcelWriter(excel_report_date, engine='xlsxwriter')
    
    empty = pd.DataFrame()
    empty.to_excel(writer, sheet_name='DLS Results')
    row_counter = 0
    
    for i in range(len(accepted_values)):
        # is sample name
        idx1 = accepted_values[i][0]
        # is dilution factor
        idx2 = accepted_values[i][1]
        slct_df = dfidx_sort.loc[(idx1, idx2), :]
        if slct_df.mean(axis=0, numeric_only=True)["%PD"] <= 15.0:
            # Save the data, the triplicate rows and the descriptives, to an excel sheet
            # with pd.ExcelWriter(foldersave, engine='xlsxwriter') as writer:
            cume = slct_df[header_list.cume()]
            cume.to_excel(writer, sheet_name='DLS Results', startrow = row_counter)
            row_counter = row_counter + len(cume.index) + 2
            cume_stat = cume.describe(include='all')
            
            cume_stat.to_excel(writer, sheet_name='DLS Results', startrow = row_counter, startcol=1)
            row_counter = row_counter + len(cume_stat.index) + 3
        else:
            cume = slct_df[header_list.reg()]
            print("printing Cume:.... ", cume["Lot Number"], "  ", cume["Dilution Factor"])
            
            cume.to_excel(writer, sheet_name='DLS Results', startrow = row_counter)
            row_counter = row_counter + len(cume.index) + 2
            
            cume_stat = cume.describe(include='all') 
            cume_stat.to_excel(writer, sheet_name='DLS Results', startrow = row_counter, startcol = 1)
            row_counter = row_counter + len(cume_stat.index) + 3

    writer.close()


def template_generate():
    # main call function to make the template
    headers = headers_generate()
    well = wells()
    ln = lot_number()
    wells_list = well_list(well, ln)
    ln_list = lot_number_list(ln, well)
    dilution = dilutions(ln, well)
    samp_name = generic_sample_names(ln, well)
    template_gen(well, ln, wells_list, ln_list, dilution, headers, samp_name)


def headers_generate():  # Generate headers if needed
    default_headers = ["Well", "Sample", "Dilution Factor", "Sample Name"]
    print("The currently defined headers: \n")
    [print(i) for i in default_headers]
    print("\n")
    request = input("Are additional headers required? Answer Yes or No.\n Response: ").lower()
    template_headers = default_headers
    if request == "yes":
        new_headers = [x.strip() for x in list(input("Add headers separated with commas ','.\n Response: ").split(','))]
        ##TODO added mechanism to append default headers to the template headers list##
        for i in new_headers:
            template_headers.append(i)
    else:
        print("All necessary headers are present.\n")
    return template_headers


def wells():  # define the number of wells to be used.
    wells = 384
    request = input("Default plate size is 384-well, do you wish to change? \n Response: ")
    if request == 'yes':
        well_check = False
        while not well_check:
            try:
                well_request = int(input("Choose between: 384 OR 96 wells. \n Response:"))
                if well_request == 384:
                    well_check = True
                    print("Selected well size: ", wells)
                elif well_request == 96:
                    wells = well_request
                    well_check = True
                    print("Selected well size: ", wells)
            except:
                print("Choose between 384 or 96 wells. Input only a number.\n\n")
    return wells


def well_list(well_number, lot_numbers):
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
    # appending the well number to the well letter and creating a list in well.label variable.
    wells = well_number
    well_list = []
    for i in range(len(lot_numbers)):
        if wells == 384:  # checking number of columns to assign well count.
            plate_col = 24
        elif wells == 96:
            plate_col = 12
        for j in range(plate_col):
            number = str(j + 1)
            well_list.append(alphabet[i] + number)
    return well_list
    

def lot_number():
    lot_numbers = []
    print("\nCurrent Samples in the script: ", lot_numbers)
    # clear_request = input("\nDo you want to clear the list? Respond with Yes or No. \n Response:  ").lower()
    # print("\n\n")
   # if clear_request == "yes":
        # lot_numbers = []
    request = [x.strip() for x in list(input("Please input each sample name to be analyzed. 384-well max of 16, "
                                             "96 well,max of 8."
                                             "\nSeparate each name with a comma ','. Response:  ").split(','))]
    [lot_numbers.append(i) for i in request]
    return lot_numbers


def lot_number_list(sample_number_names, wells):
    number_of_samples = sample_number_names
    lot_num_list = []
    plate_col = 0
    if wells == 384:  # checking number of columns to assign well count.
        plate_col = 24
    elif wells == 96:
        plate_col = 12
    [lot_num_list.append(number_of_samples[i]) for i in range(len(number_of_samples)) for j in range(plate_col)]
    return lot_num_list


def dilutions(lot_numbers, wells):
    # Dilutions for number of samples listed in sample name.
    print("(8) - 2-fold dilutions will be prepared.\n")
    dilutions = []
    dilution_list = []
    dilution_number = None
    if wells == 384:
        dilution_number = 8
    elif wells == 96:
        dilution_number = 4
    [dilutions.append(2 ** i) for i in range(dilution_number)]
    print(dilutions)
    [dilution_list.append(j) for m in range(len(lot_numbers)) for i in range(3) for j in dilutions]
    print(dilution_list)
    return dilution_list

def generic_sample_names(sample_name_list, wells):
    generic_name_list = ['Sample 1', 'Sample 2', 'Sample 3', 'Sample 4', 'Sample 5',
                        'Sample 6', 'Sample 7', 'Sample 8', 'Sample 9', 'Sample 10', 
                        'Sample 11', 'Sample 12', 'Sample 13', 'Sample 14', 'Sample 15',
                        'Sample 16']
    
    number_of_samples = len(sample_name_list)
    
    plate_col = 0
    if wells == 384:  # checking number of columns to assign well count.
        plate_col = 24
    elif wells == 96:
        plate_col = 12
    generated_sample_names = []
    
    [generated_sample_names.append(generic_name_list[i]) for i in range((number_of_samples)) for j in range(plate_col)]
    print(generated_sample_names)
    return generated_sample_names
    
def template_gen(wells, ln, well_label, t_samplelist, dilution_list, header_list, generic_name_list):
    # Aggregate list for well, samplename, and dilution factor
    ##TODO generate mechanism to create a dictionary from the template_headers list and a list of lists
    global folder_path
    print("The folder path is: ", folder_path, "\n\n")
    if folder_path == None:
        folderset()
    
    template_date = datetime.datetime.now().strftime('DLS_Template_%d%b%y_%H%M')
    master_list = {'Well': well_label,
                   'Sample Name': t_samplelist,
                   'Dilution Factor': dilution_list,
                   'Sample': generic_name_list}

    for i in header_list:
        if i not in master_list:
            master_list[i] = Additional_Solvents(wells, i, ln).header_value()
    template_import = pd.DataFrame(master_list)

    template_import.to_csv(template_date, index=False)
    print("\nExported the template to the defined working directory.\n\n")
    return template_import


class Additional_Solvents():
    """Class takes inputs:
    well number as 'wells'
    newly added header as 'header'
    list of lot numbers as 'ln'

    This class will take a new header and fill in the value needed for all samples.
    This class will not allow for variable input or allow for changed to only certain samples (sample names)
    """
    def __init__(self, wells, header, ln):
        self.well_number = wells
        self.new_header = header
        self.lot_number_list = ln
        self.default_headers = ["Well", "Lot Number", "Dilution Factor"]
        self.col_number = None
        if self.well_number == 384:
            self.col_number = 24
        elif self.well_number == 96:
            self.col_number = 12
    def header_value(self):
        # main function to add headers to the additional headers added/requested.
        print("The header ", self.new_header, " has been added.")
        header_key_input = input("Please input a single value to define this header, i.e., for solvent input PBS. \n")
        header_key_list = []
        [header_key_list.append(header_key_input) for i in range(len(self.lot_number_list)) for j in range(self.col_number)]
        print("Added new header value: ", self.new_header)
        return header_key_list


def main():
    """ The main function that prompts the user to make a selection of a task they would like to perform."""
    global file_path
    #file_path = ("/Users/natedziuba/Library/Mobile Documents/com~apple~CloudDocs/Computer Science/Python/Repos"
                # "/DLS_Files/pius 31oct23 test data.csv")
    #file_path = "/Users/NDziuba/OneDrive - FUJIFILM/VAD/VAD/Innovation/Projects/DLS_Files"
    # Initiation of the prompt.
    print("Welcome to the DLS Python script, please select an option below.\n")
    # Loops to allow the user to select an option, and requires only int.

    "--- Variable Initiation For Storage While Running ---"
    # TODO put in a funtion to list and define the adjustment parameters.
    baseline_lower = 0.99
    baseline_upper = 1.01
    sos = 25
    amplitude_limit = 0.1
    percent_acqs_unmarked = 70
    relative_std = 5
    replicate_size = 3

    while True:
        main_menu()

        try:
            request = int(input("Make a selection from the table above.\n\n"))
        except ValueError:
            print("Your input is incorrect. Make a selection from 0-3.\n")
            continue
        if request == 1:
            template_generate()
        elif request == 2:
            directorychange()
            df = init_dataframe()
            df_sort = sort_dataframe(df)
            filtered = norm_init(df_sort)
            verified_list = select_samples(filtered)
            cum_reg_report(verified_list, df_sort)

        elif request == 3:
            folderset()
        elif request == 4:
            print("\nThe filepath is:\n",file_path, "\n\n")
        elif request == 0:
            print("Thank-you for using the DLS python program.\n\n")
            break
        else:
            print("Invalid choice. \n")


if __name__ == "__main__":
    main()
