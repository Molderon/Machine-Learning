bloodgas = pd.read_gbq(
    '''
WITH Patient_Gender AS (
    SELECT
        o.person_id,
        CASE
            WHEN o.value_as_concept_id = 8507 THEN 'Male'
            WHEN o.value_as_concept_id = 8532 THEN 'Female'
            ELSE 'Unknown'
        END AS gender
    FROM
        observation o
    WHERE
        o.observation_concept_id = 4083588
        AND o.value_as_concept_id IN (8532, 8507)
        AND o.provider_id IS NOT NULL
),

LOS_Data AS (
    SELECT
        v.person_id,
        v.visit_occurrence_id,
        TIMESTAMP_DIFF(v.visit_end_datetime, v.visit_start_datetime, HOUR) AS los_hours,
        EXTRACT(YEAR FROM v.visit_start_datetime) - p.year_of_birth AS age,
        v.visit_start_datetime -- Include visit_start_datetime for use in subsequent joins
    FROM
        visit_occurrence v
    INNER JOIN
        person p ON v.person_id = p.person_id
    WHERE
        TIMESTAMP_DIFF(v.visit_end_datetime, v.visit_start_datetime, HOUR) >= 24  -- Patients stayed more than 24 hours in the ICU
),

Death_Data AS (
    SELECT
        person_id,
        1 AS deceased,
        death_date
    FROM
        death
),

Ranked_Measurements AS (
    SELECT
        m.person_id,
        m.visit_occurrence_id,
        m.measurement_concept_id,
        m.measurement_datetime,
        CAST(m.value_as_number AS FLOAT64) AS value,
        m.unit_concept_id,
        m.provider_id,
        m.measurement_source_value,
        pg.gender,
        ld.age,
        dd.death_date,
        dd.deceased,
        ROW_NUMBER() OVER(PARTITION BY m.person_id ORDER BY m.measurement_datetime) AS row_num
    FROM
        measurement m
    LEFT JOIN
        LOS_Data ld ON m.person_id = ld.person_id
        AND m.measurement_datetime BETWEEN TIMESTAMP_SUB(ld.visit_start_datetime, INTERVAL 6 HOUR)
                                       AND TIMESTAMP_ADD(ld.visit_start_datetime, INTERVAL 24 HOUR)
    LEFT JOIN
        Patient_Gender pg ON m.person_id = pg.person_id
    LEFT JOIN
        Death_Data dd ON m.person_id = dd.person_id
    WHERE
        NOT m.provider_id IS NULL
        AND m.measurement_concept_id IN (
            3010421,  3013290,  3027315,  3006576,  3012501,  3047181,  42869608,  3005456,  40762351,  42869588,
            3000285,  3039000,  3048816,  3018572,  3020491,  3014646,  3023081,  3007930,  3044904
        )
)

SELECT                            
    *                             ############################
FROM                              ##                        ##
    Ranked_Measurements           ##                        ##
WHERE         #----#              ##     _______________    ##
    row_num <= 100 # <<----------------- HARDCODED LIMIT!   ##
ORDER BY      #----#              ##                        ##
    person_id,                    ##                        ##
    visit_occurrence_id,          ##                        ##
    measurement_datetime,         ############################
    measurement_concept_id
    '''
    , configuration=config_gbq, use_bqstorage_api=True)

specimen = pd.read_gbq(
    '''
    SELECT person_id, specimen_datetime, specimen_concept_id
    FROM specimen
    '''
    , configuration=config_gbq, use_bqstorage_api=True)

bloodgas = pd.DataFrame(bloodgas)

# Convert to DataFrame and proceed with processing
bloodgas.dropna()

bloodgas_df = bloodgas.copy()

# Remove duplicates
bloodgas_no_dup = bloodgas_df[~bloodgas_df[["person_id", "visit_occurrence_id", "measurement_datetime", "measurement_concept_id"]].duplicated()]

# Pivot the data
bloodgas_pivot = bloodgas_no_dup.pivot(index=["person_id", "visit_occurrence_id", "measurement_datetime"], columns=["measurement_concept_id"], values="value")

# Rename columns
bloodgas_pivot.rename(columns={
        3010421: "ph",
        3013290: "pco2",
        3027315: "po2",
        3006576: "bicarbonate",
        3012501: "base_excess",
        3047181: "lactate",
        42869608: "o2sat",
        3005456: "potassium",
        40762351: "hemoglobin",
        42869588: "hematocrit",
        3000285: "sodium",
        3039000: "anion_gap",
        3048816: "ca_ion",
        3018572: "chloride",
        3020491: "glucose",
        3014646: "oxyhb",
        3023081: "cohb",
        3007930: "methhb",
        3044904: "o2-content"
    }, inplace=True)

# Create a demographic dataframe with unique person_id
demographics = bloodgas_no_dup[['person_id', 'gender', 'age', 'deceased', 'death_date']].drop_duplicates('person_id')

# Check for missing ages before merging
missing_age_count = demographics['age'].isna().sum()
print(f'Missing ages in demographics: {missing_age_count}')

# Merge demographic information with bloodgas_pivot
bloodgas_pivot = bloodgas_pivot.reset_index().merge(demographics, on='person_id', how='left').set_index(['person_id', 'visit_occurrence_id', 'measurement_datetime'])

# Merge with specimen data
bloodgas_pivot = bloodgas_pivot.merge(specimen, how='left', left_on=['person_id', 'measurement_datetime'], right_on=['person_id', 'specimen_datetime'])

# Filter the data
bloodgas_pivot = bloodgas_pivot[
    ~(bloodgas_pivot['ph'].isna()) &
    ~(bloodgas_pivot['po2'].isna()) &
    ~(bloodgas_pivot['pco2'].isna()) &
    ~(bloodgas_pivot['bicarbonate'].isna()) &
    ~(bloodgas_pivot['base_excess'].isna()) &
    ~(bloodgas_pivot['sodium'].isna()) &
    ~(bloodgas_pivot['potassium'].isna()) &
    ~(bloodgas_pivot['glucose'].isna()) &
    ~(bloodgas_pivot['chloride'].isna()) &
    ~(bloodgas_pivot['lactate'].isna()) &
    (bloodgas_pivot['specimen_concept_id'] == 4047496)  # Arterial blood specimen
]
del bloodgas

num_patients = bloodgas_pivot['person_id'].nunique()
print("Available patients: ", num_patients)
bloodgas_pivot.info()
bloodgas_pivot.head()