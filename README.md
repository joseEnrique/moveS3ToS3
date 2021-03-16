# moveS3ToS3
## Description
Process to move objects between two differents S3 buckets.

##Components emulated to test it locally

1. __[gaul/s3proxy](https://github.com/gaul/s3proxy)__. S3 emulation to have the S3 API functionalities
2. __mariadb__. Db to save the old, and the new route of each document. Used for a tracking purpose

## Variables

| Variable      | Description | Default value     |
| :---        |    :---:   |          :----: |
| URL_ENDPOINT      | S3 endpoint       | http://localhost:8080  |
| AWS_ACCESS_KEY_ID   | AWS Access Key Id        | blank   |
| AWS_SECRET_ACCESS_KEY   | AWS Secret Access Key       | blank   |
| OLD_BUCKET   | Name of the old bucket        | legacy-s3   |
| OLD_PREFIX   | Old Prefix where all objs are        | images   |
| NEW_BUCKET   | Name of the new bucket        | production-s3   |
| NEW_PREFIX   | New Prefix where all objs are         | avatar   |
| MYSQL_URL   | Mysql URL connection        |  'mysql+pymysql://sketchUser:sketchPassword@localhost/sketch'  |
| LOAD_FILES   | Load sample files at the beginning        | false   |




## Installation
``` bash
pip install -r src/requirements.txt
```

## Load initial files
You can load documents with a counter name to test the application

``` bash
cd src/
python load_files.py
```


## Run the application
You can load documents with a counter name to test the application

``` bash
python main.py
```

## Run all the scenario

You can test all the components with docker compose
``` bash
docker-compose up
```

## Permissions needed in a production-grade environment
### Mysql
`load-file is excluded becauses of the creation of schema in the DB and this needs other permissions`

Grants needed in the user:
1. SELECT
2. UPDATE

### S3
__Old bucket__:
1. ListBucket
2. GetObject



__New bucket__: 

1. PutObject
2. PutObjectAcl


## Improvements

To scale up the service you could scale up
the service into the docker compose or just opening as many
process as you desire. The process is resilient and is ready to get
the next object that is not migrated yet. In order to improve
the process itself, it could be copied in parallel with multiprocessing.

In addition, if this process was used as a docker service (ECS,Kubernetes...), 
I would recommend to migrate the process to a compiled lenguage such as goLang to reduce the image.
But it would study the cost-performance ratio.
