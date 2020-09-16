from marshmallow import fields, Schema


# Request
class RequestTopN(Schema):
  top = fields.Int(description="상위 몇개까지 리턴받을지 설정합니다.")


# Response
class Concept(Schema):
  concept_id = fields.Int(description="Concept ID")
  concept_name = fields.Str(description="Concept 이름")


class PersonCount(Schema):
  person_count = fields.Int(description="환자 수")


class UsageCount(Schema):
  usage_count = fields.Int(description="사용 수")


class ConceptPersonCount(Concept, PersonCount):
  pass


class ConceptUsageCount(Concept, UsageCount):
  pass


def create_nested_list_schema(root_name, schema, name):
  return Schema.from_dict({
      root_name: fields.List(fields.Nested(schema))
  }, name=name)


def create_concept_person_count_list_schema(root_name):
  schema_name = root_name.split("_")[0].capitalize()
  schema_name = f"Response{schema_name}PersonCount"
  return create_nested_list_schema(root_name, ConceptPersonCount, schema_name)


def create_concept_usage_count_list_schema(root_name):
  schema_name = root_name.split("_")[0].capitalize()
  schema_name = f"Response{schema_name}Usagecount"
  return create_nested_list_schema(root_name, ConceptUsageCount, schema_name)


# shortage for export
ResponseConceptPersonCount = create_concept_person_count_list_schema
ResponseConceptUsageCount = create_concept_usage_count_list_schema

