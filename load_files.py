import boto3, logging

from config import OLD_BUCKET, OLD_PREFIX
from db import Images, generate_metadata, generate_session
from utils import S3Utils


def load_data(session, s3, name):
    object = s3.Object(OLD_BUCKET, f'{OLD_PREFIX}/{name}.png')
    object.put(Body=f'body of {name}')
    try:
        new_rec = Images(name=f'{name}.png', old_key=f'{OLD_PREFIX}/{name}.png')
        session.add(new_rec)
        session.commit()
    except Exception as e:
        logging.error(e)
        session.rollback()
