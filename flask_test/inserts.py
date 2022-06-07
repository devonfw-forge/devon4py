# coding=utf-8

# 1 - imports
from datetime import date

from entities.order import Order, Actor
from settings import Session, engine, Base
# 2 - generate database schema
Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()

# 5 - creates actors
matt_damon = Actor(4)
dwayne_johnson = Actor(5)
mark_wahlberg = Actor(6)



# 4 - create orders 
order1 = Order(date.today(), "23", "accpeted", date.today())
order2 = Order(date.today(), "2", "accpeted", date.today())
order3 = Order(date.today(), "3", "accpeted", date.today())

order4 = Order(date.today(), 67, "something", date.today())


matt_damon.order_receiver = [order1, order2, order4]
matt_damon.order_sender = [order3]

mark_wahlberg.order_receiver = [order3]

dwayne_johnson.order_sender = [order1, order2, order4]





# 6 - add actors to movies
# order1.actor_sender = [matt_damon]
# order1.actor_receiver = [dwayne_johnson]


# order2.actor_sender = [mark_wahlberg]
# order2.actor_receiver = [dwayne_johnson]

# order3.actor_sender = [matt_damon]
# order3.actor_receiver = [mark_wahlberg]

# 9 - persists data
# session.add(matt_damon)
# session.add(dwayne_johnson)
# session.add(mark_wahlberg)


# session.add(order1)
# session.add(order2)
# session.add(order3)


order1.create()
order2.create()
order3.create()


order4.create()


# 10 - commit and close session
# session.commit()
session.close()

print("code terminated succesfully! :)")