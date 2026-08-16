from configurations import Configuration

from .common import Common


class Dev(Common, Configuration):
    DEBUG = True
    COMPRESS_ENABLED = False
    COMPRESS_OFFLINE = False
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }
    CONTENT_SECURITY_POLICY_REPORT_ONLY = Common.CSP_POLICY
    COMPRESS_ROOT = Common.BASE_DIR / "static"
    print("Running in non production. Now setting all prod options OFF...")

    INSTALLED_APPS = Common.apps
