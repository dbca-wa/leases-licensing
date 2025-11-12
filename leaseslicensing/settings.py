import hashlib
import os
import sys

import confy
import tomli
from confy import env
from decouple import Csv, config

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
if os.path.exists(BASE_DIR + "/.env"):
    confy.read_environment_file(BASE_DIR + "/.env")

os.environ.setdefault("BASE_DIR", BASE_DIR)

from ledger_api_client.settings_base import *  # noqa: F403

project = tomli.load(open(os.path.join(BASE_DIR, "pyproject.toml"), "rb"))

WORKING_FROM_HOME = env("WORKING_FROM_HOME", False)

if DEBUG:
    ADMINS = [
        ("Oak McIlwain", "oak.mcilwain@dbca.wa.gov.au"),
        ("Karsten Prehn", "karsten.prehn@dbca.wa.gov.au"),
    ]
else:
    ADMINS = [
        ("ASI", "asi@dpaw.wa.gov.au"),
    ]

ROOT_URLCONF = "leaseslicensing.urls"
SITE_ID = 1
DEPT_DOMAINS = env("DEPT_DOMAINS", ["dpaw.wa.gov.au", "dbca.wa.gov.au"])
SYSTEM_MAINTENANCE_WARNING = env("SYSTEM_MAINTENANCE_WARNING", 24)  # hours
DISABLE_EMAIL = env("DISABLE_EMAIL", False)
SHOW_TESTS_URL = env("SHOW_TESTS_URL", False)
SHOW_DEBUG_TOOLBAR = env("SHOW_DEBUG_TOOLBAR", False)
BUILD_TAG = env(
    "BUILD_TAG", hashlib.md5(os.urandom(32)).hexdigest()
)  # URL of the Dev app.js served by webpack & express
TIME_ZONE = "Australia/Perth"

SILENCE_SYSTEM_CHECKS = env("SILENCE_SYSTEM_CHECKS", False)
if SILENCE_SYSTEM_CHECKS:
    SILENCED_SYSTEM_CHECKS = ["fields.W903", "fields.W904", "debug_toolbar.W004"]


STATIC_URL = "/static/"


INSTALLED_APPS += [
    "reversion",
    "reversion_compare",
    "webtemplate_dbca",
    "ledger_api_client",
    "django_cron",
    "appmonitor_client",
    "leaseslicensing",
    "leaseslicensing.components.main",
    "leaseslicensing.components.organisations",
    "leaseslicensing.components.users",
    "leaseslicensing.components.proposals",
    "leaseslicensing.components.approvals",
    "leaseslicensing.components.compliances",
    "leaseslicensing.components.competitive_processes",
    "leaseslicensing.components.invoicing",
    "leaseslicensing.components.tenure",
    "leaseslicensing.components.texts",
    "rest_framework",
    "rest_framework_datatables",
    "rest_framework_gis",
    "drf_standardized_errors",
    "ckeditor",
    "django_vite",
]

# Not using django cron
INSTALLED_APPS.pop(INSTALLED_APPS.index("django_cron"))

ADD_REVERSION_ADMIN = True

WSGI_APPLICATION = "leaseslicensing.wsgi.application"

INCLUDE_BROWSABLE_API_RENDERER = env("INCLUDE_BROWSABLE_API_RENDERER", False)

if INCLUDE_BROWSABLE_API_RENDERER:
    rest_framework_renderer_classes = (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework_datatables.renderers.DatatablesRenderer",
    )
else:
    rest_framework_renderer_classes = (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework_datatables.renderers.DatatablesRenderer",
    )

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES": rest_framework_renderer_classes,
    "DEFAULT_FILTER_BACKENDS": (
        "rest_framework_datatables.filters.DatatablesFilterBackend",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework_datatables.pagination.DatatablesPageNumberPagination",
    "PAGE_SIZE": 20,
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
}


