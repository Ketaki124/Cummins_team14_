import pandas as pd
import datetime
from sklearn.preprocessing import LabelEncoder

# Read each Excel file into separate DataFrames
df_2012 = pd.read_csv("Exchange_Rate_Report_2012.csv")
df_2013 = pd.read_csv("Exchange_Rate_Report_2013.csv")
df_2014 = pd.read_csv("Exchange_Rate_Report_2014.csv")
df_2015 = pd.read_csv("Exchange_Rate_Report_2015.csv")
df_2016 = pd.read_csv("Exchange_Rate_Report_2016.csv")
df_2017 = pd.read_csv("Exchange_Rate_Report_2017.csv")
df_2018 = pd.read_csv("Exchange_Rate_Report_2018.csv")
df_2019 = pd.read_csv("Exchange_Rate_Report_2019.csv")
df_2020 = pd.read_csv("Exchange_Rate_Report_2020.csv")
df_2021 = pd.read_csv("Exchange_Rate_Report_2021.csv")
df_2022  = pd.read_csv("Exchange_Rate_Report_2022.csv")

dfs = [df_2012, df_2013, df_2014, df_2015, df_2016, df_2017, df_2018, df_2019, df_2020, df_2021, df_2022]

# Concatenate all DataFrames into one
combined_df = pd.concat(dfs, ignore_index=True)
# Save the combined DataFrame to a new CSV file
combined_df.to_csv("combined_exchange_rate.csv", index=False)