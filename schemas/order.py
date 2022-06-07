from flask_marshmallow import Marshmallow
from marshmallow import fields

ma = Marshmallow()

class OrderSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    created_data = fields.String()
    order_number = fields.String()
    status = fields.String() # It can be an enum
    requested_delivery_date = fields.String()
    sender = fields.Integer()
    receiver = fields.Integer()
    order_lines = fields.Nested('OrderLinesSchema', many=True)

class OrderLinesSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    order_line_number = fields.String()
    status = fields.String()# It can be an enum
    product_code = fields.String()
    requested_quantity = fields.String() # combination of value and measurement unit
    requested_delivery_date = fields.String()

class ActorSchema(ma.Schema):
    gln_code = fields.Integer(dump_only=True)
    order_sender = fields.Nested('OrderSchema', many=True)
    order_receiver = fields.Nested('OrderSchema', many=True)