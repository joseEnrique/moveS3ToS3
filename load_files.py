import boto3

from db import Images, generate_metadata, generate_session

session = boto3.session.Session()

s3_client = session.client(
    service_name='s3',
    endpoint_url='http://localhost:8080',

)

generate_metadata()
session = generate_session()


def load_data(i):
    res = s3_client.put_object(Bucket='legacy', Key=f'image/{i}.png', Body=f'body of {i}')
    try:
        new_rec = Images(name=f'{i}.png',old_key=f'image/{i}.png')
        session.add(new_rec)
        session.commit()
    except Exception as e:
        print (e)
        session.rollback()
    return res


if __name__ == "__main__":
    for i in range(1000000):
        print(i)
        load_data(i)
