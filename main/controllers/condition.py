from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with, doc
from sqlalchemy import func

from main import db
from main.controllers.common import get_top_concept_by_person_count, get_top_concept_by_usage_count
from main.models.cdm import t_condition_occurrence
from main.models.resources import RequestTopN, ResponseConceptPersonCount, ResponseConceptUsageCount


condition_bp = Blueprint("condition", __name__, url_prefix="/api/data/condition")
MODEL_TYPE = "Condition"


@condition_bp.route("/person-count", methods=["GET"])
@doc(tags=[MODEL_TYPE],
     summary="환자 수 기준 상위 N개 진단",
     description="환자 수를 기준으로 상위 N개 진단의 Concept ID와 이름, 환자 수를 리턴합니다.")
@marshal_with(ResponseConceptPersonCount("condition_list"),
              description="""
<pre>
condition_list: 진단 정보가 들어갈 리스트
  .concept_id: 진단 Concept ID
  .concept_name: 진단 Concept 이름
  .person_count: 환자 수
</pre>
""")
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
     description="진단 수를 기준으로 상위 N개 진단의 Concept ID와 이름, 진단 수를 리턴합니다.")
@marshal_with(ResponseConceptUsageCount("condition_list"),
              description="""
<pre>
condition_list: 진단 정보가 들어갈 리스트
  .concept_id: 진단 Concept ID
  .concept_name: 진단 Concept 이름
  .usage_count: 진단 수 (사용 수, 테이블에서 사용된 row 수)
</pre>
""")
@use_kwargs(RequestTopN, location="query")
def condition_usage_count(**kwargs):
  top = kwargs.get("top", 10)
  return {
      "condition_list": get_top_concept_by_usage_count(t_condition_occurrence,
                                                       "condition_concept_id",
                                                       top)
  }
