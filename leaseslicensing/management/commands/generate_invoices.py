import logging
import traceback
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.db.models import Q
from django.utils import timezone

from leaseslicensing.components.approvals.models import Approval
from leaseslicensing.components.invoicing.email import (
    send_new_invoice_raised_internal_notification,
)
from leaseslicensing.components.invoicing.models import Invoice, ScheduledInvoice
from leaseslicensing.components.proposals.models import Proposal

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "This script is designed to run as a daily cron job and generate any invoices that need to be issued"

    def add_arguments(self, parser):
        parser.add_argument(
            "--test",
            action="store_true",
            help=(
                "Adding the test flag will prevent database objects being saved "
                "and emails being sent and will instead just output messages."
            ),
        )
        parser.add_argument(
            "--test_date",
            type=str,
            help="Test date (YYYY-MM-DD) to use instead of today",
        )

    def handle(self, *args, **options):
        logger.info(f"Running command {__name__}")

        testing = options["test"]

        today = timezone.localtime(timezone.now()).date()
        if options["test_date"]:
            logger.info(f"Using test date {options['test_date']} instead of today")
            today = datetime.strptime(options["test_date"], "%Y-%m-%d").date()

        scheduled_invoices = ScheduledInvoice.objects.filter(
            Q(invoice__isnull=True)
            | (
                Q(notification_email_sent=False)
                & Q(
                    attempts_to_send_notification_email__lte=settings.MAX_ATTEMPTS_TO_SEND_INVOICE_NOTIFICATION_EMAIL
                    - 1
                )
            ),
            invoicing_details__proposal__approval__status__in=Approval.CURRENT_APPROVAL_STATUSES,
            invoicing_details__proposal__processing_status=Proposal.PROCESSING_STATUS_APPROVED,
            date_to_generate__lte=today,
        )
        scheduled_invoice_count = scheduled_invoices.count()
        logger.info(
            f"Found {scheduled_invoice_count} scheduled invoices that need generation "
            f"and or notification today({today})"
        )

        invoices_generated = []
        for scheduled_invoice in scheduled_invoices:
            logger.info(f"Processing scheduled invoice {scheduled_invoice.id}")
            if not hasattr(scheduled_invoice, "invoice"):
                try:
                    self.generate_invoice(
                        scheduled_invoice, invoices_generated, test=testing
                    )

                except (TypeError, IntegrityError) as e:
                    logger.exception(
                        f"Failed to generate invoice from scheduled invoice {scheduled_invoice.id}: {e}"
                        f"\n{traceback.format_exc()}"
                    )
                    continue

            if testing:
                logger.info(
                    "Test mode - Invoice email nofitication would have been sent to proponent and finance group"
                )
                continue

            if (
                hasattr(scheduled_invoice, "invoice")
                and not scheduled_invoice.notification_email_sent
            ):
                # send to the applicant and cc finance officer
                msg = send_new_invoice_raised_internal_notification(
                    scheduled_invoice.invoice
                )
                scheduled_invoice.attempts_to_send_notification_email += 1
                if msg:
                    scheduled_invoice.notification_email_sent = True
                else:
                    if (
                        scheduled_invoice.attempts_to_send_notification_email
                        >= settings.MAX_ATTEMPTS_TO_SEND_INVOICE_NOTIFICATION_EMAIL
                    ):
                        logger.error(
                            f"Failed to send email notification for invoice {scheduled_invoice.invoice.id} "
                            f"after {settings.MAX_ATTEMPTS_TO_SEND_INVOICE_NOTIFICATION_EMAIL} "
                            "attempts. Will not attempt again."
                        )
                    else:
                        logger.error(
                            f"Failed to send email notification for invoice {scheduled_invoice.invoice.id}"
                        )

                scheduled_invoice.save()

        if scheduled_invoice_count > 0:
            logger.info(f"Generated the following invoices {invoices_generated}")
        logger.info(f"Finished running command {__name__}")

    def generate_invoice(self, scheduled_invoice, invoices_generated, test=False):
        invoicing_details = scheduled_invoice.invoicing_details
        logger.info(
            f"\tGenerating Invoice for Approval: {invoicing_details.approval} from schedule: {scheduled_invoice.id}"
        )
        approval = invoicing_details.approval
        preview_invoice = invoicing_details.preview_invoice_by_original_issue_date(
            scheduled_invoice.date_to_generate
        )
        if not preview_invoice:
            logger.warning(
                f"preview_invoice_by_date returned None for {scheduled_invoice.date_to_generate} "
                f"(Approval: {approval.lodgement_number}, Scheduled Invoice: {scheduled_invoice.id})"
            )
            return

        amount = preview_invoice["amount_object"]["amount"]

        invoice, created = Invoice.objects.get_or_create(
            approval=approval,
            amount=amount,
            gst_free=approval.approval_type.gst_free,
            scheduled_invoice=scheduled_invoice,
        )
        if not created:
            logger.warning(
                f"\tPossible duplication attempt. Invoice {invoice.lodgement_number} "
                f"already exists for Approval: {approval.lodgement_number}"
            )
            return

        if test:
            logger.info(f"Test mode - Invoice record would be generated: {invoice}")
            return

        invoice.save()

        logger.info(
            self.style.SUCCESS(f"\tGenerated Invoice: {invoice.lodgement_number}\n")
        )

        invoices_generated.append(invoice)

        return invoice
