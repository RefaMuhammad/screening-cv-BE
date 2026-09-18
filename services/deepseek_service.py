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

    def extract_candidate_info(self, cv_text: str) -> CandidateInfo:
        prompt = """
        You are a recruitment document extraction assistant.
        Extract information only from the provided CV text.
        Do not invent missing facts.
        
        RULES FOR EXPERIENCE DATES:
        - If a job's end date is 'Recent', 'Present', or 'Now', assume the candidate is working there up to the current year (2024). Calculate the duration from the start date to the current year.
        - If the start date is completely missing and you mathematically cannot calculate the total years, return null for 'duration_years' and 'total_relevant_experience_years'.
        
        You MUST return ONLY valid JSON matching this exact structure:
        {
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
                {
                    "job_title": "Title",
                    "company": "Company",
                    "start_date": "Jan 2020",
                    "end_date": "Present",
                    "duration_years": 3.5,
                    "relevant_skills": ["Skill 1"]
                }
            ],
            "languages": [{"language": "English", "level": "C1"}],
            "education": []
        }
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
