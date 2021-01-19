from cohortextractor import (
    codelist,
    codelist_from_csv,
)

# https://codelists.opensafely.org/codelist/opensafely/icd-10-chapter-ix/4868c7af/
cvd_codelist = codelist_from_csv(
    "codelists/opensafely-icd-10-chapter-ix-4868c7af.csv",
    system="icd10",
    column="code",
)


# https://codelists.opensafely.org/codelist/opensafely/icd-10-chapter-x/2f59547a/
resp_codelist - codelist_from_csv(
    "codelists/opensafely-icd-10-chapter-x-2f59547a.csv", 
    system="icd10", 
    column="code",
)


# https://codelists.opensafely.org/codelist/opensafely/icd-10-chapter-ii/77d4ee23/
cancer_codelist = codelist_from_csv(
    "codelists/opensafely-icd-10-chapter-ii-77d4ee23.csv",
    system="icd10",
    column="code",
)
