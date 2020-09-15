from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with, doc
from sqlalchemy import func

from main import db
from main.controllers.common import get_top_concept_by_person_count, get_top_concept_by_usage_count
from main.models.cdm import t_procedure_occurrence
from main.models.resources import RequestTopN, ResponseConceptPersonCount, ResponseConceptUsageCount


procedure_bp = Blueprint("procedure", __name__, url_prefix="/api/data/procedure")
MODEL_TYPE = "Procedure"


@procedure_bp.route("/person-count", methods=["GET"])
@doc(tags=[MODEL_TYPE],
     summary="환자 수 기준 상위 N개 의료행위",
     description="환자 수를 기준으로 상위 N개 의료행위의 Concept ID와 이름 행위 수를 리턴합니다.")
@marshal_with(ResponseConceptPersonCount("procedure_list"),
              description="""
<pre>
procedure_list: 의료행위 정보가 들어갈 리스트
  .concept_id: 의료행위 Concept ID
  .concept_name: 의료행위 Concept 이름
  .person_count: 환자 수
</pre>
""")
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
     summary="행위 수 기준 상위 N개 의료행위",
     description="행위 수를 기준으로 상위 N개 의료행위의 Concept ID와 이름 행위 수를 리턴합니다.")
@marshal_with(ResponseConceptUsageCount("procedure_list"),
              description="""
<pre>
procedure_list: 의료행위 정보가 들어갈 리스트
  .concept_id: 의료행위 Concept ID
  .concept_name: 의료행위 Concept 이름
  .usage_count: 행위 수 (사용 수, 테이블에서 사용된 row 수)
</pre>
""")
@use_kwargs(RequestTopN, location="query")
def procedure_usage_count(**kwargs):
  top = kwargs.get("top", 10)
  return {
      "procedure_list": get_top_concept_by_usage_count(t_procedure_occurrence,
                                                       "procedure_concept_id",
                                                       top)
  }
