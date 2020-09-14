from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with, doc
from sqlalchemy import func

from main import db
from main.controllers.common import get_top_concept_by_person_count, get_top_concept_by_usage_count
from main.models.cdm import t_procedure_occurrence
from main.models.resources import RequestTopN


procedure_bp = Blueprint("procedure", __name__, url_prefix="/api/data/procedure")
MODEL_TYPE = "procedure"


@procedure_bp.route("/person-count", methods=["GET"])
@doc(tags=[MODEL_TYPE],
     summary="환자 수 기준 상위 N개 의료행위",
     description="환자 수를 기준으로 상위 N개 의료행위를 리턴합니다.")

@use_kwargs(RequestTopN, location="query")
def procedure_person_count(**kwargs):
  top = kwargs.get("top", 10)
  return {
    "procedure_list": get_top_concept_by_person_count(t_procedure_occurrence,
                                                      "procedure_concept_id",
                                                      top)
  }


@procedure_bp.route("/usage-count", methods=["GET"])
@doc(tags=[MODEL_TYPE],
     summary="진단 수 기준 상위 N개 의료행위",
     description="진단 수를 기준으로 상위 N개 의료행위를 리턴합니다.")
@use_kwargs(RequestTopN, location="query")
def procedure_usage_count(**kwargs):
  top = kwargs.get("top", 10)
  return {
    "procedure_list": get_top_concept_by_usage_count(t_procedure_occurrence,
                                                      "procedure_concept_id",
                                                      top)
  }
