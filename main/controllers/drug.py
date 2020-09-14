from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with, doc
from sqlalchemy import func

from main import db
from main.controllers.common import get_top_concept_by_person_count, get_top_concept_by_usage_count
from main.models.cdm import t_drug_exposure
from main.models.resources import RequestTopN


drug_bp = Blueprint("drug", __name__, url_prefix="/api/data/drug")
MODEL_TYPE = "Drug"


@drug_bp.route("/person-count", methods=["GET"])
@doc(tags=[MODEL_TYPE],
     summary="환자 수 기준 상위 N개 의약품",
     description="환자 수를 기준으로 상위 N개 의약품을 리턴합니다.")
@use_kwargs(RequestTopN, location="query")
def drug_person_count(**kwargs):
  top = kwargs.get("top", 10)
  return {
    "drug_list": get_top_concept_by_person_count(t_drug_exposure,
                                                 "drug_concept_id",
                                                 top)
  }


@drug_bp.route("/usage-count", methods=["GET"])
@doc(tags=[MODEL_TYPE],
     summary="진단 수 기준 상위 N개 의약품",
     description="진단 수를 기준으로 상위 N개 의약품을 리턴합니다.")
@use_kwargs(RequestTopN, location="query")
def drug_usage_count(**kwargs):
  top = kwargs.get("top", 10)
  return {
    "drug_list": get_top_concept_by_usage_count(t_drug_exposure,
                                                "drug_concept_id",
                                                top)
  }
