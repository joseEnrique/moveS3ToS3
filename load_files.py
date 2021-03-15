import boto3

from config import OLD_BUCKET, OLD_PREFIX
from db import Images, generate_metadata, generate_session
from utils import S3Utils

session = boto3.session.Session()

s3_client = S3Utils.get_s3_resource()
generate_metadata()
session = generate_session()

print(s3_client)


def load_data(i):
    object = s3_client.Object(OLD_BUCKET, f'{OLD_PREFIX}/{i}.png')
    object.put(Body=f'body of {i}')
    try:
        new_rec = Images(name=f'{i}.png', old_key=f'{OLD_PREFIX}/{i}.png')
        session.add(new_rec)
        session.commit()
    except Exception as e:
        session.rollback()


if __name__ == '__main__':
    for i in range(1000000):
        load_data(i)