MIDDLEWARE_CLASSES += [
    "leaseslicensing.middleware.FirstTimeNagScreenMiddleware",
    "leaseslicensing.middleware.CacheControlMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]
MIDDLEWARE = MIDDLEWARE_CLASSES
MIDDLEWARE_CLASSES = None

if SHOW_DEBUG_TOOLBAR:

    def show_toolbar(request):
        if request:
            return True

    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
    INSTALLED_APPS += ("debug_toolbar",)
    INTERNAL_IPS = ("127.0.0.1", "localhost")

    # this dict removes check to dtermine if toolbar should display --> works for rks docker container
    DEBUG_TOOLBAR_CONFIG = {
        # "SHOW_TOOLBAR_CALLBACK": show_toolbar,
        "INTERCEPT_REDIRECTS": False,
    }

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

TEMPLATES[0]["DIRS"].append(os.path.join(BASE_DIR, "leaseslicensing", "templates"))
TEMPLATES[0]["DIRS"].append(
    os.path.join(
        BASE_DIR, "leaseslicensing", "components", "organisations", "templates"
    )
)
TEMPLATES[0]["DIRS"].append(
    os.path.join(BASE_DIR, "leaseslicensing", "components", "emails", "templates")
)
TEMPLATES[0]["OPTIONS"]["context_processors"].append(
    "leaseslicensing.context_processors.leaseslicensing_url"
)

USE_DUMMY_CACHE = env("USE_DUMMY_CACHE", False)
if USE_DUMMY_CACHE:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        },
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
            "LOCATION": os.path.join(BASE_DIR, "leaseslicensing", "cache"),
        },
    }

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles_ll")
STATICFILES_DIRS.extend(
    [
        os.path.join(
            os.path.join(BASE_DIR, "leaseslicensing", "static", "leaseslicensing_vue")
        ),
        os.path.join(os.path.join(BASE_DIR, "leaseslicensing", "static")),
    ]
)

DATA_UPLOAD_MAX_NUMBER_FIELDS = None

# Department details
SYSTEM_NAME = env("SYSTEM_NAME", "Leases and Licensing")
SYSTEM_NAME_SHORT = env("SYSTEM_NAME_SHORT", "LALS")
SITE_PREFIX = env("SITE_PREFIX")
SITE_DOMAIN = env("SITE_DOMAIN")
SITE_SUBDOMAIN_INTERNAL_SUFFIX = env(
    "SITE_SUBDOMAIN_INTERNAL_SUFFIX", "-internal-pvs02"
)

LEASES_LICENSING_EXTERNAL_URL = env("LEASES_LICENSING_EXTERNAL_URL")

DEP_URL = env("DEP_URL", "www." + SITE_DOMAIN)
DEP_PHONE = env("DEP_PHONE", "(08) 9219 9978")
DEP_PHONE_FILMING = env("DEP_PHONE_FILMING", "(08) 9219 8411")
DEP_PHONE_SUPPORT = env("DEP_PHONE_SUPPORT", "(08) 9219 9000")
DEP_FAX = env("DEP_FAX", "(08) 9423 8242")
DEP_POSTAL = env(
    "DEP_POSTAL", "Locked Bag 104, Bentley Delivery Centre, Western Australia 6983"
)
DEP_NAME = env("DEP_NAME", "Department of Biodiversity, Conservation and Attractions")
DEP_NAME_SHORT = env("DEP_NAME_SHORT", "DBCA")
DEP_ABN = env("DEP_ABN", "38052249024")

BRANCH_NAME = env("BRANCH_NAME", "Leases and Licensing Branch")
DEP_ADDRESS = env("DEP_ADDRESS", "17 Dick Perry Avenue, Kensington WA 6151")
SITE_URL = env("SITE_URL", "https://" + SITE_PREFIX + "." + SITE_DOMAIN)
PUBLIC_URL = env("PUBLIC_URL", SITE_URL)
MEDIA_APP_DIR = env("MEDIA_APP_DIR", "leaseslicensing")

# CRON Settings

