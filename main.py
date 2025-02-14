import time


from config import (
    EXCEL_FILE_PATH,
    ANALYTICS_OUTPUT_FILE_PATH,
    HOLDINGS_OUTPUT_FILE_PATH,
    NAV_OUTPUT_FILE_PATH
)
from transformations import WisdomTreeDataPipeline

start_time = time.time()


if __name__ == "__main__":

    etl_pipeline = WisdomTreeDataPipeline(EXCEL_FILE_PATH)

    nav_df = etl_pipeline.extract_nav()

    holdings_df = etl_pipeline.process_client_holdings()

    monthly_analytics_df = etl_pipeline.transform_monthly_analytics(
        holdings_df, nav_df)

    holdings_df.to_excel(HOLDINGS_OUTPUT_FILE_PATH, index=False)

    nav_df.to_excel(NAV_OUTPUT_FILE_PATH, index=False)

    monthly_analytics_df.to_excel(ANALYTICS_OUTPUT_FILE_PATH, index=False)


end_time = time.time()

runtime = end_time - start_time
print("Runtime:", runtime, "seconds")
