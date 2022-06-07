import logging
from xml.dom import ValidationErr

import azure.functions as func

from jsonschema import validate

from database_config import create_db_connection, execute_query
from entities.order import Actor, Order
from settings import Session, engine, Base

# 2 - generate database schema
Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()



# TODO change the order_schema to actually be like the one in user story: 
order_schema = {
    "type": "object",
    "properties": {
        "sender": {"type": "number"}, # TODO change to type "actor"
        "receiver": {"type": "number"},
        "status": {"type": "string"},
    }
}

def validate_json(order):
    try:
        validate(instance=order, schema=order_schema)
        logging.info("the json has the correct format")
        return True
    except Exception:
        return False


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        order = req_body.get('order')

        #validate the json schema
        if not validate_json(order):
            return func.HttpResponse(
                f'''
                The "order" must have the format:
                {order_schema}
                '''
            )
        else:


            if order["sender"] and order["receiver"]:
                sender = order["sender"]
                receiver = order["receiver"]

                logging.info("these are the actors")
                logging.info(sender)
                logging.info(receiver)

                # we retrieve the orders from the database

                # orders = Order.get_all()

                required_order = session.query(Order).filter(sender == sender)
                required_order = Order.filter(Order.order_number == 3).all()
                required_order = Order.filter_all(Order.sender == sender)

                Order.update({Order.status: "prueba"}, Order.order_number == 3)

                Order.filter(Order.order_number == 3).update({Order.status: "prueba"})

                logging.info("These are the required orders")

                logging.info(required_order)


                
                # for spike purposes, we connect to the already existing local database

                # connection = create_db_connection("localhost", "root", "NEW_USER_PASSWORD", "order_mock") #change credentials as necessary
                
                # # change this query as intended
                # query = f"""
                # SELECT * FROM order_mock WHERE sender={sender};
                # """
                # execute_query(connection, query)

                #################################

                return func.HttpResponse(f'The order is {required_order}')


            else:
                return func.HttpResponse("Pass an actor and receiver into the order")

    except ValueError:
        return func.HttpResponse("This function requires an order in the query to work")



