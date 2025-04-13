from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any

class BasicJobInfo(BaseModel):
    job_title: str = Field(..., description="Job title for the position")
    job_code: Optional[str] = Field(None, description="Job code or requisition ID")
    job_level: Optional[str] = Field(None, description="Internal job level (e.g., L5, Band 3)")
    department: Optional[str] = Field(None, description="Department, division, or business unit")
    job_category: Optional[str] = Field(None, description="Function or job category")

class JobPostingMetadata(BaseModel):
    contract_duration: Optional[str] = Field(None, description="Duration of contract, if applicable")
    time_commitment: Optional[str] = Field(None, description="Time commitment (e.g., 40 hrs/week, flexible)")

class DetailedRoleDescription(BaseModel):
    job_summary: str = Field(..., description="Job summary or objective")
    daily_tasks: List[str] = Field(default_factory=list, description="Day-to-day tasks and responsibilities")
    performance_indicators: List[str] = Field(default_factory=list, description="Performance indicators or KPIs")
    decision_making_authority: Optional[str] = Field(None, description="Decision-making authority level")
    stakeholder_interactions: List[str] = Field(default_factory=list, description="Key stakeholder interactions")

class RequirementsBreakdown(BaseModel):
    required_qualifications: List[str] = Field(default_factory=list, description="Required qualifications")
    preferred_qualifications: List[str] = Field(default_factory=list, description="Preferred qualifications")
    mandatory_certifications: List[str] = Field(default_factory=list, description="Mandatory certifications")
    legal_eligibility: Optional[str] = Field(None, description="Legal eligibility requirements")
    background_checks: Optional[str] = Field(None, description="Background checks or drug testing requirements")
    clearance_level: Optional[str] = Field(None, description="Clearance level required")

class SkillsClassification(BaseModel):
    hard_skills: List[str] = Field(default_factory=list, description="Technical skills, programming languages, tools, platforms")
    soft_skills: List[str] = Field(default_factory=list, description="Communication, teamwork, leadership skills")
    domain_expertise: List[str] = Field(default_factory=list, description="Domain knowledge (e.g., FinTech, Healthcare)")
    methodologies: List[str] = Field(default_factory=list, description="Methodologies (Agile, Scrum, Six Sigma)")
    languages: List[str] = Field(default_factory=list, description="Language skills required")
    skills_priority: Dict[str, List[str]] = Field(default_factory=dict, description="Skills categorized by priority (must-have vs nice-to-have)")

class CompensationDetails(BaseModel):
    base_salary: Optional[str] = Field(None, description="Base salary or salary range")
    bonus_structure: Optional[str] = Field(None, description="Bonus or commission structure")
    equity: Optional[str] = Field(None, description="Equity or stock options")
    benefits: List[str] = Field(default_factory=list, description="Benefits (healthcare, 401(k), etc.)")
    relocation_assistance: Optional[bool] = Field(None, description="Relocation assistance availability")
    visa_sponsorship: Optional[bool] = Field(None, description="Visa sponsorship availability")

class WorkEnvironment(BaseModel):
    work_model: Optional[str] = Field(None, description="Work model (on-site, hybrid, remote)")
    locations: List[str] = Field(default_factory=list, description="Work location(s)")
    travel_requirements: Optional[str] = Field(None, description="Travel requirements (percentage or destinations)")
    shift_type: Optional[str] = Field(None, description="Shift type (e.g., night shift, rotational)")

class CareerPathInfo(BaseModel):
    growth_opportunities: Optional[str] = Field(None, description="Opportunities for growth or promotion")
    training_programs: List[str] = Field(default_factory=list, description="Training and development programs")
    mentorship: Optional[str] = Field(None, description="Mentorship or onboarding details")
    succession_planning: Optional[str] = Field(None, description="Succession planning tags (internal use)")
    culture_page_link: Optional[str] = Field(None, description="Link to company culture page")
    careers_page_link: Optional[str] = Field(None, description="Link to careers page")

class JobDescriptionSchema(BaseModel):
    basic_info: BasicJobInfo
    posting_metadata: JobPostingMetadata = Field(default_factory=JobPostingMetadata)
    role_description: DetailedRoleDescription
    requirements: RequirementsBreakdown = Field(default_factory=RequirementsBreakdown)
    skills: SkillsClassification = Field(default_factory=SkillsClassification)
    compensation: CompensationDetails = Field(default_factory=CompensationDetails)
    work_environment: WorkEnvironment = Field(default_factory=WorkEnvironment)
    career_path: CareerPathInfo = Field(default_factory=CareerPathInfo)
    original_text: Optional[str] = Field(None, description="Original text of the job description")

class JobDescriptionExtractionResponse(BaseModel):
    extracted_jd: JobDescriptionSchema
    message: str = Field(default="Job description extracted successfully")

class JobDescriptionEnhancementResponse(BaseModel):
    enhanced_jd: JobDescriptionSchema
    message: str = Field(default="Job description enhanced successfully") 