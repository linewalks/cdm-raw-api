from sqlalchemy import func

from main import db
from main.models.cdm import t_concept
from main.controllers.utils import convert_query_to_response


def get_top_concept_by_person_count(table, col_name, top):
  query = db.session.query(table.c.get(col_name),
                           t_concept.c.concept_name,
                           func.count(table.c.person_id.distinct()))\
                    .group_by(table.c.get(col_name), t_concept.c.concept_name)\
                    .order_by(func.count(table.c.person_id.distinct()).desc())\
                    .join(t_concept, t_concept.c.concept_id == table.c.get(col_name))
  result = query.limit(top).all()
  return convert_query_to_response(("concept_id", "concept_name", "person_count"), result)


def get_top_concept_by_usage_count(table, col_name, top):
  query = db.session.query(table.c.get(col_name),
                           t_concept.c.concept_name,
                           func.count(table.c.get(col_name)))\
                    .group_by(table.c.get(col_name), t_concept.c.concept_name)\
                    .order_by(func.count(table.c.get(col_name)).desc())\
                    .join(t_concept, t_concept.c.concept_id == table.c.get(col_name))
  result = query.limit(top).all()
  return convert_query_to_response(("concept_id", "concept_name", "usage_count"), result)
