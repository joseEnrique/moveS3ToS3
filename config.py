import os
#S3 Config
URL_ENDPOINT = os.getenv('URL_ENDPOINT') or 'http://localhost:8080'


#       s3.amazonaws.com
OLD_BUCKET = os.getenv('OLD_BUCKET') or 'legacy-s3'
OLD_PREFIX = os.getenv('OLD_PREFIX') or 'images'
NEW_BUCKET = os.getenv('NEW_BUCKET') or 'production-s3'
NEW_PREFIX = os.getenv('NEW_PREFIX') or 'avatar'

#MYSQL URL connection
MYSQL_URL = os.getenv('MYSQL_URL') or 'mysql+pymysql://sketchUser:sketchPassword@localhost/sketch'

#LOAD files
LOAD_FILES = os.getenv('LOAD_FILES') or 'false'

