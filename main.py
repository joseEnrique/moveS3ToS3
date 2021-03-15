import boto3

from db import generate_session, Images
from utils import DtoMaria, DtoS3

if __name__ == "__main__":
    session = generate_session()
    s3 = DtoS3.get_s3_resource()

    print(session.query(Images).filter(Images.new_key == None).count())

    for object_not_migrated in DtoMaria.get_not_processed_key(session):
        new_key = f'avatar/{object_not_migrated.name}'
        old_key = f'image/{object_not_migrated.name}'
        transferred = DtoS3.transfer_s3_to_s3(s3, old_key, new_key)
        if transferred:
            DtoMaria.update_element(session, object_not_migrated, new_key)
            print("Processed", object_not_migrated.old_key)
