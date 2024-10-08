import logging

from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.urls import reverse
from django.utils.encoding import smart_str
from ledger_api_client.ledger_models import EmailUserRO as EmailUser

from leaseslicensing.components.emails.emails import TemplateEmailBase
from leaseslicensing.components.organisations.models import (
    Organisation,
    OrganisationLogEntry,
)
from leaseslicensing.helpers import (
    convert_internal_url_to_external_url,
    emails_list_for_group,
)
from leaseslicensing.ledger_api_utils import retrieve_email_user

logger = logging.getLogger(__name__)

SYSTEM_NAME = settings.SYSTEM_NAME_SHORT + " Automated Message"


class ApprovalExpireNotificationEmail(TemplateEmailBase):
    def __init__(self):
        super().__init__()
        self.subject = f"{settings.DEP_NAME} - Lease or Licence has expired."
        self.html_template = "leaseslicensing/emails/approval_expire_notification.html"
        self.txt_template = "leaseslicensing/emails/approval_expire_notification.txt"


class ApprovalCancelNotificationEmail(TemplateEmailBase):
    def __init__(self):
        super().__init__()
        self.subject = f"{settings.DEP_NAME} - Lease or Licence has been cancelled."
        self.html_template = "leaseslicensing/emails/approval_cancel_notification.html"
        self.txt_template = "leaseslicensing/emails/approval_cancel_notification.txt"


class ApprovalSuspendNotificationEmail(TemplateEmailBase):
    def __init__(self):
        super().__init__()
        self.subject = f"{settings.DEP_NAME} - Lease or Licence has been suspended."
        self.html_template = "leaseslicensing/emails/approval_suspend_notification.html"
        self.txt_template = "leaseslicensing/emails/approval_suspend_notification.txt"


class ApprovalSurrenderNotificationEmail(TemplateEmailBase):
    def __init__(self):
        super().__init__()
        self.subject = "{} - Lease or Licence has been surrendered.".format(
            settings.DEP_NAME
        )
        self.html_template = (
            "leaseslicensing/emails/approval_surrender_notification.html"
        )
        self.txt_template = "leaseslicensing/emails/approval_surrender_notification.txt"


class ApprovalReinstateNotificationEmail(TemplateEmailBase):
    def __init__(self):
        super().__init__()
        self.subject = f"{settings.DEP_NAME} - Lease or Licence has been reinstated."
        self.html_template = (
            "leaseslicensing/emails/approval_reinstate_notification.html"
        )
        self.txt_template = "leaseslicensing/emails/approval_reinstate_notification.txt"


class ApprovalRenewalReviewNotificationEmail(TemplateEmailBase):
    def __init__(self):
        super().__init__()
        self.subject = (
            f"{settings.DEP_NAME} - Lease or Licence requires renewal decision."
        )
        self.html_template = (
            "leaseslicensing/emails/approval_renewal_review_notification.html"
        )
        self.txt_template = (
            "leaseslicensing/emails/approval_renewal_review_notification.txt"
        )


class ApprovalRenewalNotificationEmail(TemplateEmailBase):
    def __init__(self):
        super().__init__()
        self.subject = f"{settings.DEP_NAME} - Lease or Licence ready for renewal."
        self.html_template = "leaseslicensing/emails/approval_renewal_notification.html"
        self.txt_template = "leaseslicensing/emails/approval_renewal_notification.txt"


class ApprovalTransferHolderNotificationEmail(TemplateEmailBase):
    def __init__(self):
        super().__init__()
        self.subject = (
            f"{settings.DEP_NAME} - Lease or Licence transfer has been initiated."
        )
        self.html_template = (
            "leaseslicensing/emails/approval_transfer_holder_notification.html"
        )
        self.txt_template = (
            "leaseslicensing/emails/approval_transfer_holder_notification.txt"
        )


