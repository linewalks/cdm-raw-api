from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with, doc
from sqlalchemy import func

from main import db
from main.controllers.common import get_top_concept_by_person_count, get_top_concept_by_usage_count
from main.models.cdm import t_measurement
from main.models.resources import RequestTopN, ResponseConceptPersonCount, ResponseConceptUsageCount


measurement_bp = Blueprint("measurement", __name__, url_prefix="/api/data/measurement")
MODEL_TYPE = "Measurement"


@measurement_bp.route("/person-count", methods=["GET"])
@doc(tags=[MODEL_TYPE],
     summary="환자 수 기준 상위 N개 검사",
     description="환자 수를 기준으로 상위 N개 검사를 리턴합니다.")
@marshal_with(ResponseConceptPersonCount("measurement_list"))
@use_kwargs(RequestTopN, location="query")
def measurement_person_count(**kwargs):
  top = kwargs.get("top", 10)
  return {
      "measurement_list": get_top_concept_by_person_count(t_measurement,
                                                          "measurement_concept_id",
                                                          top)
  }


@measurement_bp.route("/usage-count", methods=["GET"])
@doc(tags=[MODEL_TYPE],
     summary="진단 수 기준 상위 N개 검사",
     description="진단 수를 기준으로 상위 N개 검사를 리턴합니다.")
@marshal_with(ResponseConceptUsageCount("measurement_list"))
@use_kwargs(RequestTopN, location="query")
def measurement_usage_count(**kwargs):
  top = kwargs.get("top", 10)
  return {
      "measurement_list": get_top_concept_by_usage_count(t_measurement,
                                                         "measurement_concept_id",
                                                         top)
  }
