from main import db, app

cdm = app.config["SCHEMA_CDM"]


t_concept = db.Table(
    "concept",
    db.Column("concept_id", db.Integer, primary_key=True, unique=True),
    db.Column("concept_name", db.String(255), nullable=False),
    db.Column("domain_id", nullable=False, index=True),
    db.Column("vocabulary_id", nullable=False, index=True),
    db.Column("concept_class_id", nullable=False, index=True),
    db.Column("standard_concept", db.String(1)),
    db.Column("concept_code", db.String(50), nullable=False, index=True),
    db.Column("valid_start_date", db.Date, nullable=False),
    db.Column("valid_end_date", db.Date, nullable=False),
    db.Column("invalid_reason", db.String(1)),
    schema=cdm,
    extend_existing=True
)


t_person = db.Table(
    "person",
    db.Column("person_id", db.Integer, primary_key=True),
    db.Column("gender_concept_id", db.Integer, nullable=False),
    db.Column("year_of_birth", db.Integer, nullable=False),
    db.Column("month_of_birth", db.Integer, nullable=True),
    db.Column("day_of_birth", db.Integer, nullable=True),
    db.Column("race_concept_id", db.Integer, nullable=False),
    db.Column("ethnicity_concept_id", db.Integer, nullable=False),
    db.Column("location_id", db.Integer, nullable=True),
    db.Column("provider_id", db.Integer, nullable=True),
    db.Column("care_site_id", db.Integer, nullable=True),
    db.Column("person_source_value", db.String(50), nullable=True),
    db.Column("gender_source_value", db.String(50), nullable=True),
    db.Column("gender_source_concept_id", db.Integer, nullable=True),
    db.Column("race_source_value", db.String(50), nullable=True),
    db.Column("race_source_concept_id", db.Integer, nullable=True),
    db.Column("ethnicity_source_value", db.String(50), nullable=True),
    db.Column("ethnicity_source_concept_id", db.Integer, nullable=True),
    schema=cdm,
    extend_existing=True
)


t_death = db.Table(
    "death",
    db.Column("person_id", db.Integer, primary_key=True),
    db.Column("death_date", db.DateTime, nullable=False),
    db.Column("death_type_concept_id", db.Integer, nullable=False),
    db.Column("cause_concept_id", db.Integer, nullable=True),
    db.Column("cause_source_value", db.String(50), nullable=True),
    db.Column("cause_source_concept_id", db.Integer, nullable=True),
    schema=cdm,
    extend_existing=True
)


t_visit_occurrence = db.Table(
    "visit_occurrence",
    db.Column("visit_occurrence_id", db.Integer, primary_key=True),
    db.Column("person_id", db.Integer, nullable=False),
    db.Column("visit_concept_id", db.Integer, nullable=False),
    db.Column("visit_start_date", db.DateTime, nullable=False),
    db.Column("visit_end_date", db.DateTime, nullable=False),
    db.Column("visit_type_concept_id", db.Integer, nullable=False),
    db.Column("provider_id", db.Integer, nullable=True),
    db.Column("care_site_id", db.Integer, nullable=True),
    db.Column("visit_source_value", db.String(50), nullable=True),
    db.Column("visit_source_concept_id", db.Integer, nullable=True),
    schema=cdm,
    extend_existing=True
)


t_condition_occurrence = db.Table(
    "condition_occurrence",
    db.Column("condition_occurrence_id", db.Integer, primary_key=True),
    db.Column("person_id", db.Integer, index=True, nullable=False),
    db.Column("condition_concept_id", db.Integer, index=True, nullable=False),
    db.Column("condition_start_date", db.DateTime, nullable=False),
    db.Column("condition_end_date", db.DateTime, nullable=True),
    db.Column("condition_type_concept_id", db.Integer, nullable=False),
    db.Column("stop_reason", db.String(20), nullable=True),
    db.Column("provider_id", db.Integer, nullable=True),
    db.Column("visit_occurrence_id", db.Integer, index=True, nullable=True),
    db.Column("condition_source_value", db.String(50), nullable=True),
    db.Column("condition_source_concept_id", db.Integer, nullable=True),
    schema=cdm,
    extend_existing=True
)


