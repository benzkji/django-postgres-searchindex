import logging
import os
import tempfile

import environ

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENV_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

env = environ.Env()
environ.Env.read_env(os.path.join(ENV_ROOT, ".env"))

DEBUG = True

logging.getLogger("factory").setLevel(logging.WARN)

SITE_ID = 1


DB_CONF = env.db()
DATABASES = {"default": DB_CONF}

LANGUAGE_CODE = "en"
LANGUAGES = (
    (
        "en",
        "ENGLISH",
    ),
)

X_FRAME_OPTIONS = "SAMEORIGIN"
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
ROOT_URLCONF = "postgres_searchindex.tests.urls"

# media root is overridden when needed in tests
MEDIA_ROOT = tempfile.mkdtemp(suffix="ckeditor_media_root")
MEDIA_URL = "/media/"
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(APP_ROOT, "../test_app_static")
STATICFILES_DIRS = (os.path.join(APP_ROOT, "static"),)

CMS_CONFIRM_VERSION4 = True

COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(os.path.join(APP_ROOT, "tests/coverage"))
COVERAGE_MODULE_EXCLUDES = [
    "tests$",
    "settings$",
    "urls$",
    "locale$",
    "migrations",
    "fixtures",
    "admin$",
    "django_extensions",
]

EXTERNAL_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "cms",
    "treebeard",
    "menus",
    "sekizai",
)
INTERNAL_APPS = (
    "postgres_searchindex",
    "postgres_searchindex.tests.test_app",
)


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "sekizai.context_processors.sekizai",
                "cms.context_processors.cms_settings",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
                # 'django.template.loaders.eggs.Loader',
            ],
        },
    },
]


MIDDLEWARE = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    # Uncomment the next line for simple clickjacking protection:
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
)

INSTALLED_APPS = EXTERNAL_APPS + INTERNAL_APPS
COVERAGE_MODULE_EXCLUDES += EXTERNAL_APPS

SECRET_KEY = "foobarXXXxxsasdvasdvsd()&/%vXY"
