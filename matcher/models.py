from django.db import models

class CandidateProfile(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    resume_file = models.FileField(upload_to="resumes/")
    skills = models.JSONField(default=list)  # Stores skills as a list
    education = models.JSONField(default=list)
    work_experience = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class JobPosting(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    required_skills = models.JSONField(default=list)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

class MatchResult(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    match_score = models.IntegerField()
    missing_skills = models.JSONField(default=list)
    summary = models.TextField()

    def __str__(self):
        return f"Match {self.match_score}% - {self.candidate.name} & {self.job.title}"
