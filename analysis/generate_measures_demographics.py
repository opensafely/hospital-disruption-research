import os
import pandas as pd
import numpy as np

demographics = ["imd", "ethnicity", "sex"]
populations = ["total", "emergency", "elective"]

for pop in populations:

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
                
                if pop == 'total':
                    
                    values = df.groupby(["AgeGroup", var]).agg(
                        {'cvd_emergency_elective': 'sum', 'cancer_emergency_elective': 'sum', 'respiratory_disease_emergency_elective': 'sum'}).reset_index()
                    
                elif pop == 'emergency':
                    
                    values = df.groupby(["AgeGroup", var]).agg(
                        {'cvd_emergency': 'sum', 'cancer_emergency': 'sum', 'respiratory_disease_emergency': 'sum'}).reset_index()
                    
                elif pop == 'elective':
                    
                    values = df.groupby(["AgeGroup", var]).agg(
                        {'cvd_elective': 'sum', 'cancer_elective': 'sum', 'respiratory_disease_elective': 'sum'}).reset_index()
                    
                
                values['population'] = population.iloc[:, -1]
                values['date'] = date
                df_sublist.append(values)
            df_list.append(df_sublist)


    for i, demographic in enumerate(demographics):
        df_combined = pd.concat(df_list[y][i] for y in range(len(df_list)))
        
        if pop == 'total':
            cv_df = df_combined[["AgeGroup", demographic,
                             "cvd_emergency_elective", "population", "date"]].to_csv(f"output/measure_cvd_rate_{pop}_{demographic}.csv")
            cancer_df = df_combined[["AgeGroup", demographic,
                             "cancer_emergency_elective", "population", "date"]].to_csv(f"output/measure_cancer_rate_{pop}_{demographic}.csv")
            respiratory_df = df_combined[["AgeGroup", demographic,
                             "respiratory_disease_emergency_elective", "population", "date"]].to_csv(f"output/measure_respiratory_disease_rate_{pop}_{demographic}.csv")
        
        
        elif pop == 'emergency':
            cv_df = df_combined[["AgeGroup", demographic,
                             "cvd_emergency", "population", "date"]].to_csv(f"output/measure_cvd_rate_{pop}_{demographic}.csv")
            cancer_df = df_combined[["AgeGroup", demographic,
                             "cancer_emergency", "population", "date"]].to_csv(f"output/measure_cancer_rate_{pop}_{demographic}.csv")
            respiratory_df = df_combined[["AgeGroup", demographic,
                             "respiratory_disease_emergency", "population", "date"]].to_csv(f"output/measure_respiratory_disease_rate_{pop}_{demographic}.csv")
        
        
        elif pop == 'elective':
            cv_df = df_combined[["AgeGroup", demographic,
                             "cvd_elective", "population", "date"]].to_csv(f"output/measure_cvd_rate_{pop}_{demographic}.csv")
            cancer_df = df_combined[["AgeGroup", demographic,
                             "cancer_elective", "population", "date"]].to_csv(f"output/measure_cancer_rate_{pop}_{demographic}.csv")
            respiratory_df = df_combined[["AgeGroup", demographic,
                             "respiratory_disease_elective", "population", "date"]].to_csv(f"output/measure_respiratory_disease_rate_{pop}_{demographic}.csv")
