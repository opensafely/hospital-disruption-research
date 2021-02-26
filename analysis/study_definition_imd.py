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
    index_date="2020-01-03",
    population=patients.registered_with_one_practice_between(
        "index_date", "index_date"
    ),

    imd=patients.address_as_of(
        "index_date",
        returning="index_of_multiple_deprivation",
        round_to_nearest=100,
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"100": 0.2, "200": 0.2, "300": 0.2, "400": 0.2, "500": 0.2}},
        },
    ),



)
