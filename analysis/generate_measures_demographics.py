import os
import pandas as pd


df_list = []
for file in os.listdir('output'):
    if file.startswith('input_2'):
        date = file.split('_')[-1][:-4]

        file_path = os.path.join('output', file)
        df = pd.read_csv(file_path)

        population = df.groupby(
            ['region', "AgeGroup", "ethnicity", "imd"]).size().reset_index()
        values = df.groupby(['region', "AgeGroup", "ethnicity", "imd"]).agg(
            {'CVD': 'sum', 'cancer': 'sum', 'respiratory_disease': 'sum'}).reset_index()
        values['population'] = population.iloc[:, -1]
        values['date'] = date
        df_list.append(values)

df_combined = pd.concat(df_list)
cv_df = df_combined[["region", "AgeGroup", "ethnicity", "imd",
                     "CVD", "population", "date"]].to_csv("output/measure_CVD_rate_demographics.csv")
cancer_df = df_combined[["region", "AgeGroup", "ethnicity", "imd",
                         "cancer", "population", "date"]].to_csv("output/measure_cancer_rate_demographics.csv")
respiratory_df = df_combined[["region", "AgeGroup", "ethnicity", "imd", "respiratory_disease",
                              "population", "date"]].to_csv("output/measure_respiratory_disease_rate_demographics.csv")
