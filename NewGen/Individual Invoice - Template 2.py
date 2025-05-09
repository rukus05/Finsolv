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

    # Get the updated Chart of Accounts File
    print('Select the NewGen Input file:')
    z = FilePrompt()
    df_TS = pd.read_excel(z)
    df_TS = df_TS.reset_index()
    df_TS.fillna(0, inplace=True)
    
    # CLean up the date format
    df_TS['Payment Date'] = df_TS['Payment Date'].dt.date

    df_Output = pd.DataFrame(columns=['Database', 'VendorID', 'ApplyDate', 'PaymentNumber', 'InvoiceNumber', 'ApplyAmount'])
    
    df_Output['VendorID'] = df_TS['Vendor ID']
    df_Output['ApplyDate'] = df_TS['Payment Date']
    df_Output['PaymentNumber'] = df_TS['Payment Reference']
    df_Output['InvoiceNumber'] = df_TS['Invoice Number']
    df_Output['ApplyAmount'] = df_TS['Amount']
    '''
    for index, row in df_Output.iterrows():
        df_Output['Electronic'] = np.where(df_Output['PaymentMethod'] == 'Credit Card', 0, 1)
        df_Output.loc[index, 'Description'] = df_Output.loc[index, 'PaymentMethod'] + ' ' + str(df_Output.loc[index,'DocDate']) + ' ' + df_Output.loc[index, 'VendorID'] + ' ' + str(df_Output.loc[index,'MEMFacilityID'])
    '''
    for index, row in df_Output.iterrows():
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