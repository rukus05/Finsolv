## TOI DEFINITIONS FILE##

# This file holds definitions for the TOI Payroll Journal Entry Automations Python Program.

# Create a Dictionary Class that ignores trailing and leading spaces.
class RemoveSpacesDict(dict):
    
    # Constructor Method
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    # Helper method that returns the stripped key
    def _strip_key(self, key):
        return key.strip()
    
    # Helper method that returns 2 keys; original and stripped key, which could be the same.
    def _generate_lookup_keys(self, key):
        return key, self._strip_key(key)
    
    # Method that overrides original Dict key retrieval method.
    # Calls _generate_lookup_keys to get 2 kesy.
    # Uses only the stripped key for the dictionary lookup.
    #  This allows you to look up keys with or without trailing spaces at the end, and it retrieves the value associated with the stripped key.
    def __getitem__(self, key):
        original_key, stripped_key = self._generate_lookup_keys(key)
        return super().__getitem__(stripped_key)

    # Method that overrides original Dict key assignment method.  Similar to above method
    # Only stripped key is used for assigning the key value.  
    def __setitem__(self, key, value):
        original_key, stripped_key = self._generate_lookup_keys(key)
        super().__setitem__(stripped_key, value)



# This list represents the column headers for the COA.  It is ultimately used to get the column number ("index")
hdc_list = [100100, 100200, 100300, 400100, 100400, 200000, 200100, 200200, 300100, 300200, 300250, 300300, 300400, 300500, 700100, 700110, 700120, 700200, 700205, \
            700210, 700215, 700225, 700230, 700300, 700305, 700310, 700315, 700320, 700325, 700326, 700327, 700330, 700335, 700340, 700345, 700350, 700355, 700360, \
            701000, 701100, 701200, 701210, 702010, 702100, 702300, 702400, 702410, 702415, 703000, 704000, 704100, 704500, 705000, 705500, 705600, 702420]


# Define the accounts to roll up.
roll_up_accts = {
    "Wages" : ['Regular Earnings Total', '1FA_FF-FMLA_Other Earnings', '1FE_FF-PSL-EE_Other Earnings', '1FF_FF-PSL-FAM_Other Earnings', '1XQ_CA SPSL 22_Other Earnings', \
               '1XV_CA SPSL PT_Other Earnings', '1XX_CA SUP PSL_Other Earnings', '7I_Other Earnings', 'AIP_Ann Incn Prog_Other Earnings', 'BST_Benefit Stipend_Other Earnings', \
               'C_Miscellaneous_Other Earnings', 'CBI_CA Break_Other Earnings', 'E_EDUCATION HRS_Other Earnings', 'IDE - IDEOlogy', 'I_Other Earnings', 'N_Other Earnings', \
               'O_Other_Other Earnings', 'OI_Other Earnings', 'P_PERSONAL_Other Earnings', 'PDT_Prior DT_Other Earnings', 'QMD QMD', 'REG_Regular Pay_Other Earnings', \
               'RET Retro', 'RIV_Riverside_Other Earnings', 'SP1_Sev  COVID_Other Earnings', 'SPL_C19 Supp Sick_Other Earnings', 'STP', \
               'T_Other Earnings', 'TMD', 'U_Other Earnings', 'WRQ_WRK REQ_Other Earnings', 'X_Other Earnings', 'Z_Other Earnings', \
               'UMD', 'O OTHER', 'SMO', 'RMD RMD'], \
    "401K Payable" : ['K_401K$_Deduction', 'L_401k L_Deduction', 'R_Roth 401k $_Deduction'], \
    # "AIP Bonus" : [29], \
    "Bonus-B_Bonus" : ['B_BONUS_Other Earnings', 'BON_Other Earnings', 'RTB RetBon'], \
    "FICA" : ['Medicare - Employer Tax', 'Social Security - Employer Tax'], \
    # "FUTA" : [167], \
    "Garnishments" : ['69_TAXL$_Deduction', '70_Bankruptcy$_Deduction', '71_Tax Levy$_Deduction', '72_Tax Levy$_Deduction', '73_Garnishment$_Deduction', \
                      '74_Garnishment$_Deduction', '75_Child Support$_Deduction', '76_Child Support$_Deduction', '77_Child Support$_Deduction', '78_Child Support$_Deduction', \
                      '79_Wage Agreement$_Deduction', 'BA1_BANKRUPTCY 1 $_Deduction', 'BA2_BANKRUPTCY 1 %_Deduction', 'CS1_CHILD SUPPORT_Deduction', 'G_GARNISHMENT_Deduction', \
                      'GA1_GARNISH 1 $_Deduction', 'GA2_GARNISH 2 $_Deduction', 'GA3_GARNISH 3 $_Deduction', 'GA4_GARNISH 1 %_Deduction', 'GA5_GARNISH 2 %_Deduction', \
                      'GA6_GARNISH 3 %_Deduction', 'N_ADVANCE_Deduction', 'OVP_Loan_Deduction', 'TL1_TAX LEVY 1 $_Deduction', 'TL2_TAX LEVY 2 $_Deduction', \
                      'TL3_TAX LEVY 1 %_Deduction', 'TL4_TAX LEVY 2 %_Deduction'], \
    "HSA_Deduction" : ['HS_HSA_Deduction', 'HSA_Deduction', 'HSP_HOSPIN_Deduction', 'HSS_HSA SAVING_Deduction'], \
    "Medical Ins Ded" : ['M_MEDI_Deduction', 'MIB_MEDINSBUYUP_Deduction'], \
    "Net Pay" : ['CK1_CHECKING_Deduction', 'CK2_CHECKING 2_Deduction', 'CK3_CHECKING 3_Deduction', 'SV1_SAVINGS_Deduction', 'SV2_SAVINGS 2_Deduction'], \
    "Other Payroll Taxes" : ['Family Leave Insurance - Employer Tax', 'Lived in Local - Employer Tax', 'Lived in State - Employer Tax', 'Local 4 - Employer Tax', \
                             'Local 5 - Employer Tax', 'Medical Leave Insurance - Employer Tax', 'SDI - Employer Tax', 'SUI/SDI - Employer Tax', 'Transit - Employer Tax', \
                             'Worked in Local - Employer Tax', 'Worked in State - Employer Tax'], \
    "Overtime" : ['Overtime Earnings Total', 'DT_DOUBLETIME_Other Earnings', 'POT_Prior OT_Other Earnings'], \
    "Physician Bonus" : ['PBO_PEC Bonus_Other Earnings', 'PYB_Physician Bon_Other Earnings'], \
    "Severance Expense" : ['SEV_Severance_Other Earnings', 'SP2_Severance_Other Earnings'], \
    "Tax Deduction" : ['SUI/SDI Employee Tax', 'Transit - Employee Tax', 'Worked in Local - EE Tax', 'Worked in State- EE Tax', 'Family Leave Insurance - Employee Tax'], \
            

}

