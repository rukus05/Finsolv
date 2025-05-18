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
    # Create a dict representing the Chart of Accounts.  See Dict\CoA.txt for what it looks like
    dict_COA = getCOA(df_COA_file)
    
    # Create a list to hold the payroll items that are Debit and Credit Accounts, respectively.  
    debit_accounts = []
    credit_accounts = []
    # Loop through the dictionary to determine which are Debit and Credit, and place these in the appropriate list created directly above.
    for k, v in dict_COA.items():
        #print(k)
        #print(v)
        if v['DR/CR'] == 'Debit':
            debit_accounts.append(k)
        elif v['DR/CR'] == 'Credit':
            credit_accounts.append(k)
        
  

    # Get the Dept Location lookup File
    print('Select the latest Dept-to-Location lookup file:')
    z = FilePrompt()
    df_d2l_file = pd.read_excel(z)
    df_d2l_file = df_d2l_file.reset_index()
    df_d2l_file.fillna(0, inplace=True)
    # Create a dict representing the Dept Location Lookup.  See Dict\Dept_to_Loc.txt for what it looks like
    dict_d2l = get_dept_to_location(df_d2l_file)
    #print(dict_d2l)
    

    
    
    # Read in Data from the "RawData.xlsx" file.
    print('Select the raw data file to run Payroll for:')
    f = FilePrompt()
    df_afc = pd.read_excel(f)
    #df_afc = pd.read_excel(f, dtype={'Home Department Code': str})
    df_afc = df_afc.reset_index()
    # Add these columns to the raw data Dataframe.  The values will be provided in a lookup against Primary Job Title.  See the iterrows loop.
    df_afc['Department ID'] = ''
    df_afc['LOCATION'] = ''
    df_afc['Class'] = ''
    
    # Create a list based on the keys of the COA dict.  These are the columns used for Journal Entries, and will be used to fill df_Output from the GroupBy object below.
    JE_list = list(dict_COA)

    # Vector summarization that can possibly be used elsewhere; more effective method
    # So, keeping this as reference.
    #df_afc['Credit Sum'] = df_afc[credit_accounts].sum(axis=1)
    #df_afc['Debit Sum'] = df_afc[debit_accounts].sum(axis=1)

    # Convert the Pay Date column to a datetime data type
    df_afc['Payroll pay date'] = pd.to_datetime(df_afc['Payroll pay date'])
    # Remove the hours, minutes, and seconds
    df_afc['Payroll pay date'] = df_afc['Payroll pay date'].dt.date
    
    # Use the Primary Job Title from the Input to determine the rows Department ID, Location, and Class--all defined in the Dept to Loc mapping dict, dict_d2l.
    for index, row in df_afc.iterrows():
        df_afc.loc[index, 'Department ID'] = dict_d2l[df_afc.loc[index, 'Primary job title']]['Department ID']
        df_afc.loc[index, 'LOCATION'] = dict_d2l[df_afc.loc[index, 'Primary job title']]['LOC']
        df_afc.loc[index, 'Class'] = dict_d2l[df_afc.loc[index, 'Primary job title']]['Class']
        #print (df_afc.loc[index, 'Department ID'])
        
    # Create new Dataframe for the Output.
    df_Output = pd.DataFrame(columns=['DEPARTMENT', 'LOCATION',  'Class', 'Pay Date', 'Pay Period', 'GL Account', 'Dr', 'CR', 'Description'])
    

    # Group the Data Frame by Depatment ID, Location, Class, and payroll pay date.
    df_groupby = df_afc.groupby(['Department ID', 'LOCATION', 'Class', 'Payroll pay date'])
    
    #print(df_afc.columns)
    # Loop through the groupby object.
    for groupings, row in df_groupby:
        # Create a dictionary whose Keys are the Journel entry items.  
        # The values will be a list representing [the sums for the Journal Entry (Payroll) items, the corresponding G/L Accounts].
        # Both initialized to 0.
        JE_dict = {key: [0, 0] for key in JE_list}
    
        for i in JE_list:
            # Variable to hold the type of account:  Credit, Deibt, or DR/CR
            account = ''
            #The if/elif below checks to see what the Payroll Item is:  
            # It sums the appropriate column 
            # defines the GL according to the Dept (gropuings[0]), 
            # if the sum is not 0 (actually contains a value), then print the row into df_Output
            if i in debit_accounts:
                account = "Debit"
                JE_dict[i][0] += row[i].sum()
                JE_dict[i][1] = dict_COA[i][groupings[0]]
                if JE_dict[i][0] != 0:
                    df_Output.loc[len(df_Output.index)] = [groupings[0], groupings[1], groupings[2], groupings[3], row['Payroll'], JE_dict[i][1], JE_dict[i][0], '', i]
            elif i in credit_accounts:
                account = "Credit"
                JE_dict[i][0] += row[i].sum()
                JE_dict[i][1] = dict_COA[i][groupings[0]]
                if JE_dict[i][0] != 0:
                    df_Output.loc[len(df_Output.index)] = [groupings[0], groupings[1], groupings[2], groupings[3], row['Payroll'], JE_dict[i][1], '', JE_dict[i][0], i]
            # This last elif adds both a debit and credit row
            # The debit row is determinied similarly to the first if statement above
            # The credit row has the same amount in the 'Debit' column filled in the 'Credit' column.  The GL is taken from the CR GL Account in the Dep-Loc maaping (dict_d2l)
            elif dict_COA[i]['DR/CR'] == 'DR/CR':
                JE_dict[i][0] += row[i].sum()
                JE_dict[i][1] = dict_COA[i][groupings[0]]
                CR_GL = dict_COA[i]['CR GL Account']
                if JE_dict[i][0] != 0:
                    df_Output.loc[len(df_Output.index)] = [groupings[0], groupings[1], groupings[2], groupings[3], row['Payroll'], JE_dict[i][1], JE_dict[i][0], '', i]
                    df_Output.loc[len(df_Output.index)] = [groupings[0], groupings[1], groupings[2], groupings[3], row['Payroll'], CR_GL, '', JE_dict[i][0], i]


            
            

        
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