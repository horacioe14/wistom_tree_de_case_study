import time


from transformations import WisdomTreeDataPipeline

start_time = time.time()


if __name__ == "__main__":
    file_path = "HistoricalClientHoldings.xlsx"
    etl_pipeline = WisdomTreeDataPipeline(file_path)

    nav_df = etl_pipeline.extract_nav()
    holdings_df = etl_pipeline.process_client_holdings()

    monthly_analytics_df = etl_pipeline.transform_monthly_analytics(
        holdings_df, nav_df)

    nav_df.to_excel("nav_output.xlsx", index=False)
    holdings_df.to_excel("holdings_output.xlsx", index=False)
    monthly_analytics_df.to_excel("monthly_analytics_output.xlsx", index=False)


end_time = time.time()

runtime = end_time - start_time
print("Runtime:", runtime, "seconds")
