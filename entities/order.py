import datetime

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey

from settings import Base
from sqlalchemy.orm import relationship
from repository.repository import BaseModelMixin

class Order(Base, BaseModelMixin):

    __tablename__ = 'order_table'

    id = Column(Integer, primary_key=True)
    created_data = Column(Date)
    order_number = Column(String(100))
    status = Column(String(100)) # It can be an enum
    requested_delivery_date = Column(Date)
    sender = Column(Integer, ForeignKey('actor.gln_code'), nullable=False)
    receiver = Column(Integer, ForeignKey('actor.gln_code'), nullable=False)
    order_lines = relationship('OrderLines', foreign_keys = "OrderLines.order", backref='order_associated', lazy="dynamic", cascade='all, delete-orphan')


    def __init__(self, created_data: datetime.date, order_number: str, status: str, requested_delivery_date: datetime.date):
        self.created_data = created_data
        self.order_number = order_number
        self.status = status
        self.requested_delivery_date = requested_delivery_date


    def __repr__(self):
        return f'Order ({self.order_number})'


class OrderLines(Base, BaseModelMixin):

    __tablename__ = 'order_lines_table'

    id = Column(Integer, primary_key=True)
    order_line_number = Column(String(100))
    status = Column(String(100)) # It can be an enum
    product_code = Column(String(100))
    requested_quantity = Column(String(100)) # combination of value and measurement unit
    requested_delivery_date = Column(Date)
    order = Column(Integer, ForeignKey('order_table.id'), nullable=False)

    def __init__(self, order_line_number: str, status: str, product_code: str, requested_quantity: str, requested_delivery_date: datetime.date):
        self.order_line_number = order_line_number
        self.status = status
        self.product_code = product_code
        self.requested_quantity = requested_quantity
        self.requested_delivery_date = requested_delivery_date

    def __repr__(self):
        return f'Order Line number ({self.order_line_number})'


class Actor(Base, BaseModelMixin):

    __tablename__ = "actor"
    
    gln_code = Column(Integer, primary_key=True)
    order_sender = relationship("Order", foreign_keys = "Order.sender", backref = "actor_sender", lazy = "dynamic")
    order_receiver = relationship("Order", foreign_keys = "Order.receiver", backref = "actor_receiver", lazy = "dynamic")
    # order = relationship('Order', backref='actor', lazy=False, cascade='all, delete-orphan')
    # order_sender = relationship('Order', backref='order.sender', lazy=False, cascade='all, delete-orphan')
    # order_receiver = relationship('Order', backref='order.receiver', lazy=False, cascade='all, delete-orphan')

    def __init__(self, gln_code: int):
        self.gln_code = gln_code

    # def __repr__(self):
    #     return f'Order Line number ({self.order_line_number})'