import pandas as pd
from pandas_profiling import ProfileReport

df = pd.read_csv("station_hour.csv")

print(df)

profile = ProfileReport(df)
profile.to_file(output_file="station_hour.csv")