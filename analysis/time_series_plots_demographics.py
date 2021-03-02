import matplotlib.pyplot as plt
from rate_calculation_demographics import time_series, measures
import pandas as pd

diseases = ["CVD", "respiratory_disease", "cancer"]
demographic_variables = ["region", "ethnicity", "imd"]

for disease in diseases:
    df_dict = time_series[disease]
    
    




    fig, axes = plt.subplots(len(demographic_variables), figsize=[10, 12])

    for i, variable in enumerate(demographic_variables):
        df = df_dict[variable]
        
        #if imd qcut
        if variable == "imd":
           
            imd_column =df[variable]
            imd_cut = pd.qcut(x=imd_column, q=5, duplicates="drop")
            df['imd'] = imd_cut

        for x in df[variable].unique():
            df_subset = df[df[variable] == x]
            df_subset = df_subset.sort_values(by="date")
           

            axes[i].plot(
                df_subset["date"], df_subset["European Standard population rate per 100,000"], label=x)
            axes[i].grid(which="both", axis="y", color="#666666",
                        linestyle="-", alpha=0.2)
            title = f"{chr(97 + i)}) {disease} hospitalisation rates by {variable}"
            axes[i].set_title(title, loc="left")

            axes[i].legend(loc=3, prop={"size": 9})
            axes[i].set_ylabel("Rate per 100,000 people")
            axes[i].set_ylim(ymin=0)
            plt.tight_layout()
  
    plt.savefig(f"output/time_series_plot_{disease}.svg")
