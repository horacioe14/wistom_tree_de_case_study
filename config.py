# config.py

import os

# Define environment variables
EXCEL_FILE_PATH = os.getenv("EXCEL_FILE_PATH", "HistoricalClientHoldings.xlsx")

ANALYTICS_OUTPUT_FILE_PATH = os.getenv(
    "ANALYTICS_OUTPUT_FILE_PATH", "./outputs/monthly_analytics_output.xlsx")
EXPENSE_OUTPUT_FILE_PATH = os.getenv(
    "EXPENSE_OUTPUT_FILE_PATH", "./outputs/expense_ratios_output.xlsx")

HOLDINGS_OUTPUT_FILE_PATH = os.getenv(
    "HOLDINGS_OUTPUT_FILE_PATH", "./outputs/holdings_output.xlsx")
NAV_OUTPUT_FILE_PATH = os.getenv(
    "NAV_OUTPUT_FILE_PATH", "./outputs/nav_output.xlsx")
