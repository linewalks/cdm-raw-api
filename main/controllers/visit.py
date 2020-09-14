from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with, doc
from sqlalchemy import func, extract

from main import db
from main.models.cdm import t_visit_occurrence, t_concept
from main.controllers.utils import convert_query_to_response


visit_bp = Blueprint("visit", __name__, url_prefix="/api/data/visit")
MODEL_TYPE = "Visit"


@visit_bp.route("/year-count", methods=["GET"])
@doc(tags=[MODEL_TYPE],
     summary="연도별 방문 분포",
     description="연도별 방문 수를 리턴합니다..")
def visit_year_count(**kwargs):
  query = db.session.query(extract("year", t_visit_occurrence.c.visit_start_date),
                           func.count(t_visit_occurrence.c.visit_occurrence_id))\
                    .group_by(extract("year", t_visit_occurrence.c.visit_start_date))

  return {
    "visit_list": convert_query_to_response(("year", "visit_count"),
                                             query.all())
  }
