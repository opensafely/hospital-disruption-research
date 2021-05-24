import numpy as np
import pandas as pd
from cohortextractor import Measure

measures = [
    Measure(
        id="CVD_rate",
        numerator="CVD",
        denominator="population",
        group_by=["AgeGroup"],
    ),

    Measure(
        id="CVD_rate_region",
        numerator="CVD",
        denominator="population",
        group_by=["AgeGroup", "region"],
    ),

    Measure(
        id="CVD_rate_sex",
        numerator="CVD",
        denominator="population",
        group_by=["AgeGroup", "sex"],
    ),

    Measure(
        id="CVD_rate_ethnicity",
        numerator="CVD",
        denominator="population",
        group_by=["AgeGroup", "ethnicity"],
    ),
    Measure(
        id="CVD_rate_imd",
        numerator="CVD",
        denominator="population",
        group_by=["AgeGroup", "imd"],
    ),
    
    Measure(
        id="CVD_rate_admission_method",
        numerator="CVD",
        denominator="population",
        group_by=["AgeGroup", "cvd_emergency_or_elective"],
    ),


    Measure(
        id="respiratory_disease_rate",
        numerator="respiratory_disease",
        denominator="population",
        group_by=["AgeGroup"],
    ),

    Measure(
        id="respiratory_disease_rate_region",
        numerator="respiratory_disease",
        denominator="population",
        group_by=["AgeGroup", "region"],
    ),

    Measure(
        id="respiratory_disease_rate_sex",
        numerator="respiratory_disease",
        denominator="population",
        group_by=["AgeGroup", "sex"],
    ),

    Measure(
        id="respiratory_disease_rate_ethnicity",
        numerator="respiratory_disease",
        denominator="population",
        group_by=["AgeGroup", "ethnicity"],
    ),

    Measure(
        id="respiratory_disease_rate_imd",
        numerator="respiratory_disease",
        denominator="population",
        group_by=["AgeGroup", "imd"],
    ),
    
    Measure(
        id="respiratory_disease_rate_admission_method",
        numerator="respiratory_disease",
        denominator="population",
        group_by=["AgeGroup", "respiratory_emergency_or_elective"],
    ),

    Measure(
        id="cancer_rate",
        numerator="cancer",
        denominator="population",
        group_by=["AgeGroup"],
    ),

    Measure(
        id="cancer_rate_region",
        numerator="cancer",
        denominator="population",
        group_by=["AgeGroup", "region"],
    ),
    Measure(
        id="cancer_rate_sex",
        numerator="cancer",
        denominator="population",
        group_by=["AgeGroup", "sex"],
    ),
    Measure(
        id="cancer_rate_ethnicity",
        numerator="cancer",
        denominator="population",
        group_by=["AgeGroup", "ethnicity"],
    ),
    Measure(
        id="cancer_rate_imd",
        numerator="cancer",
        denominator="population",
        group_by=["AgeGroup", "imd"],
    ),
    
    Measure(
        id="cancer_rate_admission_method",
        numerator="cancer",
        denominator="population",
        group_by=["AgeGroup", "cancer_emergency_or_elective"],
    ),
]


path = "analysis/european_standard_population.csv"
## European standardisation data from:
# from urllib.request import urlopen
# url = "https://www.opendata.nhs.scot/dataset/4dd86111-7326-48c4-8763-8cc4aa190c3e/resource/edee9731-daf7-4e0d-b525-e4c1469b8f69/download/european_standard_population.csv"
# with urlopen(url) as f:
#     pd.read_csv(f).to_csv(path, index=False)
standard_pop = pd.read_csv(path)
standard_pop["AgeGroup"] = standard_pop["AgeGroup"].str.replace(" years", "")
standard_pop = standard_pop.set_index("AgeGroup")["EuropeanStandardPopulation"]
standard_pop = standard_pop / standard_pop.sum()


def calculate_rates(df):
    rates = (df[m.numerator] / df[m.denominator]) * 100000
    return rates.round()



def get_data(demographic_var):
    p = f"output/measure_{m.id}.csv"
    by_age = pd.read_csv(
        p, usecols=["date", m.numerator, m.denominator] + m.group_by)
    by_age["date"] = pd.to_datetime(by_age["date"])

    #remove people with "Missing" in demographic vars
    by_age = by_age[by_age[demographic_var] != "Missing"]


    return by_age


def standardise_rates_apply(by_age_row):
    row_age_group = by_age_row['AgeGroup']
    if row_age_group == 'missing':
        row_standardised_rate = np.nan
        return row_standardised_rate
    else:
        
        row_standardised_rate = by_age_row['age_rates'] * standard_pop[row_age_group]
        return row_standardised_rate


def redact_small_numbers(df):
    mask_n = df[m.numerator].isin([1, 2, 3, 4, 5])
    mask_d = df[m.denominator].isin([1, 2, 3, 4, 5])
    mask = mask_n | mask_d
    df.loc[mask, :] = np.nan
    return df

def convert_imd(df, disease):
    df = calculate_imd_group(df, disease_column=disease, rate_column="European Standard population rate per 100,000")
    mask_n = df[disease].isin([1, 2, 3, 4, 5])
    mask_d = df['population'].isin([1, 2, 3, 4, 5])
    mask = mask_n | mask_d
    df.loc[mask, :] = np.nan

    return df

def make_table(demographic_var, redact=True):
    by_age = get_data(demographic_var)
    by_age['age_rates'] = calculate_rates(by_age)
    by_age["European Standard population rate per 100,000"] = by_age.apply(
        standardise_rates_apply, axis=1)
    by_age.drop(['age_rates'], axis=1, inplace=True)
    standardised_totals = by_age.groupby(
        ["date", demographic_var]).sum().reset_index()
    if redact:
        standardised_totals = redact_small_numbers(standardised_totals)
    return standardised_totals

