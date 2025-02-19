import pandas as pd


class WisdomTreeDataPipeline:
    """
    Class that extracts and transforms:
    Two years of **NAV history**, by day, for four WisdomTree products.
    Rolling 1-year files containing **holdings of clients**, provided
    quarterly.
    The reporting partnership started in December 2023 and is received
    on each quarter-end.
    Each reporting covers the preceding 12 months, so restatements or
    alterations toprevious months will be handled in a subsequent
    reporting cycle.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.excel_file = pd.ExcelFile(file_path)
        self.products_table = self.extract_products()
        # self.expense_ratios_table = self.extract_expense_ratios()

    def nav_format_and_convert_date(self, date_string: str):
        """
        Check if the first part of the date is >= 12,
        then reformat and convert to datetime to y-m-d.
        """
        try:
            if "/" in date_string:
                date_part = date_string.split("/")
            else:
                date_part = date_string.split("-")

            if len(date_part) == 3 and int(date_part[0]) > 12:
                formatted_date = f"{date_part[2]
                                    }-{date_part[1]}-{date_part[0]}"

            else:
                formatted_date = f"{date_part[2]
                                    }-{date_part[0]}-{date_part[1]}"

            return pd.to_datetime(formatted_date, format="%Y-%m-%d", errors="coerce")
        except Exception as e:
            print(f"Error, nav_format_and_convert_date() failed: {str(e)}")
            return None

    def holdings_format_and_convert_date(self, date_string: str):
        """
        Check if the middle part of the date is >= 12,
        then reformat and convert to datetime to y-m-d.
        """
        try:
            if "/" in date_string:
                date_part = date_string.split("/")
            else:
                date_part = date_string.split("-")

            if len(date_part) == 3 and int(date_part[1]) > 12:
                formatted_date = f"{date_part[0]
                                    }-{date_part[2]}-{date_part[1]}"
            else:
                # Keep original format if condition is not met
                formatted_date = date_string

            return pd.to_datetime(formatted_date, format="%Y-%m-%d", errors="coerce")
        except Exception as e:
            print(
                f"Error, holdings_format_and_convert_date() failed: {str(e)}")
            return None

    def extract_products(self) -> pd.DataFrame:
        """
        1.Extracts WT Products table
        2.Renames columns.
        """
        try:
            products_df = pd.read_excel(
                self.excel_file, sheet_name="WT Products")
            products_df = products_df.rename(
                columns={
                    "WT ID": "product_id",
                    "Ticker": "ticker",
                    "Product Name": "product_name",
                }
            )
            return products_df
        except Exception as e:
            print(f"Error, extract_products_data() failed: {str(e)}")
            return None

    def adjust_expense_ratio(
            self,
            input_raw_expense_df: pd.DataFrame,
            input_nav_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Backfills expense ratios data of missing dates and NAV values
        """
        try:
            # Date range to get missing dates
            start_year = input_nav_df["market_date"].min().year
            end_year = input_nav_df["market_date"].max().year

            # Generate a complete date range using the last day of each month
            complete_dates = pd.date_range(
                start=f"{start_year}-01-01",
                end=f"{end_year}-12-31",
                freq="ME"  # "ME" ensures the last day of each month
            )

            # Create a new dataframe with completed date range
            # for each product_id
            unique_ids = input_raw_expense_df["product_id"].unique()
            # Cartesian product of indexes using the product ids
            # and full list of dates
            complete_index = pd.MultiIndex.from_product(
                [unique_ids, complete_dates], names=[
                    "product_id", "last_modified_date"]
            )

            # Reindex expense data to ensure all dates exist for each
            # product_id
            expense_ratios_df = input_raw_expense_df.set_index(["product_id", "last_modified_date"]).reindex(
                complete_index
            )

            # Backward fill expense values within each product_id
            expense_ratios_df = expense_ratios_df.sort_values(
                ["last_modified_date"]).reset_index()

            expense_ratios_df["is_expense_ratios_backfilled"] = (
                expense_ratios_df["expense_ratio"].isna().astype(bool)
            )
            expense_ratios_df["expense_ratio"] = expense_ratios_df.groupby(["product_id"])[
                "expense_ratio"
            ].bfill()

            # Forward fill if any remaining nulls
            if expense_ratios_df["expense_ratio"].isnull().values.any():
                expense_ratios_df["expense_ratio"] = expense_ratios_df.groupby(["product_id"])[
                    "expense_ratio"
                ].ffill()

            return expense_ratios_df

        except Exception as e:
            print(f"Error, adjust_expense_ratio() failed: {str(e)}")
            return None

    def extract_expense_ratios(self, input_nav_df: pd.DataFrame) -> pd.DataFrame:
        """
        1. Extracts WT Expense Ratios table
        2. renames columns.
        """
        try:
            expense_df = pd.read_excel(
                self.excel_file, sheet_name="WT Expense Ratios")
            expense_df = expense_df.rename(
                columns={"Expense Ratio": "expense_ratio",
                         "WT ID": "product_id"}
            )
            expense_df["last_modified_date"] = pd.to_datetime(
                expense_df["last_modified_date"],
                format="%Y-%m-%d",
                errors="coerce",
            )
            output_expense_df = self.adjust_expense_ratio(
                expense_df, input_nav_df)
            print("expense ratios data processing completed successfully")

            return output_expense_df
        except Exception as e:
            print(f"Error, extract_expense_ratios() failed: {str(e)}")
            return None

    def extract_nav(self) -> pd.DataFrame:
        """
        1. Extracts Net Asset Value Data from the Excel file
        2. renames columns
        3. Converts date column to date type.
        """
        try:
            nav_df = pd.read_excel(self.excel_file, sheet_name="NAV Data")
            nav_df = nav_df.rename(
                columns={
                    "WT ID": "product_id",
                    "Date": "market_date",
                    "NAV": "net_asset_value",
                }
            )
            # If 'coerce', then invalid parsing will be set as NaT.
            nav_df["market_date"] = nav_df["market_date"].apply(
                self.nav_format_and_convert_date
            )

            nav_df["product_id"] = nav_df["product_id"].astype(int)

            output_nav_df = self.fill_missing_nav_dates(nav_df)

            # Adjust WCLD stock split (1-for-3 on 31 March 2024)
            # Starting from 30th due to backfill
            # output_nav_df.loc[
            #     (output_nav_df["product_id"] == 3105371)
            #     & (output_nav_df["market_date"] >= "2024-03-30"),
            #     "net_asset_value",
            # ] *= 3

            print("nav data processing completed successfully")
            return output_nav_df
        except Exception as e:
            print(f"Error, extract_nav_data {str(e)}")
            return None
            # return  log.logMsg("Error", f"extract_nav_data() failed: {str(e)}")

    def process_client_holdings(self) -> pd.DataFrame:
        """
        1. Extracts multiple client holdings data from multiple sheets
        2. Combines client data into single table and adds start_date
        and end_date for each quarter sheet to manage changing dimensions
        3. Adds id of tickers from products tables
        """
        try:
            client_holdings_list = []
            # Extract client ids
            client_ids_list = [
                sheet.split("_")[0]
                for sheet in self.excel_file.sheet_names
                if "client" in sheet.lower()
            ]
            # Remove client ids duplicates and sort ascending

            client_ids_list = list(dict.fromkeys(client_ids_list))
            client_ids_list.sort()

            # Loop by client
            for client_id in client_ids_list:
                # Extract all sheets matching the client_id and sort ascending
                sheet_quarters_list = [
                    sheet for sheet in self.excel_file.sheet_names if client_id in sheet
                ]
                # quarters_list = [sheet_name.split("_")[1] for sheet_name in sheet_quarters_list]
                # print(quarters_list)
                sheet_quarters_list.sort()
                # print(sheet_quarters_list)
                # Loop thorugh sheet name to start extracting data
                for sheet in sheet_quarters_list:
                    # Extract quarter date
                    sheet_quarter = sheet.split("_")[1]
                    # Extract all sheets of the same client id
                    client_sheet_df = pd.read_excel(
                        self.excel_file, sheet_name=sheet)
                    # make all columns lower case
                    client_sheet_df.columns = map(
                        str.lower, client_sheet_df.columns)
                    # make all acronyms upper case
                    client_sheet_df["ticker"] = client_sheet_df["ticker"].str.upper(
                    )
                    # unpivot table to create "month_date" column
                    client_unpivot_df = client_sheet_df.melt(
                        id_vars=["ticker"], var_name="month_date", value_name="holdings"
                    )
                    # check for missing months
                    client_unpivot_df = self.fill_missing_months_holdings(
                        client_id.lower(), sheet_quarter, client_unpivot_df
                    )

                    client_unpivot_df["client_id"] = client_id.lower()
                    client_unpivot_df["quarter_date"] = sheet_quarter
                    client_unpivot_df["start_date"] = sheet_quarter
                    client_unpivot_df["start_date"] = pd.to_datetime(
                        client_unpivot_df["start_date"],
                        format="%Y-%m-%d",
                        errors="coerce",
                    )
                    client_unpivot_df["quarter_date"] = pd.to_datetime(
                        client_unpivot_df["quarter_date"],
                        format="%Y-%m-%d",
                        errors="coerce",
                    )

                    # Create end_date column
                    client_unpivot_df = self.add_holdings_end_date_column(
                        sheet, sheet_quarters_list, client_unpivot_df)

                    client_holdings_list.append(client_unpivot_df)

            # Join with products table to get product_id
            holdings_df = pd.concat(client_holdings_list, ignore_index=True)
            holdings_df = holdings_df.merge(
                self.products_table.drop(columns=["product_name"]),
                on="ticker",
                how="left",
            )
            holdings_df.drop(columns=["ticker"])
            holdings_df["product_id"] = holdings_df["product_id"].astype(
                int)

            # Adjust for WCLD stock split (1:3 on 31 March 2024)
            holdings_df.loc[
                (holdings_df["product_id"] == 3105371)
                & (holdings_df["month_date"] >= "2024-03-31"),
                "holdings",
            ] *= 3
            # clean table columns
            holdings_df = holdings_df[
                [
                    "client_id",
                    "quarter_date",
                    "month_date",
                    "product_id",
                    "holdings",
                    "start_date",
                    "end_date",
                ]
            ]

            output_holdings_df = self.fill_zero_holdings(holdings_df)
            print("client holdings data processing completed successfully")

            return output_holdings_df

        except Exception as e:
            print(f"Error, process_client_holdings() failed: {str(e)}")
            return None

    def add_holdings_end_date_column(
            self,
            input_sheet_name: str,
            input_sheets_list: list,
            input_df: pd.DataFrame) -> pd.DataFrame:
        """
        Creates end_date column using the next quarter date for a month_date.
        Adds NULL where there is no next quater date
        """
        try:

            quarter_index = input_sheets_list.index(input_sheet_name)
            if quarter_index < len(input_sheets_list) - 1:
                current_quarter = input_sheets_list[quarter_index].split("_")[
                    1
                ]
                target_date = pd.Timestamp(current_quarter) - pd.DateOffset(
                    months=8
                )
                quarter_index += 1
                next_quarter = pd.Timestamp(
                    input_sheets_list[quarter_index].split("_")[1]
                )
                input_df["end_date"] = input_df[
                    "month_date"
                ].apply(
                    lambda month_date: (
                        next_quarter if month_date >= target_date else pd.NA
                    )
                )

            else:
                input_df["end_date"] = pd.NA

            # If 'coerce', then invalid parsing will be set as NaT.
            input_df["end_date"] = pd.to_datetime(
                input_df["end_date"],
                format="%Y-%m-%d",
                errors="coerce",
            )

            return input_df
        except Exception as e:
            print(f"Error, add_holdings_end_date_column() failed: {str(e)}")
            return None

    def fill_missing_months_holdings(
        self,
        input_client_id: str,
        input_quarter_date: str,
        input_holdings_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Checks for missing months and inserts row with holdings == 0
        """
        try:
            # Generate a full list of months from the given date going back 11 months
            all_months = pd.date_range(
                end=input_quarter_date, periods=12, freq="ME")

            # Find the missing months
            input_holdings_df["month_date"] = input_holdings_df["month_date"].apply(
                self.holdings_format_and_convert_date
            )
            existing_months = input_holdings_df["month_date"].unique()
            missing_months = all_months.difference(existing_months)

            if len(missing_months) > 0:
                print("Client Holdings Processing Warning:")
                print(
                    f"{input_client_id} | {input_quarter_date} | missing months:{
                        list(missing_months)}"
                )
                for name in input_holdings_df["ticker"].unique():
                    # Create rows for missing months with holdings set to 0
                    new_rows = pd.DataFrame(
                        {
                            "ticker": [name for month in range(len(missing_months))],
                            "month_date": missing_months,
                            "holdings": [0 for month in range(len(missing_months))],
                        }
                    )
                    # Append the new rows to the original DataFrame and sort by month_tdate
                    input_holdings_df = pd.concat(
                        [input_holdings_df, new_rows.astype(
                            input_holdings_df.dtypes)],
                        ignore_index=True,
                    ).sort_values("month_date")

                    # print(input_holdings_df.dtypes)
                return input_holdings_df

            return input_holdings_df
        except Exception as e:
            print(f"Error, fill_missing_months_holdings() failed: {str(e)}")
            return None

    def fill_zero_holdings(self, holdings_df):
        """
        1. Replace holdings == 0 with the value from
        the same month_date in the previous quarter
        2. Forward fills holdings with previous month
        where that month does not exist on the previous quarter
        3. Creates boolean column "is_holdings_backfilled" where holdings == 0
        """
        try:
            holdings_df = holdings_df.sort_values(
                ["client_id", "product_id", "quarter_date"]
            )

            # Convert nulls and empty cells to 0
            holdings_df["holdings"] = holdings_df["holdings"].fillna(0)
            holdings_df["holdings"] = holdings_df["holdings"].replace("", 0)
            holdings_df["holdings"] = holdings_df["holdings"].replace(" ", 0)
            holdings_df["is_holdings_backfilled"] = (
                holdings_df["holdings"] == 0
            ).astype(bool)

            missing_holdings_mask = holdings_df["holdings"] == 0

            # Shift one to get previous quarter
            holdings_df.loc[missing_holdings_mask, "holdings"] = holdings_df.groupby(
                ["client_id", "product_id", "month_date"]
            )["holdings"].shift(1)

            # Forward fills holdings previous month instead where
            # month does not exist on the previous quarter
            if holdings_df["holdings"].isnull().values.any():
                holdings_df["holdings"] = holdings_df.groupby(
                    ["client_id", "product_id"]
                )["holdings"].ffill()

            return holdings_df
        except Exception as e:
            print(f"Error, fill_missing_nav_dates() failed: {str(e)}")
            return None

    def fill_missing_nav_dates(self, nav_data: pd.DataFrame) -> pd.DataFrame:
        """
        Backfills NAV data of missing dates and NAV values
        """
        try:
            # Date range to get missing dates
            start_year = nav_data["market_date"].min().year
            end_year = nav_data["market_date"].max().year

            complete_dates = pd.date_range(
                start=f"{start_year}-01-01", end=f"{end_year}-12-31", freq="D"
            )

            # Create a new dataframe with completed date range
            # for each product_id
            unique_ids = nav_data["product_id"].unique()
            # Cartesian product of indexes using the product ids
            # and full list of dates
            complete_index = pd.MultiIndex.from_product(
                [unique_ids, complete_dates], names=[
                    "product_id", "market_date"]
            )

            # Reindex NAV data to ensure all dates exist for each
            # product_id
            nav_data = nav_data.set_index(["product_id", "market_date"]).reindex(
                complete_index
            )

            # Backward fill NAV values within each product_id
            nav_data = nav_data.sort_values(["market_date"]).reset_index()

            nav_data["is_nav_backfilled"] = (
                nav_data["net_asset_value"].isna().astype(bool)
            )
            nav_data["net_asset_value"] = nav_data.groupby(["product_id"])[
                "net_asset_value"
            ].bfill()

            # Forward fill if any remaining nulls
            if nav_data["net_asset_value"].isnull().values.any():
                nav_data["net_asset_value"] = nav_data.groupby(["product_id"])[
                    "net_asset_value"
                ].ffill()

            return nav_data

        except Exception as e:
            print(f"Error, fill_missing_nav_dates() failed: {str(e)}")
            return None

    def transform_monthly_analytics(
        self,
        input_expense_df: pd.DataFrame,
        input_holdings_df: pd.DataFrame,
        input_nav_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Estimates:
        - Monthly AUM
        - Daily revenue
        - Net flows
        - market movement
        """
        try:

            # Get the latest data of holdings
            holdings_latest_df = input_holdings_df[
                input_holdings_df["end_date"].isnull()
            ]

            # Get the latest data of expense
            # expense_latest_df = self.adjust_expense_ratio(input_nav_df)
            # print(expense_latest_df.head(100))

            holdings_latest_df = holdings_latest_df.sort_values(
                ["client_id", "product_id", "month_date"]
            )

            # Left join holdings table with with nav and expenses tables
            holdings_nav_df = holdings_latest_df.merge(
                input_nav_df,
                left_on=["product_id", "month_date"],
                right_on=["product_id", "market_date"],
                how="left",
            )

            holdings_nav_expense_df = holdings_nav_df.merge(
                input_expense_df,
                left_on=["product_id", "month_date"],
                right_on=["product_id", "last_modified_date"],
                how="left",
            )

            # # Adjust GGRA expense ratio change on 30 June 2024
            # holdings_nav_expense_df.loc[
            #     (holdings_nav_expense_df["product_id"] == 1001656)
            #     & (holdings_nav_expense_df["market_date"] < pd.Timestamp("2024-06-30")),
            #     "expense_ratio",
            # ] = 0.0028

            ## CALCULATIONS##
            # AUM = hodlings * nav
            holdings_nav_expense_df["assets_under_management"] = (
                holdings_nav_expense_df["holdings"]
                * holdings_nav_expense_df["net_asset_value"]
            )

            # Daily Revenue = aum * (yearly expense ratio/252)
            holdings_nav_expense_df["daily_revenue"] = holdings_nav_expense_df[
                "assets_under_management"
            ] * (holdings_nav_expense_df["expense_ratio"] / 252)

            # Net Flow = share change (monthly holdings − previous month holdings) * monthly nav
            holdings_nav_expense_df["share_change"] = holdings_nav_expense_df[
                "holdings"
            ].diff()
            holdings_nav_expense_df["net_flow"] = (
                holdings_nav_expense_df["share_change"]
                * holdings_nav_expense_df["net_asset_value"]
            )

            # Market Movement = AUM month - AUM previous month - Net Flow
            holdings_nav_expense_df["market_movement"] = (
                holdings_nav_expense_df["assets_under_management"].diff()
                - holdings_nav_expense_df["net_flow"]
            )

            holdings_nav_expense_df = holdings_nav_expense_df[
                [
                    "client_id",
                    "product_id",
                    "month_date",
                    "is_holdings_backfilled",
                    "holdings",
                    "is_nav_backfilled",
                    "net_asset_value",
                    "assets_under_management",
                    "is_expense_ratios_backfilled",
                    "daily_revenue",
                    "share_change",
                    "net_flow",
                    "market_movement",
                ]
            ]
            holdings_nav_expense_df.sort_values("month_date")

            # Clean oldest month for each client make null
            wrong_values_mask = (
                holdings_nav_expense_df["month_date"]
                == holdings_nav_expense_df["month_date"].min()
            )
            holdings_nav_expense_df.loc[wrong_values_mask,
                                        "share_change"] = pd.NA
            holdings_nav_expense_df.loc[wrong_values_mask, "net_flow"] = pd.NA
            holdings_nav_expense_df.loc[wrong_values_mask,
                                        "market_movement"] = pd.NA
            print("client monthly analytics processing completed successfully")

            return holdings_nav_expense_df
        except Exception as e:
            print(f"Error, transform_monthly_aum() failed: {str(e)}")
            return None
