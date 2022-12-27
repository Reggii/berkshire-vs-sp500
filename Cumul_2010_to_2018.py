import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
from statistics import mean


# We read our data file using pandas and bind it to 'df'
df = pd.read_csv("Raw data/Berkshire_vs_500.csv", index_col="date")
# We set our index to the year, instead of an incremented integer for easier sorting
df.index = pd.to_datetime(df.index, format="%Y-%m-%d").year


# We will be analyzing years 2010 - 2018
# For that we filter out the years that we will not be looking at
df = df.loc["2010":"2018"]
df.loc[2010] = np.nan

df["Berkshire Hathaway"] = (
    df[["low_BRK", "high_BRK"]].pct_change(axis=1)["high_BRK"].mul(10)
)
df["S&P 500"] = df[["low_SP500", "high_SP500"]].pct_change(axis=1)["high_SP500"].mul(10)


df_cleared = (
    df.groupby([df.index])
    .mean()
    .fillna(0)
    .drop(
        columns=[
            "open_BRK",
            "open_SP500",
            "close_BRK",
            "close_SP500",
            "high_BRK",
            "high_SP500",
            "low_BRK",
            "low_SP500",
        ]
    )
)

# We create a line plot showing cumulative percentage changes from 2010 through 2017
plot = df_cleared.plot.line(grid=True)
plot.set_title(
    "Cumulative percentage change year to year from a 2010 baseline through 2017",
    fontsize=10,
)
loc = plticker.MultipleLocator(base=2.0)
plot.xaxis.set_major_locator(loc)
plot.set_xlabel("Year", fontsize=9)
vals = plot.get_yticks()
plot.set_yticklabels(["{:,.0%}".format(x) for x in vals])
plt.show()
