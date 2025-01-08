from rest_framework import serializers
from .models import *

class CompaniesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Companies
        fields = '__all__'


class DefaultCriteriaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = DefaultCriteria
        fields = '__all__'


class CachedResultsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CachedResults
        fields = '__all__'

    
class AhpResultSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = AhpResult
        fields = '__all__'


class TopsisResultSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = TopsisResult
        fields = '__all__'


class FuzzyTopsisResultSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = FuzzyTopsisResult
        fields = '__all__'


class WaspasResultSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = WaspasResult
        fields = '__all__'