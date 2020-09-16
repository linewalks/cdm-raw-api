from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with, doc
from sqlalchemy import func, extract

from main import db
from main.controllers.utils import convert_query_to_response
from main.models.cdm import t_visit_occurrence, t_concept
from main.models.resources import (
    VisitCount,
    ResponseYearlyVisitCount,
    ResponseConceptVisitCount
)


visit_bp = Blueprint("visit", __name__, url_prefix="/api/data/visit")
MODEL_TYPE = "Visit"


@visit_bp.route("/count", methods=["GET"])
@doc(tags=[MODEL_TYPE],
     summary="전체 방문 수",
     description="전체 방문 수를 리턴합니다.")
@marshal_with(VisitCount,
              description="""
<pre>
visit_count: 전체 방문 수
</pre>
""")
def visit_count():
  return {"visit_count": db.session.query(t_visit_occurrence).count()}


@visit_bp.route("/year-count", methods=["GET"])
@doc(tags=[MODEL_TYPE],
     summary="연도별 방문 분포",
     description="연도별 방문 수를 리턴합니다.")
@marshal_with(ResponseYearlyVisitCount,
              description="""
<pre>
visit_list: 방문 수 정보가 들어갈 리스트
  .year: 연도
  .visit_count: 방문 수
</pre>
""")
def visit_year_count(**kwargs):
  query = db.session.query(extract("year", t_visit_occurrence.c.visit_start_date),
                           func.count(t_visit_occurrence.c.visit_occurrence_id))\
                    .group_by(extract("year", t_visit_occurrence.c.visit_start_date))

  return {
      "visit_list": convert_query_to_response(("year", "visit_count"),
                                              query.all())
  }


@visit_bp.route("/visit-count", methods=["GET"])
@doc(tags=[MODEL_TYPE],
     summary="방문 유형별 방문 수",
     description="방문 유형별 방문 수를 리턴합니다.")
@marshal_with(ResponseConceptVisitCount("visit_list"),
              description="""
<pre>
visit_list: 방문 수 정보가 들어갈 리스트
  .concept_id: 방문 유형 Concept ID
  .concept_name: 방문 유형 Concept 이름
  .visit_count: 방문 수
</pre>
""")
def visit_type_count():
  query = db.session.query(t_visit_occurrence.c.visit_concept_id,
                           t_concept.c.concept_name,
                           func.count(t_visit_occurrence.c.visit_occurrence_id))\
                    .join(t_concept, t_concept.c.concept_id == t_visit_occurrence.c.visit_concept_id)\
                    .group_by(t_visit_occurrence.c.visit_concept_id,
                              t_concept.c.concept_name)

  return {
      "visit_list": convert_query_to_response(("concept_id", "concept_name", "visit_count"),
                                               query.all())
  }
