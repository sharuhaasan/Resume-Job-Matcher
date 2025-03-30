from rest_framework import serializers
from .models import CandidateProfile, JobPosting, MatchResult

class CandidateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProfile
        fields = "__all__"

class JobPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = "__all__"

class MatchResultSerializer(serializers.ModelSerializer):
    candidate = CandidateProfileSerializer()
    job = JobPostingSerializer()

    class Meta:
        model = MatchResult
        fields = "__all__"
