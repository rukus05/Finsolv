import pandas as pd
import time
import numpy as np
import re
import tkinter as tk
from tkinter import filedialog as fd
#from definitions import coa_dict as coa
#from afc_module.definitions import coa_dict as coa
from afc_module.definitions import hdc_list as hdcl
from afc_module.definitions import roll_up_accts as rollup
from afc_module.definitions import remove_acct_list as remove_accts
from zpack.fns import FilePrompt
from zpack.fns import save_dataframe
from get_coa import getCOA
from get_coa import get_dept_to_location
#from definitions import baseline_accounts as baseline


def main():
    
    start = time.time()

    # Get the updated Chart of Accounts File
    print('Select the latest Chart of Accounts file:')
    z = FilePrompt()
    df_COA_file = pd.read_excel(z)
    df_COA_file = df_COA_file.reset_index()
    df_COA_file.fillna(0, inplace=True)

    dict_COA = getCOA(df_COA_file)
    #print(dict_COA)
    #  To see how dictionary looks, see the COA_Dict.py file in the Dict Directory
    # Create a list for Debit and Credit Accounts.
    debit_accounts = []
    credit_accounts = []
    for k, v in dict_COA.items():
        #print(k)
        #print(v)
        if v['DR/CR'] == 'Debit':
            debit_accounts.append(k)
        elif v['DR/CR'] == 'Credit':
            credit_accounts.append(k)
        
    #print('The debit accounts are:', debit_accounts)
    #print('')
    #print('The credit accounts are', credit_accounts)
    

    # Get the Dept Location lookup File
    print('Select the latest Dept-to-Location lookup file:')
    z = FilePrompt()
    df_d2l_file = pd.read_excel(z)
    df_d2l_file = df_d2l_file.reset_index()
    df_d2l_file.fillna(0, inplace=True)

    dict_d2l = get_dept_to_location(df_d2l_file)
    #print(dict_d2l)
    

    
    
    # Read in Data from the "RawData.xlsx" file.
    print('Select the raw data file to run Payroll for:')
    f = FilePrompt()
    df_afc = pd.read_excel(f)
    #df_afc = pd.read_excel(f, dtype={'Home Department Code': str})

    df_afc = df_afc.reset_index()
    # Fill all blank cells with zeros.  
    # It's critiacal that any columns you do calculations do not have blanks.
    #df_afc.fillna(0, inplace=True)
    
    # Add to the raw data Dataframe 
    df_afc['Department ID'] = ''
    df_afc['LOCATION'] = ''
    df_afc['Class'] = ''
    
    # Put column headers into a Lis
    all_col_headers = list(df_afc.columns)
    #print(all_col_headers)
    #print('')   

    # Create a list based on the keys of the COA dict.  These are the columns used for Journal Entries
    JE_list = list(dict_COA)
    
    
    #df_afc['Credit Sum'] = df_afc[credit_accounts].sum(axis=1)
    #df_afc['Debit Sum'] = df_afc[debit_accounts].sum(axis=1)

    # Convert the Pay Date column to a datetime data type
    df_afc['Payroll pay date'] = pd.to_datetime(df_afc['Payroll pay date'])
    # Remove the hours, minutes, and seconds
    df_afc['Payroll pay date'] = df_afc['Payroll pay date'].dt.date
    
    #Verify company you're running this program for by printing out the company name
    #print('This input file is for Company ' + df_afc['Company Code'].iloc[0])

    for index, row in df_afc.iterrows():
        df_afc.loc[index, 'Department ID'] = dict_d2l[df_afc.loc[index, 'Primary job title']]['Department ID']
        df_afc.loc[index, 'LOCATION'] = dict_d2l[df_afc.loc[index, 'Primary job title']]['LOC']
        df_afc.loc[index, 'Class'] = dict_d2l[df_afc.loc[index, 'Primary job title']]['Class']
        #print (df_afc.loc[index, 'Department ID'])
    '''
    print("Test the DF_AFC till here")
    # Start the "Save As" dialog box.
    app = tk.Tk()
    app.title("Save File As")
    status_label = tk.Label(app, text="", fg="green")
    status_label.pack()
    save_button = tk.Button(app, text="Save as", command=save_dataframe(df_afc, status_label))
    save_button.pack(padx=20, pady=10)
    '''
       
    # Create new Dataframe for the Output.
    df_Output = pd.DataFrame(columns=['DEPARTMENT', 'LOCATION',  'Class', 'Pay Date', 'Pay Period', 'GL Account', 'Dr', 'CR', 'Description'])
    

    # Group the Data Frame by Company Code,  Home Department Code, and Location.
    df_groupby = df_afc.groupby(['Department ID', 'LOCATION', 'Class', 'Payroll pay date'])
    #Verify the groupby columns
    #print(df_afc.columns)

    for groupings, row in df_groupby:
        #print(groupings)
        #print(row)
        # Create a dictionary to hold the sums for the Journal Entry items (initialized to 0) and G/L Accounts (initialized to 0)
        JE_dict = {key: [0, 0] for key in JE_list}
    
        for i in JE_list:
            account = ''
            if i in debit_accounts:
                account = "Debit"
                JE_dict[i][0] += row[i].sum()
                JE_dict[i][1] = dict_COA[i][groupings[0]]
                df_Output.loc[len(df_Output.index)] = [groupings[0], groupings[1], groupings[2], groupings[3], row['Payroll'], JE_dict[i][1], JE_dict[i][0], '', i]
            elif i in credit_accounts:
                account = "Credit"
                JE_dict[i][0] += row[i].sum()
                JE_dict[i][1] = dict_COA[i][groupings[0]]
                df_Output.loc[len(df_Output.index)] = [groupings[0], groupings[1], groupings[2], groupings[3], row['Payroll'], JE_dict[i][1], '', JE_dict[i][0], i]
            

        
    runningtime = time.time() - start
    print("Save the Output File...")
    # Start the "Save As" dialog box.
    app = tk.Tk()
    app.title("Save File As")
    status_label = tk.Label(app, text="", fg="green")
    status_label.pack()
    save_button = tk.Button(app, text="Save as", command=save_dataframe(df_Output, status_label))
    save_button.pack(padx=20, pady=10)
   
    
    print("The execution time is:", runningtime)




if __name__ == "__main__":
    main()