from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with, doc
from sqlalchemy import func

from main import db
from main.controllers.utils import convert_query_to_response
from main.models.cdm import t_concept, t_person, t_death
from main.models.resources import (
    PersonCount,
    ResponseConceptPersonCount
)


person_bp = Blueprint("person", __name__, url_prefix="/api/data/person")
MODEL_TYPE = "Person"


def get_person_group_count_query(group_col):
  query = db.session.query(t_person.c.get(group_col),
                           t_concept.c.concept_name,
                           func.count(t_person.c.person_id))\
                    .join(t_concept, t_concept.c.concept_id == t_person.c.get(group_col))\
                    .group_by(t_person.c.get(group_col), t_concept.c.concept_name)
  return query


@person_bp.route("/count", methods=["GET"])
@doc(tags=[MODEL_TYPE],
     summary="전체 환자 수",
     description="전체 환자 수를 리턴합니다.")
@marshal_with(PersonCount,
              description="""
<pre>
person_count: 전체 환자 수
</pre>
""")
def person_count():
  return {"person_count": db.session.query(t_person).count()}


@person_bp.route("/death-count", methods=["GET"])
@doc(tags=[MODEL_TYPE],
     summary="사망 환자 수",
     description="사망 기록이 있는 환자 수를 리턴합니다.")
@marshal_with(PersonCount,
              description="""
<pre>
person_count: 사망 기록이 있는 환자 수
</pre>
""")
def person_death_count():
  return {"person_count": db.session.query(t_death).count()}


@person_bp.route("/gender-count", methods=["GET"])
@doc(tags=[MODEL_TYPE],
     summary="성별 환자 분포",
     description="성별 환자 수를 리턴합니다.")
@marshal_with(ResponseConceptPersonCount("person_list"),
              description="""
<pre>
person_list: 환자 수 정보가 들어갈 리스트
  .concept_id: 성별 Concept ID
  .concept_name: 성별 Concept 이름
  .person_count: 환자 수
</pre>
""")
def person_gender_count():
  query = get_person_group_count_query("gender_concept_id")

  return {
      "person_list": convert_query_to_response(("concept_id", "concept_name", "person_count"),
                                               query.all())
  }


@person_bp.route("/race-count", methods=["GET"])
@doc(tags=[MODEL_TYPE],
     summary="인종(race)별 환자 분포",
     description="인종(race)별 환자 수를 리턴합니다.")
@marshal_with(ResponseConceptPersonCount("person_list"),
              description="""
<pre>
person_list: 환자 수 정보가 들어갈 리스트
  .concept_id: 인종(race)별 Concept ID
  .concept_name: 인종(race)별 Concept 이름
  .person_count: 환자 수
</pre>
""")
def person_race_count():
  query = get_person_group_count_query("race_concept_id")
  return {
      "person_list": convert_query_to_response(("concept_id", "concept_name", "person_count"),
                                               query.all())
  }


@person_bp.route("/ethnicity-count", methods=["GET"])
@doc(tags=[MODEL_TYPE],
     summary="민족(ethnicity)별 환자 분포",
     description="민족(ethnicity)별 환자 수를 리턴합니다.")
@marshal_with(ResponseConceptPersonCount("person_list"),
              description="""
<pre>
person_list: 환자 수 정보가 들어갈 리스트
  .concept_id: 민족(ethnicity)별 Concept ID
  .concept_name: 민족(ethnicity)별 Concept 이름
  .person_count: 환자 수
</pre>
""")
def person_ethnicity_count():
  query = get_person_group_count_query("ethnicity_concept_id")
  return {
      "person_list": convert_query_to_response(("concept_id", "concept_name", "person_count"),
                                               query.all())
  }
