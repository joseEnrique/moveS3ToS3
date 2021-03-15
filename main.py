import boto3

from db import generate_session, Pictures
from dto import DtoMaria, DtoS3

if __name__ == "__main__":
    session = generate_session()
    s3 = DtoS3.get_s3_resource()

    print(session.query(Pictures).filter(Pictures.new_route == None).count())

    for i in DtoMaria.get_not_processed_key(session):
        transferred = DtoS3.transfer_s3_to_s3(s3, i.old_route, i.old_route)
        if transferred:
            DtoMaria.update_element(session, i)
            print("Processed",i.old_route)
