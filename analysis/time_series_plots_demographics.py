import matplotlib.pyplot as plt
from rate_calculation_demographics import combined_diseases
import pandas as pd
import numpy as np


populations = ['total', 'emergency', 'elective']
demographic_variables = ["ethnicity", "imd_group", "sex"]
ethnicity_codes = {'1.0': "White", '2.0': "Mixed", '3.0': "Asian", '4.0': "Black", '5.0':"Other", np.nan: "unknown"}

y_lims = {'total': 180, 'emergency': 90 , 'elective': 110}

for pop in populations:
    df_dict = combined_diseases[pop]
    
    fig, axes = plt.subplots(len(demographic_variables), figsize=[10, 12])

    for i, variable in enumerate(demographic_variables):
        df = df_dict[variable]
        
            
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
            title = f"{chr(97 + i)}) cvd/resp/cancer hospitalisation rates by {variable}"
            axes[i].set_title(title, loc="left")

            
        

            axes[i].legend(loc=3, prop={"size": 9})
            axes[i].set_ylabel("Rate per 100,000 people")
            axes[i].set_ylim(ymin=0, ymax=y_lims[pop])
            
          
            plt.tight_layout()
  
    plt.savefig(f"output/{pop}_combined_diseases_time_series_plot.svg")