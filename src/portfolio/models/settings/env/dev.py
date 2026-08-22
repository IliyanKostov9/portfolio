from configurations import Configuration

from .common import Common


class Dev(Common, Configuration):
    DEBUG = True
    COMPRESS_ENABLED = False
    COMPRESS_OFFLINE = False
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }
    CONTENT_SECURITY_POLICY_REPORT_ONLY = Common.CSP_POLICY
    COMPRESS_ROOT = Common.BASE_DIR / "static"
    STATIC_ROOT = "/var/www/localhost/static/"
    INSTALLED_APPS = Common.apps

    STORAGES = {
        "default": {"BACKEND": "storages.backends.s3.S3Storage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
