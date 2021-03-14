from sqlalchemy import func

from db import generate_session, Pictures

session = generate_session()


def get_not_processed_key():
    while session.query(Pictures).filter(Pictures.new_route is None).count() > 0:
        # ran_object = session.query(Pictures).filter(Pictures.new_route == None).order_by(func.rand()).first()
        ran_object = session.query(Pictures).filter(Pictures.new_route is None).order_by(func.rand()).first()
        yield ran_object
    # for not_new_route_element in session.query(Pictures).filter(Pictures.new_route == None):
    #    yield not_new_route_element.old_route


def update_element(pic):
    try:
        pic.new_route = 'updated'
        session.add(pic)
        session.commit()
    except:
        session.rollback()


for i in get_not_processed_key():
    update_element(i)
    print(session.query(Pictures).filter(Pictures.new_route is None).count())
