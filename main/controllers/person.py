from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with, doc
from sqlalchemy import func

from main import db
from main.models.cdm import t_person, t_concept
from main.controllers.utils import convert_query_to_response


person_bp = Blueprint("person", __name__, url_prefix="/api/data/person")
MODEL_TYPE = "Person"


@person_bp.route("/gender-count", methods=["GET"])
@doc(tags=[MODEL_TYPE],
     summary="성별 환자 분포",
     description="성별 환자 수를 리턴합니다..")
def person_gender_count(**kwargs):
  query = db.session.query(t_person.c.gender_concept_id,
                           t_concept.c.concept_name,
                           func.count(t_person.c.person_id))\
                    .join(t_concept, t_concept.c.concept_id == t_person.c.gender_concept_id)\
                    .group_by(t_person.c.gender_concept_id, t_concept.c.concept_name)

  return {
    "person_list": convert_query_to_response(("gender_concept_id", "gender_concept_name", "person_count"),
                                             query.all())
  }
