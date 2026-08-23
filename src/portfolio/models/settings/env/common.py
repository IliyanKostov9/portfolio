import os
from pathlib import Path

from csp.constants import SELF, UNSAFE_INLINE
from django.urls import reverse_lazy


class Common:
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent.parent
    ALLOWED_HOSTS = [os.environ.get("PORTFOLIO_HOST")]
    ROOT_URLCONF: str = "portfolio.urls"
    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    SECRET_KEY = os.environ.get("PORTFOLIO_SECRET_KEY")
    if not SECRET_KEY and not bool(
        os.environ.get("PORTFOLIO_SKIP_SECRET_KEY_CHECK", False)
    ):
        raise OSError("SECRET KEY is not set!")

    STATIC_URL = "/static/"
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    STATICFILES_DIRS = [
        BASE_DIR / "static",
        f"{BASE_DIR}/apps/resume/static",
        f"{BASE_DIR}/apps/blogs/static",
    ]
    STATICFILES_FINDERS = (
        "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
        "compressor.finders.CompressorFinder",
    )
    AWS_QUERYSTRING_AUTH = False
    CDN_URL = os.environ.get("PORTFOLIO_CDN_ASSETS_URL", "")
    if CDN_URL == "":
        raise OSError("CDN_URL should not be empty!")
    else:
        AWS_S3_CUSTOM_DOMAIN = CDN_URL.split("//")[1]
        MEDIA_URL = CDN_URL + "/"

    COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)
    # NOTE: Maybe remove it from prod ?
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "portfolio-cache",
        }
    }
    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [
                f"{BASE_DIR}/apps/resume/templates/pages",
                f"{BASE_DIR}/apps/resume/templates",
                f"{BASE_DIR}/apps/blogs/templates/pages",
                f"{BASE_DIR}/apps/blogs/templates",
                BASE_DIR / "templates",
            ],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                    "apps.resume.processors.cookie.change_theme",
                ],
            },
        },
    ]

    sqlite3_engine = "django.db.backends.sqlite3"
    DATABASE_ROUTERS = ["portfolio.routers.portfolio_router.PortfolioRouter"]
    DATABASES = {
        "default": {
            "ENGINE": sqlite3_engine,
            "NAME": BASE_DIR / "db.sqlite3",
            "TEST": {
                "NAME": BASE_DIR / "db.test.sqlite3",
                "ENGINE": sqlite3_engine,
            },
        },
        # TODO: Configure multiple database
        # "portfolio": {
        #     "NAME": "portfolio",
        #     "ENGINE": "django.db.backends.postgresql",
        #     "USER": os.environ.get("PORTFOLIO_POSTGRES_USER"),
        #     "PASSWORD": os.environ.get("PORTFOLIO_POSTGRES_PASSWORD"),
        #     "HOST": os.environ.get("PORTFOLIO_POSTGRES_HOST"),
        #     "PORT": "5432",
        #     "OPTIONS": {
        #         "server_side_binding": True,
        #     },
        #     "TEST": {
        #         "NAME": BASE_DIR / "db.test.sqlite3",
        #         "ENGINE": sqlite3_engine,
        #     },
        # },
    }

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = os.environ.get("PORTFOLIO_FROM_EMAIL")
    EMAIL_HOST = os.environ.get("PORTFOLIO_EMAIL_HOST")
    EMAIL_HOST_USER = os.environ.get("PORTFOLIO_EMAIL_USER")
    EMAIL_HOST_PASSWORD = os.environ.get("PORTFOLIO_EMAIL_PASSWORD")

    CSP_REPORT_URI = reverse_lazy("monitor/csp-report")
    CSP_REPORTS_EMAIL_ADMINS = True
    CSP_REPORTS_LOG = False
    CSP_REPORTS_SAVE = False
    CSP_POLICY = {
        "DIRECTIVES": {
            "default-src": [SELF],
            "media-src": [
                SELF,
                "blob:",
                os.environ.get("PORTFOLIO_CDN_ASSETS_URL"),
            ],
            "connect-src": [SELF, "https://api.github.com"],
            "script-src": [
                SELF,
                UNSAFE_INLINE,
                "https://cdnjs.cloudflare.com",
                "https://unpkg.com",
            ],
            "style-src": [
                SELF,
                "https://cdnjs.cloudflare.com",
                "https://fonts.googleapis.com",
                "'sha256-47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU='",
                "'sha256-3ITP0qhJJYBulKb1omgiT3qOK6k0iB3rMDhGfpM8b7c='",
                "'sha256-DqHyLrY03A99krj4zwj8j6M04dAkecX+/ck4dgG6zCk='",
                "'sha256-bsV5JivYxvGywDAZ22EZJKBFip65Ng9xoJVLbBg7bdo='",
                # NOTE: For Error 404 && 500
                "'sha256-oxny43U4yMNZqsxffAINTdjzidFj6nAZr/6MrmG+WZA='",
            ],
            "frame-src": [
                "'self'",
                "https://youtube.com",
                "https://www.youtube.com",
                "https://youtube-nocookie.com",
                "https://www.youtube-nocookie.com",
            ],
            "font-src": ["https://fonts.gstatic.com", "https://cdnjs.cloudflare.com"],
            "img-src": [
                SELF,
                "blob:",
                "https://mdbootstrap.com",
                os.environ.get("PORTFOLIO_CDN_ASSETS_URL"),
            ],
            "frame-ancestors": [SELF],
            "form-action": [SELF],
            "report-uri": "/monitor/csp-report",
        },
    }

    apps: list[str] = [
        "apps.common.apps.CommonConfig",
        "apps.resume.apps.ResumeConfig",
        "apps.blogs.apps.BlogsConfig",
        "compressor",
        # "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        # NOTE: Test
        "whitenoise.runserver_nostatic",
        "django_test_migrations.contrib.django_checks.AutoNames",
        "django_test_migrations.contrib.django_checks.DatabaseConfiguration",
        "django_migration_linter",
    ]

    MIDDLEWARE: list[str] = [
        "django.middleware.cache.UpdateCacheMiddleware",  # INFO: Must be first
        # NOTE: Send email messages to admins when user gets 404 error
        "django.middleware.common.BrokenLinkEmailsMiddleware",
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "django.middleware.cache.FetchFromCacheMiddleware",  # INFO: Must be last
        "django.middleware.locale.LocaleMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "csp.middleware.CSPMiddleware",
    ]

    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    LANGUAGE_CODE = "en-us"
    TIME_ZONE = "Europe/Sofia"
    LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]
    USE_I18N = True
    USE_TZ = True
    LANGUAGES = [
        ("en", "English"),
        ("bg", "Bulgarian"),
        ("fr", "French"),
        ("ge", "German"),
    ]

    if os.environ.get("PORTFOLIO_ENV") == "prod":
        print("Running in production. Now setting all prod options ON...")
    elif os.environ.get("PORTFOLIO_ENV") == "dev":
        print("Running in non production. Now setting all prod options OFF...")
