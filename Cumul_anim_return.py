import pandas as pd
import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
from statistics import mean


# We read our data file using pandas and bind it to 'df'
df = pd.read_csv("Raw data/Berkshire_vs_500.csv")
# We set our index to the year, instead of an incremented integer for easier sorting
df["Year"] = pd.to_datetime(df["date"], format="%Y-%m-%d").apply(lambda x: x.year)


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
        "date",
    ]
).rename(columns={"close_BRK": "Berkshire Hathaway", "close_SP500": "S&P 500"})


# We will be analyzing years 1998 - 2018
# For that we filter out the years that we will not be looking at
df_cleared = df_cleared.loc[(df["Year"] > 1997) & (df["Year"] < 2019)]


# We group the daily closing figures we have per year, get their mean (average)
# then convert it to a cumulative percentage increase, starting from 0% in 1998
df_cleared = (
    df_cleared.groupby(df["Year"])["Berkshire Hathaway", "S&P 500"]
    .mean()
    .pct_change()
    .cumsum()
    .fillna(0)
    .reset_index()
)

fig, ax = plt.subplots()
plt.ion()

for i, row in df_cleared.iterrows():
    ax.cla()
    ax.set_title(
        "Cumulative percentage change year to year from a 1998 baseline through 2018",
        fontsize=9,
    )

    loc_x = plticker.MultipleLocator(base=2.0)
    loc_y = plticker.MultipleLocator(base=0.15)
    formatter = matplotlib.ticker.StrMethodFormatter("{x:.0f}")

    ax.xaxis.set_major_locator(loc_x)
    ax.yaxis.set_major_locator(loc_y)
    ax.xaxis.set_minor_formatter(plticker.NullFormatter())
    ax.xaxis.set_major_formatter(formatter)

    plot = df_cleared.iloc[: i + 1, :].plot(x="Year", ax=ax)
    vals = plot.get_yticks()
    plot.set_yticklabels(["{:,.0%}".format(x) for x in vals])
    plt.legend(loc="upper left", fontsize=7)
    fig.canvas.draw_idle()
    savefile = str(i) + "_plot" + ".png"
    plt.savefig(savefile)

plt.show()
