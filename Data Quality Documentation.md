**Data Quality Documentation**

### **Expense Ratios Table**

- Refer to methods:
   + extract_expense_ratios()

- extract_expense_ratios(): 
   + Columns renamed to lower case, spaces removed with underscores.

### **Holdings Table**

- Refer to methods:
   + add_holdings_end_date_column()
   + fill_missing_months_holdings()
   + fill_zero_holdings()
   + holdings_format_and_convert_date()
   + process_client_holdings()

- add_holdings_end_date_column(): 
   + Creates an "end_date" column using the next quarter date for a month_date.
   + Adds NULL where there is no next quater date.

- process_client_holdings(): 
   + Columns renamed to lower case, spaces removed with underscores.
   + Excel sheets sorted by client by quarter date ascending to process
      data in correct sequence and avoid mixing data between clients.
   + "client_id" column added.
   + "quarter_date" column added.
   + "start_date" (current quarter_date) and "end_date" (next quarter_date) 
     columns added. This ensures correct storage of rolling data. 
     end_date = NULL will be the most recent data for that month.

- fill_missing_months_holdings(): 
   + Missing months are added per quarter per client with holdings = 0.
   + Forward fills holdings previous month where month does not exist 
     on the previous quarter.

- fill_zero_holdings():
   + Checks for nulls and empty cells and converts holdings to 0.
   + Backfills holdings = 0 with the holdings value from the same 
     month date from the previous quarter.
   + Forward fills holdings previous month where month does not exist 
     on the previous quarter.
   + "is_holdings_backfilled" boolean column created to flag backfilled rows.

### **Monthly Analytics Table**

- Refer to methods:
   + transform_monthly_analytics()

- transform_monthly_analytics():
   + Uses end_date = NULL to filter latest monthly available data
   + Sorts by client, product_id, and month_date to ensure accurate process
     of calculations (current month - previous month)
   + Change on GGRE expense ratio applied
   + Oldest month metrics will be NULL as no there is no previous month 
      to perform operations


### **NAV Table**

- Refer to methods:
   + extract_nav()
   + nav_format_and_convert_date()
   + fill_missing_nav_dates()

- extract_nav(): 
   + Columns renamed to lower case, spaces removed with underscores.
   + Product id column to integer type.
   + Market Date date formated to date type and yyyy-mm-dd column using 
     nav_format_and_convert_date() method.
   + df.loc for 1:3 stock split on product 3105371.

- fill_missing_nav_dates(): 
   + Missing dates added using backward fill.
   + Forward fill applied to remaining nulls.
   + "is_nav_backfilled" boolean column created to flag backfilled rows.

### **Products Table**

- Refer to methods:
   + extract_products()

- extract_products(): 
   + Columns renamed to lower case, spaces removed with underscores.

### **Potential Upgrades**

- On holdings table Check for missing quarters and add full list of months. 
- Add logger to log error messages and monitor missing months.
- Develop separate pipeline to add single/multiple quarter data to holdings table.

