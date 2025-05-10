import pandas as pd
import time
import math
import numpy as np
import json
import re
import tkinter as tk
from tkinter import filedialog as fd

#from definitions import baseline_accounts as baseline


def getCOA(df):
   
    
    # converts the DataFrame into a dictionary where the keys are the index values  
    # and the values are dictionaries containing the column names and corresponding values for each row.
    df = df.drop(columns=['Description', 'DR/CR'])
    ed = df.set_index("Payroll Item").to_dict("index")

    # iterate over each item (key-value pair) in the dictionary 
    #print(df.head)
    for k1, v1 in ed.items(): 
        # Use list comprehension to remove decimal points from the dictionary
        # Change k1 : v1 key value pair to k : v (where v is v1 converted to an integet)
        ed[k1] = {k: int(v) for k, v in v1.items()}
       
    return ed
