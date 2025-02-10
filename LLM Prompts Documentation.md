**LLM Prompts Documentation**

### **Finance Prompts**

- Act as a finance expert. Review the attached screenshot and information
below:
Daily revenue is calculated as that day’s AUM * (Expense Ratio / 252). 
We use the divisor of 252 as the total number of business days in a year.
Flows are calculated as the change in shares outstanding 
for a client month over month, times the respective month end NAV.
So, if Client 1 holds 100 shares of X on Nov 30 at $25 a share, and then holds 
105 shares of X as of Dec 31 at $30 a share, then we would take (105-100) * 30 
to get the total net flow ($150). Market movement would have contributed 
$500 to the client’s position appreciating.
- on the net flows column. Would a positive net flow mean inflow and a 
negative net flow means outflow?
- What is an AUM history


### **Python Prompts**
- Act as a python expert. Load and excel sheet with pandas and return the 
columns names only. Do not load any rows.
- Given a date and a date time array, check that the array has any 
missing months. if missing add it. The array is the given date plus the 
last 11 months
For example:
given_date: '2023-12-31 00:00:00'
date_array = <DatetimeArray> 
['2023-01-31 00:00:00', '2023-02-28 00:00:00', '2023-03-31 00:00:00',
  '2023-05-31 00:00:00', '2023-06-30 00:00:00', 
 '2023-07-31 00:00:00', '2023-08-31 00:00:00', '2023-09-30 00:00:00',
 '2023-10-31 00:00:00', '2023-11-30 00:00:00', '2023-12-31 00:00:00']
Length: 12, dtype: datetime64[ns]1
- Insert the missing month in a pandas dataframe with the following columns. 
holdings should be 0 for the added row client_id, given_date, month_date, 
holdings missing:  '2023-04-30 00:00:00' return array with added date
- ValueError: all the input array dimensions except for the concatenation 
axis must match exactly, but along dimension 1, the array at index 0 has 
size 10 and the array at index 1 has size 2
- given a str date '2024-12-10' verify that the middle digits 12 are 
smaller than 13 if not flip to the last section to leave as yyyy-mm-dd
- if a month_date column in pandas dataframe is bigger than a 
2024-12-31 then add that date else Null to a new column
- the new date should be '2024-12-31' this is not working
- pd.Timestamp('2024-12-31') should be minus eight months
- I have two columns id month_date and expense_ratio:
update expense_ratio when id = 1001656  and month_date < 30-06-2024 to 28
- should I use pd.NA or np.nan for nulls

### **Data Engineer Prompts**
- Act as an expert data engineer and python developer. 
Review the following case study for a data enginneer interview position 
using python pandas. 
- Provide step one of the case study:
1. **Structure a Python ETL** to load the data.  
-1. Update the code to load WT Products table and WT Expense Rations. 
2. Update extract_client_holdings() to include wisdom_tree_id for each 
  ticker based on the WT Products table. 
3. transform_merge_data() to use numeric columns not strings 
- the NAV Data table has missing dates. What is the best practice to add 
the NAV values for the missing dates?
- This line is not working:
    nav_data = nav_data.set_index(["wisdom_tree_id", "market_date"]).unstack()
    .reindex(complete_dates).stack().reset_index()
- On extract_client_holdings some dates show up on different formats. 
I need to have all dates formated in y-m-d provide code only don't update 
- given a string date column '2024-30-01' review that the charcaters in the 
middle are equal or bigger than 12 if so format the date to be 2024-01-30
- On extract_nav_data do the following:
1. Remove line 12 the WT ID needs to be numeric
2. rename WT ID to wisdom_tree_id 
3. rename Date to quarter_date
4. rename NAV to net_asset_value
- add an option if there a slash on the string to do the split by slash
- fFx this message:
UserWarning: Could not infer format, so each element will be parsed individually, 
falling back to dateutil. To ensure parsing is consistent and as-expected, 
please specify a format.
  df_long["quarter_date"] = pd.to_datetime(df_long["quarter_date"], errors="coerce")
- correct this lines:
   complete_dates = pd.date_range(start=nav_data["market_date"].min(), 
                                   end=nav_data["market_date"].max(), freq="D")
the start should be the first day of oldest year and the end the last day of the latest year
- On holdings_df columns ['client_id', 'quarter_date', 'month_date', 'wisdom_tree_id', 'holdings', 
       'start_date', 'end_date']
Whenever holdings == 0 replace the value using the month_date from the previous quarter
provide code only
- explain code
- On fill_missing_nav_dates() add column named "is_backfilled" make 1 all 
NaN values "net_asset_value" provide code only
- On the following function fill_zero_holdings() add a line to create a
 column is_backfilled for all the holdings = 0
- before return holdings_df do a forward fill on holdings that are Nan