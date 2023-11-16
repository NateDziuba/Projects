import pandas as pd
import numpy as np
import os as os
import csv

class DataFrameGen:
    df = "test"
    
    #initializing the class.
    def __init__(self):

        self.directorychange()
        self.init_dataframe()

   
    ### Function determines if the current filepath contains the data of interest, if not it requests
    ### a direct filepath and returns a raw string.
    def directorychange(self):
        print(os.getcwd())
        pathdir = r'{}'.format(os.getcwd())
        request = input("Is this the above filepath where your data is stored? Yes or No\n").lower()
        print("\n")
        if request == "yes":
            print("Filepath to data is:" + pathdir)
            pass
        if request =='no':
            self.pathdir = r'{}'.format(input("Paste the filepath where your data is stored (i.e., C:...).\n \n"))
            os.chdir(pathdir)
            print("\nFilepath has been changed to:    " + os.getcwd())
        else:
            print("Please input either Yes or No.\n \n")
            
            
    def init_dataframe(self):
        print('\n\n initi datframe activated \n\n')
        print(self.pathdir)
        for i in os.listdir():
            print(i)
            if i[-3:] == 'csv':
                
                request = input("Is this the correct file? (yes or no) File: ", i).lowercase()
                if request == 'yes':
                    self.df = pd.read_csv(os.listdir(), encodinf = 'cp1252')
        print(self.df)

        return(df)
    
    
    
def FrameSort(df):
    df_sorted = df[["Well", "Sample", "Normalized Intensity (Cnt/s)", "Dilution Factor","Diameter (nm)", 
                  "Amplitude","Baseline", "SOS","%PD",
    "Range1 Diameter (I) (nm)", "Range1 %Pd (I)", "Range1 %Number (I)",
    "Range2 Diameter (I) (nm)", "Range2 %Pd (I)", "Range2 %Number (I)",
    "Range3 Diameter (I) (nm)", "Range3 %Pd (I)", "Range3 %Number (I)",
    "Range4 Diameter (I) (nm)", "Range4 %Pd (I)", "Range4 %Number (I)",
    "Range5 Diameter (I) (nm)", "Range5 %Pd (I)", "Range5 %Number (I)",
    "Number Acqs", "% Acqs Unmarked", "Number Acqs", "Number Marked Acqs", "Item"
   ]].copy()
    
    return(df_sorted)



def FrameFilter(df_sorted):
    df_filtered = df_sorted[(df_sorted['Baseline'] >= 0.99) & (df_sorted['Baseline'] <= 1.01)& (df_sorted['SOS'] <= 10) 
          & (df_sorted['Amplitude'] >= 0.1) & (df_sorted['% Acqs Unmarked'] >= 70)].copy()
    return(df_filtered)


def PRsd(x):
    return (x.std() / x.mean())*100

def NormInt():
    
    #Variable for the filtered data from df_sorted
    df_filtered = df_sorted[(df_sorted['Baseline'] >= 0.99) & (df_sorted['Baseline']<=1.01)& (df_sorted['SOS'] <= 25) 
          & (df_sorted['Amplitude'] >= 0.1) & (df_sorted['% Acqs Unmarked'] >= 70)]
    
    # Sorted results  by sample, then dilution factor and calculated basic statistic values for the described values    
    df_NI = df_filtered.groupby(['Sample', 'Dilution Factor']).agg({'Normalized Intensity (Cnt/s)' : ['size','mean', 'std', PRsd]}).reset_index().copy()
    
    #%RSD needs to be 5% or lower and the size (the number of grouped dilution factors) needs to be 3.
    df_rsd = df_NI[(df_NI['Normalized Intensity (Cnt/s)', "PRsd"] <=5) & (df_NI['Normalized Intensity (Cnt/s)', 'size'] == 3)]
    print("df_filtered", df_filtered)
    print("df_NI", df_NI)
    print("\n\ndf_rsd", df_rsd)
    return(df_rsd.loc[:,(['Sample', 'Dilution Factor', 'Normalized Intensity (Cnt/s)'], ["", 'mean'])])    
    