t_drug_exposure = db.Table(
    "drug_exposure",
    db.Column("drug_exposure_id", db.Integer, primary_key=True),
    db.Column("person_id", db.Integer, index=True, nullable=False),
    db.Column("drug_concept_id", db.Integer, index=True, nullable=False),
    db.Column("drug_exposure_start_date", db.DateTime, nullable=False),
    db.Column("drug_exposure_end_date", db.DateTime, nullable=True),
    db.Column("drug_type_concept_id", db.Integer, nullable=False),
    db.Column("stop_reason", db.String(20), nullable=True),
    db.Column("refills", db.Integer, nullable=True),
    db.Column("quantity", db.Numeric, nullable=True),
    db.Column("days_supply", db.Integer, nullable=True),
    db.Column("sig", db.Text, nullable=True),
    db.Column("route_concept_id", db.Integer, nullable=True),
    db.Column("effective_drug_dose", db.Numeric, nullable=True),
    db.Column("dose_unit_concept_id", db.Integer, nullable=True),
    db.Column("lot_number", db.String(50), nullable=True),
    db.Column("provider_id", db.Integer, nullable=True),
    db.Column("visit_occurrence_id", db.Integer, index=True, nullable=True),
    db.Column("drug_source_value", db.String(50), nullable=True),
    db.Column("drug_source_concept_id", db.Integer, nullable=True),
    db.Column("route_source_value", db.String(50), nullable=True),
    db.Column("dose_unit_source_value", db.String(50), nullable=True),
    schema=cdm,
    extend_existing=True
)


t_measurement = db.Table(
    "measurement",
    db.Column("measurement_id", db.Integer, primary_key=True),
    db.Column("person_id", db.Integer, index=True, nullable=False),
    db.Column("measurement_concept_id", db.Integer, index=True, nullable=False),
    db.Column("measurement_date", db.DateTime, nullable=False),
    db.Column("measurement_time", db.String(10), nullable=True),
    db.Column("measurement_type_concept_id", db.Integer, nullable=False),
    db.Column("operator_concept_id", db.Integer, nullable=False),
    db.Column("value_as_number", db.Float, nullable=False),
    db.Column("value_as_Concept_id", db.Integer, nullable=False),
    db.Column("unit_concept_id", db.Integer, nullable=False),
    db.Column("range_low", db.Float, nullable=False),
    db.Column("range_high", db.Float, nullable=False),
    db.Column("provider_id", db.Integer, nullable=False),
    db.Column("visit_occurrence_id", db.Integer, nullable=False),
    db.Column("measurement_source_value", db.String(50), nullable=False),
    db.Column("measurement_source_concept_iud", db.Integer, nullable=False),
    db.Column("unit_source_Value", db.String(50), nullable=False),
    db.Column("value_source_value", db.String(50), nullable=False),
    schema=cdm,
    extend_existing=True
)


t_procedure_occurrence = db.Table(
    "procedure_occurrence",
    db.Column("procedure_occurrence_id", db.Integer, primary_key=True),
    db.Column("person_id", db.Integer, index=True, nullable=False),
    db.Column("procedure_concept_id", db.Integer, index=True, nullable=False),
    db.Column("procedure_date", db.DateTime, nullable=False),
    db.Column("procedure_type_concept_id", db.Integer, nullable=False),
    db.Column("modifier_concept_id", db.Integer, nullable=True),
    db.Column("quantity", db.Integer, nullable=True),
    db.Column("provider_id", db.Integer, nullable=True),
    db.Column("visit_occurrence_id", db.Integer, index=True, nullable=True),
    db.Column("procedure_source_value", db.String(50), nullable=True),
    db.Column("procedure_source_concept_id", db.Integer, nullable=True),
    db.Column("qualifier_source_value", db.String(50), nullable=True),
    schema=cdm,
    extend_existing=True
)
