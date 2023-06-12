from fastf1.core import Laps
import fastf1 as f1
import pandas as pd
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

f1.Cache.enable_cache(r"C:\Users\krusa\Documents\GitHub\Formula1\Cache")
# f1.Cache.clear_cache(r"C:\Users\krusa\Documents\GitHub\Formula1\Cache")


# f1.Cache.enable_cache(r"D:\krusa\Documents\GitHub\Formula1\Cache")
# f1.Cache.clear_cache(r"D:\krusa\Documents\GitHub\Formula1\Cache")

races = ["BAHRAIN", "SAUDI", "AUSTRALIA", "BAKU", "MIAMI", "MONACO", "SPAIN"]


for race in races:
    Year = 2023
    GP = race
    Type = "R"
    session = f1.get_session(Year, GP, Type)
    session.load()

    df = pd.DataFrame(session.laps)
    df.to_csv(f"Data/{GP}_Race_laps.csv", index=False)