#generate a list of non repeating sample names from the normalized intensity data that has been filtered

def SelectSamples():
    df = NormInt()

    sname = df['Sample'].tolist()
    snamer = []
    [snamer.append(i) for i in sname if i not in snamer]

    print(snamer)

    for i in snamer:
        if df['Sample'] is i:
            print("True")
    return(snamer)

""" Template Generator"""

###Global Variables
#Generate list for default headers that are required
default_headers = ["Well", "Sample", "Dilution Factor"]

#Sample Names desired
samplename = []

#Sample list for dataframe
samplelist = []

#sample number from list
samplenumber = 0

#Dilution list for each sample well for dataframe
dilution_list = []


def TemplateGenerate():
    HeadersGenerate()
    #Generate the dataframe 
    template_import = pd.DataFrame(columns=[template_headers])
    SampleName()
    Wells()
    Dilutions()
    Datacsv()
    
    
def HeadersGenerate(): #Generate headers if needed
    print ("The currently defined headers: \n")
    [print (i) for i in default_headers]
    print("\n")
    request = input("Are additional headers required? Answer Yes or No.\n Response: ").lower()
    template_headers = default_headers
    if request == "yes":
        new_headers = [x.strip() for x in list(input("Add headers separated with commas ','.\n Response: ").split(','))]
        ##TODO added mechanism to append default headers to the template headers list##
        for i in new_headers:
            template_headers.append(i)
    else:print("All necessary headers are present.\n")
    return template_headers
        
def Wells():#define the number of wells to be used.
    wells = 384
    #  well label variable for dataframe
    well_label = []
    request = input("Default plate size is 384-well, do you wish to change? \n Response: ")
    if request == 'yes':
        well_check = False
        while not well_check:
            try:
                well_request = int(input("Choose between: 384 OR 96 wells. \n Response:"))
                if well_request == 384 or well_request == 96:
                    wells = well_request
                    well_check = True
                    print("Selected well size: ", wells)
            except:
                print("Choose between 384 or 96 wells. Input only a number.\n\n")
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
    #appending the well number to the well letter and creating a list in well.label variable. 
    well_list = []
    for i in range(len(samplename)):
        if wells = 384:#checking number of columns to assign well count.
            plate_col = 24
        elif wells = 96:
            plate_col = 12
        for j in range(plate_col):
            number = str(j+1)
            well_label.append(alphabet[i]+number)
    return well_list
        
        
    
def SampleName():
    global samplename
    global samplelist
    print("\nCurrent sample names in the script: ", samplename)
    clear_request = input("/nDo you want to clear the list? Respond with Yes or No. \n Response:  ").lower()
    print("\n\n")
    if clear_request == "yes":
        samplename = []
        samplelist = []
    
        request = [x.strip() for x in list(input("Please input each sample name to be analyzed. 384-well max of 16, 96 well,\
        max of 8.\nSeparate each name with a comma ','. Response:  ").split(','))]
        [samplename.append(i) for i in request]
    samplenumber = len(samplename)
    [samplelist.append(samplename[i]) for i in range(samplenumber) for j in range(24)]
    
def Dilutions():

    ##Dilutions for number of samples listed in sample name.
    dilutions = []
    global dilution_list
    dilution_list = []
    [dilutions.append(2**i) for i in range(8)]
    print(dilutions)
    [dilution_list.append(j) for m in range(len(samplename)) for i in range(3) for j in dilutions]
    print(dilution_list)
        
def DataframeGenerate():
   
    #Aggregate list for well, samplename, and dilution factor
    
    ##TODO generate mechanism to create a dictionary from the template_headers list and a list of lists
    master_list = {'Well' : well_label, 
                  'Sample' : samplelist,
                  'Dilution Factor' : dilution_list}
    template_import = pd.DataFrame(master_list)
    return(template_import)

def Datacsv():
    df = DataframeGenerate()
    print(df)
    df.to_csv(r"C:\Users\NDziuba\PythonDump\templatedoc_Samplenumbers.csv", index=False)
    
    

df = DataFrameGen()