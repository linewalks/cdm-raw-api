from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with, doc
from sqlalchemy import func

from main import db
from main.controllers.common import get_top_concept_by_person_count, get_top_concept_by_usage_count
from main.models.cdm import t_drug_exposure
from main.models.resources import RequestTopN, ResponseConceptPersonCount, ResponseConceptUsageCount


drug_bp = Blueprint("drug", __name__, url_prefix="/api/data/drug")
MODEL_TYPE = "Drug"


@drug_bp.route("/person-count", methods=["GET"])
@doc(tags=[MODEL_TYPE],
     summary="환자 수 기준 상위 N개 의약품",
     description="환자 수를 기준으로 상위 N개 의약품의 Concept ID와 이름, 환자 수를 리턴합니다.")
@marshal_with(ResponseConceptPersonCount("drug_list"),
              description="""
<pre>
drug_list: 의약품 정보가 들어갈 리스트
  .concept_id: 의약품 Concept ID
  .concept_name: 의약품 Concept 이름
  .person_count: 환자 수
</pre>
""")
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
     summary="처방 수 기준 상위 N개 의약품",
     description="처방 수를 기준으로 상위 N개 의약품의 Concept ID와 이름, 처방 수를 리턴합니다.")
@marshal_with(ResponseConceptUsageCount("drug_list"),
              description="""
<pre>
drug_list: 의약품 정보가 들어갈 리스트
  .concept_id: 의약품 Concept ID
  .concept_name: 의약품 Concept 이름
  .usage_count: 처방 수 (사용 수, 테이블에서 사용된 row 수)
</pre>
""")
@use_kwargs(RequestTopN, location="query")
def drug_usage_count(**kwargs):
  top = kwargs.get("top", 10)
  return {
      "drug_list": get_top_concept_by_usage_count(t_drug_exposure,
                                                  "drug_concept_id",
                                                  top)
  }
