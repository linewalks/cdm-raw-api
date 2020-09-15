from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with, doc
from sqlalchemy import func

from main import db
from main.controllers.common import get_top_concept_by_person_count, get_top_concept_by_usage_count
from main.models.cdm import t_condition_occurrence
from main.models.resources import (
    RequestTopN,
    ResponseConceptPersonCount,
    ResponseConceptUsageCount
)


condition_bp = Blueprint("condition", __name__, url_prefix="/api/data/condition")
MODEL_TYPE = "Condition"


@condition_bp.route("/person-count", methods=["GET"])
@doc(tags=[MODEL_TYPE],
     summary="환자 수 기준 상위 N개 진단",
     description="환자 수를 기준으로 상위 N개 진단을 리턴합니다.")
@marshal_with(ResponseConceptPersonCount("condition_list"))
@use_kwargs(RequestTopN, location="query")
def condition_person_count(**kwargs):
  top = kwargs.get("top", 10)
  return {
      "condition_list": get_top_concept_by_person_count(t_condition_occurrence,
                                                        "condition_concept_id",
                                                        top)
  }


@condition_bp.route("/usage-count", methods=["GET"])
@doc(tags=[MODEL_TYPE],
     summary="진단 수 기준 상위 N개 진단",
     description="진단 수를 기준으로 상위 N개 진단을 리턴합니다.")
@marshal_with(ResponseConceptUsageCount("condition_list"))
@use_kwargs(RequestTopN, location="query")
def condition_usage_count(**kwargs):
  top = kwargs.get("top", 10)
  return {
      "condition_list": get_top_concept_by_usage_count(t_condition_occurrence,
                                                       "condition_concept_id",
                                                       top)
  }
