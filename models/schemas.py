from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Salary(BaseModel):
    currency: str
    min: int
    max: int

class JobInfo(BaseModel):
    job_title: str
    open_positions: int
    destination_country: str
    regional_hub: str
    shift: str
    salary: Salary
    placement_tier: Optional[str] = None

class SkillReq(BaseModel):
    name: str
    mandatory: bool

class LanguageReq(BaseModel):
    language: str
    minimum_level: str

class CandidateRequirements(BaseModel):
    minimum_experience_years: int
    language_requirements: List[LanguageReq]
    visa_sponsorship: bool
    work_authorization_required: bool
    visa_requirement: str
    skills: List[SkillReq]

class RoleDescription(BaseModel):
    overview: str
    responsibilities: List[str]

class JobRequirement(BaseModel):
    job_info: JobInfo
    candidate_requirements: CandidateRequirements
    role_description: RoleDescription

# Candidate extraction schema
class WorkExperience(BaseModel):
    job_title: str = Field(default="")
    company: str = Field(default="")
    start_date: Optional[str] = Field(default="unknown")
    end_date: Optional[str] = Field(default="unknown")
    duration_years: Optional[float] = Field(default=0.0)
    relevant_skills: List[str] = Field(default_factory=list)

class CandidateLanguage(BaseModel):
    language: str = Field(default="")
    level: str = Field(default="")

class CandidateInfo(BaseModel):
    candidate_name: str = Field(default="Unknown")
    email: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    location: Optional[str] = Field(default=None)
    skills: List[str] = Field(default_factory=list, description="Array of skill names as simple strings. Example: ['HACCP', 'Cooking']")
    education: List[Dict[str, Any]] = Field(default_factory=list)
    work_experience: List[WorkExperience] = Field(default_factory=list)
    total_relevant_experience_years: Optional[float] = Field(default=0.0)
    languages: List[CandidateLanguage] = Field(default_factory=list)
    passport_status: Optional[str] = Field(default="unknown")
    visa_status: Optional[str] = Field(default="unknown")
    relevant_experience_summary: str = Field(default="")
    evidence: List[str] = Field(default_factory=list, description="Array of exact text snippets (strings) from the CV as evidence. Example: ['Worked 5 years in Dubai', 'Hold UAE Visa']")

# Screening Results Schema
class CriteriaResult(BaseModel):
    status: str # PASS, FAIL, REVIEW
    required: Any
    actual: Any
    reason: Optional[str] = None

class Gate1Criteria(BaseModel):
    experience: CriteriaResult
    skills: CriteriaResult
    language: CriteriaResult
    visa: CriteriaResult

class Gate1Result(BaseModel):
    candidate_name: str
    filename: str
    status: str # PASS, FAIL, REVIEW
    criteria: Gate1Criteria
    overall_reason: str
    evidence_snippets: List[str]

class ScreeningResponse(BaseModel):
    job_title: str
    results: List[Gate1Result]
