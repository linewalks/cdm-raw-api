from marshmallow import Schema, fields


class RequestDeathsSchema(Schema):
  features = fields.List(
      fields.Str(),
      missing=None,
      description="머신러닝 모델의 피쳐로 사용할 카테고리명\n현재 지원: (demo)"
  )
  model = fields.Str(
      missing="lgbm",
      description="사용할 머신러닝 모델\n현재 지원: (lgbm)"
  )


class DataInfo(Schema):
  num_patients = fields.Int(required=True, description="환자 수")
  num_visits = fields.Int(required=True, description="방문 수")
  label_ratio = fields.Float(required=True, description="타겟 라벨 비율")


class EvaluateInfo(Schema):
  auroc = fields.Float(required=True, description="AUROC Score")
  auprc = fields.Float(required=True, description="AUPRC Score")
  f1 = fields.Float(required=True, description="F1 Score")


class ResponseDeathSchema(Schema):
  train_data = fields.Nested(DataInfo, description="Train 데이터 통계")
  test_data = fields.Nested(DataInfo, description="Test 데이터 통계")
  evaluate = fields.Nested(EvaluateInfo, description="모델 예측 성능")
