"""Resume record generator."""

import logging
import random
from typing import List, Optional

from .models import ResumeRecord
from .repository import DataRepository

logger = logging.getLogger(__name__)


class ResumeGenerator:
    """Generates synthetic resume records.

    This generator creates realistic resume data by:
    - Combining first and last names
    - Selecting appropriate tech stacks based on career level
    - Generating company names and achievement descriptions
    - Creating formatted resume content

    Args:
        seed: Optional random seed for reproducibility.
    """

    def __init__(self, seed: Optional[int] = None) -> None:
        """Initialize the resume generator.

        Args:
            seed: Random seed for reproducibility. If None, uses system randomness.
        """
        self.random = random.Random(seed)
        self.resume_counter = 0
        self.repo = DataRepository()
        self.first_names = ["Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Grace", "Henry"]
        self.last_names = ["Smith", "Johnson", "Chen", "Wang", "Kumar", "Garcia", "Brown", "Lee"]

    def _generate_name(self) -> str:
        """Generate a random full name.

        Returns:
            A name in format "FirstName LastName".
        """
        first = self.random.choice(self.first_names)
        last = self.random.choice(self.last_names)
        return f"{first} {last}"

    def _generate_company_name(self) -> str:
        """Generate a random company name.

        Returns:
            Company name combining prefix and suffix.
        """
        prefix = self.random.choice(self.repo.COMPANY_NAME_PREFIXES)
        suffix = self.random.choice(self.repo.COMPANY_NAME_SUFFIXES)
        return f"{prefix}{suffix}"

    def _generate_tech_stack(self, level: str) -> List[str]:
        """Generate technology stack based on career level.

        Args:
            level: Career level (Junior, Mid-level, Senior, Lead, Staff).

        Returns:
            List of technologies.
        """
        num_skills = 5 if level in ["Junior", "Mid-level"] else 8
        all_techs = []
        for techs in self.repo.TECH_STACKS.values():
            all_techs.extend(techs)
        return self.random.sample(all_techs, min(num_skills, len(all_techs)))

    def _generate_soft_skills(self) -> List[str]:
        """Generate soft skills for a resume.

        Returns:
            List of 3-6 soft skills.
        """
        return self.random.sample(self.repo.SOFT_SKILLS, k=self.random.randint(3, 6))

    def _generate_achievements(self, tech_stack: List[str], level: str) -> List[str]:
        """Generate professional achievements.

        Args:
            tech_stack: List of technologies for the resume.
            level: Career level.

        Returns:
            List of achievement descriptions.
        """
        achievements = []
        num_achievements = self.random.randint(3 if level == "Junior" else 4, 6)

        for _ in range(num_achievements):
            template = self.random.choice(self.repo.EXPERIENCE_TEMPLATES)
            tech = self.random.choice(tech_stack)

            params = {
                "tech": tech,
                "users": self.random.choice([1, 10, 100, 1000]) * 1000000,
                "scale": self.random.choice([100, 1000, 100000]) / 1,
                "percentage": self.random.randint(20, 80),
                "count": self.random.randint(3, 20),
                "industry": self.random.choice(self.repo.INDUSTRIES),
            }

            try:
                achievement = template.format(**params)
                achievements.append(achievement)
            except KeyError:
                logger.warning(f"Failed to format achievement template: {template}")

        return achievements

    def _generate_content(self, record: ResumeRecord) -> str:
        """Generate formatted resume content.

        Args:
            record: Resume record (content field not yet populated).

        Returns:
            Formatted resume text.
        """
        content = f"""
{record.name}
Level: {record.level}
Years of Experience: {record.years_experience}
Current Company: {record.current_company}

Technical Skills:
- {', '.join(record.tech_stack)}

Soft Skills:
- {', '.join(record.soft_skills)}

Work Location Preference: {record.location}

Professional Achievements:
"""
        for achievement in record.achievements:
            content += f"- {achievement}\n"

        if record.previous_companies:
            content += f"\nPrevious Companies: " f"{', '.join(record.previous_companies)}\n"

        return content.strip()

    def generate(self) -> ResumeRecord:
        """Generate a single resume record.

        Returns:
            A ResumeRecord with all fields populated.
        """
        self.resume_counter += 1

        level = self.random.choice(self.repo.LEVELS)
        years = self.repo.SALARY_RANGES[level][0] // 20000

        name = self._generate_name()
        current_company = self._generate_company_name()
        previous_companies = [
            self._generate_company_name() for _ in range(self.random.randint(1, 3))
        ]
        tech_stack = self._generate_tech_stack(level)
        soft_skills = self._generate_soft_skills()
        achievements = self._generate_achievements(tech_stack, level)
        location = self.random.choice(self.repo.LOCATIONS)

        record = ResumeRecord(
            id=f"resume_{self.resume_counter:06d}",
            name=name,
            level=level,
            years_experience=years,
            tech_stack=tech_stack,
            soft_skills=soft_skills,
            location=location,
            current_company=current_company,
            previous_companies=previous_companies,
            achievements=achievements,
            content="",  # Generated below
        )

        record.content = self._generate_content(record)
        return record