class ApprovalTransferTransfereeNotificationEmail(TemplateEmailBase):
    def __init__(self):
        super().__init__()
        self.subject = f"{settings.DEP_NAME} - Lease or Licence transfer proposal ready for actioning."
        self.html_template = (
            "leaseslicensing/emails/approval_transfer_transferee_notification.html"
        )
        self.txt_template = (
            "leaseslicensing/emails/approval_transfer_transferee_notification.txt"
        )


def send_approval_expire_email_notification(approval):
    email = ApprovalExpireNotificationEmail()
    proposal = approval.current_proposal

    url = settings.SITE_URL if settings.SITE_URL else ""
    url += reverse("external")

    url = convert_internal_url_to_external_url(url)

    context = {"approval": approval, "proposal": proposal, "url": url}
    all_ccs = []
    if proposal.org_applicant and proposal.org_applicant.email:
        cc_list = proposal.org_applicant.email
        if cc_list:
            all_ccs = [cc_list]
    msg = email.send(proposal.submitter_obj.email, cc=all_ccs, context=context)
    sender = settings.DEFAULT_FROM_EMAIL
    try:
        sender_user = EmailUser.objects.get(email__icontains=sender)
    except EmailUser.DoesNotExist:
        EmailUser.objects.create(email=sender, password="")
        sender_user = EmailUser.objects.get(email__icontains=sender)

    _log_approval_email(msg, approval, sender=sender_user)
    # _log_org_email(msg, approval.applicant, proposal.submitter, sender=sender_user)
    if approval.is_org_applicant:
        _log_org_email(msg, approval.applicant, proposal.submitter, sender=sender_user)
    else:
        _log_user_email(msg, approval.submitter, proposal.submitter, sender=sender_user)


def send_approval_cancel_email_notification(approval):
    email = ApprovalCancelNotificationEmail()
    proposal = approval.current_proposal

    context = {
        "approval": approval,
    }
    sender = settings.DEFAULT_FROM_EMAIL
    try:
        sender_user = EmailUser.objects.get(email__icontains=sender)
    except EmailUser.DoesNotExist:
        EmailUser.objects.create(email=sender, password="")
        sender_user = EmailUser.objects.get(email__icontains=sender)
    all_ccs = []
    if proposal.org_applicant and proposal.org_applicant.email:
        cc_list = proposal.org_applicant.ledger_organisation_email
        if cc_list:
            all_ccs = [cc_list]
    submitter_obj = retrieve_email_user(proposal.submitter)
    msg = email.send(submitter_obj.email, cc=all_ccs, context=context)
    sender = settings.DEFAULT_FROM_EMAIL
    _log_approval_email(msg, approval, sender=sender_user)
    # _log_org_email(msg, approval.applicant, proposal.submitter, sender=sender_user)
    if approval.is_org_applicant:
        _log_org_email(msg, approval.applicant, proposal.submitter, sender=sender_user)
    else:
        _log_user_email(msg, approval.submitter, proposal.submitter, sender=sender_user)


def send_approval_suspend_email_notification(approval, request=None):
    email = ApprovalSuspendNotificationEmail()
    proposal = approval.current_proposal

    if request and "test-emails" in request.path_info:
        details = "This are my test details"
        from_date = "01/01/1970"
        to_date = "01/01/2070"
    else:
        details = approval.suspension_details["details"]
        from_date = approval.suspension_details["from_date"]
        to_date = approval.suspension_details["to_date"]

    context = {
        "approval": approval,
        "details": details,
        "from_date": from_date,
        "to_date": to_date,
    }
    sender = settings.DEFAULT_FROM_EMAIL
    try:
        sender_user = EmailUser.objects.get(email__icontains=sender)
    except EmailUser.DoesNotExist:
        EmailUser.objects.create(email=sender, password="")
        sender_user = EmailUser.objects.get(email__icontains=sender)
    all_ccs = []
    if approval.is_org_applicant and approval.applicant.email:
        cc_list = approval.applicant.email
        if cc_list:
            all_ccs = [cc_list]
    msg = email.send(proposal.submitter_obj.email, cc=all_ccs, context=context)
    sender = settings.DEFAULT_FROM_EMAIL
    _log_approval_email(msg, approval, sender=sender_user)
    # _log_org_email(msg, approval.applicant, proposal.submitter, sender=sender_user)
    if approval.is_org_applicant:
        _log_org_email(msg, approval.applicant, proposal.submitter, sender=sender_user)
    else:
        _log_user_email(msg, approval.submitter, proposal.submitter, sender=sender_user)


