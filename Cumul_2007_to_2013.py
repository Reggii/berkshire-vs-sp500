import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
from matplotlib.ticker import FuncFormatter
from statistics import mean


# We read our data file using pandas and bind it to 'df'
df = pd.read_csv("Raw data/Berkshire_vs_500.csv", index_col="date")
# We set our index to the year, instead of an incremented integer for easier sorting
df.index = pd.to_datetime(df.index, format="%Y-%m-%d").year


# We also filter out the columns we will not need in this plot
# We will be using the close columns only and we'll also rename them
df_cleared = df.drop(
    columns=[
        "high_BRK",
        "high_SP500",
        "low_BRK",
        "low_SP500",
        "open_BRK",
        "open_SP500",
    ]
).rename(
    columns={"close_BRK": "Berkshire Avg. Close", "close_SP500": "SP500 Avg. Close"}
)


# We will be analyzing years 2007 - 2013
# For that we filter out the years that we will not be looking at
df_cleared = df_cleared.loc["2007":"2012"]


# We group the daily closing figures we have per year, get their mean (average)
# then convert it to a cumulative percentage increase, starting from 0% in 1998
df_cleared = (
    df_cleared.groupby([df_cleared.index])
    .mean()
    .pct_change()
    .cumsum()
    .fillna(0)
    .mul(100)
    .round(2)
)


# We create a box plot showing cumulative percentage changes from 2007 through 2012
df_cleared = df_cleared.loc["2008":"2012"]
fig, ax = plt.subplots()
bar_width = 0.35
x = np.arange(len(df_cleared.index))
ax.grid(zorder=0)
berkshire = ax.bar(
    x - bar_width / 2,
    df_cleared["Berkshire Avg. Close"],
    bar_width,
    label="Berkshire Hathaway",
    zorder=3,
)
sp500 = ax.bar(
    x + bar_width / 2,
    df_cleared["SP500 Avg. Close"],
    bar_width,
    label="S&P 500",
    zorder=3,
)
ax.set_xlabel("Year", fontsize=9)
ax.set_title(
    "Cumulative percentage change year to year from a 2007 baseline through 2012",
    fontsize=10,
)
ax.set_xticks(x, df_cleared.index)

ax.legend(fontsize=9)

ax.bar_label(berkshire, padding=1, fontsize=7, fmt="%.2f%%")
ax.bar_label(sp500, padding=1, fontsize=7, fmt="%.2f%%")

formatter = FuncFormatter(lambda y, pos: "%d%%" % y)
ax.yaxis.set_major_formatter(formatter)

fig.tight_layout()

plt.show()
