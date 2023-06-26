from rest_framework import serializers

from leaseslicensing.components.compliances.models import (
    Compliance,
    ComplianceAmendmentRequest,
    ComplianceDocument,
    ComplianceLogEntry,
    ComplianceUserAction,
)
from leaseslicensing.components.main.serializers import EmailUserSerializer
from leaseslicensing.components.main.utils import get_secure_document_url, get_secure_file_url
from leaseslicensing.ledger_api_utils import retrieve_email_user


class ComplianceDocumentSerializer(serializers.ModelSerializer):
    secure_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ComplianceDocument
        fields = (
            "name",
            "_file",
            "secure_url",
            "can_delete",
            "id",
        )

    def get_secure_url(self, obj):
        return [
            get_secure_file_url(obj, "_file")
        ]


class ComplianceSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="proposal.title")
    holder = serializers.CharField(read_only=True)
    processing_status = serializers.CharField(source="get_processing_status_display")
    customer_status = serializers.CharField(source="get_customer_status_display")
    submitter = serializers.SerializerMethodField(read_only=True)
    documents = ComplianceDocumentSerializer(many=True, read_only=True)
    submitter = serializers.SerializerMethodField(read_only=True)
    allowed_assessors = serializers.SerializerMethodField(read_only=True)
    requirement = serializers.CharField(
        source="requirement.requirement", required=False, allow_null=True
    )
    approval_lodgement_number = serializers.SerializerMethodField()
    application_type = serializers.SerializerMethodField(read_only=True)
    due_date = serializers.SerializerMethodField(read_only=True)
    lodgement_date_display = serializers.SerializerMethodField(read_only=True)
    assigned_to_name = serializers.CharField(read_only=True)

    class Meta:
        model = Compliance
        fields = (
            "id",
            "proposal",
            "due_date",
            "processing_status",
            "customer_status",
            "title",
            "text",
            "holder",
            "assigned_to_name",
            "approval",
            "documents",
            "requirement",
            "can_user_view",
            "can_process",
            "reference",
            "lodgement_number",
            "lodgement_date",
            "submitter",
            "allowed_assessors",
            "lodgement_date",
            "approval_lodgement_number",
            "num_participants",
            "participant_number_required",
            "fee_invoice_reference",
            "fee_paid",
            "application_type",
            "lodgement_date_display",
        )
        datatables_always_serialize = (
            "id",
            "proposal",
            "due_date",
            "processing_status",
            "customer_status",
            "title",
            "text",
            "holder",
            "assigned_to_name",
            "approval",
            "documents",
            "requirement",
            "can_user_view",
            "can_process",
            "reference",
            "lodgement_number",
            "lodgement_date",
            "submitter",
            "allowed_assessors",
            "lodgement_date",
            "approval_lodgement_number",
            "num_participants",
            "participant_number_required",
            "fee_invoice_reference",
            "fee_paid",
            "application_type",
        )

    def get_due_date(self, obj):
        return obj.due_date.strftime("%d/%m/%Y") if obj.due_date else ""

    def get_allowed_assessors(self, obj):
        if obj.allowed_assessors:
            email_users = []
            for user in obj.allowed_assessors:
                email_users.append(retrieve_email_user(user))
            return EmailUserSerializer(email_users, many=True).data
        else:
            return ""

    def get_approval_lodgement_number(self, obj):
        return obj.approval.lodgement_number

    def get_submitter(self, obj):
        if obj.submitter:
            return retrieve_email_user(obj.submitter).get_full_name()
        return None

    def get_application_type(self, obj):
        if obj.proposal.application_type:
            return obj.proposal.application_type.name_display
        return None

    def get_lodgement_date_display(self, obj):
        if obj.lodgement_date:
            return (
                obj.lodgement_date.strftime("%d/%m/%Y")
                + " at "
                + obj.lodgement_date.strftime("%I:%M %p")
            )


class InternalComplianceSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="proposal.title")
    holder = serializers.CharField(source="proposal.applicant")
    processing_status = serializers.CharField(source="get_processing_status_display")
    customer_status = serializers.CharField(source="get_customer_status_display")
    submitter = serializers.SerializerMethodField(read_only=True)
    documents = ComplianceDocumentSerializer(many=True, read_only=True)
    submitter = serializers.SerializerMethodField(read_only=True)
    allowed_assessors = serializers.SerializerMethodField(read_only=True)
    requirement = serializers.CharField(
        source="requirement.requirement", required=False, allow_null=True
    )
    approval_lodgement_number = serializers.SerializerMethodField()
    lodgement_date = serializers.SerializerMethodField()

    class Meta:
        model = Compliance
        fields = (
            "id",
            "proposal",
            "due_date",
            "processing_status",
            "customer_status",
            "title",
            "text",
            "holder",
            "assigned_to",
            "approval",
            "documents",
            "requirement",
            "can_user_view",
            "can_process",
            "reference",
            "lodgement_number",
            "lodgement_date",
            "submitter",
            "allowed_assessors",
            "lodgement_date",
            "approval_lodgement_number",
            "participant_number_required",
            "num_participants",
            "fee_invoice_reference",
            "fee_paid",
        )

    def get_allowed_assessors(self, obj):
        if obj.allowed_assessors:
            email_users = []
            for user in obj.allowed_assessors:
                email_users.append(retrieve_email_user(user))
            return EmailUserSerializer(email_users, many=True).data
        else:
            return ""

    def get_lodgement_date(self, obj):
        return obj.lodgement_date.strftime("%d/%m/%Y") if obj.lodgement_date else ""

    def get_approval_lodgement_number(self, obj):
        return obj.approval.lodgement_number

    def get_submitter(self, obj):
        if obj.submitter:
            return retrieve_email_user(obj.submitter).get_full_name()
        return None


class SaveComplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compliance
        fields = (
            "id",
            "title",
            "text",
            "num_participants",
        )


class ComplianceActionSerializer(serializers.ModelSerializer):
    who = serializers.CharField(source="who_full_name")

    class Meta:
        model = ComplianceUserAction
        fields = "__all__"


class ComplianceCommsSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField()

    class Meta:
        model = ComplianceLogEntry
        fields = "__all__"

    def get_documents(self, obj):
        return [[d.name, d._file.url] for d in obj.documents.all()]


class ComplianceAmendmentRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = ComplianceAmendmentRequest
        fields = "__all__"


class CompAmendmentRequestDisplaySerializer(serializers.ModelSerializer):
    reason = serializers.SerializerMethodField()

    class Meta:
        model = ComplianceAmendmentRequest
        fields = "__all__"

    def get_reason(self, obj):
        return obj.reason.reason if obj.reason else None
