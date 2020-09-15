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
     description="환자 수를 기준으로 상위 N개 검사의 Concept ID와 이름, 환자 수를 리턴합니다.")
@marshal_with(ResponseConceptPersonCount("measurement_list"),
              description="""
<pre>
measurement_list: 검사 정보가 들어갈 리스트
  .concept_id: 검사 Concept ID
  .concept_name: 검사 Concept 이름
  .person_count: 환자 수
</pre>
""")
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
     summary="검사 수 기준 상위 N개 검사",
     description="검사 수를 기준으로 상위 N개 검사의 Concept ID와 이름, 검사 수행 수를 리턴합니다.")
@marshal_with(ResponseConceptUsageCount("measurement_list"),
              description="""
<pre>
measurement_list: 검사 정보가 들어갈 리스트
  .concept_id: 검사 Concept ID
  .concept_name: 검사 Concept 이름
  .usage_count: 검사 수행 수 (사용 수, 테이블에서 사용된 row 수)
</pre>
""")
@use_kwargs(RequestTopN, location="query")
def measurement_usage_count(**kwargs):
  top = kwargs.get("top", 10)
  return {
      "measurement_list": get_top_concept_by_usage_count(t_measurement,
                                                         "measurement_concept_id",
                                                         top)
  }