# Defines the Credit Accounts
credit_acct_list = ['5_OREGON WBF TAX_Deduction', '69_TAXL$_Deduction', '70_Bankruptcy$_Deduction', '71_Tax Levy$_Deduction', '72_Tax Levy$_Deduction', '73_Garnishment$_Deduction', \
                    '74_Garnishment$_Deduction', '75_Child Support$_Deduction', '76_Child Support$_Deduction', '77_Child Support$_Deduction', '78_Child Support$_Deduction', \
                    '79_Wage Agreement$_Deduction', 'A_AFLACPRETAX_Deduction', 'ADD_Persnl Acc_Deduction', 'B_ALFAC POSTAX_Deduction', 'BA1_BANKRUPTCY 1 $_Deduction', \
                    'BA2_BANKRUPTCY 1 %_Deduction', 'C_MEDICARE SURTAX_Deduction', 'CK1_CHECKING_Deduction', 'CK2_CHECKING 2_Deduction', 'CK3_CHECKING 3_Deduction', 'CLB_CLifeBuy_Deduction', \
                    'CS1_CHILD SUPPORT_Deduction', 'D_DENT_Deduction', 'DEP_Dep Care FSA_Deduction', 'DN1_Dental Care_Deduction', 'ELB_ELifeBuy_Deduction', \
                    'FSA_Medical FSA_Deduction', 'G_GARNISHMENT_Deduction', 'GA1_GARNISH 1 $_Deduction', 'GA2_GARNISH 2 $_Deduction', 'GA3_GARNISH 3 $_Deduction', \
                    'GA4_GARNISH 1 %_Deduction', 'GA5_GARNISH 2 %_Deduction', 'GA6_GARNISH 3 %_Deduction', 'HS_HSA_Deduction', 'HSA_Deduction', 'HSC_HSA CHECKING_Deduction', \
                    'HSP_HOSPIN_Deduction', 'HSS_HSA SAVING_Deduction', 'IDT_IDTHFT_Deduction', 'K_401K$_Deduction', 'L_401k L_Deduction', 'LFS_Ltd. Purpose_Deduction', \
                    'LGL_LEGAL_Deduction', 'LTD_Long Term Disb_Deduction', 'M_MEDI_Deduction', 'ME1_Medical Care_Deduction', 'MIB_MEDINSBUYUP_Deduction', \
                    'N_ADVANCE_Deduction', 'ORX_OR TRANSIT TAX_Deduction', 'OVP_Loan_Deduction', 'P_PPLS_Deduction', 'PET_Deduction', 'R_Roth 401k $_Deduction', \
                    'RSU_Other_Deduction', 'S_MISCELLANEOUS_Deduction', 'SL1_Supp. Life Ins._Deduction', 'SLB_SLifeBuy_Deduction', 'ST1_Short Trm Disb_Deduction', \
                    'STI_Short Trm Disb_Deduction', 'SV1_SAVINGS_Deduction', 'SV2_SAVINGS 2_Deduction', 'TL1_TAX LEVY 1 $_Deduction', 'TL2_TAX LEVY 2 $_Deduction', \
                    'TL3_TAX LEVY 1 %_Deduction', 'TL4_TAX LEVY 2 %_Deduction', 'V_VISION_Deduction', 'VCI_Critical Illnes_Deduction', 'VI1_Vision Care_Deduction', \
                    'Z_1099 Employess_Deduction', 'Family Leave Insurance - Employee Tax', 'Federal Income - Employee Tax', 'Lived in Local - EE Tax', 'Lived in State- EE Tax', \
                    'Local 10 - Employee Tax', 'Local 4 - Employee Tax', 'Local 5 - Employee Tax', 'Local 9 - Employee Tax', 'Medical Leave Insurance - Employee Tax', \
                    'Medicare - Employee Tax', 'SDI - Employee Tax', 'Social Security - Employee Tax', 'SUI - Employee Tax', 'SUI/SDI Employee Tax', 'Transit - Employee Tax', \
                    'Worked in Local - EE Tax', 'Worked in State- EE Tax', 'Medicare Surtax - Employee Tax', 'Net Pay', 'Medicare Surtax Adjust - Employee Tax']