def send_approval_surrender_email_notification(approval, request=None):
    email = ApprovalSurrenderNotificationEmail()
    proposal = approval.current_proposal

    if request and "test-emails" in request.path_info:
        details = "This are my test details"
        surrender_date = "01/01/1970"
    else:
        details = approval.surrender_details["details"]
        surrender_date = approval.surrender_details["surrender_date"]

    context = {
        "approval": approval,
        "details": details,
        "surrender_date": surrender_date,
    }
    sender = settings.DEFAULT_FROM_EMAIL
    try:
        sender_user = EmailUser.objects.get(email__icontains=sender)
    except EmailUser.DoesNotExist:
        EmailUser.objects.create(email=sender, password="")
        sender_user = EmailUser.objects.get(email__icontains=sender)
    all_ccs = []
    if approval.is_org_applicant and approval.applicant.email:
        cc_list = approval.applicant.email
        if cc_list:
            all_ccs = [cc_list]
    msg = email.send(proposal.submitter_obj.email, cc=all_ccs, context=context)
    sender = settings.DEFAULT_FROM_EMAIL
    _log_approval_email(msg, approval, sender=sender_user)
    if approval.is_org_applicant:
        _log_org_email(msg, approval.applicant, proposal.submitter, sender=sender_user)
    else:
        _log_user_email(msg, approval.submitter, proposal.submitter, sender=sender_user)


def send_approval_renewal_review_email_notification(approval):
    email = ApprovalRenewalReviewNotificationEmail()
    url = settings.SITE_URL
    url += reverse("internal-approval-detail", kwargs={"pk": approval.pk})

    context = {
        "approval": approval,
        "proposal": approval.current_proposal,
        "url": url,
    }
    sender = settings.DEFAULT_FROM_EMAIL
    sender_user = EmailUser.objects.get(email=sender)

    msg = email.send(
        emails_list_for_group(settings.GROUP_NAME_ASSESSOR),
        context=context,
    )

    _log_approval_email(msg, approval, sender=sender_user)


def send_approval_renewal_email_notification(approval):
    email = ApprovalRenewalNotificationEmail()
    url = settings.SITE_URL
    url += reverse("external-approval-detail", kwargs={"approval_pk": approval.pk})

    context = {
        "approval": approval,
        "proposal": approval.current_proposal,
        "url": url,
    }
    sender = settings.DEFAULT_FROM_EMAIL
    sender_user = EmailUser.objects.get(email=sender)

    if approval.is_org_applicant:
        # For organisations also cc in all the active organisation contacts
        msg = email.send(
            approval.applicant.email,
            cc=approval.applicant.contact_emails,
            context=context,
        )
    else:
        emailuser = retrieve_email_user(approval.current_proposal.ind_applicant)
        msg = email.send(
            emailuser.email,
            context=context,
        )

    _log_approval_email(msg, approval, sender=sender_user)


def send_approval_reinstate_email_notification(approval, request):
    email = ApprovalReinstateNotificationEmail()
    proposal = approval.current_proposal

    context = {
        "approval": approval,
    }
    all_ccs = []
    if approval.is_org_applicant and approval.applicant.email:
        cc_list = approval.applicant.email
        if cc_list:
            all_ccs = [cc_list]
    msg = email.send(proposal.submitter_obj.email, cc=all_ccs, context=context)
    sender = request.user if request else settings.DEFAULT_FROM_EMAIL
    _log_approval_email(msg, approval, sender=sender)
    # _log_org_email(msg, approval.applicant, proposal.submitter, sender=sender)
    if approval.is_org_applicant:
        _log_org_email(msg, approval.applicant, proposal.submitter, sender=sender)
    else:
        _log_user_email(msg, approval.submitter, proposal.submitter, sender=sender)


