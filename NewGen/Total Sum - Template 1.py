"""
This script requires the pandas library to be installed.
To install pandas, run: pip install pandas
"""

import pandas as pd
import os
import time
import tkinter as tk
from zpack.fns import FilePrompt
from zpack.fns import save_dataframe_csv
import datetime
import numpy as np




def main():
    print("Welcome to the Column Extractor!")
    print("This program will extract and map columns from your input CSV file.")
    
    start = time.time()

    # Import checkbook lookup tab (Definitions file)
    # Get the updated Chart of Accounts File
    print('Select the Checkbook Lookup file:')
    z = FilePrompt()
    df_checkbook = pd.read_excel(z)
    
    #Create a dict with the key being the first column (CC Name) and value being the 2nd column (Checkbook ID)
    checkbook_dict = dict(zip(df_checkbook.iloc[:, 0], df_checkbook.iloc[:, 1]))
    
    # Get the updated Chart of Accounts File
    print('Select the NewGen Input file:')
    z = FilePrompt()
    df_TS = pd.read_excel(z)
    df_TS = df_TS.reset_index()
    #df_TS.fillna(0, inplace=True)

    
    
    # CLean up the date format
    df_TS['Payment Date'] = df_TS['Payment Date'].dt.date

    df_Output = pd.DataFrame(columns=['Database', 'Checkbook', 'VendorID', 'VendorName', 'PaymentMethod', 'Electronic', 'CardName', 'DocDate', 'DocNumber', 'Amount', 'Description', 'CreditDRAcct', 'CreditCRAcct', 'MEMFacilityID', 'PostingDate'])
    
    # df_Output['Database'] = 'NGH'
    df_Output['Checkbook'] = df_TS['Bank Acct']
    df_Output['VendorID'] = df_TS['Vendor ID']
    df_Output['VendorName'] = df_TS['Vendor Name']
    df_Output['PaymentMethod'] = df_TS['Payment Type']
    df_Output['CardName'] = df_TS['Credit Card #']
    df_Output['DocDate'] = df_TS['Payment Date']
    df_Output['DocNumber'] = df_TS['Payment Reference']
    df_Output['Amount'] = df_TS['Payment Total']
    df_Output['MEMFacilityID'] = df_TS['Entity #']
    df_Output['PostingDate'] = df_TS['Payment Date']

    
    for index, row in df_Output.iterrows():
        # df_Output['Electronic'] = np.where(df_Output['PaymentMethod'] == 'Credit Card', 0, 1)

        
        
        if df_Output.loc[index, 'PaymentMethod'] == 'Credit Card':
            df_Output.loc[index, 'PaymentMethod'] = 'CC'
            df_Output.loc[index, 'Electronic'] = 0
        else:
            df_Output.loc[index, 'PaymentMethod'] = 'EFT'
            df_Output.loc[index, 'Electronic'] = 1
       
        # df_Output.loc[mask, 'Checkbook'] = df_Output.loc[mask, df_Output.loc[index, 'CardName']].map(checkbook_dict)
        
        
        if df_Output.loc[index, 'Checkbook'] == '' or pd.isna(df_Output.loc[index, 'Checkbook']):
            print('Checkbook is 0.  Value is ' + checkbook_dict[df_Output.loc[index, 'CardName']])
            df_Output.loc[index, 'Checkbook'] = checkbook_dict[df_Output.loc[index, 'CardName']]
        

        df_Output.loc[index, 'Description'] = df_Output.loc[index, 'PaymentMethod'] + ' ' + str(df_Output.loc[index,'DocDate']) + ' ' + df_Output.loc[index, 'VendorID'] + ' ' + str(df_Output.loc[index,'MEMFacilityID'])
        df_Output.loc[index, 'Database'] = 'NGH'


    runningtime = time.time() - start
    print("Save the Output File...")
    # Start the "Save As" dialog box.
    app = tk.Tk()
    app.title("Save File As")
    status_label = tk.Label(app, text="", fg="green")
    status_label.pack()
    save_button = tk.Button(app, text="Save as", command=save_dataframe_csv(df_Output, status_label))
    save_button.pack(padx=20, pady=10)

if __name__ == "__main__":
    main() 