from db import generate_session, Pictures
from dto import DtoMaria, DtoS3

if __name__ == "__main__":
    session = generate_session()
    print(session.query(Pictures).filter(Pictures.new_route is None).count())

    for i in DtoMaria.get_not_processed_key(session):
        DtoMaria.update_element(i)

