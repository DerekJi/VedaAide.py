"""Job posting record generator."""

import logging
import random
from typing import List, Optional

from .models import JobPostingRecord
from .repository import DataRepository

logger = logging.getLogger(__name__)


class JobPostingGenerator:
    """Generates synthetic job posting records.

    This generator creates realistic job posting data by:
    - Generating job titles and company names
    - Selecting appropriate tech stacks based on level
    - Creating job descriptions and requirements
    - Generating salary ranges and benefits

    Args:
        seed: Optional random seed for reproducibility.
    """

    def __init__(self, seed: Optional[int] = None) -> None:
        """Initialize the job posting generator.

        Args:
            seed: Random seed for reproducibility. If None, uses system randomness.
        """
        self.random = random.Random(seed)
        self.job_counter = 0
        self.repo = DataRepository()
        self.job_titles = [
            "Software Engineer",
            "Backend Engineer",
            "Frontend Engineer",
            "Full Stack Engineer",
            "DevOps Engineer",
            "Data Engineer",
            "Data Scientist",
            "ML Engineer",
            "Product Manager",
            "Engineering Manager",
            "Tech Lead",
        ]
        self.team_names = [
            "Platform",
            "Infrastructure",
            "Analytics",
            "Backend",
            "Frontend",
            "Product",
            "AI/ML",
            "Data",
            "Cloud",
            "Security",
        ]

    def _generate_company_name(self) -> str:
        """Generate a random company name.

        Returns:
            Company name combining prefix and suffix.
        """
        prefix = self.random.choice(self.repo.COMPANY_NAME_PREFIXES)
        suffix = self.random.choice(self.repo.COMPANY_NAME_SUFFIXES)
        return f"{prefix}{suffix}"

    def _generate_tech_requirements(self, level: str) -> List[str]:
        """Generate technology requirements based on level.

        Args:
            level: Career level (Junior, Mid-level, Senior, Lead, Staff).

        Returns:
            List of required technologies.
        """
        num_skills = 5 if level in ["Junior", "Mid-level"] else 7
        all_techs = []
        for techs in self.repo.TECH_STACKS.values():
            all_techs.extend(techs)
        return self.random.sample(all_techs, min(num_skills, len(all_techs)))

    def _generate_requirements(self, tech_stack: List[str], level: str) -> List[str]:
        """Generate job requirements.

        Args:
            tech_stack: List of required technologies.
            level: Career level.

        Returns:
            List of job requirements.
        """
        years_req = {
            "Junior": "0-2",
            "Mid-level": "3-5",
            "Senior": "6+",
            "Lead": "8+",
            "Staff": "10+",
        }

        requirements = [
            f"{years_req[level]} years of professional experience",
            (
                f"Experience with "
                f"{', '.join(self.random.sample(tech_stack, min(3, len(tech_stack))))}"
            ),
            "Strong problem-solving skills",
            "Experience with agile development",
        ]

        if level in ["Senior", "Lead", "Staff"]:
            requirements.extend(
                [
                    "Experience mentoring junior engineers",
                    "Strong system design knowledge",
                    "Experience with code reviews and technical discussions",
                ]
            )

        return requirements

    def _generate_benefits(self) -> List[str]:
        """Generate job benefits.

        Returns:
            List of offered benefits.
        """
        all_benefits = [
            "Competitive salary",
            "Stock options",
            "Health insurance",
            "Dental coverage",
            "Vision coverage",
            "401(k) matching",
            "Unlimited PTO",
            "Professional development budget",
            "Relocation assistance",
            "Work from home options",
            "Gym membership",
            "Free snacks and drinks",
            "Learning stipend",
        ]
        return self.random.sample(all_benefits, k=self.random.randint(6, 10))

    def _generate_description(self, level: str, role: str, team: str, industry: str) -> str:
        """Generate job description.

        Args:
            level: Career level.
            role: Job role/title.
            team: Team name.
            industry: Industry sector.

        Returns:
            Job description text.
        """
        descriptions = [
            f"building scalable {industry} solutions",
            f"leading {team} team initiatives",
            "solving complex technical challenges",
            "mentoring team members",
            "architecting next-generation systems",
        ]
        desc = self.random.choice(descriptions)

        template = self.random.choice(self.repo.JOB_DESCRIPTION_TEMPLATES)
        company = self._generate_company_name()

        return template.format(
            level=level,
            role=role,
            team_name=team,
            description=desc,
            company=company,
        )

    def generate(self) -> JobPostingRecord:
        """Generate a single job posting record.

        Returns:
            A JobPostingRecord with all fields populated.
        """
        self.job_counter += 1

        level = self.random.choice(self.repo.LEVELS)
        job_type = self.random.choice(self.repo.JOB_TYPES)
        industry = self.random.choice(self.repo.INDUSTRIES)
        location = self.random.choice(self.repo.LOCATIONS)

        role = self.random.choice(self.job_titles)
        title = f"{level} {role}" if level != "Mid-level" else role

        salary_min, salary_max = self.repo.SALARY_RANGES[level]
        tech_stack = self._generate_tech_requirements(level)
        soft_skills = self.random.sample(self.repo.SOFT_SKILLS, k=3)
        requirements = self._generate_requirements(tech_stack, level)
        team = self.random.choice(self.team_names)

        description = self._generate_description(level, role, team, industry)

        record = JobPostingRecord(
            id=f"job_{self.job_counter:06d}",
            title=title,
            company=self._generate_company_name(),
            location=location,
            level=level,
            job_type=job_type,
            salary_min=salary_min,
            salary_max=salary_max,
            industry=industry,
            tech_stack=tech_stack,
            required_skills=requirements,
            soft_skills=soft_skills,
            description=description,
            requirements=requirements,
            benefits=self._generate_benefits(),
        )

        return record
