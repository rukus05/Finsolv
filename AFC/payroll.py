import pandas as pd
import time
import numpy as np
import re
import tkinter as tk
from tkinter import filedialog as fd
# from definitions import coa_dict as coa
# from afc_module.definitions import coa_dict as coa
from afc_module.definitions import hdc_list as hdcl
from afc_module.definitions import roll_up_accts as rollup
from afc_module.definitions import remove_acct_list as remove_accts
from afc_module.definitions import credit_acct_list as cr_accts
from afc_module.definitions import credit_rollup_accts as credit_rollups
from afc_module.definitions import locations_dict as ld
from afc_module.definitions import duplicate_debits_dict as duplicate_debits
from zpack.fns import FilePrompt
from zpack.fns import save_dataframe
from get_coa import getCOA
#from definitions import baseline_accounts as baseline


def main():
    
    start = time.time()

    # Get the updated Chart of Accounts File
    print('Select the latest Chart of Accounts file:')
    z = FilePrompt()
    df_COA_file = pd.read_excel(z)
    df_COA_file = df_COA_file.reset_index()
    df_COA_file.fillna(0, inplace=True)

    df_COA = getCOA(df_COA_file)
    print(df_COA)
    #  To see how dictionary looks, see the COA_Dict.py file in the archive

    # If the raw data file has all the data in one file (002, 007, 008 sheets), you must save each entity in it's own file and run the program against each.
    # Read in Data from the "RawData.xlsx" file.
    print('Select the raw data file to run Payroll for:')
    f = FilePrompt()
    df_toi = pd.read_excel(f)
    #df_toi = pd.read_excel(f, dtype={'Home Department Code': str})

    df_toi = df_toi.reset_index()
    # Fill all blank cells with zeros.  
    # It's critiacal that any columns you do calculations do not have blanks.
    # df_toi.fillna(0, inplace=True)
    # Put column headers into a List
    all_col_headers = list(df_toi.columns)   

    # Remove the columns not used in the JE's
    # result_list = [x for x in original_list if x not in elements_to_remove]
    col_headers = [x for x in all_col_headers if x not in remove_accts]
   
    no_of_columns = len(col_headers)    
    
    # Remember:  Index is at 0, then first column, second column, etc, etc.  To get last Column, subtract 1
    # Like this:  print(col_headers[no_of_columns - 1])  
    
    # Reduce the size of the col_headers list to start with the Columns we want.  In this case, "Regular Earnings Total"
    RET = "Regular Earnings Total"
    if RET in col_headers:
        # Find index for element of "Regular Earnings Total"
        index_ret = col_headers.index(RET)

    # Create a new list that starts with the "Regular Earnings Total" header.
    money_headers = col_headers[index_ret:]
    last_header = 'Batch Number'
    
    
    # Remove the last columns that aren't necessary.
    while last_header == 'Batch Number' or last_header == 'Position ID':
        money_headers.pop()
        lh = money_headers[-1]
        last_header = lh
    
    #print(last_header)
    # Save the number of money headers.
    size_of_money_headers = len(money_headers)
    #print(size_of_money_headers)
    '''
    # Not used anymore#
    if size_of_money_headers != 199:
        print('Columns in Raw Data File have changed!!!!')
    else:
        print('Columns in Raw Data File appear to be unchanged')
    '''

    # Convert the Pay Date column to a datetime data type
    df_toi['Pay Date'] = pd.to_datetime(df_toi['Pay Date'])
    # Remove the hours, minutes, and seconds
    df_toi['Pay Date'] = df_toi['Pay Date'].dt.date
    print('This input file is for Company ' + df_toi['Company Code'].iloc[0])

    # Group the Data Frame by Company Code,  Home Department Code, and Location.
    df_groupby = df_toi.groupby(['Batch Number', 'Home Department Code', 'Location Description', 'Pay Date'])
    
    
    # Create a list the size of the columns of interest, "money_headers"
    values_list = [0 for _ in range(size_of_money_headers)]
    #print(values_list)
    #print(size_of_money_headers)
    
    # Create new Dataframe for the Output.
    df_Output = pd.DataFrame(columns=['Pay Date', 'Account Number', 'Description', 'Debit Amount', 'Credit Amount', 'Location', 'Dept'])
    
    for groupings, row in df_groupby:
        # Find out what Home Department Code this row is, and get the index from the Home Department Code List
        if groupings[1] in hdcl:
            #hdc_index = hdcl.index(groupings[1])
            homedeptcode = groupings[1]
        else:
           print(f"{groupings[1]} is not in the Home Dept Codes!")
        # Use the Home Department Code Index to get the right GL's from the Chart of Accounts

        # Dictionary Defining the Roll up Accounts, and initialize sum amd G/L for each to 0.  
        rollupsums = {
            "Wages" : [0, 0], "401K Payable" : [0, 0], "Bonus-B_Bonus" : [0, 0], "FICA" : [0, 0], "Garnishments" : [0, 0], "HSA_Deduction" : [0, 0], "Medical Ins Ded" : [0, 0], \
            "Net Pay" : [0, 0], "Other Payroll Taxes" : [0, 0], "Overtime" : [0, 0], "Physician Bonus" : [0, 0], "Severance Expense" : [0, 0], "Tax Deduction" : [0, 0]
        }
        # Vaulues list counter
        counter = 0
        for i in money_headers:
            found = False
            lookupkey = ""
            for key, value_list in rollup.items():
                if i in value_list:
                    found = True
                    lookupkey = key
                    break
            # If this payroll item was found above, and the COA is not empty for it, then execute.      
            
            # if found and (i in coa and coa[i]):
            if found and (i in df_COA and df_COA[i][homedeptcode] != 0):
                rollupsums[lookupkey][0] += row[i].sum()
                rollupsums[lookupkey][1] = df_COA[i][homedeptcode]
                
            else:    
                if i == 'PHA_Phone Allowance_Deduction':
                    values_list[counter] = abs(row[i].sum())
                else:
                    values_list[counter] = row[i].sum()
                if values_list[counter] != 0:
                    if df_COA[i][homedeptcode]:
                       
                        # Convert data type to datetime64[ns]
                        ped = groupings[3]
                                                
                        # Clean up Batch Number text
                        '''
                        text = str(row['Batch Number'])
                        keyword = "Name"
                        parts = text.split(keyword)
                        if len(parts) > 1:
                            truncated_text = parts[0]
                        else:
                            truncated_text = text
                        '''

                                                
                        # If matches for credit accounts, else it's a debit account.  Values are printed in appropriate column. 
                        # To address leading or trailing spaces in Location Descriptions, strip() method had to be employed whereever groupings[2] of the groupby object was referenced.
                        if i in cr_accts:
                            df_Output.loc[len(df_Output.index)] = [ped, df_COA[i][homedeptcode], str(groupings[0]) + ' ' + ' ' + str([i]), "", values_list[counter], ld[groupings[2].strip()], homedeptcode]
                        else:
                            if i in duplicate_debits:
                                df_Output.loc[len(df_Output.index)] = [ped, df_COA[i][homedeptcode], str(groupings[0]) + ' ' + str([i]), values_list[counter], "", ld[groupings[2].strip()], homedeptcode]
                                df_Output.loc[len(df_Output.index)] = [ped, '14900', str(groupings[0]) + ' ' + str([i]), "", values_list[counter], ld[groupings[2].strip()], homedeptcode]
                            else: 
                                df_Output.loc[len(df_Output.index)] = [ped, df_COA[i][homedeptcode], str(groupings[0]) + ' ' + str([i]), values_list[counter], "", ld[groupings[2].strip()], homedeptcode]
            counter += 1
        #print(rollupsums)
        for acct, z in rollupsums.items():
            if z[0] != 0:
                ped = groupings[3]
                
                # Clean up Batch Number text
                '''
                text = str(row['Batch Number'])
                keyword = "Name"
                parts = text.split(keyword)
                if len(parts) > 1:
                    truncated_text = parts[0]
                else:
                    truncated_text = text
                '''

                # If matches for credit accounts, else it's a debit account
                if acct in credit_rollups:
                    df_Output.loc[len(df_Output.index)] = [ped, z[1], str(groupings[0]) + ' ' + acct, "", z[0], ld[groupings[2].strip()], homedeptcode]
                else:
                    if acct in duplicate_debits:
                        df_Output.loc[len(df_Output.index)] = [ped, z[1], str(groupings[0]) + ' ' + acct, z[0], "", ld[groupings[2].strip()], homedeptcode]
                        df_Output.loc[len(df_Output.index)] = [ped, '14900', str(groupings[0]) + ' ' + acct, "", z[0], ld[groupings[2].strip()], homedeptcode]
                    else:
                        df_Output.loc[len(df_Output.index)] = [ped, z[1], str(groupings[0]) + ' ' + acct, z[0], "", ld[groupings[2].strip()], homedeptcode]
                        
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