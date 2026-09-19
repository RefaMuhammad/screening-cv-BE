import os
import json
from openai import OpenAI
from models.schemas import CandidateInfo, JobRequirement

class DeepSeekService:
    def __init__(self):
        api_key = os.getenv("DEEPSEEK_API_KEY")
        base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        self.model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

    def extract_candidate_info(self, cv_text: str, job_desc: str = "", job_title: str = "") -> CandidateInfo:
        role_alignment_instruction = ""
        if job_desc:
            role_alignment_instruction = f"""
        EMPLOYER ROLE DESCRIPTION:
        {job_desc}
        
        RULES FOR ROLE ALIGNMENT:
        - Analyze the Employer Role Description above. Look for any explicit mandatory requirements (e.g., nationality, specific licenses, specific prior company types).
        - If the candidate explicitly violates a strict requirement from the Role Description, set role_alignment.status to "FAIL" and provide the reason.
        - If the requirement is unclear or the CV doesn't mention it, set status to "REVIEW".
        - If the candidate meets the implicit/explicit requirements, or if no strict knockouts are found in the Role Description, set status to "PASS".
        """
        else:
            role_alignment_instruction = 'Set role_alignment status to "PASS" and reason to "No role description provided".'

        prompt = f"""
        You are a recruitment document extraction assistant.
        Extract information only from the provided CV text.
        Do not invent missing facts.
        
        RULES FOR RELEVANT EXPERIENCE:
        - The employer is hiring for the position of: "{job_title}".
        - When calculating `total_relevant_experience_years`, you MUST ONLY sum the durations of jobs that are relevant to this target position.
        - If a past job is completely unrelated (e.g. Software Engineer applying for a Chef role), do NOT include its duration in the total.
        - If the candidate has NO relevant jobs, `total_relevant_experience_years` must be 0.
        
        RULES FOR EXPERIENCE DATES:
        - If a job's end date is 'Recent', 'Present', or 'Now', assume the candidate is working there up to the current year (2024). Calculate the duration from the start date to the current year.
        - If the start date is completely missing and you mathematically cannot calculate the total years, return null for 'duration_years' and 'total_relevant_experience_years'.
        
        {role_alignment_instruction}
        
        RULES FOR LANGUAGES:
        - For the `level` field in languages, you MUST normalize any proficiency description (like IELTS 7.5, TOEFL, Fluent, Native, Basic) into one of the following exact strings: "A1", "A2", "B1", "B2", "C1", "C2", or "Native".
        - Examples: IELTS 4.0-5.0 -> B1, IELTS 5.5-6.5 -> B2, IELTS 7.0-8.0 -> C1, IELTS 8.5+ -> C2, Fluent -> C1, Basic -> A2.

        You MUST return ONLY valid JSON matching this exact structure:
        {{
            "candidate_name": "Full Name",
            "email": "email@example.com",
            "phone": "+123456",
            "location": "City, Country",
            "skills": ["Skill 1", "Skill 2"],
            "total_relevant_experience_years": 5.5,
            "passport_status": "unknown",
            "visa_status": "unknown",
            "relevant_experience_summary": "Brief summary",
            "evidence": ["Exact quote 1", "Exact quote 2"],
            "work_experience": [
                {{
                    "job_title": "Title",
                    "company": "Company",
                    "start_date": "Jan 2020",
                    "end_date": "Present",
                    "duration_years": 3.5,
                    "relevant_skills": ["Skill 1"]
                }}
            ],
            "languages": [{{"language": "English", "level": "C1"}}],
            "education": [],
            "role_alignment": {{
                "status": "PASS",
                "reason": "Meets requirements"
            }}
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"Extract the following CV into the exact JSON format:\n\n{cv_text}"}
                ],
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            data = json.loads(content)
            return CandidateInfo(**data)
        except Exception as e:
            print(f"Error extracting candidate info: {e}")
            # If validation fails, try to print what the AI actually returned
            if 'content' in locals():
                print(f"Raw AI Output: {content}")
            return CandidateInfo()
            
    def polish_role_description(self, text: str) -> str:
        prompt = "Polish the following role description for grammar, structure, and readability. Do NOT change any factual requirements or numbers."
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content.strip()
        except:
            return text
