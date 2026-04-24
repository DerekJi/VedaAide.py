"""Data models for resume and job posting records."""

from dataclasses import dataclass
from typing import List


@dataclass
class ResumeRecord:
    """Represents a resume record with structured information.

    Attributes:
        id: Unique resume identifier.
        name: Candidate name.
        level: Career level (Junior, Mid-level, Senior, Lead, Staff).
        years_experience: Years of professional experience.
        tech_stack: List of technologies and programming languages.
        soft_skills: List of soft skills (leadership, communication, etc.).
        location: Preferred work location.
        current_company: Current employer.
        previous_companies: List of previous employers.
        achievements: Professional achievements and accomplishments.
        content: Full resume content as formatted text.
    """

    id: str
    name: str
    level: str
    years_experience: int
    tech_stack: List[str]
    soft_skills: List[str]
    location: str
    current_company: str
    previous_companies: List[str]
    achievements: List[str]
    content: str


@dataclass
class JobPostingRecord:
    """Represents a job posting record with structured information.

    Attributes:
        id: Unique job posting identifier.
        title: Job title.
        company: Company name.
        location: Job location.
        level: Required career level.
        job_type: Type of employment (Full-time, Contract, Part-time, Freelance).
        salary_min: Minimum salary.
        salary_max: Maximum salary.
        industry: Industry sector.
        tech_stack: List of required technologies.
        required_skills: List of required skills.
        soft_skills: List of required soft skills.
        description: Job description.
        requirements: List of job requirements.
        benefits: List of offered benefits.
    """

    id: str
    title: str
    company: str
    location: str
    level: str
    job_type: str
    salary_min: int
    salary_max: int
    industry: str
    tech_stack: List[str]
    required_skills: List[str]
    soft_skills: List[str]
    description: str
    requirements: List[str]
    benefits: List[str]
