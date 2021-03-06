import os
import pandas as pd
import numpy as np

demographics = ["region", "imd", "ethnicity", "sex"]
df_list = []
for file in os.listdir('output'):
    if file.startswith('input_2'):
        date = file.split('_')[-1][:-4]

        file_path = os.path.join('output', file)
        df = pd.read_csv(file_path)

        
        

        df_sublist = []
        for var in demographics:

            var_column = df[var]
            df[var] = df[var].replace(np.nan, "Missing")

            # Missing values in ethnicity coded as 0.  Remove these
            if var=='ethnicity':
                df[var] = df[var].replace(0, "Missing")

            population = df.groupby(
                ["AgeGroup", var]).size().reset_index()
            values = df.groupby(["AgeGroup", var]).agg(
                {'CVD': 'sum', 'cancer': 'sum', 'respiratory_disease': 'sum'}).reset_index()
            values['population'] = population.iloc[:, -1]
            values['date'] = date
            df_sublist.append(values)
        df_list.append(df_sublist)
        
        
for i, demographic in enumerate(demographics):
    df_combined = pd.concat(df_list[y][i] for y in range(len(df_list)))
    
    cv_df = df_combined[["AgeGroup", demographic,
                     "CVD", "population", "date"]].to_csv(f"output/measure_CVD_rate_{demographic}.csv")
    cancer_df = df_combined[["AgeGroup", demographic,
                     "cancer", "population", "date"]].to_csv(f"output/measure_cancer_rate_{demographic}.csv")
    respiratory_df = df_combined[["AgeGroup", demographic,
                     "respiratory_disease", "population", "date"]].to_csv(f"output/measure_respiratory_disease_rate_{demographic}.csv")
