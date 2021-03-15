
from config import NEW_BUCKET, OLD_BUCKET, NEW_PREFIX, OLD_PREFIX
from db import generate_session, Images
from utils import MariaUtils, S3Utils

if __name__ == '__main__':
    session = generate_session()
    s3 = S3Utils.get_s3_resource()

    print(session.query(Images).filter(Images.new_key == None).count())

    for object_not_migrated in MariaUtils.get_not_processed_key(session):
        new_key = f'{NEW_PREFIX}/{object_not_migrated.name}'
        old_key = f'{OLD_PREFIX}/{object_not_migrated.name}'
        transferred = S3Utils.transfer_s3_to_s3(s3, old_key, new_key, NEW_BUCKET, OLD_BUCKET)
        if transferred:
            MariaUtils.update_element(session, object_not_migrated, new_key)
            print("Processed", object_not_migrated.old_key)
