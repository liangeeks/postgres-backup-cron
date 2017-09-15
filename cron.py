# -*- coding: utf-8 -*-
# flake8: noqa
import os
import datetime
import subprocess
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
AK = os.environ.get("QINIU_AK")
SK = os.environ.get("QINIU_SK")
BUCKET_NAME = os.environ.get("QINIU_BUCKET_NAME")

POSTGRES_HOST = os.environ.get("POSTGRES_HOST", 'db')
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
    POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB)


def backup():
    backup_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    fpath = "/data/backups/dump.{}.{}.gz".format(POSTGRES_DB, backup_time)

    subprocess.call("pg_dump --dbname={} | gzip > {}".format(POSTGRES_URI, fpath), shell=True)
    return fpath

def put2qiniu(fpath):
    # 上传到七牛后保存的文件名
    key = fpath[1:]
    # 生成上传 Token，可以指定过期时间等
    token = Auth(AK, SK).upload_token(BUCKET_NAME, key, 3600)
    # 要上传文件的本地路径
    ret, info = put_file(token, key, fpath)
    return ret

fp = backup()

put2qiniu(fp)
