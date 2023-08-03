import logging

from django.conf import settings
from django.urls import reverse
from ledger_api_client.ledger_models import EmailUserRO as EmailUser

from leaseslicensing.components.approvals.email import (
    _log_approval_email,
    _log_org_email,
    _log_user_email,
)
from leaseslicensing.components.emails.emails import TemplateEmailBase
from leaseslicensing.helpers import emails_list_for_group

logger = logging.getLogger(__name__)

SYSTEM_NAME = settings.SYSTEM_NAME_SHORT + " Automated Message"


def send_new_invoice_raised_notification(request, approval, invoice):
    email = TemplateEmailBase(
        subject=f"New Invoice Ready for {approval.approval_type} {approval.lodgement_number}",
        html_template="leaseslicensing/emails/invoicing/send_new_invoice_raised_notification.html",
        txt_template="leaseslicensing/emails/invoicing/send_new_invoice_raised_notification.txt",
    )
    logger.debug(reverse("external-invoices"))
    external_invoices_url = request.build_absolute_uri(reverse("external-invoices"))

    pay_now_url = request.build_absolute_uri(
        reverse("external-pay-invoice", kwargs={"pk": invoice.id})
    )

    context = {
        "approval": approval,
        "invoice": invoice,
        "external_invoices_url": external_invoices_url,
        "pay_now_url": pay_now_url,
    }
    proposal = approval.current_proposal
    recipients = proposal.applicant_emails
    finance_group_member_emails = emails_list_for_group(settings.GROUP_FINANCE)
    finance_group_member_emails.append(settings.LEASING_FINANCE_NOTIFICATION_EMAIL)
    msg = email.send(recipients, cc=finance_group_member_emails, context=context)

    sender = settings.DEFAULT_FROM_EMAIL
    sender_user = EmailUser.objects.get(email=sender)

    if approval.org_applicant:
        _log_org_email(
            msg, approval.org_applicant, proposal.submitter, sender=sender_user
        )
    else:
        _log_user_email(msg, approval.submitter, proposal.submitter, sender=sender_user)

    _log_approval_email(msg, approval, sender=sender_user)


def send_new_invoice_raised_internal_notification(approval, invoice):
    email = TemplateEmailBase(
        subject=f"New Invoice Record Generated for {approval.approval_type} {approval.lodgement_number}",
        html_template="leaseslicensing/emails/invoicing/send_new_invoice_raised_internal_notification.html",
        txt_template="leaseslicensing/emails/invoicing/send_new_invoice_raised_internal_notification.txt",
    )
    internal_invoices = reverse(
        "internal-invoices",
    )
    internal_invoices_url = (
        f"{settings.LEASES_LICENSING_EXTERNAL_URL}{internal_invoices}"
    )

    context = {
        "approval": approval,
        "invoice": invoice,
        "internal_invoices_url": internal_invoices_url,
    }

    finance_group_member_emails = emails_list_for_group(settings.GROUP_FINANCE)
    msg = email.send(
        finance_group_member_emails,
        cc=[settings.LEASING_FINANCE_NOTIFICATION_EMAIL],
        context=context,
    )

    sender = settings.DEFAULT_FROM_EMAIL
    sender_user = EmailUser.objects.get(email=sender)

    _log_approval_email(msg, approval, sender=sender_user)