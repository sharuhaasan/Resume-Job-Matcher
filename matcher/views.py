from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from django.core.files.storage import default_storage
import json

from .models import CandidateProfile, JobPosting
from .serializers import JobPostingSerializer
from .utils import extract_text_from_pdf, extract_text_from_docx, parse_resume

# ----------------------------------------
# Resume Upload API
# ----------------------------------------
class ResumeUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        print("🚀 ResumeUploadView: Received a request")
        file = request.FILES.get("resume")
        
        if not file:
            print("❌ No file provided")
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Save file to storage
        file_path = default_storage.save(f"resumes/{file.name}", file)

        # Extract text based on file type
        if file.name.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif file.name.endswith(".docx"):
            text = extract_text_from_docx(file_path)
        else:
            print("❌ Unsupported file format")
            return Response({"error": "Unsupported file format"}, status=status.HTTP_400_BAD_REQUEST)

        # Parse the extracted text
        parsed_data = parse_resume(text)

        # Extract candidate details
        name = parsed_data.get("name", "Unknown")
        email = parsed_data.get("email", None)
        skills = parsed_data.get("skills", [])
        education = parsed_data.get("education", [])
        work_experience = parsed_data.get("work_experience", [])

        if not email:
            return Response({"error": "Email not found in resume"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if candidate already exists or update existing profile
        candidate, created = CandidateProfile.objects.update_or_create(
            email=email,
            defaults={
                "name": name,
                "resume_file": file_path,
                "skills": skills,
                "education": education,
                "work_experience": work_experience,
            }
        )

        response_data = {
            "message": "Resume processed and candidate profile saved successfully",
            "data": {
                "id": candidate.id,
                "name": candidate.name,
                "email": candidate.email,
                "skills": candidate.skills,
                "education": candidate.education,
                "work_experience": candidate.work_experience,
            },
        }
        
        print("✅ Response JSON:", response_data)
        return Response(response_data, status=status.HTTP_201_CREATED)

# ----------------------------------------
# Job Posting API
# ----------------------------------------
class JobPostingView(APIView):
    def get(self, request):
        jobs = JobPosting.objects.all()
        serializer = JobPostingSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        job = JobPosting.objects.create(
            title=data["title"],
            company=data["company"],
            description=data["description"],
            required_skills=data["required_skills"],
        )
        return Response({"message": "Job posted successfully"}, status=status.HTTP_201_CREATED)

# ----------------------------------------
# Candidate-Job Matching API
# ----------------------------------------
class MatchCandidateToJobView(APIView):
    def post(self, request):
        candidate_id = request.data.get("candidate_id")
        job_id = request.data.get("job_id")

        if not candidate_id or not job_id:
            return Response({"error": "candidate_id and job_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            candidate = CandidateProfile.objects.get(id=candidate_id)
            job = JobPosting.objects.get(id=job_id)
        except CandidateProfile.DoesNotExist:
            return Response({"error": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)
        except JobPosting.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure skills are stored as a proper list
        candidate_skills = candidate.skills if isinstance(candidate.skills, list) else json.loads(candidate.skills)
        job_skills = job.required_skills if isinstance(job.required_skills, list) else json.loads(job.required_skills)

        # Normalize skills for case-insensitive matching
        candidate_skills_lower = {skill.lower() for skill in candidate_skills}
        job_skills_lower = {skill.lower() for skill in job_skills}

        matched_skills = candidate_skills_lower & job_skills_lower
        missing_skills = job_skills_lower - candidate_skills_lower

        match_score = (len(matched_skills) / len(job_skills_lower)) * 100 if job_skills_lower else 0

        return Response(
            {
                "candidate": {
                    "id": candidate.id,
                    "name": candidate.name,
                    "email": candidate.email,
                },
                "job": {
                    "id": job.id,
                    "title": job.title,
                    "company": job.company,
                },
                "match_score": round(match_score, 2),
                "matched_skills": list(matched_skills),
                "missing_skills": list(missing_skills),
                "summary": f"Candidate is a {round(match_score, 2)}% match.",
            },
            status=status.HTTP_200_OK,
        )
