import pandas as pd
import time
import tkinter as tk
from zpack.fns import FilePrompt
from zpack.fns import save_dataframe
import datetime
#from Dict.mapping import

# This function is to save and process the input file
class RevenueRows:
    def __init__(self, row_name, dollar_value):
        self.row_name = row_name
        self.dollar_value = dollar_value
    


def processInput(df_rev):
    
    df_rev = pd.read_excel(f)
    #df_afc = pd.read_excel(f, dtype={'Home Department Code': str})
    df_rev = df_rev.reset_index()
    # Convert Service Date to datetime type, and extract Month and Year, and add that to a 'Month_Year' column.
    df_rev['Service Date'] = pd.to_datetime(df_rev['Service Date'])
    df_rev = df_rev.sort_values(by='Service Date')
    df_rev['Month_Year'] = df_rev['Service Date'].dt.strftime('%B %Y')
    # This yields pairs of (column name, column data in a series)
    '''for col_name, col_data in df_rev.items():
        print(col_name)
        print(col_data)
    '''

    return df_rev

def saveFile(df):
    
    # Start the "Save As" dialog box.
    app = tk.Tk()
    app.title("Save File As")
    status_label = tk.Label(app, text="", fg="green")
    status_label.pack()
    save_button = tk.Button(app, text="Save as", command=save_dataframe(df, status_label))
    save_button.pack(padx=20, pady=10)

def parse_key(key):
    return datetime.datetime.strptime(key, "%B %Y")


if __name__ == "__main__":
    
    # Import the Raw data input file
    print('Select the Revenue Payroll data file:')
    f = FilePrompt()
    df = processInput(f)
    
    # Get the unique Insurance Carriers, and Month_Year's.  This will be used to group the dataframe
    payors = df['Visit Primary Carrier Name'].unique()
    mos = df['Month_Year'].unique()

    #mos_dict = dict.fromkeys(mos, 0)
    
    '''
    print(payors)
    print(type(payors))
    print(month_pay)
    print(type(month_pay))
    '''
    # Create a list for the rows (Charges, etc as defined in the sample output)
    row_names = ['Charges', 'Allowed Amount', 'Adjustments', 'Insurance Payments', 'Patient Payments', 'Collection Rate']
    
    #df_grouped = df.groupby(['Visit Primary Carrier Name', 'Month_Year'])
    
    '''
    for group_name, group_df in df_grouped:
        # This shows that you access the group by index by group_name[0], etc
        print(f"Insurer: {group_name[0]}, MoS: {group_name[1]}")

        #print(group_df.head())  # or simply print(group_df)
        # This demonstrated how to get the column values for a particular group
        # In this case, Aetna in 1/25 ... get the 'Charges'; this prints out all the charges where insurer was Aetna and occurred in 1/25.
        group = df_grouped.get_group(('AET07 - AETNA', 'January 2025'))
        col_series = group['Charges']
        #print(col_series)
    '''
    
    # Create the Dataframe to output
    df_output = pd.DataFrame(columns = ['Carrier Name'])
    # This part of the dataframe will have variable length columns, depending on the unique MoS for the raw date
    #df_output2 = pd.DataFrame(columns= mos)
    #df_output = pd.concat([df_output1, df_output2], axis = 1)

    #saveFile(df_output)

    

    # Testing with Pivot Table method

    #df_output = pd.DataFrame(['Revenue'])
    dfs = []
    for payor in payors:
        #Add a line for the insurance carrier
        # Add carrier
        
        # Add row labels
        df_row_labels = pd.DataFrame({
            'Carrier Name' : [payor, 'Charges', 'Allowed Amount', 'Adjustments', 'Insurance Payments', 'Patient Payments', 'Collection Rate']
        })
        #df_output = pd.concat([df_output, df_row_labels], ignore_index=True)
        df_output = pd.DataFrame()
        #saveFile(df_output)
        
        #df_output = pd.concat([df_output, df_payor], ignore_index=True)
        #Initialize the dictionary that has MoS as the keys, and row numbers (ie, Charges, etc) as values
        # To see what an instance of this dict looks like, see mos_dict.txt in the Dict directory
        
        #rows_dict = dict.fromkeys(row_names, 0)
        #mos_dict = dict.fromkeys(mos, rows_dict)
        # This sorts the dict keys (MoS) by date
        #mos_sorted_dict = dict(sorted(mos_dict.items(), key = lambda item: parse_key(item[0])))
        #print(mos_sorted_dict)

        
        #print(ins_dict.keys())
        
        # Filter for the payor
        payorfiltered_df = df[df['Visit Primary Carrier Name'] == payor]
        p = payorfiltered_df.pivot_table(
            index=['Visit Primary Carrier Name', 'Month_Year'],
            values = ['Charges', 'Allowed Amount', 'Adjustments', 'Insurance Payments', 'Patient Payments'],
            aggfunc ='sum', 
            fill_value=0
        )
        p_reset = p.reset_index()
        #saveFile(p_reset)

        p_reset = p_reset.set_index('Month_Year')
        MoS_dict = p_reset.to_dict(orient='index')

        #print(MoS_dict)
        # This sorts the dict keys (MoS) by date
        #MoS_dict_Sorted = dict(sorted(MoS_dict.items(), key = lambda item: parse_key(item[0])))
        
        for month in mos:
            if month in MoS_dict:
                if MoS_dict[month]['Charges'] != 0:
                    rate = MoS_dict[month]['Insurance Payments'] / MoS_dict[month]['Charges']
                else:
                    rate = 'N/A'
                rows = [' ', MoS_dict[month]['Charges'], MoS_dict[month]['Allowed Amount'], MoS_dict[month]['Adjustments'], MoS_dict[month]['Insurance Payments'], MoS_dict[month]['Patient Payments'], rate]
                df_month = pd.DataFrame(rows, columns = [month])
                #Here you concatenate all the months for this particular carrier.
                df_row_labels = pd.concat([df_row_labels, df_month], axis = 1)
        # Here you concatenate all 
        #df_output = pd.concat([df_output, df_row_labels], ignore_index=True)
        # The DF kept getting overwritten.  After researching, it appeared the best thing was to store each of these outputs into a list, and concatenate once you're done looping. 
        dfs.append(df_row_labels)
        #saveFile(df_output)        
        #df_Final = pd.concat([df_output, df_row_labels], ignore_index=True)
        
        
        #for outer_key, inner_dict in mos_dict.items():
         #   for inner_key, value in inner_dict.items():


        #numbers_pd = pd.DataFrame.from_dict(MoS_dict, orient='columns')
        
        #df_output = pd.concat([df_output, numbers_pd], ignore_index=False)
    result_df = pd.concat(dfs, ignore_index=True)
    saveFile(result_df)

    

    #saveFile(p_reset)



    



    #print("Save the Output File...")
    #saveFile(pivot_reset)
