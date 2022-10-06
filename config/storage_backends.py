from storages.backends.s3boto3 import S3Boto3Storage


class PublicStorage(S3Boto3Storage):
    location = 'public'
    default_acl = 'public-read'
    file_overwrite = False


class PrivateStorage(S3Boto3Storage):
    location = 'private'
    default_acl = 'private'
    file_overwrite = False