def send_approval_crown_land_rent_review_email_notification(approval, months_due_in):
    email = TemplateEmailBase(
        subject=f"Crown Land Rent Review due for {approval.approval_type} {approval.lodgement_number}",
        html_template="leaseslicensing/emails/approval_crown_land_rent_review_notification.html",
        txt_template="leaseslicensing/emails/approval_crown_land_rent_review_notification.txt",
    )
    url = settings.SITE_URL
    url += reverse("internal-approval-detail", kwargs={"pk": approval.pk})

    due_text = "today" if months_due_in <= 0 else f" in {months_due_in} months"

    context = {
        "approval": approval,
        "invoicing_details": approval.current_proposal.invoicing_details,
        "due_text": due_text,
        "url": url,
    }
    finance_group_member_emails = emails_list_for_group(settings.GROUP_FINANCE)
    msg = email.send(
        finance_group_member_emails,
        cc=[settings.LEASING_FINANCE_NOTIFICATION_EMAIL],
        context=context,
    )
    sender = settings.DEFAULT_FROM_EMAIL
    try:
        sender_user = EmailUser.objects.get(email__icontains=sender)
    except EmailUser.DoesNotExist:
        EmailUser.objects.create(email=sender, password="")
        sender_user = EmailUser.objects.get(email__icontains=sender)

    _log_approval_email(msg, approval, sender=sender_user)


def send_approval_gto_advance_turnover_entry_reminder_email_notification(
    approval, days_prior
):
    email = TemplateEmailBase(
        subject=f"Turnover Entry Required for {approval.approval_type} {approval.lodgement_number}",
        html_template="leaseslicensing/emails/approval_gto_advance_turnover_entry_reminder_email_notification.html",
        txt_template="leaseslicensing/emails/approval_gto_advance_turnover_entry_reminder_email_notification.txt",
    )
    url = settings.SITE_URL
    url += reverse("internal-approval-detail", kwargs={"pk": approval.pk})

    context = {
        "approval": approval,
        "invoicing_details": approval.current_proposal.invoicing_details,
        "days_prior": days_prior,
        "url": url,
    }
    finance_group_member_emails = emails_list_for_group(settings.GROUP_FINANCE)
    msg = email.send(
        finance_group_member_emails,
        cc=[settings.LEASING_FINANCE_NOTIFICATION_EMAIL],
        context=context,
    )
    sender = settings.DEFAULT_FROM_EMAIL
    try:
        sender_user = EmailUser.objects.get(email__icontains=sender)
    except EmailUser.DoesNotExist:
        EmailUser.objects.create(email=sender, password="")
        sender_user = EmailUser.objects.get(email__icontains=sender)

    _log_approval_email(msg, approval, sender=sender_user)


def send_approval_custom_cpi_entry_email_notification(approval, days_before_issue_date):
    email = TemplateEmailBase(
        subject=f"Custom CPI Entry Required for {approval.approval_type} {approval.lodgement_number}",
        html_template="leaseslicensing/emails/approval_custom_cpi_entry_notification.html",
        txt_template="leaseslicensing/emails/approval_custom_cpi_entry_notification.txt",
    )
    url = settings.SITE_URL
    url += reverse("internal-approval-detail", kwargs={"pk": approval.pk})

    invoicing_details = approval.current_proposal.invoicing_details

    days_before_issue_date = f"{days_before_issue_date} days"
    next_reminder_date = invoicing_details.invoicing_periods_next_reminder_date
    start_of_next_invoicing_period = invoicing_details.invoicing_periods_next_start_date

    context = {
        "approval": approval,
        "invoicing_details": invoicing_details,
        "days_before_issue_date": days_before_issue_date,
        "next_reminder_date": next_reminder_date,
        "start_of_next_invoicing_period": start_of_next_invoicing_period,
        "url": url,
    }
    finance_group_member_emails = emails_list_for_group(settings.GROUP_FINANCE)
    msg = email.send(
        finance_group_member_emails,
        cc=[settings.LEASING_FINANCE_NOTIFICATION_EMAIL],
        context=context,
    )
    sender = settings.DEFAULT_FROM_EMAIL
    try:
        sender_user = EmailUser.objects.get(email__icontains=sender)
    except EmailUser.DoesNotExist:
        EmailUser.objects.create(email=sender, password="")
        sender_user = EmailUser.objects.get(email__icontains=sender)

    _log_approval_email(msg, approval, sender=sender_user)


