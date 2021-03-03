import matplotlib.pyplot as plt
from rate_calculation_demographics import time_series, measures
import pandas as pd
import numpy as np

diseases = ["CVD", "respiratory_disease", "cancer"]
figure_cut_offs = {"CVD": 250, "respiratory_disease": 200, "cancer": 100}
demographic_variables = ["region", "ethnicity", "imd"]
ethnicity_codes = {1: "White", 2: "Mixed", 3: "Asian", 4: "Black", 5:"Other", np.nan: "unknown"}





for disease in diseases:
    df_dict = time_series[disease]
    
    




    fig, axes = plt.subplots(len(demographic_variables), figsize=[10, 12])

    for i, variable in enumerate(demographic_variables):
        df = df_dict[variable]
        
        #if imd qcut
        if variable == "imd":
            
            imd_column = df["imd"]
            df["imd"] = pd.qcut(imd_column, q=5,duplicates="drop")
        
            df = df.groupby(by=["date", variable])["European Standard population rate per 100,000"].mean().reset_index()
            
        #if ethnicity map codes
        if variable == "ethnicity":

            ethnicity_column = df["ethnicity"]
            df = df.replace({"ethnicity": ethnicity_codes})
        

        for x in df[variable].unique():
            df_subset = df[df[variable] == x]
            df_subset = df_subset.sort_values(by="date")
           

            axes[i].plot(
                df_subset["date"], df_subset["European Standard population rate per 100,000"], label=x)
            axes[i].grid(which="both", axis="y", color="#666666",
                        linestyle="-", alpha=0.2)
            title = f"{chr(97 + i)}) {disease} hospitalisation rates by {variable}"
            axes[i].set_title(title, loc="left")

            if variable=="imd":
                axes[i].legend(loc=3, prop={"size": 9}, labels=["Most deprived", "", "", "","Least deprived"])
                
            else:

                axes[i].legend(loc=3, prop={"size": 9})
            axes[i].set_ylabel("Rate per 100,000 people")
            
            axes[i].set_ylim(ymin=0, ymax=figure_cut_offs[disease])
            
          
            plt.tight_layout()
  
    plt.savefig(f"output/time_series_plot_{disease}.svg")
