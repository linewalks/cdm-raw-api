from marshmallow import Schema, fields


class RequestDeathsSchema(Schema):
  features = fields.List(fields.Str(), missing=None)
  model = fields.Str(missing="lgbm")
