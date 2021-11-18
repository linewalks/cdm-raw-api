import pandas as pd

from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with, doc

from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, average_precision_score, f1_score

from main import db
from main.models.cdm import t_person, t_death, t_visit_occurrence
from main.schema.ml import RequestDeathsSchema


ml_bp = Blueprint("ml", __name__, url_prefix="/api/ml")
MODEL_TYPE = "ML"


def _get_dummies_with_nested_column_name(target, prefix=None):
  df = pd.get_dummies(target, prefix=prefix, prefix_sep="$")
  df.columns = [tuple(col.split("$")) for col in df.columns]
  return df


def _load_key_target(target_days=30):
  query = f"""
      SELECT
          v.person_id,
          v.visit_occurrence_id,
          v.visit_start_date,
          COALESCE(v.visit_end_date, v.visit_start_date) AS visit_end_date,
          d.death_date
      FROM
          {t_visit_occurrence.name} v
          JOIN
              {t_death} d
          ON
              v.person_id = d.person_id
  """
  df = pd.read_sql(query, db.engine)
  df.loc[:, "target"] = (df.death_date - df.visit_end_date) <= pd.to_timedelta(f"{target_days} days")
  return df[["person_id", "visit_occurrence_id", "target"]]  


def _load_demographics(key_df):
  query = f"""
      SELECT
          person_id,
          gender_concept_id,
          race_concept_id,
          ethnicity_concept_id
      FROM
          {t_person.name}
  """
  df = pd.read_sql(query, db.engine)
  df = pd.concat([
      df["person_id"],
      _get_dummies_with_nested_column_name(df.gender_concept_id, "gender"),
      _get_dummies_with_nested_column_name(df.race_concept_id, "race"),
      _get_dummies_with_nested_column_name(df.ethnicity_concept_id, "ethnicity")
  ], axis=1)

  return pd.merge(key_df, df, on=["person_id"], how="left")


@ml_bp.route("/create-death", methods=["POST"])
@use_kwargs(RequestDeathsSchema)
@doc(
    tags=[MODEL_TYPE],
    summary="사망 예측 모델 생성",
    description="사망 예측 모델을 생성합니다."
)
def create_death_model(features, model):

  key_target_df = _load_key_target()
  key_df = key_target_df[["person_id", "visit_occurrence_id"]]
  target_df = key_target_df["target"]
  feat_func_map = {
      "demo": _load_demographics
  }
  if features is None:
    features = list(feat_func_map.keys())

  data_list = []
  for feature in features:
    data_list.append(feat_func_map[feature](key_df))

  data_df = pd.concat(data_list, axis=1)
  patient_list = key_df.person_id.unique()

  train_patients, test_patients = train_test_split(patient_list, test_size=0.2, random_state=42)
  
  train_x = data_df.loc[key_df.person_id.isin(train_patients), :].values
  test_x = data_df.loc[key_df.person_id.isin(test_patients), :].values

  train_y = target_df.loc[key_df.person_id.isin(train_patients)].values
  test_y = target_df.loc[key_df.person_id.isin(test_patients)].values

  if model == "lgbm":
    model = LGBMClassifier(
        objective="binary"
    ).fit(train_x, train_y)
  else:
    raise NotImplementedError("Not Implemented model")

  pred_y = model.predict_proba(test_x)

  return {
      "train_data": {
          "num_patients": len(train_patients),
          "num_visits": len(train_x),
          "label_ratio": train_x.sum() / len(train_x)
      },
      "test_data": {
          "num_patients": len(test_patients),
          "num_visits": len(test_x),
          "label_ratio": test_x.sum() / len(test_x)
      },
      "evaluate": {
          "auroc": roc_auc_score(test_y, pred_y[:, 1]),
          "auprc": average_precision_score(test_y, pred_y[:, 1]),
          "f1": f1_score(test_y, pred_y[:, 1] > 0.5)
      }
  }
