#!/usr/bin/env python3
"""
数据生成系统：通过基础数据的排列组合生成大规模样例数据。

支持生成：
1. 简历数据（Resume）
2. 招聘岗位（Job Posting）
3. 技术问答对（Q&A Pairs）
"""

import json
import random
from typing import List, Dict, Any, Tuple
from pathlib import Path
from itertools import combinations, product
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta


# ============================================================================
# 基础数据库定义 - 用于排列组合
# ============================================================================

class DataRepository:
    """所有基础数据的仓库，用于生成排列组合"""
    
    # 技术栈
    TECH_STACKS = {
        "backend": ["Python", "Java", "Go", "Rust", "Node.js", "C#", "PHP", "Ruby"],
        "frontend": ["React", "Vue.js", "Angular", "Svelte", "Next.js", "Flutter", "Swift"],
        "database": ["PostgreSQL", "MongoDB", "MySQL", "Redis", "Elasticsearch", "DynamoDB", "Cassandra"],
        "devops": ["Docker", "Kubernetes", "Terraform", "Jenkins", "GitHub Actions", "ArgoCD"],
        "cloud": ["AWS", "Azure", "GCP", "Alibaba Cloud", "Tencent Cloud"],
        "ml": ["TensorFlow", "PyTorch", "Scikit-learn", "XGBoost", "LLaMA"],
    }
    
    # 工作地点
    LOCATIONS = [
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
    
    # 职级
    LEVELS = ["Junior", "Mid-level", "Senior", "Lead", "Staff"]
    
    # 薪资范围（按职级）
    SALARY_RANGES = {
        "Junior": (60000, 90000),
        "Mid-level": (90000, 150000),
        "Senior": (150000, 200000),
        "Lead": (180000, 250000),
        "Staff": (220000, 350000),
    }
    
    # 软技能
    SOFT_SKILLS = [
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
    
    # 工作类型
    JOB_TYPES = ["Full-time", "Contract", "Part-time", "Freelance"]
    
    # 行业
    INDUSTRIES = [
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
    
    # 公司名称模板
    COMPANY_NAME_PREFIXES = ["Tech", "Cloud", "Data", "Smart", "Cyber", "Digital", "Quantum", "Meta"]
    COMPANY_NAME_SUFFIXES = ["Corp", "Labs", "Systems", "Solutions", "Innovations", "Tech", "AI"]
    
    # 经验描述模板
    EXPERIENCE_TEMPLATES = [
        "Led development of {tech} platform serving {users}+ users",
        "Built {tech} system handling {scale} events/second",
        "Implemented {tech} solution improving performance by {percentage}%",
        "Designed and architected {tech} infrastructure for {industry} industry",
        "Optimized {tech} pipeline reducing latency by {percentage}%",
        "Managed team of {count} engineers delivering {tech} project",
    ]
    
    # 职位描述模板
    JOB_DESCRIPTION_TEMPLATES = [
        "We are looking for a {level} {role} to join our {team_name} team. You will work on {description}.",
        "Join {company} as a {role} and help us build {description}.",
        "Are you a talented {role}? We need someone to lead {description}.",
    ]


@dataclass
class ResumeRecord:
    """简历数据结构"""
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
    """招聘岗位数据结构"""
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


# ============================================================================
# 生成器类
# ============================================================================

class ResumeGenerator:
    """简历数据生成器"""
    
    def __init__(self, seed: int = None):
        self.random = random.Random(seed)
        self.resume_counter = 0
        self.repo = DataRepository()
        self.first_names = ["Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Grace", "Henry"]
        self.last_names = ["Smith", "Johnson", "Chen", "Wang", "Kumar", "Garcia", "Brown", "Lee"]
    
    def _generate_name(self) -> str:
        """生成随机名字"""
        first = self.random.choice(self.first_names)
        last = self.random.choice(self.last_names)
        return f"{first} {last}"
    
    def _generate_company_name(self) -> str:
        """生成公司名称"""
        prefix = self.random.choice(self.repo.COMPANY_NAME_PREFIXES)
        suffix = self.random.choice(self.repo.COMPANY_NAME_SUFFIXES)
        return f"{prefix}{suffix}"
    
    def _generate_tech_stack(self, level: str) -> List[str]:
        """根据职级生成技术栈"""
        num_skills = 5 if level in ["Junior", "Mid-level"] else 8
        all_techs = []
        for techs in self.repo.TECH_STACKS.values():
            all_techs.extend(techs)
        return self.random.sample(all_techs, min(num_skills, len(all_techs)))
    
    def _generate_soft_skills(self) -> List[str]:
        """生成软技能"""
        return self.random.sample(self.repo.SOFT_SKILLS, k=self.random.randint(3, 6))
    
    def _generate_achievements(self, tech_stack: List[str], level: str) -> List[str]:
        """生成成就描述"""
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
                pass
        
        return achievements
    
    def _generate_content(self, record: ResumeRecord) -> str:
        """生成完整的简历内容"""
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
            content += f"\nPrevious Companies: {', '.join(record.previous_companies)}\n"
        
        return content.strip()
    
    def generate(self) -> ResumeRecord:
        """生成一条简历记录"""
        self.resume_counter += 1
        
        level = self.random.choice(self.repo.LEVELS)
        years = self.repo.SALARY_RANGES[level][0] // 20000
        
        name = self._generate_name()
        current_company = self._generate_company_name()
        previous_companies = [
            self._generate_company_name() 
            for _ in range(self.random.randint(1, 3))
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
            content="",  # 稍后生成
        )
        
        record.content = self._generate_content(record)
        return record


class JobPostingGenerator:
    """招聘岗位生成器"""
    
    def __init__(self, seed: int = None):
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
            "Platform", "Infrastructure", "Analytics", "Backend", "Frontend",
            "Product", "AI/ML", "Data", "Cloud", "Security"
        ]
    
    def _generate_company_name(self) -> str:
        """生成公司名称"""
        prefix = self.random.choice(self.repo.COMPANY_NAME_PREFIXES)
        suffix = self.random.choice(self.repo.COMPANY_NAME_SUFFIXES)
        return f"{prefix}{suffix}"
    
    def _generate_tech_requirements(self, level: str) -> List[str]:
        """生成技术要求"""
        num_skills = 5 if level in ["Junior", "Mid-level"] else 7
        all_techs = []
        for techs in self.repo.TECH_STACKS.values():
            all_techs.extend(techs)
        return self.random.sample(all_techs, min(num_skills, len(all_techs)))
    
    def _generate_requirements(self, tech_stack: List[str], level: str) -> List[str]:
        """生成职位要求"""
        years_req = {
            "Junior": "0-2",
            "Mid-level": "3-5",
            "Senior": "6+",
            "Lead": "8+",
            "Staff": "10+",
        }
        
        requirements = [
            f"{years_req[level]} years of professional experience",
            f"Experience with {', '.join(self.random.sample(tech_stack, min(3, len(tech_stack))))}",
            "Strong problem-solving skills",
            "Experience with agile development",
        ]
        
        if level in ["Senior", "Lead", "Staff"]:
            requirements.extend([
                "Experience mentoring junior engineers",
                "Strong system design knowledge",
                "Experience with code reviews and technical discussions",
            ])
        
        return requirements
    
    def _generate_benefits(self) -> List[str]:
        """生成福利待遇"""
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
        """生成岗位描述"""
        descriptions = [
            f"building scalable {industry} solutions",
            f"leading {team} team initiatives",
            f"solving complex technical challenges",
            f"mentoring team members",
            f"architecting next-generation systems",
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
        """生成一条招聘岗位记录"""
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


# ============================================================================
# 数据导出器
# ============================================================================

class DataExporter:
    """数据导出为标准格式"""
    
    @staticmethod
    def to_jsonl(records: List[Any], output_file: str):
        """导出为JSONL格式（支持大文件）"""
        with open(output_file, 'w', encoding='utf-8') as f:
            for record in records:
                if isinstance(record, (ResumeRecord, JobPostingRecord)):
                    json_str = json.dumps(asdict(record), ensure_ascii=False)
                else:
                    json_str = json.dumps(record, ensure_ascii=False)
                f.write(json_str + '\n')
        print(f"✓ Exported {len(records)} records to {output_file}")
    
    @staticmethod
    def to_json(records: List[Any], output_file: str):
        """导出为JSON格式"""
        data = []
        for record in records:
            if isinstance(record, (ResumeRecord, JobPostingRecord)):
                data.append(asdict(record))
            else:
                data.append(record)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✓ Exported {len(records)} records to {output_file}")


# ============================================================================
# 主程序
# ============================================================================

def main():
    """演示数据生成"""
    import argparse
    
    parser = argparse.ArgumentParser(description="生成大规模样例数据")
    parser.add_argument("--resumes", type=int, default=100, help="生成简历数量")
    parser.add_argument("--jobs", type=int, default=100, help="生成岗位数量")
    parser.add_argument("--output-dir", default="data/generated", help="输出目录")
    parser.add_argument("--format", choices=["json", "jsonl"], default="jsonl", help="输出格式")
    parser.add_argument("--seed", type=int, default=None, help="随机种子")
    
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🚀 开始生成样例数据...")
    print(f"   简历: {args.resumes} 条")
    print(f"   岗位: {args.jobs} 条")
    print(f"   格式: {args.format}")
    
    # 生成简历
    print("\n📄 生成简历数据...")
    resume_gen = ResumeGenerator(seed=args.seed)
    resumes = [resume_gen.generate() for _ in range(args.resumes)]
    
    resume_file = output_dir / f"resumes.{args.format}"
    if args.format == "jsonl":
        DataExporter.to_jsonl(resumes, str(resume_file))
    else:
        DataExporter.to_json(resumes, str(resume_file))
    
    # 生成岗位
    print("\n💼 生成岗位数据...")
    job_gen = JobPostingGenerator(seed=args.seed)
    jobs = [job_gen.generate() for _ in range(args.jobs)]
    
    job_file = output_dir / f"jobs.{args.format}"
    if args.format == "jsonl":
        DataExporter.to_jsonl(jobs, str(job_file))
    else:
        DataExporter.to_json(jobs, str(job_file))
    
    print(f"\n✅ 完成！数据已保存到 {output_dir}/")


if __name__ == "__main__":
    main()