def send_approval_transfer_holder_email_notification(approval):
    from leaseslicensing.components.approvals.models import ApprovalTransfer

    email = ApprovalTransferHolderNotificationEmail()

    initiator = retrieve_email_user(approval.active_transfer.initiator)

    if (
        approval.active_transfer.transferee_type
        == ApprovalTransfer.TRANSFEREE_TYPE_ORGANISATION
    ):
        transferee_organisation = Organisation.objects.get(
            id=approval.active_transfer.transferee
        )
        transferee_name = (
            f"{transferee_organisation.ledger_organisation_name} "
            f"(ABN: {transferee_organisation.ledger_organisation_abn})"
        )
    else:
        transferee_user = retrieve_email_user(approval.active_transfer.transferee)
        transferee_name = f"{transferee_user.get_full_name} ({transferee_user.email})"

    context = {
        "approval": approval,
        "transferee_name": transferee_name,
    }

    msg = email.send(
        [initiator.email],
        context=context,
    )
    sender = settings.DEFAULT_FROM_EMAIL
    try:
        sender_user = EmailUser.objects.get(email__icontains=sender)
    except EmailUser.DoesNotExist:
        EmailUser.objects.create(email=sender, password="")
        sender_user = EmailUser.objects.get(email__icontains=sender)

    _log_approval_email(msg, approval, sender=sender_user)


def send_approval_transfer_transferee_email_notification(approval, transfer_proposal):
    from leaseslicensing.components.approvals.models import ApprovalTransfer

    email = ApprovalTransferTransfereeNotificationEmail()

    transferee = retrieve_email_user(approval.active_transfer.transferee)

    if (
        approval.active_transfer.transferee_type
        == ApprovalTransfer.TRANSFEREE_TYPE_ORGANISATION
    ):
        transferee_organisation = Organisation.objects.get(
            id=approval.active_transfer.transferee
        )
        transferee_name = (
            f"{transferee_organisation.ledger_organisation_name} "
            f"(ABN: {transferee_organisation.ledger_organisation_abn})"
        )
    else:
        transferee_user = retrieve_email_user(approval.active_transfer.transferee)
        transferee_name = f"{transferee_user.get_full_name} ({transferee_user.email})"

    context = {
        "approval": approval,
        "holder_name": approval.holder,
        "transferee_name": transferee_name,
        "transfer_proposal": transfer_proposal,
    }

    msg = email.send(
        [transferee.email],
        context=context,
    )
    sender = settings.DEFAULT_FROM_EMAIL
    try:
        sender_user = EmailUser.objects.get(email__icontains=sender)
    except EmailUser.DoesNotExist:
        EmailUser.objects.create(email=sender, password="")
        sender_user = EmailUser.objects.get(email__icontains=sender)

    _log_approval_email(msg, approval, sender=sender_user)


