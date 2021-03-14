from sqlalchemy import func

from db import generate_session, Pictures

session = generate_session()


def get_not_processed_key():
    while session.query(Pictures).filter(Pictures.new_route == None).count() > 0:
        yield session.query(Pictures).filter(Pictures.new_route == None).first()
    #for not_new_route_element in session.query(Pictures).filter(Pictures.new_route == None):
    #    yield not_new_route_element.old_route


for i in get_not_processed_key():
    print (i)