CRON_RUN_AT_TIMES = env("CRON_RUN_AT_TIMES", "04:05")
CRON_EMAIL = env("CRON_EMAIL", "cron@" + SITE_DOMAIN).lower()
CRON_NOTIFICATION_EMAIL = env("CRON_NOTIFICATION_EMAIL", NOTIFICATION_EMAIL).lower()
CRON_EMAIL_FILE_NAME = "cron_email.log"

DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", "no-reply@" + SITE_DOMAIN).lower()
SUPPORT_EMAIL = env("SUPPORT_EMAIL", "licensing@" + SITE_DOMAIN).lower()
EMAIL_FROM = DEFAULT_FROM_EMAIL
LEASING_FINANCE_NOTIFICATION_EMAIL = env(
    "LEASING_FINANCE_NOTIFICATION_EMAIL", "leasing@dbca.wa.gov.au"
)

OTHER_PAYMENT_ALLOWED = env("OTHER_PAYMENT_ALLOWED", False)  # Cash/Cheque

EMAIL_DELIVERY = env("EMAIL_DELIVERY", "off")
EMAIL_INSTANCE = env("EMAIL_INSTANCE", "DEV")

GIT_COMMIT_HASH = os.popen(
    f"cd {BASE_DIR}; git log -1 --format=%H"
).read()  # noqa: S605
GIT_COMMIT_DATE = os.popen(
    f"cd {BASE_DIR}; git log -1 --format=%cd"
).read()  # noqa: S605

APPLICATION_VERSION = project["tool"]["poetry"]["version"] + "-" + GIT_COMMIT_HASH[:7]

RUNNING_DEVSERVER = len(sys.argv) > 1 and sys.argv[1] == "runserver"

# Sentry settings
SENTRY_DSN = env("SENTRY_DSN", default=None)
SENTRY_SAMPLE_RATE = env("SENTRY_SAMPLE_RATE", default=1.0)  # Error sampling rate
SENTRY_TRANSACTION_SAMPLE_RATE = env(
    "SENTRY_TRANSACTION_SAMPLE_RATE", default=0.0
)  # Transaction sampling
if not RUNNING_DEVSERVER and SENTRY_DSN and EMAIL_INSTANCE:
    import sentry_sdk

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        sample_rate=SENTRY_SAMPLE_RATE,
        traces_sample_rate=SENTRY_TRANSACTION_SAMPLE_RATE,
        environment=EMAIL_INSTANCE.lower(),
        release=APPLICATION_VERSION,
    )

OSCAR_BASKET_COOKIE_OPEN = "leaseslicensing_basket"
PAYMENT_SYSTEM_ID = env("PAYMENT_SYSTEM_ID", "S675")
PAYMENT_SYSTEM_PREFIX = env(
    "PAYMENT_SYSTEM_PREFIX", PAYMENT_SYSTEM_ID.replace("S", "0")
)  # '0675'
os.environ["LEDGER_PRODUCT_CUSTOM_FIELDS"] = (
    "('ledger_description','quantity','price_incl_tax','price_excl_tax','oracle_code')"
)

LEDGER_DEFAULT_LINE_STATUS = 1

TEST_ORACLE_CODE = env("TEST_ORACLE_CODE", "LEASES_LICENSING_TEST_ORACLE_CODE")

if not VALID_SYSTEMS:
    VALID_SYSTEMS = [PAYMENT_SYSTEM_ID]

CRON_CLASSES = [
    "appmonitor_client.cron.CronJobAppMonitorClient",
    "ledger_api_client.cron.CronJobLedgerTotals",
]

PROTECTED_MEDIA_ROOT = env(
    "PROTECTED_MEDIA_ROOT", os.path.join(BASE_DIR, "protected_media")
)
SECURE_FILE_API_BASE_PATH = "/api/main/secure_file/"
SECURE_DOCUMENT_API_BASE_PATH = "/api/main/secure_document/"