def _log_approval_email(email_message, approval, sender=None):
    from leaseslicensing.components.approvals.models import ApprovalLogEntry

    if isinstance(
        email_message,
        (
            EmailMultiAlternatives,
            EmailMessage,
        ),
    ):
        # Note: This will log the plain text body (not the html body)
        text = email_message.body
        subject = email_message.subject
        fromm = smart_str(sender) if sender else smart_str(email_message.from_email)
        # the to email is normally a list
        if isinstance(email_message.to, list):
            to = ",".join(email_message.to)
        else:
            to = smart_str(email_message.to)
        # we log the cc and bcc in the same cc field of the log entry as a ',' comma separated string
        all_ccs = []
        if email_message.cc:
            all_ccs += list(email_message.cc)
        if email_message.bcc:
            all_ccs += list(email_message.bcc)
        all_ccs = ",".join(all_ccs)

    else:
        text = smart_str(email_message)
        subject = ""
        to = approval.current_proposal.submitter_obj.email
        fromm = smart_str(sender) if sender else SYSTEM_NAME
        all_ccs = ""

    customer = approval.current_proposal.submitter

    staff = sender.id

    kwargs = {
        "subject": subject,
        "text": text,
        "approval": approval,
        "customer": customer,
        "staff": staff,
        "to": to,
        "fromm": fromm,
        "cc": all_ccs,
    }

    email_entry = ApprovalLogEntry.objects.create(**kwargs)

    return email_entry


def _log_org_email(email_message, organisation, customer, sender=None):
    if not isinstance(organisation, Organisation):
        # is a proxy_applicant
        return None

    if isinstance(
        email_message,
        (
            EmailMultiAlternatives,
            EmailMessage,
        ),
    ):
        # Note: This will log the plain text body (not the html body)
        text = email_message.body
        subject = email_message.subject
        fromm = smart_str(sender) if sender else smart_str(email_message.from_email)
        # the to email is normally a list
        if isinstance(email_message.to, list):
            to = ",".join(email_message.to)
        else:
            to = smart_str(email_message.to)
        # we log the cc and bcc in the same cc field of the log entry as a ',' comma separated string
        all_ccs = []
        if email_message.cc:
            all_ccs += list(email_message.cc)
        if email_message.bcc:
            all_ccs += list(email_message.bcc)
        all_ccs = ",".join(all_ccs)

    else:
        text = smart_str(email_message)
        subject = ""
        to = customer
        fromm = smart_str(sender) if sender else SYSTEM_NAME
        all_ccs = ""

    staff = sender.id

    kwargs = {
        "subject": subject,
        "text": text,
        "organisation": organisation,
        "customer": customer,
        "staff": staff,
        "to": to,
        "fromm": fromm,
        "cc": all_ccs,
    }

    email_entry = OrganisationLogEntry.objects.create(**kwargs)

    return email_entry


def _log_user_email(email_message, emailuser, customer, sender=None):
    from leaseslicensing.components.users.models import EmailUserLogEntry

    if isinstance(
        email_message,
        (
            EmailMultiAlternatives,
            EmailMessage,
        ),
    ):
        # Note: This will log the plain text body (not the html body)
        text = email_message.body
        subject = email_message.subject
        fromm = smart_str(sender) if sender else smart_str(email_message.from_email)
        # the to email is normally a list
        if isinstance(email_message.to, list):
            to = ",".join(email_message.to)
        else:
            to = smart_str(email_message.to)
        # we log the cc and bcc in the same cc field of the log entry as a ',' comma separated string
        all_ccs = []
        if email_message.cc:
            all_ccs += list(email_message.cc)
        if email_message.bcc:
            all_ccs += list(email_message.bcc)
        all_ccs = ",".join(all_ccs)

    else:
        text = smart_str(email_message)
        subject = ""
        to = customer
        fromm = smart_str(sender) if sender else SYSTEM_NAME
        all_ccs = ""

    staff = sender.id

    kwargs = {
        "subject": subject,
        "text": text,
        "email_user": emailuser,
        "customer": customer,
        "staff": staff,
        "to": to,
        "fromm": fromm,
        "cc": all_ccs,
    }

    email_entry = EmailUserLogEntry.objects.create(**kwargs)

    return email_entry