def calculate_imd_group(df, disease_column, rate_column):
    imd_column = pd.to_numeric(df["imd"])
    df["imd"] = pd.qcut(imd_column, q=5,duplicates="drop", labels=['1', '2', '3', '4', '5'])      
    df_rate = df.groupby(by=["date", "imd"])[[rate_column]].mean().reset_index()
    df_population = df.groupby(by=["date", "imd"])[[disease_column, "population"]].sum().reset_index()
    df = df_rate.merge(df_population, on=["date", "imd"], how="inner")
    
    
 
    group_mapping_dict = {'1': "Most deprived", '2': "Middle level", '3': "Middle level", '4': "Middle level", '5': "Least deprived"}
    df['imd_group'] = df.apply(lambda row: group_mapping_dict[row.imd], axis=1)
    
    df_rate = df.groupby(by=["date", "imd_group"])[[rate_column]].mean().reset_index()

    df_population = df.groupby(by=["date", "imd_group"])[[disease_column, "population"]].sum().reset_index()
    
    df_merged = df_rate.merge(df_population, on=["date", "imd_group"], how="inner")
    
    return df_merged




time_series = {}

for m in measures:
    if len(m.group_by) >1:

        if m.group_by[1] =="imd":
            df = make_table(demographic_var = m.group_by[1], redact=False)
            df = convert_imd(df, disease=m.numerator)
        
        else:


            df = make_table(demographic_var = m.group_by[1])

            #if sex remove "U/T"
            if m.group_by[1] == "sex":
                df = df[df['sex'].isin(["M", "F"])]

        
            


        df.to_csv(f"output/{m.id}_breakdown.csv")
        if m.numerator not in time_series:
            time_series[m.numerator] = {}
            time_series[m.numerator][m.group_by[1]] = df
        
        else:
            time_series[m.numerator][m.group_by[1]] = df
        

#combine diseases
combined_diseases = {}
demographic_variables = ["region", "ethnicity", "imd", "sex", "admission_method"]
for d in demographic_variables:
    cvd_df = pd.read_csv(f'output/measure_CVD_rate_{d}.csv')
#     cvd_df.drop(["Unnamed: 0"], inplace=True, axis=1)
    cvd_df = cvd_df.rename(columns={"cvd_emergency_or_elective": "admission_method"})
    
    if d == 'admission_method':
        population_cvd = cvd_df.groupby(by=['date'])['population'].sum().reset_index()
        cvd_df = cvd_df[cvd_df['cvd_emergency_or_elective']!='0']
        cvd_df = cvd_df.drop('population', axis=1)
        cvd_df = cvd_df.merge(population_cvd, on='date')

    cancer_df = pd.read_csv(f'output/measure_cancer_rate_{d}.csv')
#     cancer_df.drop(["Unnamed: 0"], inplace=True, axis=1)
    cancer_df = cancer_df.rename(columns={"cancer_emergency_or_elective": "admission_method"})
    
    if d == 'admission_method':
        population_cancer = cancer_df.groupby(by=['date'])['population'].sum().reset_index()
        cancer_df = cancer_df[cancer_df['cancer_emergency_or_elective']!='0']
        cancer_df = cancer_df.drop('population', axis=1)
        cancer_df = cancer_df.merge(population_cancer, on='date')
    
    resp_df = pd.read_csv(f'output/measure_respiratory_disease_rate_{d}.csv')
#     resp_df.drop(["Unnamed: 0"], inplace=True, axis=1)
    resp_df = resp_df.rename(columns={"respiratory_emergency_or_elective": "admission_method"})
    
    if d == 'admission_method':
        population_resp = resp_df.groupby(by=['date'])['population'].sum().reset_index()
        resp_df = resp_df[cvd_df['resp_emergency_or_elective']!='0']
        resp_df = resp_df.drop('population', axis=1)
        resp_df = resp_df.merge(population_resp, on='date')
    
    combined = cvd_df.merge(cancer_df, on=["date", d, "AgeGroup"]).merge(resp_df, on=["date", d, "AgeGroup"])
    combined.drop(["population_x", "population_y"], inplace=True, axis=1)
    combined['disease'] = combined['cancer'] + combined['CVD'] + combined['respiratory_disease']
    combined.drop(['cancer', 'CVD', 'respiratory_disease'], inplace=True, axis=1)

    combined["date"] = pd.to_datetime(combined["date"])

    #remove people with "Missing" in demographic vars
    combined= combined[combined[d] != "Missing"]
    combined['age_rates'] = (combined['disease']/combined['population'])*100000

    combined["European Standard population rate per 100,000"] = combined.apply(
        standardise_rates_apply, axis=1)
    combined.drop(['age_rates'], axis=1, inplace=True)
    standardised_totals = combined.groupby(
            ["date", d]).sum().reset_index()

    #redact small numbers
    mask_n = standardised_totals['disease'].isin([1, 2, 3, 4, 5])
    mask_d = standardised_totals['population'].isin([1, 2, 3, 4, 5])
    mask = mask_n | mask_d
    standardised_totals.loc[mask, :] = np.nan
    

    if d =="imd":
        standardised_totals = calculate_imd_group(standardised_totals, 'disease', "European Standard population rate per 100,000")
        combined_diseases["imd_group"] = standardised_totals

    elif d == "sex":
        # drop rows where sex!= "M" or "F"
        standardised_totals = standardised_totals[standardised_totals['sex'].isin(["M", "F"])]
        combined_diseases[d] = standardised_totals

    else:
        combined_diseases[d] = standardised_totals

    standardised_totals.to_csv(f"output/combined_disease_breakdown_{d}.csv")
    



    