# Defines the Rollup Accounts that are Credit Accounts
credit_rollup_accts = ["Garnishments", "Net Pay",  "HSA_Deduction", "401K Payable", "Medical Ins Ded", "Tax Deduction"]

# This list is used to remove the columns not used for J/E.
remove_acct_list = ['Overtime Hours Total', 'WAGES', 'OT', 'BONUS', 'SIGNING BONUS', 'VACATION', 'SEVERANCE', 'Gross Pay']

# Create an instance of the custom RemoveSpacesDict class, which will contain the dictionary of locations.
locations_dict = RemoveSpacesDict()

locations_dict = {
    'The Oncology Institute, Inc.' : 101, \
    'Parent' : 100, \
    'Acquisition' : 200, \
    'MGMT' : 300, \
    'Cerritos Corporate' : 9001, \
    'Florida Corporate - Not Active' : 9002, \
    'TOI' : 400, \
    'Clinical Research' : 410, \
    'TOI FL' : 500, \
    'TOI TX' : 600, \
    'TOI North' : 'North', \
    'California North' : 'CA-North', \
    'Pod 1' : 1, \
    'TOI Downey' : 1001, \
    'TOI Lynwood' : 1002, \
    'TOI Whittier' : 1003, \
    'Pod 2' : 2, \
    'TOI Lakewood' : 1004, \
    'TOI Los Alamitos' : 1005, \
    'TOI Torrance' : 1006, \
    'TOI Culver City' : 1048, \
    'Pod 3' : 3, \
    'TOI Downtown LA' : 1007, \
    'TOI East LA' : 1008, \
    'TOI Montebello' : 1009, \
    'TOI City West' : 1047, \
    'Pod 4' : 4, \
    'TOI Mission Hills' : 1010, \
    'TOI Northridge' : 1011, \
    'TOI Valencia' : 1012, \
    'TOI Burbank' : 1016, \
    'TOI Glendale' : 1017, \
    'Pod 5' : 5, \
    'TOI Simi Valley' : 1013, \
    'TOI Thousand Oaks' : 1014, \
    'TOI West Hills' : 1015, \
    'Pod 6' : 6, \
    'TOI Pasadena' : 1018, \
    'TOI West Covina' : 1028, \
    'TOI San Gabriel' : 1042, \
    'TOI Alhambra' : 1049, \
    'TOI Hacienda Heights' : 1050, \
    'TOI Monterey Park' : 1054, \
    'TOI South' : 'South', \
    'California South' : 'CA-South', \
    'Pod 7' : 7, \
    'TOI Anaheim' : 1019, \
    'TOI Fountain Valley' : 1020, \
    'TOI Mission Viejo' : 1021, \
    'TOI Santa Ana' : 1022, \
    'Pod 8' : 8, \
    'TOI Corona' : 1023, \
    'TOI Riverside2' : 1025, \
    'TOI Riverside' : 1025, \
    'TOI San Bernardino' : 1026, \
    'TOI Upland' : 1027, \
    'TOI Victorville' : 1046, \
    'Pod 9' : 9, \
    'Pod 10' : 10, \
    'TOI Hemet' : 1029, \
    'TOI Murrieta' : 1030, \
    'TOI Temecula' : 1031, \
    'Pod 15' : 15, \
    'TOI Vista' : 1043, \
    'TOI Hillcrest' : 1044, \
    'TOI Chula Vista' : 1045, \
    'TOI Fresno' : 'Fresno', \
    'Pod 17' : 17, \
    'Fresno WCC' : 1051, \
    'RadOnc' : 'RadOnc', \
    'Pod R1' : 'R1', \
    'TOI R1- Lakewood' : 1801, \
    'Nevada' : 'NV', \
    'Pod 11' : 11, \
    'TOI Henderson - Closed' : 1032, \
    'TOI Las Vegas' : 1033, \
    'TOI Spring Valley - Do not use' : 1034, \
    'TOI Henderson 2' : 1052, \
    'TOI Spring Valley 2' : 1053, \
    'Arizona' : 'AZ', \
    'Pod 12' : 12, \
    'TOI Green Valley' : 1035, \
    'TOI Oro Valley' : 1036, \
    'TOI East Tucson' : 1037, \
    'TOI West Tucson' : 1038, \
    'Florida' : 'Florida', \
    'Pod 13' : 13, \
    'TOI FL Mid-Pinellas' : 2001, \
    'TOI FL Downtown St. Pete' : 2002, \
    'Pod 14' : 14, \
    'TOI FL Tampa-Habana' : 2003, \
    'TOI FL Brandon' : 2004, \
    'TOI FL Plant City' : 2005, \
    'TOI FL Lakeland' : 2006, \
    'TOI FL Miramar' : 2016, \
    'Pod 18' : 18, \
    'TOI Fort Lauderdale-17th Street' : 2007, \
    'TOI Fort Lauderdale-Imperial Point' : 2008, \
    'TOI Plantation' : 2009, \
    'Pod 19' : 19, \
    'TOI North Miami' : 2015, \
    'TOI South Miami' : 2010, \
    'TOI South Miami-West' : 2011, \
    'Texas' : 'Texas', \
    'Pod 16' : 16, \
    'TOI TX Central Austin' : 3001, \
    'TOI TX Southwest Austin' : 3002, \
    'TOI Hospitals' : 'Hospitals', \
    'TOI Closed Clinics' : 'Closed', \
    'Pod 99' : 99, \
    'TOI Alhambra CLOSED' : 1040, \
    'TOI San Pedro CLOSED' : 1041, \
    'TOI Riverside CLOSED' : 1024, \
    'TOI Marana CLOSED' : 1039, \
    'TOI Chino/Chino Hills' : 1055, \
    'TOI Hollywood' : 2014, \
    'TOI R1-Downey RadOnc' : 1802, \
    'TOI R-1 Pomona RadOnc' : 1803, \
    'TOI R1-Covina RadOnc' : 1804, \
    'TOI R1-Victorville RadOnc' : 1805, \
    'TOI R-1 Hemet RadOnc' : 1806, \
    'TOI Palm Desert' : 1057, \
    'TOI Hialeah' : 2013, \
    'TOI PH1-Westminster' : 4001, \
    'TOI Temecula 2' : 1058, \
    'TOI OR Salem' : 5001, \
    'TOI OR Portland' : 5002, \

}

