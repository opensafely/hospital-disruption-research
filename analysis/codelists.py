from cohortextractor import (
    codelist,
    codelist_from_csv,
)

# https://codelists.opensafely.org/codelist/opensafely/icd-10-chapter-ix/4868c7af/
cvd_codelist = codelist_from_csv(
    "codelists/opensafely-icd-10-chapter-ix.csv",
    system="icd10",
    column="code",
)


# https://codelists.opensafely.org/codelist/opensafely/icd-10-chapter-x/2f59547a/
resp_codelist = codelist_from_csv(
    "codelists/opensafely-icd-10-chapter-x.csv",
    system="icd10", 
    column="code",
)


# https://codelists.opensafely.org/codelist/opensafely/icd-10-chapter-ii/77d4ee23/
cancer_codelist = codelist_from_csv(
    "codelists/opensafely-icd-10-chapter-ii.csv",
    system="icd10",
    column="code",
)

#https://codelists.opensafely.org/codelist/opensafely/ethnicity/2020-04-27/
ethnicity_codes = codelist_from_csv(
        "codelists/opensafely-ethnicity.csv",
        system="ctv3",
        column="Code",
        category_column="Grouping_6",
    )
