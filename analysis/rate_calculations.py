import numpy as np
import pandas as pd
from cohortextractor import Measure

measures = [
    Measure(
        id="cvd_total_rate",
        numerator="cvd_emergency_elective",
        denominator="population",
        group_by=["AgeGroup"],
    ),
    
    Measure(
        id="cvd_emergency_rate",
        numerator="cvd_emergency",
        denominator="population",
        group_by=["AgeGroup"],
    ),
    
    Measure(
        id="cvd_elective_rate",
        numerator="cvd_elective",
        denominator="population",
        group_by=["AgeGroup"],
    ),

    Measure(
        id="respiratory_disease_total_rate",
        numerator="respiratory_disease_emergency_elective",
        denominator="population",
        group_by=["AgeGroup"],
    ),
    
    Measure(
        id="respiratory_disease_emergency_rate",
        numerator="respiratory_disease_emergency",
        denominator="population",
        group_by=["AgeGroup"],
    ),
    
    Measure(
        id="respiratory_disease_elective_rate",
        numerator="respiratory_disease_elective",
        denominator="population",
        group_by=["AgeGroup"],
    ),

    Measure(
        id="cancer_total_rate",
        numerator="cancer_emergency_elective",
        denominator="population",
        group_by=["AgeGroup"],
    ),
    
    Measure(
        id="cancer_emergency_rate",
        numerator="cancer_emergency",
        denominator="population",
        group_by=["AgeGroup"],
    ),
    
    Measure(
        id="cancer_elective_rate",
        numerator="cancer_elective",
        denominator="population",
        group_by=["AgeGroup"],
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


def get_data():
    p = f"output/measure_{m.id}.csv"
    by_age = pd.read_csv(p, usecols=["date", m.numerator, m.denominator] + m.group_by)
    by_age["date"] = pd.to_datetime(by_age["date"])
    by_age = by_age.set_index(["date"] + m.group_by)
    totals = by_age.groupby("date").sum()
    return by_age, totals


def calculate_rates(df):
    rates = (df[m.numerator] / df[m.denominator]) * 100000
    return rates.round()


def standardise_rates(by_age):
    rates = calculate_rates(by_age)
    standardised_rates = rates * standard_pop
    standardised_totals = standardised_rates.groupby("date").sum()
    return standardised_totals


def redact_small_numbers(df):
    mask_n = df[m.numerator].isin([1, 2, 3, 4, 5])
    mask_d = df[m.denominator].isin([1, 2, 3, 4, 5])
    mask = mask_n | mask_d
    df.loc[mask, :] = np.nan
    return df


def make_table():
    by_age, totals = get_data()
    rates = calculate_rates(totals)
    rates.name = "Crude rate per 100,000 population"
    standardised_rates = standardise_rates(by_age)
    standardised_rates.name = "European Standard population rate per 100,000"
    df = pd.concat([totals, rates, standardised_rates], axis=1)
    df = redact_small_numbers(df)
    return df

time_series = {'total': [], 'elective': [], 'emergency': []}

for m in measures:
    df = make_table()
    df.to_csv(f"output/{m.id}_table.csv")
    
    if 'total' in m.id:
        time_series['total'].append(df.drop(columns=[m.numerator, m.denominator]))
    
    elif 'elective' in m.id:
        time_series['elective'].append(df.drop(columns=[m.numerator, m.denominator]))
    
    elif 'emergency' in m.id:
        time_series['emergency'].append(df.drop(columns=[m.numerator, m.denominator]))
    