# Department : GL Account 
pto_gl_dict = {
    100100 : 52500, \
    100200 : 52500, \
    100300 : 52500, \
    100400 : 60400, \
    200100 : 60400, \
    200200 : 60400, \
    300100 : 60400, \
    300200 : 60400, \
    300250 : 60400, \
    300300 : 60400, \
    300400 : 60400, \
    300500 : 60400, \
    400100 : 52500, \
    700100 : 60400, \
    700110 : 60400, \
    700120 : 60400, \
    700200 : 60400, \
    700205 : 60400, \
    700210 : 60400, \
    700215 : 60400, \
    700230 : 60400, \
    700300 : 60400, \
    700305 : 60400, \
    700310 : 60400, \
    700315 : 60400, \
    700320 : 60400, \
    700325 : 60400, \
    700326 : 60400, \
    700327 : 60400, \
    700330 : 60400, \
    700335 : 60400, \
    700340 : 60400, \
    700345 : 60400, \
    700350 : 60400, \
    700355 : 60400, \
    700360 : 60400, \
    701000 : 60400, \
    701100 : 60400, \
    701200 : 60400, \
    701210 : 60400, \
    702010 : 60400, \
    702100 : 60400, \
    702300 : 60400, \
    702400 : 60400, \
    702410 : 60400, \
    702415 : 60400, \
    702420 : 60400, \
    703000 : 60400, \
    704000 : 60400, \
    704100 : 60400, \
    704500 : 60400, \
    704505 : 60400, \
    705000 : 60400, \
    705500 : 60400, \
    705600 : 60400
}

