import logging

from django.db import migrations
from django.core.management import call_command


logger = logging.getLogger(__name__)


fixtures_path = "leaseslicensing/components/approvals/fixtures/"


def load_approvaltype(apps, schema_editor):
    call_command("loaddata", fixtures_path + "approvaltype.json", verbosity=0)


def load_approvaltypedocumenttype(apps, schema_editor):
    call_command(
        "loaddata", fixtures_path + "approvaltypedocumenttype.json", verbosity=0
    )


def load_approvaltypedocumenttypeonapprovaltype(apps, schema_editor):
    call_command(
        "loaddata",
        fixtures_path + "approvaltypedocumenttypeonapprovaltype.json",
        verbosity=0,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("leaseslicensing", "0157_delete_approvalsubtype"),
    ]

    operations = [
        # Comment out as it's best to run these commands manually since the
        # structure of the data changes over time and the fixtures may not
        # be compatible with the current state of the database at this point in time.
        # migrations.RunPython(load_approvaltype, atomic=True),
        # migrations.RunPython(load_approvaltypedocumenttype, atomic=True),
        # migrations.RunPython(load_approvaltypedocumenttypeonapprovaltype, atomic=True)
    ]
