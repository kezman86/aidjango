from rest_framework import serializers
from .models import Case

class CaseSerializers(serializers.ModelSerializer):

    class Meta:
        model = Case
        fields = (
            'caseID',
            'caseNumber',
            'caseSubject',
            'caseModule',
            'published',
            'caseDescription'
        )