coa_accrual_dict = {
    'WF MGMT Operating' : 10100,
    'WF Arizona Medicare Business Checking' : 10111,
    'FHB Business Checking' : 10120,
    'VNB TOI FL PC' : 10140,
    'WF PC Non-Government Lockbox' : 10210,
    'UB MGMT Operating' : 10300,
    'UB Parent Operating' : 10305,
    'UB PC Preferred CAP' : 10320,
    'JPM TOI Inc 328' : 10500,
    'JPM TOI Inc Custody 002' : 10501,
    'JPM MGMT Master Concentration 552' : 10505,
    'JPM ICRI General 185' : 10510,
    'JPM TOI CA Preferred CAP 111' : 10520,
    'JPM TOI CA AR Non Govt 773' : 10620,
    'JPM TOI CA AR Govt 151' : 10621,
    'JPM TOI FL AR Non Govt 055' : 10625,
    'JPM TOI FL AR Govt 576' : 10626,
    'JPM TOI TX AR Non Govt 369' : 10630,
    'JPM TOI TX AR Govt 880' : 10631,
    'JPM MGMT AP 719' : 10705,
    'JPM TOI CA AP 029' : 10720,
    'JPM TOI FL AP 352' : 10725,
    'JPM TOI TX AP 682' : 10730,
    'JPM TOI EXP 298' : 10735,
    'Money Market' : 10800,
    'US Treasury T-Bills' : 10900,
    'Restricted Cash' : 11000,
    'UB CC Cash Collateral Account' : 11001,
    'Current Fixed Income - Treasury' : 11500,
    'Oral Drug Accounts Receivable' : 12100,
    'Capitated Accounts Receivable' : 12110,
    'FFS Accounts Receivable' : 12120,
    'FFS Unapplied Cash' : 12129,
    'ICRI Accounts Receivable' : 12130,
    'ICRI Unbilled AR' : 12135,
    'Radiation Case Rate Accounts Receivable' : 12170,
    'Rebate Receivables - IV Drugs' : 12180,
    'Rebate Receivables - Oral Drugs' : 12185,
    'Other Trade Receivables' : 12190,
    'TSA AR' : 12200,
    'Current Portion of Notes Receivable' : 12500,
    'Income Tax Receivable' : 12600,
    'Interest Receivable' : 12700,
    'Other Receivables' : 12900,
    'Oral Drug Inventory' : 13000,
    'IV Drug Inventory' : 13010,
    'Prepaid Rent - Real Estate' : 14010,
    'Prepaid Rent - Equipment' : 14011,
    'Prepaid CAM' : 14020,
    'Prepaid Medical Benefits' : 14031,
    'Prepaid Dental Benefits' : 14032,
    'Prepaid Vision Benefits' : 14033,
    'Prepaid Basic Life Benefits' : 14034,
    'Prepaid Misc Benefits' : 14035,
    'Prepaid Insurance' : 14070,
    'Prepaid Hospital Dues' : 14071,
    'Prepaid Computer Software and Maintenance' : 14072,
    'Prepaid Miscellaneous' : 14089,
    'Other Prepaid Expenses' : 14090,
    'Current Deferred Income Tax Assets' : 14600,
    'Payroll Clearing' : 14900,
    'Credit Card Clearing' : 14905,
    'Other Current Assets' : 14999,
    'Computers and Software' : 15010,
    'Office Furniture' : 15020,
    'Leasehold Improvements' : 15030,
    'Medical Equipment' : 15040,
    'Internally Developed Software' : 15050,
    'Construction In Progress' : 15090,
    'Computers and Software Accumulated Depreciation' : 15110,
    'Office Furniture Accumulated Depreciation' : 15120,
    'Leasehold Improvements Accumulated Depreciation' : 15130,
    'Medical Equipment Accumulated Depreciation' : 15140,
    'Internally Developed Software Accumulated Depreciation ' : 15150,
    'Financing Lease Asset - Medical Equipment' : 15200,
    'Financing Lease Asset - Other Equipment' : 15210,
    'Financing Lease Accumulated Depreciation - Medical Equipment' : 15300,
    'Financing Lease Accumulated Depreciation - Other Equipment' : 15310,
    'Operating Lease Asset - Real Estate' : 15405,
    'Operating Lease Asset - Estimated Leases' : 15415,
    'Investment in TOI Acquisition, LLC' : 16000,
    'Investment in TOI Management, LLC' : 16005,
    'Investment in The Oncology Institute, LLC' : 16010,
    'Non-Current Fixed Income - Treasury' : 16500,
    'Notes Receivable' : 17000,
    'Security Deposits' : 18000,
    'Deferred Tax Asset' : 18600,
    'Goodwill' : 19000,
    'Practice Acquisition Goodwill' : 19005,
    'Pinellas Cancer Center Goodwill' : 19010,
    'Payor Contracts' : 19210,
    'Trade Names' : 19220,
    'ICRI Clinical Contracts' : 19230,
    'Non-Compete Agreements' : 19240,
    'Other Intangible Assets' : 19290,
    'Payor Contracts Accumulated Amortization' : 19310,
    'Trade Names Accumulated Amortization' : 19320,
    'ICRI Clinical Contracts Accumulated Amortization' : 19330,
    'Non-Compete Agreements Accumulated Amortization' : 19340,
    'Other Intangible Assets Accumulated Amortization' : 19390,
    'Accounts Payable' : 20000,
    'AP Discounts Clearing' : 20005,
    'Cash Overdraft' : 20499,
    'Income Taxes Payable' : 20800,
    'PPP Loans' : 21055,
    'Financing Lease Current Obligation - Medical Equipment' : 22200,
    'Financing Lease Current Obligation - Other Equipment' : 22210,
    'Operating Lease Current Obligation - Real Estate' : 22405,
    'Operating Lease Current Obligation - Estimated Leases' : 22415,
    'Union Bank Corporate CC' : 23000,
    'JPM Corporate CC' : 23005,
    'FHB CC-1919' : 23010,
    'Accrued Payroll' : 23100,
    'Garnishments' : 23101,
    '401k Payable' : 23102,
    'Accrued FSA' : 23103,
    'Accrued Vacation' : 23110,
    '401k Employer Match Accrual' : 23120,
    'Accrued Clinical Bonus' : 23200,
    'Accrued Management Bonus' : 23250,
    'Accrued DFP Note Interest' : 23300,
    'Accrued Expense' : 23400,
    'Accrued Medical Supplies' : 23410,
    'Accrued PI Fees' : 23440,
    'Accrued Severance' : 23450,
    'Accrued Sub-CAP COS' : 23460,
    'Pre-acquisition Outstanding Checks' : 23490,
    'Deferred FFS Revenue' : 23500,
    'Deferred CAP Revenue' : 23505,
    'Current Deferred Income Tax Liabilities' : 23600,
    'Current Rebate Liability' : 23970,
    'Current Deferred Purchase Price' : 23980,
    'Other Current Liabilities' : 23990,
    'Stock Comp Liability' : 23995,
    'DFP Note' : 25000,
    'DFP Note Deferred Debt Issuance Costs' : 25001,
    'DFP Note Unamortizated Debt Discount' : 25002,
    'Financing Lease Obligation - Medical Equipment' : 26200,
    'Financing Lease Obligation - Other Equipment' : 26210,
    'Operating Lease Obligation - Real Estate' : 26405,
    'Operating Lease Obligation - Estimated Leases' : 26415,
    'Deferred Rent' : 28000,
    'Tenant Improvement Allowance' : 28050,
    'Deferred Tax Liability' : 28600,
    'FIN 48 Liability' : 28605,
    'Private Warrants Liability' : 28700,
    'DFP Note Warrant Liability' : 28705,
    'Earnout Liability' : 28710,
    'DFP Note Embedded Derivative Liability' : 28715,
    'Noncurrent Accrued Severance' : 28950,
    'Non-Current Rebate Liability' : 28970,
    'Non-Current Deferred Purchase Price' : 28980,
    'Other Liabilities' : 28990,
    'Class A Common Stock' : 30001,
    'Series A Common Equivalent Preferred Stock' : 30101,
    'Treasury Stock' : 30210,
    'Additional Paid-in Capital' : 31000,
    'Intercompany TOI/MGMT' : 32000,
    'Intercompany TOI FL/MGMT' : 32001,
    'Intercompany TOI TX/MGMT' : 32002,
    'Intercompany ICRI/MGMT' : 32005,
    'Intercompany HHHC/MGMT' : 32010,
    'Intercompany TOI PSO/MGMT' : 32011,
    'Intercompany HHHC/TOI' : 32015,
    'Intercompany TOI/AZ Pharmacy' : 32020,
    'Intercompany TOI/TOI FL' : 32021,
    'Intercompany TOI/ICRI' : 32025,
    'Intercompany Acquisition/MGMT' : 32900,
    'Intercompany Parent/MGMT' : 32950,
    'Intercompany TOI Inc/MGMT' : 32951,
    "Members' Equity" : 33000,
    'Retained Earnings' : 35000,
    'Oral Drug Revenue' : 40000,
    'Oral Drug Patient Assistance' : 40001,
    'Oral Drug DIR Fees' : 40005,
    'Capitated Revenue' : 41000,
    'Capitated Revenue - Radiation' : 41001,
    'Cap Deducts' : 41005,
    'FFS Revenue - Drugs' : 42001,
    'FFS Revenue - Chemo Infusion' : 42002,
    'FFS Revenue - PS' : 42003,
    'FFS Revenue - Late Charges' : 42004,
    'FFS Revenue - CAP Carve-out Drugs' : 42005,
    'FFS Revenue - Radiation' : 42010,
    'FFS Revenue - Radiation Case Rates' : 42011,
    'Gainshare Bonus' : 42500,
    'ICRI Revenue' : 43000,
    'ICRI Patient Visit Revenue' : 43001,
    'ICRI Procedure Revenue' : 43002,
    'TOI/ICRI Management Fees' : 46490,
    'Caremore Pilot Program' : 49000,
    'Forms & Medical Records' : 49010,
    'Prop 56 Revenue' : 49020,
    'CMMI OCM Revenue' : 49030,
    'MLK Hospital Call Coverage Revenue' : 49040,
    'Patient Refunds' : 49050,
    'Pre-acquisition Revenue' : 49060,
    'Miscellaneous Other Revenue' : 49100,
    'ICRI Clinical Trials' : 49200,
    'Sub-capitation Administrative Fee' : 49300,
    'Profit-sharing Contract Revenue' : 49305,
    'Gainshare Bonus Revenue' : 49310,
    'Oral Drug COS' : 50000,
    'Oral Drug COS - Rebates' : 50005,
    'IV Drug COS' : 51000,
    'IV Drug COS - CAP' : 51001,
    'IV Drug COS - CAP-FFS' : 51002,
    'IV Drug COS - FFS' : 51003,
    'IV Drug COS - Rebates FFS' : 51004,
    'IV Drug COS - Sub-CAP' : 51005,
    'IV Drug COS - Rebates CAP' : 51006,
    'Clinical Wages' : 52000,
    'Clinical Overtime Wages' : 52005,
    'Clinical Payroll Accrual' : 52010,
    'Clinical Bonus Expense' : 52100,
    'Clinical Signing Bonuses' : 52105,
    'Clinical Payroll Taxes' : 52200,
    'Locums Expense' : 52300,
    'Clinical Payroll Fees' : 52400,
    'Clinical Vacation Expense' : 52500,
    'Clinical Severance Expense' : 52900,
    'Research Studies and Expenses' : 53000,
    'PI Fees' : 53005,
    'Patient Transportation' : 53010,
    'Laboratory Tests and Fees' : 53020,
    'Intercompany COS' : 53090,
    'Medical Supplies' : 54000,
    'Medical Supplies - ICRI' : 54005,
    'Sub-capitation COS' : 55000,
    'Biohazardous Medical Waste' : 59010,
    'Biohazardous Medical Waste - ICRI' : 59011,
    'Non-Clinical Wages' : 60000,
    'Non-Clinical Overtime Wages' : 60005,
    'Non-Clinical Payroll Accrual' : 60010,
    'Non-Clinical Bonus Expense' : 60100,
    'Non-Clinical Signing Bonuses' : 60105,
    'Non-Clinical Payroll Taxes' : 60200,
    'Non-Clinical Payroll Fees' : 60300,
    'Non-Clinical Vacation Expense' : 60400,
    'Severance Expense' : 60900,
    'Operating Lease Expense - Real Estate' : 61000,
    'Non-cash Rent Expense' : 61005,
    'Tenant Improvement Allowance Amortization' : 61010,
    'Sublease Income' : 61020,
    'CAM Expense' : 61040,
    'Facilities Cost' : 61045,
    'Utilities' : 61050,
    'Internet and Telephone' : 61055,
    'Property Tax' : 61200,
    'Equipment Lease Expense' : 61300,
    'Operating Lease Expense - Estimated Leases' : 61415,
    'Repairs and Maintenance' : 61500,
    'Medical Insurance' : 62000,
    'Dental Insurance' : 62001,
    'Vision Insurance' : 62005,
    'Basic Life AD&D' : 62010,
    'COBRA Admin' : 62011,
    'FSA Admin' : 62012,
    'Employee Assistance Program' : 62013,
    'Workers Compensation Insurance' : 62100,
    'General Liability Insurance' : 62105,
    'Auto Lease' : 63000,
    'Fuel and Mileage' : 63005,
    'Auto Repair and Maintenance' : 63010,
    'Parking and Tickets' : 63015,
    'Other Automobile Expense' : 63090,
    'Recruiting Fees' : 63100,
    '401k Employer Match Expense' : 63200,
    'Dues and Subscriptions' : 63300,
    'Physician Dues and Subscriptions' : 63305,
    'Training and Education' : 63400,
    'Physician Training and Education' : 63405,
    'Dry Cleaning' : 63900,
    'Uniforms' : 63905,
    'Other Employee Expenses' : 63999,
    'Advertising' : 64000,
    'Marketing' : 64005,
    'Meals' : 64100,
    'Entertainment' : 64105,
    'Travel Expense' : 64110,
    'Acquisition Costs' : 64200,
    'Deferred Purchase Price Amortization' : 64205,
    'Software Licenses' : 65000,
    'Software Licenses EBITDA Addback' : 65001,
    'Site Support Infrastructure' : 65005,
    'Outsourced IT Support' : 65010,
    'Computer Supplies' : 65020,
    'Licenses and Permits' : 65400,
    'Contract Services' : 65500,
    'Postage and Delivery' : 65600,
    'Printing and Reproduction' : 65605,
    'Storage' : 65610,
    'Website' : 65615,
    'Drinking Water' : 65620,
    'Charitable Contributions' : 65680,
    'Other Office Expenses' : 65690,
    'Office Supplies' : 65700,
    'Bank Fees' : 65800,
    'Credit Card Processing Fees' : 65850,
    'Late Fees and Penalties' : 65890,
    'Legal Fees' : 66000,
    'Legal Fees EBITDA Addback' : 66001,
    'Legal Settlements' : 66050,
    'Audit' : 66100,
    'Taxes' : 66105,
    'SEC Reporting' : 66110,
    'Accounting Services' : 66190,
    'Consulting' : 66200,
    'Consulting EBITDA Addback' : 66201,
    'Temp Labor' : 66210,
    'Management Fees to TOI MGT' : 66490,
    'Board Fees and Expenses' : 66500,
    'Goodwill impairement expense' : 67100,
    'Intangible Asset Expense' : 67200,
    'Share-based Compensation Expense' : 68000,
    'FFS Bad Debt Expense' : 68500,
    'FFS Bad Debt Recovery' : 68501,
    'Oral Drug Bad Debt Expense' : 68505,
    'ICRI Bad Debt Expense' : 68510,
    'Other Bad Debt Expense' : 68900,
    'Corp SG&A Elimination ' : 68950,
    'Fixed Costs Reclass ' : 68960,
    'Variable Costs Reclass ' : 68970,
    'Depreciation Expense' : 69000,
    'Financing Lease Depreciation Expense - Medical Equipment' : 69200,
    'Financing Lease Depreciation Expense - Other Equipment' : 69210,
    'Intangible Asset Amortization Expense' : 69600,
    'DFP Note Interest' : 70000,
    'Debt Amortization Expense' : 70005,
    'Financing Lease Interest - Medical Equipment' : 71200,
    'Financing Lease Interest - Other Equipment' : 71210,
    'Other Interest' : 79000,
    'Interest Income' : 80000,
    'Unrealized (Gain) Loss on Fixed Income - Treasury' : 81000,
    'Accretion and Amortization on Fixed Income - Treasury' : 81500,
    'Loss (Gain) on Disposal of Fixed Assets' : 85000,
    'Lease Impairment Expense' : 86200,
    'Lease Termination Expense' : 86500,
    'Private Warrants Expense' : 87000,
    'DFP Note Warrant Expense' : 87001,
    'Earnout Expense' : 87005,
    'DFP Note Embedded Derivative Expense' : 87006,
    'Miscellaneous Expense' : 89000,
    'Miscellaneous Expense EBITDA Addback' : 89001,
    'Miscellaneous Income' : 89005,
    'Miscellaneous Income EBITDA Addback' : 89006,
    'Transaction Costs' : 89900,
    'Income Tax Provision' : 90000,
    'Federal Tax Payments' : 91000,
    'State Tax Payments' : 92000,
    'Tax Penalty' : 99000,


}

duplicate_debits_dict = {
"Other Payroll Taxes",
"FUTA - Employer Tax",
"FUTA", "FICA", "SUI - Employer Tax", "SUI"
}