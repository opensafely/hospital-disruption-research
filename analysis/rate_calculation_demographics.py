import numpy as np
import pandas as pd
from study_definition import measures

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


def standardise_rates(by_age):
    rates = calculate_rates(by_age)
    standardised_rates = rates * standard_pop
    standardised_totals = standardised_rates.groupby(
        ["date", "region", "ethnicity", "imd"]).sum()
    return standardised_totals


def get_data():
    p = f"output/measure_{m.id}_demographics.csv"
    by_age = pd.read_csv(
        p, usecols=["date", m.numerator, m.denominator] + m.group_by)
    by_age["date"] = pd.to_datetime(by_age["date"])
    return by_age


def standardise_rates_apply(by_age_row):
    row_age_group = by_age_row['AgeGroup']
    row_standardised_rate = by_age_row['age_rates'] * \
        standard_pop[row_age_group]
    return row_standardised_rate


def redact_small_numbers(df):
    mask_n = df[m.numerator].isin([1, 2, 3, 4, 5])
    mask_d = df[m.denominator].isin([1, 2, 3, 4, 5])
    mask = mask_n | mask_d
    df.loc[mask, :] = np.nan
    return df


def make_table():
    by_age = get_data()
    by_age['age_rates'] = calculate_rates(by_age)
    by_age["European Standard population rate per 100,000"] = by_age.apply(
        standardise_rates_apply, axis=1)
    by_age.drop(['age_rates'], axis=1, inplace=True)
    standardised_totals = by_age.groupby(
        ["date", "region", "ethnicity", "imd"]).sum().reset_index()
    standardised_totals = redact_small_numbers(standardised_totals)
    return standardised_totals

time_series = []
for m in measures:
    df = make_table()
    df.to_csv(f"output/{m.id}.csv")
    time_series.append(df)
