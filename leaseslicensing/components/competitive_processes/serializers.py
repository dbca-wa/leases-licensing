from rest_framework import serializers
from leaseslicensing.components.competitive_processes.models import CompetitiveProcess
from leaseslicensing.components.proposals.models import Proposal
from leaseslicensing.components.main.serializers import EmailUserSerializer


class RegistrationOfInterestSerializer(serializers.ModelSerializer):
    relevant_applicant_name = serializers.CharField()
    
    class Meta:
        model = Proposal
        fields = (
            'id',
            'lodgement_number',
            'relevant_applicant_name',
        )


class CompetitiveProcessSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompetitiveProcess
        fields = '__all__'


class ListCompetitiveProcessSerializer(serializers.ModelSerializer):
    registration_of_interest = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    assigned_officer = serializers.SerializerMethodField()
    site = serializers.CharField()  # For property
    group = serializers.CharField()  # For property
    can_accessing_user_view = serializers.SerializerMethodField()
    can_accessing_user_process = serializers.SerializerMethodField()

    class Meta:
        model = CompetitiveProcess
        fields = (
            'id',
            'lodgement_number',
            'registration_of_interest',
            'status',
            'created_at',
            'assigned_officer',
            'site',
            'group',
            'can_accessing_user_view',
            'can_accessing_user_process',
        )
        # additional data to be returned for datatable
        # fields listed here should be listed 'fields' above, otherwise not returned
        datatables_always_serialize = (
            'group',
            'site',
            'can_accessing_user_view',
            'can_accessing_user_process',
        )

    def get_registration_of_interest(self, obj):
        if obj.generated_from_registration_of_interest:
            return RegistrationOfInterestSerializer(obj.generating_proposal).data
        else:
            return None

    def get_status(self, obj):
        return obj.get_status_display()  # https://docs.djangoproject.com/en/3.2/ref/models/instances/#django.db.models.Model.get_FOO_display

    def get_assigned_officer(self, obj):
        if obj.is_assigned:
            return EmailUserSerializer(obj.assigned_officer).data
        else:
            return None

    def get_can_accessing_user_view(self, obj):
        try:
            user = self.context.get("request").user
            can_view = obj.can_user_view(user)
            return can_view
        except:
            return False

    def get_can_accessing_user_process(self, obj):
        try:
            user = self.context.get("request").user
            can_process = obj.can_user_process(user)
            return can_process
        except:
            return False
