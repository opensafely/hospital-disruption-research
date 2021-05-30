from cohortextractor import (
    StudyDefinition,
    patients,
    codelist,
    codelist_from_csv,
    Measure,
)

from codelists import *

study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "1900-01-01", "latest": "today"},
        "rate": "uniform",
    },
    index_date="2020-01-01",
    population=patients.registered_with_one_practice_between(
        "index_date", "index_date"
    ),

    region=patients.registered_practice_as_of(
        "index_date",
        returning="nuts1_region_name",
        return_expectations={"category": {"ratios": {
            "North East": 0.1,
            "North West": 0.1,
            "Yorkshire and the Humber": 0.1,
            "East Midlands": 0.1,
            "West Midlands": 0.1,
            "East of England": 0.1,
            "London": 0.2,
            "South East": 0.2, }},
            "incidence": 0.8}
    ),

    sex=patients.sex(
            return_expectations={
                "rate": "universal",
                "category": {"ratios": {"M": 0.49, "F": 0.51}},
            }
        ),

    

    AgeGroup=patients.categorised_as(
        {
            "0-4": "age >= 0 AND age < 5",
            "5-9": "age >= 5 AND age < 10",
            "10-14": "age >= 10 AND age < 15",
            "15-19": "age >= 15 AND age < 20",
            "20-24": "age >= 20 AND age < 25",
            "25-29": "age >= 25 AND age < 30",
            "30-34": "age >= 30 AND age < 35",
            "35-39": "age >= 35 AND age < 40",
            "40-44": "age >= 40 AND age < 45",
            "45-49": "age >= 45 AND age < 50",
            "50-54": "age >= 50 AND age < 55",
            "55-59": "age >= 55 AND age < 60",
            "60-64": "age >= 60 AND age < 65",
            "65-69": "age >= 65 AND age < 70",
            "70-74": "age >= 70 AND age < 75",
            "75-79": "age >= 75 AND age < 80",
            "80-84": "age >= 80 AND age < 85",
            "85-89": "age >= 85 AND age < 90",
            "90plus": "age >= 90",
            "missing": "DEFAULT",
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "0-4": 0.05,
                    "5-9": 0.05,
                    "10-14": 0.05,
                    "15-19": 0.05,
                    "20-24": 0.05,
                    "25-29": 0.05,
                    "30-34": 0.05,
                    "35-39": 0.05,
                    "40-44": 0.05,
                    "45-49": 0.1,
                    "50-54": 0.05,
                    "55-59": 0.05,
                    "60-64": 0.05,
                    "65-69": 0.05,
                    "70-74": 0.05,
                    "75-79": 0.05,
                    "80-84": 0.05,
                    "85-89": 0.05,
                    "90plus": 0.03,
                    "missing": 0.02,
                }
            },
        },
        age=patients.age_as_of(
            "index_date",
        ),
    ),
    
    # patients admitted to hospital with primary diagnoses included in cvd codelist
    # filters out maternity-related admissions and transfers from other providers
    cvd_elective=patients.admitted_to_hospital(
        with_these_primary_diagnoses=cvd_codelist,
        with_admission_method=["11", "12", "13"],
        between=["index_date", "index_date + 6 days"],
        return_expectations={"incidence": 0.05},
    ),
    
    cvd_emergency=patients.admitted_to_hospital(
        with_these_primary_diagnoses=cvd_codelist,
        with_admission_method=["21", "22", "23", "24", "25", "2A", "2B", "2C", "2D", "28"],
        between=["index_date", "index_date + 6 days"],
        return_expectations={"incidence": 0.05},
    ),
    
    cvd_emergency_elective=patients.satisfying(
    """
    cvd_elective OR
    cvd_emergency
    """,
    ),
    
    

    respiratory_disease_elective=patients.admitted_to_hospital(
        with_these_primary_diagnoses=resp_codelist,
        with_admission_method=["11", "12", "13"],
        between=["index_date", "index_date + 6 days"],
        return_expectations={"incidence": 0.05},
    ),
    
    respiratory_disease_emergency=patients.admitted_to_hospital(
        with_these_primary_diagnoses=resp_codelist,
        with_admission_method=["21", "22", "23", "24", "25", "2A", "2B", "2C", "2D", "28"],
        between=["index_date", "index_date + 6 days"],
        return_expectations={"incidence": 0.05},
    ),
    
    respiratory_disease_emergency_elective=patients.satisfying(
    """
    respiratory_disease_elective OR
    respiratory_disease_emergency
    """,
    ),
    
    
    cancer_elective=patients.admitted_to_hospital(
        with_these_primary_diagnoses=cancer_codelist,
        with_admission_method=["11", "12", "13"],
        between=["index_date", "index_date + 6 days"],
        return_expectations={"incidence": 0.05},
    ),
    
    cancer_emergency=patients.admitted_to_hospital(
        with_these_primary_diagnoses=cancer_codelist,
        with_admission_method=["21", "22", "23", "24", "25", "2A", "2B", "2C", "2D", "28"],
        between=["index_date", "index_date + 6 days"],
        return_expectations={"incidence": 0.05},
    ),
    
    cancer_emergency_elective=patients.satisfying(
    """
    cancer_elective OR
    cancer_emergency
    """,
    ),
    
    
    
)


measures = [
    Measure(
        id="cvd_rate_total",
        numerator="cvd_emergency_elective",
        denominator="population",
        group_by=["AgeGroup"],
    ),
    
    Measure(
        id="cvd_rate_emergency",
        numerator="cvd_emergency",
        denominator="population",
        group_by=["AgeGroup"],
    ),
    
    Measure(
        id="cvd_rate_elective",
        numerator="cvd_elective",
        denominator="population",
        group_by=["AgeGroup"],
    ),

    Measure(
        id="respiratory_disease_total",
        numerator="respiratory_disease_emergency_elective",
        denominator="population",
        group_by=["AgeGroup"],
    ),
    
    Measure(
        id="respiratory_disease_rate_emergency",
        numerator="respiratory_disease_emergency",
        denominator="population",
        group_by=["AgeGroup"],
    ),
    
    Measure(
        id="respiratory_disease_rate_elective",
        numerator="respiratory_disease_elective",
        denominator="population",
        group_by=["AgeGroup"],
    ),

    Measure(
        id="cancer_rate_total",
        numerator="cancer_emergency_elective",
        denominator="population",
        group_by=["AgeGroup"],
    ),
    
    Measure(
        id="cancer_rate_emergency",
        numerator="cancer_emergency",
        denominator="population",
        group_by=["AgeGroup"],
    ),
    
    Measure(
        id="cancer_rate_elective",
        numerator="cancer_elective",
        denominator="population",
        group_by=["AgeGroup"],
    ),

    

]

