import logging
from xml.dom import ValidationErr
from datetime import date
import azure.functions as func

from jsonschema import validate

from database_config import create_db_connection, execute_query
from entities.order import Actor, Order, OrderLines
from settings import Session, engine, Base
from schemas.order import OrderSchema, ActorSchema, OrderLinesSchema

from fastapi import FastAPI

# app = FastAPI()

# 2 - generate database schema
Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()

# 4 - Initiate Schemas
order_schema = OrderSchema()
order_lines_schema = OrderLinesSchema()
actor_schema = ActorSchema()


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # 1 - Create
    logging.info('Create an order. A JSON is received by POST method')

    # func.AsgiMiddleware(app).handle(req, context)
    try:
        data = req.get_json()
        order_dict = order_schema.load(data)
        # req_body = req.get_json()
        # order_dict = req_body.get('order')

        sender = Actor.filter_first(Actor.gln_code == order_dict["sender"])
        logging.info(f'Sender {sender}')
        receiver = Actor.filter_first(Actor.gln_code == order_dict["receiver"])
        logging.info(f'Receiver {receiver}')

        if not sender:
            sender = Actor(gln_code = order_dict["sender"])
        
        if not receiver:
            receiver = Actor(gln_code = order_dict["receiver"])

        order = Order(created_data = date.today(), 
                    order_number = order_dict["order_number"], 
                    status = order_dict["status"], 
                    requested_delivery_date = date.today())

        for order_line in order_dict["order_lines"]:
            new_order_line = OrderLines(order_line_number = order_line["order_line_number"],
                                        status = order_line["status"],
                                        product_code = order_line["product_code"],
                                        requested_quantity = order_line["requested_quantity"],
                                        requested_delivery_date = date.today()) 
            order.order_lines.append(new_order_line)
            logging.info(f'Order line number {new_order_line.order_line_number}')

        # order.create()

        receiver.order_receiver.append(order)
        sender.order_sender.append(order)

        order.create()

        response = order_schema.dump(order)

        logging.info("These are the dump json {response}")

        return func.HttpResponse(f'{response}')

    except ValueError:
        return func.HttpResponse("This function requires an order in the query to work")


    # # 2 - Read
    # logging.info('Get an order. A order number is received and a order JSON is returned by GET method')
    # try:
    #     order_number = req.params.get('order_number')
    #     logging.info(f'Order number {order_number}')

    #     # order = session.query(Order).get(order_number == order_number)
    #     order = Order.get_by(order_number == order_number)
    #     logging.info(f'Order {order}')

    #     sender = Actor.filter_first(Actor.gln_code == order.sender)
    #     logging.info(f'Sender {sender}')
    #     receiver = Actor.filter_first(Actor.gln_code == order.receiver)
    #     logging.info(f'Receiver {receiver}')

    #     response = order_schema.dump(order)

    #     logging.info("These are the dump json {response}")

    #     return func.HttpResponse(f'{response}')

    # except ValueError:
    #     return func.HttpResponse("This function requires an order in the query to work")
    

    # # 3 - Update
    # logging.info('Delete an order. A JSON is received by POST method, the status field is changed.')
    # try:
    #     data = req.get_json()
    #     order_dict = order_schema.load(data)
    #     logging.info(f'{order_dict}')

    #     sender = Actor.filter_first(Actor.gln_code == order_dict["sender"])
    #     logging.info(f'Sender {sender}')
    #     receiver = Actor.filter_first(Actor.gln_code == order_dict["receiver"])
    #     logging.info(f'Receiver {receiver}')

    #     if not sender:
    #         sender = Actor(gln_code = order_dict["sender"])
        
    #     if not receiver:
    #         receiver = Actor(gln_code = order_dict["receiver"])

    #     Order.update({Order.status: order_dict["status"]}, Order.order_number == order_dict["order_number"])
    #     updated_order = Order.filter_first(Order.order_number == order_dict["order_number"])

    #     response = order_schema.dump(updated_order)

    #     logging.info("These are the dump json {response}")

    #     return func.HttpResponse(f'{response}')

    # except ValueError:
    #     return func.HttpResponse("This function requires an order in the query to work")

    
    # # 4 - Delete
    # logging.info('Update an order. A order number is received and its associated order is deleted by GET method.')
    # try:
    #     order_number = req.params.get('order_number')
    #     logging.info(f'Order number {order_number}')

    #     deleted_order = Order.filter_first(Order.order_number == order_number)

    #     response = order_schema.dump(deleted_order)
    #     logging.info("These are the dump json {response}")

    #     deleted_order.delete()

    #     return func.HttpResponse(f'{response}')

    # except ValueError:
    #     return func.HttpResponse("This function requires an order in the query to work")
