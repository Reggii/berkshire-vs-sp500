import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
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
).rename(columns={"close_BRK": "Berkshire Hathaway", "close_SP500": "S&P 500"})


# We will be analyzing years 1998 - 2018
# For that we filter out the years that we will not be looking at
df_cleared = df_cleared.loc["1998":"2018"]


# We group the daily closing figures we have per year, get their mean (average)
# then convert it to a cumulative percentage increase, starting from 0% in 1998
df_cleared = (
    df_cleared.groupby([df_cleared.index]).mean().pct_change().cumsum().fillna(0)
)


# We create a line plot showing cumulative percentage changes from 1998 through 2017
plot = df_cleared.plot.line(grid=True)
loc = plticker.MultipleLocator(base=2.0)
plot.xaxis.set_major_locator(loc)
plot.xaxis.set_tick_params(labelsize=9)
vals = plot.get_yticks()
plot.set_title(
    "Cumulative percentage change year to year from a 1998 baseline through 2017",
    fontsize=10,
)
plot.set_xlabel("Year")
plot.set_yticklabels(["{:,.0%}".format(x) for x in vals])
plt.show()
