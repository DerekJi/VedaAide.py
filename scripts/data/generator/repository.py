"""Shared data repository for consistent data generation."""

from typing import Dict, List


class DataRepository:
    """Central repository of all static data used for generating records.

    This class provides standardized lists of:
    - Technology stacks (backend, frontend, database, devops, cloud, ml)
    - Work locations (cities, remote)
    - Career levels and salary ranges
    - Soft skills and job types
    - Industries and company naming conventions
    - Experience and job description templates
    """

    # Technology stacks by category
    TECH_STACKS: Dict[str, List[str]] = {
        "backend": ["Python", "Java", "Go", "Rust", "Node.js", "C#", "PHP", "Ruby"],
        "frontend": ["React", "Vue.js", "Angular", "Svelte", "Next.js", "Flutter", "Swift"],
        "database": [
            "PostgreSQL",
            "MongoDB",
            "MySQL",
            "Redis",
            "Elasticsearch",
            "DynamoDB",
            "Cassandra",
        ],
        "devops": ["Docker", "Kubernetes", "Terraform", "Jenkins", "GitHub Actions", "ArgoCD"],
        "cloud": ["AWS", "Azure", "GCP", "Alibaba Cloud", "Tencent Cloud"],
        "ml": ["TensorFlow", "PyTorch", "Scikit-learn", "XGBoost", "LLaMA"],
    }

    # Work locations
    LOCATIONS: List[str] = [
        "Remote",
        "San Francisco, CA",
        "New York, NY",
        "Seattle, WA",
        "Austin, TX",
        "Boston, MA",
        "Beijing, China",
        "Shanghai, China",
        "Shenzhen, China",
        "Hangzhou, China",
        "London, UK",
        "Tokyo, Japan",
        "Singapore",
        "Toronto, Canada",
        "Sydney, Australia",
    ]

    # Career levels
    LEVELS: List[str] = ["Junior", "Mid-level", "Senior", "Lead", "Staff"]

    # Salary ranges by level (in USD)
    SALARY_RANGES: Dict[str, tuple] = {
        "Junior": (60000, 90000),
        "Mid-level": (90000, 150000),
        "Senior": (150000, 200000),
        "Lead": (180000, 250000),
        "Staff": (220000, 350000),
    }

    # Soft skills
    SOFT_SKILLS: List[str] = [
        "Leadership",
        "Communication",
        "Problem Solving",
        "Team Collaboration",
        "Project Management",
        "Mentoring",
        "Analytical Thinking",
        "Adaptability",
        "Attention to Detail",
        "Creativity",
    ]

    # Employment types
    JOB_TYPES: List[str] = ["Full-time", "Contract", "Part-time", "Freelance"]

    # Industries
    INDUSTRIES: List[str] = [
        "FinTech",
        "E-commerce",
        "Healthcare",
        "EdTech",
        "SaaS",
        "Gaming",
        "Social Media",
        "Cloud Computing",
        "AI/ML",
        "Cybersecurity",
    ]

    # Company naming components
    COMPANY_NAME_PREFIXES: List[str] = [
        "Tech",
        "Cloud",
        "Data",
        "Smart",
        "Cyber",
        "Digital",
        "Quantum",
        "Meta",
    ]
    COMPANY_NAME_SUFFIXES: List[str] = [
        "Corp",
        "Labs",
        "Systems",
        "Solutions",
        "Innovations",
        "Tech",
        "AI",
    ]

    # Experience description templates
    EXPERIENCE_TEMPLATES: List[str] = [
        "Led development of {tech} platform serving {users}+ users",
        "Built {tech} system handling {scale} events/second",
        "Implemented {tech} solution improving performance by {percentage}%",
        "Designed and architected {tech} infrastructure for {industry} industry",
        "Optimized {tech} pipeline reducing latency by {percentage}%",
        "Managed team of {count} engineers delivering {tech} project",
    ]

    # Job description templates
    JOB_DESCRIPTION_TEMPLATES: List[str] = [
        "We are looking for a {level} {role} to join our {team_name} team. "
        "You will work on {description}.",
        "Join {company} as a {role} and help us build {description}.",
        "Are you a talented {role}? We need someone to lead {description}.",
    ]