# This is needed so that the chmod is not called in django/core/files/storage.py
# (_save method of FileSystemStorage class)
# As it causes a permission exception when using azure network drives
FILE_UPLOAD_PERMISSIONS = None

BASE_URL = env("BASE_URL")

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 300,
        # 'width': 300,
        "width": "100%",
    },
    "awesome_ckeditor": {
        "toolbar": "Basic",
    },
    "toolbar_minimal": {
        "toolbar": "Custom",
        "toolbar_Custom": [
            ["Bold", "Italic", "Underline"],
            [
                "BulletedList",
                "NumberedList",
                "-",
                "Outdent",
                "Indent",
                "-",
                "Image",
                "Blockquote",
                "Table",
                "MediaEmbed",
                "-",
                "Undo",
                "Redo",
                "-",
                "JustifyLeft",
                "JustifyCenter",
                "JustifyRight",
                "JustifyBlock",
            ],
            ["Link", "Unlink"],
            ["RemoveFormat", "Source"],
        ],
    },
}


CONSOLE_EMAIL_BACKEND = env("CONSOLE_EMAIL_BACKEND", False)
if CONSOLE_EMAIL_BACKEND:
    # EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    EMAIL_BACKEND = "wagov_utils.components.utils.email_backend.EmailBackend"


# Add a debug level logger for development
if DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(name)s [Line:%(lineno)s][%(funcName)s] %(message)s"
            },
            "simple": {
                "format": "[Line:%(lineno)s][%(funcName)s] %(levelname)s %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
            },
            "leaseslicensing_rotating_file": {
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(BASE_DIR, "logs", "leaseslicensing.log"),
                "formatter": "verbose",
                "maxBytes": 5242880,
            },
            "mail_admins": {
                "level": "CRITICAL",
                "class": "django.utils.log.AdminEmailHandler",
                "include_html": True,
            },
        },
        "loggers": {
            "leaseslicensing": {
                "handlers": ["console", "leaseslicensing_rotating_file", "mail_admins"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }
else:
    # Additional logging for leaseslicensing
    LOGGING["handlers"]["payment_checkout"] = {
        "level": "INFO",
        "class": "logging.handlers.RotatingFileHandler",
        "filename": os.path.join(
            BASE_DIR, "logs", "leaseslicensing_payment_checkout.log"
        ),
        "formatter": "verbose",
        "maxBytes": 5242880,
    }
    LOGGING["loggers"]["payment_checkout"] = {
        "handlers": ["payment_checkout"],
        "level": "INFO",
    }
    # Add a handler
    LOGGING["handlers"]["file_leaseslicensing"] = {
        "level": "INFO",
        "class": "logging.handlers.RotatingFileHandler",
        "filename": os.path.join(BASE_DIR, "logs", "leaseslicensing.log"),
        "formatter": "verbose",
        "maxBytes": 5242880,
    }
    LOGGING["loggers"]["leaseslicensing"] = {
        "handlers": ["file_leaseslicensing"],
        "level": "INFO",
    }

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

PROPOSAL_TYPE_NEW = "new"
PROPOSAL_TYPE_RENEWAL = "renewal"
PROPOSAL_TYPE_AMENDMENT = "amendment"
PROPOSAL_TYPE_TRANSFER = "transfer"
PROPOSAL_TYPE_MIGRATION = "migration"
PROPOSAL_TYPES = [
    (PROPOSAL_TYPE_NEW, "New Proposal"),
    (PROPOSAL_TYPE_AMENDMENT, "Amendment"),
    (PROPOSAL_TYPE_RENEWAL, "Renewal"),
    (PROPOSAL_TYPE_TRANSFER, "Transfer"),
    (PROPOSAL_TYPE_MIGRATION, "Migration"),
]

APPLICATION_TYPE_REGISTRATION_OF_INTEREST = "registration_of_interest"
APPLICATION_TYPE_LEASE_LICENCE = "lease_licence"
APPLICATION_TYPES = [
    (APPLICATION_TYPE_REGISTRATION_OF_INTEREST, "Registration of Interest"),
    (APPLICATION_TYPE_LEASE_LICENCE, "Lease Licence"),
]
KMI_SERVER_URL = env("KMI_SERVER_URL", "https://kmi.dbca.wa.gov.au")
GIS_SERVER_URL = env(
    "GIS_SERVER_URL", "https://kaartdijin-boodja-geoserver.dbca.wa.gov.au"
)
GIS_LANDS_AND_WATERS_LAYER_NAME = env(
    "GIS_LANDS_AND_WATERS_LAYER_NAME",
    "kaartdijin-boodja-public:CPT_DBCA_LEGISLATED_TENURE",
)
GIS_INVERT_XY = env("GIS_INVERT_XY", True)

ABS_API_URL = env("ABS_API_URL", "https://api.data.abs.gov.au")
ABS_API_CPI_SUBDIRECTORY = env("ABD_API_CPI_PATH", "/data/CPI/")
ABS_API_CPI_PATH = env("ABD_API_CPI_PATH", "3.10001.10.5.Q")

KMI_AUTH_USERNAME = env("KMI_AUTH_USERNAME")
KMI_AUTH_PASSWORD = env("KMI_AUTH_PASSWORD")

APPROVAL_RENEWAL_DAYS_PRIOR_TO_EXPIRY = env("APPROVAL_RENEWAL_DAYS_PRIOR_TO_EXPIRY", 90)

DEFAULT_DAYS_BEFORE_PAYMENT_DUE = env(
    "DEFAULT_DAYS_BEFORE_PAYMENT_DUE", 30
)  # Net 30 Payment terms

DAYS_BEFORE_NEXT_INVOICING_PERIOD_TO_GENERATE_INVOICE_RECORD = env(
    "DAYS_BEFORE_NEXT_INVOICING_PERIOD_TO_GENERATE_INVOICE_RECORD", 30
)

CUSTOM_CPI_REMINDER_DAYS_PRIOR_TO_INVOICE_ISSUE_DATE = env(
    "CUSTOM_CPI_REMINDER_DAYS_PRIOR_TO_INVOICE_ISSUE_DATE", (30, 15)
)
MAX_ATTEMPTS_TO_SEND_INVOICE_NOTIFICATION_EMAIL = env(
    "MAX_ATTEMPTS_TO_SEND_INVOICE_NOTIFICATION_EMAIL", 5
)

PERCENTAGE_OF_GROSS_TURNOVER_REMINDERS_DAYS_PRIOR = env(
    "PERCENTAGE_OF_GROSS_TURNOVER_REMINDERS_DAYS_PRIOR", [30, 15]
)

COMPLIANCES_DAYS_PRIOR_TO_SEND_REMINDER = env(
    "COMPLIANCES_DAYS_PRIOR_TO_SEND_REMINDER", 14
)

template_title = "Leases and Licensing"
template_header_logo = "/static/leaseslicensing/img/leases_and_licensing_dbca_logo.png"
template_group = "parkswildlifev2"

LEDGER_TEMPLATE = "bootstrap5"
LEDGER_UI_ACCOUNTS_MANAGEMENT = [
    {"first_name": {"options": {"view": True, "edit": True}}},
    {"last_name": {"options": {"view": True, "edit": True}}},
    {"residential_address": {"options": {"view": True, "edit": True}}},
    {"postal_same_as_residential": {"options": {"view": True, "edit": True}}},
    {"postal_address": {"options": {"view": True, "edit": True}}},
    {"phone_number": {"options": {"view": True, "edit": True}}},
    {"mobile_number": {"options": {"view": True, "edit": True}}},
]
LEDGER_UI_CARDS_MANAGEMENT = True

ADMIN_GROUP = env("ADMIN_GROUP", "Leases and Licensing Admin")

GROUP_NAME_ASSESSOR = "proposal_assessor_group"
GROUP_NAME_APPROVER = "proposal_approver_group"
GROUP_NAME_ORGANISATION_ACCESS = "organisation_access_group"
GROUP_COMPETITIVE_PROCESS_EDITOR = "competitive_process_editor"
GROUP_FINANCE = "finance"

GROUP_NAME_CHOICES = (
    (GROUP_NAME_ASSESSOR, "Proposal Assessor Group"),
    (GROUP_NAME_APPROVER, "Proposal Approver Group"),
    (GROUP_NAME_ORGANISATION_ACCESS, "Organisation Access Group"),
    (GROUP_COMPETITIVE_PROCESS_EDITOR, "Competitive Process Editor"),
    (GROUP_FINANCE, "Finance"),
)

CHARGE_METHOD_ONCE_OFF_CHARGE = "once_off_charge"
CHARGE_METHOD_BASE_FEE_PLUS_FIXED_ANNUAL_INCREMENT = (
    "base_fee_plus_fixed_annual_increment"
)
CHARGE_METHOD_BASE_FEE_PLUS_FIXED_ANNUAL_PERCENTAGE = (
    "base_fee_plus_fixed_annual_percentage"
)
CHARGE_METHOD_BASE_FEE_PLUS_ANNUAL_CPI = "base_fee_plus_annual_cpi"
CHARGE_METHOD_BASE_FEE_PLUS_ANNUAL_CPI_CUSTOM = "base_fee_plus_annual_cpi_custom"
CHARGE_METHOD_PERCENTAGE_OF_GROSS_TURNOVER_IN_ARREARS = "percentage_of_gross_turnover"
CHARGE_METHOD_PERCENTAGE_OF_GROSS_TURNOVER_IN_ADVANCE = (
    "percentage_of_gross_turnover_in_advance"
)
CHARGE_METHOD_NO_RENT_OR_LICENCE_CHARGE = "no_rent_or_licence_charge"
CHARGE_METHODS = (
    (CHARGE_METHOD_NO_RENT_OR_LICENCE_CHARGE, "No Charge"),
    (CHARGE_METHOD_ONCE_OFF_CHARGE, "Once-off Charge"),
    (
        CHARGE_METHOD_BASE_FEE_PLUS_FIXED_ANNUAL_INCREMENT,
        "Base Fee Plus Fixed Annual Increment",
    ),
    (
        CHARGE_METHOD_BASE_FEE_PLUS_FIXED_ANNUAL_PERCENTAGE,
        "Base Fee Plus Fixed Annual Percentage",
    ),
    (
        CHARGE_METHOD_BASE_FEE_PLUS_ANNUAL_CPI_CUSTOM,
        "Base Fee Plus Annual CPI (Custom)",
    ),
    (CHARGE_METHOD_BASE_FEE_PLUS_ANNUAL_CPI, "Base Fee Plus Annual CPI (ABS)"),
    (
        CHARGE_METHOD_PERCENTAGE_OF_GROSS_TURNOVER_IN_ARREARS,
        "Percentage of Gross Turnover (Arrears)",
    ),
    (
        CHARGE_METHOD_PERCENTAGE_OF_GROSS_TURNOVER_IN_ADVANCE,
        "Percentage of Gross Turnover (Advance)",
    ),
)

CHARGE_METHODS_REQUIRING_CROWN_LAND_RENT_REVIEW = [
    CHARGE_METHOD_BASE_FEE_PLUS_ANNUAL_CPI_CUSTOM,
    CHARGE_METHOD_BASE_FEE_PLUS_ANNUAL_CPI,
    CHARGE_METHOD_BASE_FEE_PLUS_FIXED_ANNUAL_INCREMENT,
    CHARGE_METHOD_BASE_FEE_PLUS_FIXED_ANNUAL_PERCENTAGE,
]

REPETITION_TYPE_ANNUALLY = "annually"
REPETITION_TYPE_QUARTERLY = "quarterly"
REPETITION_TYPE_MONTHLY = "monthly"
REPETITION_TYPES = (
    (REPETITION_TYPE_ANNUALLY, "Year"),
    (REPETITION_TYPE_QUARTERLY, "Quarter"),
    (REPETITION_TYPE_MONTHLY, "Month"),
)

LATEST_REFERRAL_COUNT = 5

SOURCE_CHOICE_APPLICANT = "proponent"
SOURCE_CHOICE_ASSESSOR = "assessor"
SOURCE_CHOICE_COMPETITIVE_PROCESS_EDITOR = "competitive_process_editor"
SOURCE_CHOICES = (
    (SOURCE_CHOICE_APPLICANT, "Proponent"),
    (SOURCE_CHOICE_ASSESSOR, "Assessor"),
    (SOURCE_CHOICE_COMPETITIVE_PROCESS_EDITOR, "Competitive Process Editor"),
)


APPROVE_LEASE_LICENCE = "approve_lease_licence"
APPROVE_COMPETITIVE_PROCESS = "approve_competitive_process"
APPROVE_ADD_TO_EXISTING_COMPETITIVE_PROCESS = (
    "approve_add_to_existing_competitive_process"
)

# ---------- Standard Requirements ----------

INVOICING_PERCENTAGE_GROSS_TURNOVER_ANNUALLY = (
    "invoicing_percentage_gross_turnover_annually"
)
INVOICING_PERCENTAGE_GROSS_TURNOVER_QUARTERLY = (
    "invoicing_percentage_gross_turnover_quarterly"
)
INVOICING_PERCENTAGE_GROSS_TURNOVER_MONTHLY = (
    "invoicing_percentage_gross_turnover_monthly"
)

# ---------- CPI Calculation Methods ----------

CPI_CALCULATION_METHOD_LATEST_SEP_QUARTER = "latest_sep_qtr"
CPI_CALCULATION_METHOD_LATEST_DEC_QUARTER = "latest_dec_qtr"
CPI_CALCULATION_METHOD_LATEST_MAR_QUARTER = "latest_mar_qtr"
CPI_CALCULATION_METHOD_LATEST_JUN_QUARTER = "latest_jun_qtr"
CPI_CALCULATION_METHOD_LATEST_QUARTER = "latest_qtr"
CPI_CALCULATION_METHOD_AVERAGE_LATEST_FOUR_QUARTERS = "average_latest_four_qtrs"

CPI_CALCULATION_METHODS = (
    (CPI_CALCULATION_METHOD_LATEST_SEP_QUARTER, "Latest September Quarter"),
    (CPI_CALCULATION_METHOD_LATEST_DEC_QUARTER, "Latest December Quarter"),
    (CPI_CALCULATION_METHOD_LATEST_MAR_QUARTER, "Latest March Quarter"),
    (CPI_CALCULATION_METHOD_LATEST_JUN_QUARTER, "Latest June Quarter"),
    (CPI_CALCULATION_METHOD_LATEST_QUARTER, "Latest Quarter"),
    (
        CPI_CALCULATION_METHOD_AVERAGE_LATEST_FOUR_QUARTERS,
        "Average of Latest Four Quarters",
    ),
)


# ---------- Identifier fields for logging ----------

""" Fields that the logging functions will check for on the instance
    and use to identify the instance in the logs. """
ACTION_LOGGING_IDENTIFIER_FIELDS = [
    "lodgement_number",
    "id",
]

# ---------- Cache Timeouts ----------

LOV_CACHE_TIMEOUT = 60 * 60 * 3  # 3 hours

CACHE_TIMEOUT_5_SECONDS = 5
CACHE_TIMEOUT_10_SECONDS = 10
CACHE_TIMEOUT_1_MINUTE = 60
CACHE_TIMEOUT_5_MINUTES = 60 * 5
CACHE_TIMEOUT_2_HOURS = 60 * 60 * 2
CACHE_TIMEOUT_24_HOURS = 60 * 60 * 24
CACHE_TIMEOUT_NEVER = None

# ---------- Cache Keys ----------

CACHE_KEY_DBCA_LEDGER_ORGANISATION = "dbca_ledger_organisation"
CACHE_KEY_DEFAULT_FROM_EMAIL = "default-from-email"
CACHE_KEY_LEDGER_EMAIL_USER = "ledger-emailuser-{}"
CACHE_KEY_LEDGER_ORGANISATION = "ledger-organisation-{}"
CACHE_KEY_ORGANISATION_IDS = "cache_organisation_ids"
CACHE_KEY_ORGANISATIONS = "cache_organisations"
CACHE_KEY_USER_IDS = "cache_user_ids"
CACHE_KEY_COUNTRY_LIST = "country_list"
CACHE_KEY_APPROVAL_STATUSES = "approval_statuses_dict"
CACHE_KEY_APPLICATION_TYPE_DICT_FOR_FILTER = "application_type_dict_for_filter"
CACHE_KEY_APPLICATION_TYPE_DICT = "application_type_dict"
CACHE_KEY_APPLICATION_STATUSES_DICT_INTERNAL = "application_internal_statuses_dict"
CACHE_KEY_APPLICATION_STATUSES_DICT_EXTERNAL = "application_external_statuses_dict"
CACHE_KEY_APPLICATION_STATUSES_DICT_FOR_FILTER = (
    "application_internal_statuses_dict_for_filter"
)
CACHE_KEY_DBCA_LEGISLATED_LANDS_AND_WATERS = "dbca_legislated_lands_and_waters"
CACHE_KEY_MAP_PROPOSALS = "map-proposals"
CACHE_KEY_LODGEMENT_NUMBER_PREFIXES = "lodgement_number_prefixes"
CACHE_KEY_APPROVAL_TYPES_DICTIONARY = "approval-types-dictionary"

# ---------- User Log Actions ----------

ACTION_VIEW = "View {} {}"
ACTION_CREATE = "Create {} {}"
ACTION_UPDATE = "Update {} {}"
ACTION_DESTROY = "Destroy {} {}"

# ---------- Error messages -------------

# When debug is False, the following message will be sent to the user
# The real exception will be logged
API_EXCEPTION_MESSAGE = (
    "An error occurred while processing your request, "
    f"please try again and if the problem persists contact {SUPPORT_EMAIL}"
)

# Make sure this returns true when in local development
# so you can use the vite dev server with hot module reloading
USE_VITE_DEV_SERVER = RUNNING_DEVSERVER and EMAIL_INSTANCE == "DEV" and DEBUG is True

STATIC_URL_PREFIX = (
    "/static/leaseslicensing_vue/" if USE_VITE_DEV_SERVER else "leaseslicensing_vue/"
)

DJANGO_VITE = {
    "default": {
        "dev_mode": USE_VITE_DEV_SERVER,
        "dev_server_host": "localhost",  # Default host for vite (can change if needed)
        "dev_server_port": config("DEV_SERVER_PORT", default=9072, cast=int),  # Default port for vite (can change if needed)
        "static_url_prefix": STATIC_URL_PREFIX,
    }
}

VUE3_ENTRY_SCRIPT = env(
    "VUE3_ENTRY_SCRIPT",
    default="src/main.js",  # This path will be auto prefixed with the       static_url_prefix from DJANGO_VITE above
)  # Path of the vue3 entry point script served by vite

SECURE_CROSS_ORIGIN_OPENER_POLICY = env(
    "SECURE_CROSS_ORIGIN_OPENER_POLICY",
    "same-origin",
)

# Set USE_X_FORWARDED_HOST env to True to ensure that if the request is https
# then urls generated for file fields are also https
USE_X_FORWARDED_HOST = env("USE_X_FORWARDED_HOST", False)
if USE_X_FORWARDED_HOST:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INCLUDE_ROOT_VIEW = env("INCLUDE_ROOT_VIEW", False)

CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="", cast=Csv())
