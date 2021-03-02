import matplotlib.pyplot as plt
from rate_calculations import time_series, measures

diseases = ["CVD", "respiratory_disease", "cancer"]
fig, axes = plt.subplots(ncols=1, nrows=3, sharey=False, figsize=[10, 12])
for i, ax in enumerate(axes.flat):
    df = time_series[i]
    df.plot(ax=ax, color=["#176dde", "#ffad33"])
    ax.grid(which="both", axis="y", color="#666666", linestyle="-", alpha=0.2)
    name = measures[i].numerator.replace("_", " ")
    title = f"{chr(97 + i)}) {diseases[i]} hospitalisation rates"
    ax.set_title(title, loc="left")
    ax.xaxis.label.set_visible(False)
    ax.legend(loc=3, prop={"size": 9})
    ax.set_ylabel("Rate per 100,000 people")
    ax.set_ylim(ymin=0)
    plt.tight_layout()
plt.savefig("output/time_series_plot.svg")
