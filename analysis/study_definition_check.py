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

    
    cvd_admission_method = patients.admitted_to_hospital(
        with_these_primary_diagnoses=cvd_codelist,
        with_admission_method=["11", "12", "13", "21", "22", "23", "24", "25", "2A", "2B", "2C", "2D", "28"],
        between=["index_date", "index_date + 6 days"],
        returning="admission_method",
        return_expectations={"incidence": 0.1,
                             "category": {"ratios": {
                                 "11": 0.1,
                                 "12": 0.1,
                                 "13": 0.1,
                                 "21": 0.1,
                                 "22": 0.1,
                                 "23": 0.1,
                                 "24": 0.1,
                                 "25": 0.1,
                                 "2A": 0.1,
                                 "2B": 0.1
                             }}
                            },
    ),
    
    
    respiratory_disease_admission_method = patients.admitted_to_hospital(
        with_these_primary_diagnoses=resp_codelist,
        with_admission_method=["11", "12", "13", "21", "22", "23", "24", "25", "2A", "2B", "2C", "2D", "28"],
        between=["index_date", "index_date + 6 days"],
        returning="admission_method",
        return_expectations={"incidence": 0.1,
                             "category": {"ratios": {
                                 "11": 0.1,
                                 "12": 0.1,
                                 "13": 0.1,
                                 "21": 0.1,
                                 "22": 0.1,
                                 "23": 0.1,
                                 "24": 0.1,
                                 "25": 0.1,
                                 "2A": 0.1,
                                 "2B": 0.1
                             }}
                            },
    ),
    
    
    cancer_admission_method = patients.admitted_to_hospital(
        with_these_primary_diagnoses=cancer_codelist,
        with_admission_method=["11", "12", "13", "21", "22", "23", "24", "25", "2A", "2B", "2C", "2D", "28"],
        between=["index_date", "index_date + 6 days"],
        returning="admission_method",
        return_expectations={"incidence": 0.1,
                             "category": {"ratios": {
                                 "11": 0.1,
                                 "12": 0.1,
                                 "13": 0.1,
                                 "21": 0.1,
                                 "22": 0.1,
                                 "23": 0.1,
                                 "24": 0.1,
                                 "25": 0.1,
                                 "2A": 0.1,
                                 "2B": 0.1
                             }}
                            },
    ),
    

    
    
)




