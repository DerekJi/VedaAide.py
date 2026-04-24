#!/usr/bin/env python3
"""
演示脚本：快速测试数据生成系统

运行此脚本将生成：
- 1000条样例简历
- 500条样例岗位
- 展示生成的数据格式和统计信息
"""

import json
import sys
from pathlib import Path
from collections import Counter
from typing import List, Dict, Any

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.data.data_generator import ResumeGenerator, JobPostingGenerator, DataExporter
from scripts.data.advanced_generator import (
    AdvancedDataGenerator, PresetConfigs, ConfigManager
)


def print_section(title: str):
    """打印章节标题"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def demo_basic_generation():
    """演示基础数据生成"""
    print_section("演示1：基础数据生成器")
    
    print("\n📄 生成100条简历...")
    resume_gen = ResumeGenerator(seed=42)
    resumes = [resume_gen.generate() for _ in range(100)]
    
    print(f"✓ 生成完成！样本简历：")
    sample_resume = resumes[0]
    print(f"  - ID: {sample_resume.id}")
    print(f"  - 名字: {sample_resume.name}")
    print(f"  - 职级: {sample_resume.level}")
    print(f"  - 工作年限: {sample_resume.years_experience}")
    print(f"  - 技术栈: {', '.join(sample_resume.tech_stack)}")
    print(f"  - 软技能: {', '.join(sample_resume.soft_skills)}")
    print(f"  - 位置: {sample_resume.location}")
    
    print(f"\n📊 职级分布:")
    level_counter = Counter(r.level for r in resumes)
    for level, count in sorted(level_counter.items()):
        print(f"  - {level}: {count} ({count/len(resumes)*100:.1f}%)")
    
    print(f"\n💼 生成50条岗位...")
    job_gen = JobPostingGenerator(seed=42)
    jobs = [job_gen.generate() for _ in range(50)]
    
    print(f"✓ 生成完成！样本岗位：")
    sample_job = jobs[0]
    print(f"  - ID: {sample_job.id}")
    print(f"  - 标题: {sample_job.title}")
    print(f"  - 公司: {sample_job.company}")
    print(f"  - 位置: {sample_job.location}")
    print(f"  - 职级: {sample_job.level}")
    print(f"  - 薪资: ${sample_job.salary_min:,} - ${sample_job.salary_max:,}")
    print(f"  - 技术要求: {', '.join(sample_job.tech_stack)}")
    
    # 保存到文件
    output_dir = Path("data/generated_demo")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    DataExporter.to_jsonl(resumes, str(output_dir / "resumes_basic.jsonl"))
    DataExporter.to_jsonl(jobs, str(output_dir / "jobs_basic.jsonl"))
    
    return output_dir


def demo_advanced_generation():
    """演示高级排列组合生成"""
    print_section("演示2：高级排列组合生成器")
    
    print("\n🎯 使用'技术栈'预设配置...")
    config = PresetConfigs.create_tech_stack_config(preset="balanced")
    
    print(f"  - 简历数量: {config.resume_count}")
    print(f"  - 岗位数量: {config.job_count}")
    
    print("\n📊 配置维度信息：")
    print("  简历维度：")
    for name, dim in config.resume_dimensions.items():
        print(f"    - {name}:")
        print(f"      值: {dim.values[:3]}... (共{len(dim.values)}个)")
        print(f"      权重: {'是' if dim.weights else '否'}")
        print(f"      选择范围: {dim.count_range[0]}-{dim.count_range[1]}")
    
    print("\n🚀 生成10000条简历和5000条岗位（使用排列组合）...")
    generator = AdvancedDataGenerator(config, seed=42)
    
    # 创建小规模配置用于演示
    demo_config = PresetConfigs.create_tech_stack_config()
    demo_config.resume_count = 10000
    demo_config.job_count = 5000
    
    demo_generator = AdvancedDataGenerator(demo_config, seed=42)
    
    print("  生成简历中...")
    resumes = demo_generator.generate_resume_batch(10000)
    
    print("  生成岗位中...")
    jobs = demo_generator.generate_job_batch(5000)
    
    print(f"\n✓ 生成完成！")
    print(f"  - 简历: {len(resumes)} 条")
    print(f"  - 岗位: {len(jobs)} 条")
    
    # 分析简历数据
    print(f"\n📈 生成的简历数据分析：")
    
    sample_resume = resumes[0]
    print(f"\n  样本简历 ID: {sample_resume['id']}")
    print(f"  维度示例：")
    for key, value in list(sample_resume.items())[:5]:
        if key != 'id' and key != 'generated_at':
            value_str = str(value)[:60]
            print(f"    - {key}: {value_str}")
    
    # 统计技术栈频率
    all_skills = []
    for resume in resumes:
        if 'tech_stack' in resume:
            all_skills.extend(resume['tech_stack'])
    
    skill_counter = Counter(all_skills)
    print(f"\n  Top 10 技术栈：")
    for skill, count in skill_counter.most_common(10):
        print(f"    - {skill}: {count} ({count/len(all_skills)*100:.1f}%)")
    
    # 分析岗位数据
    print(f"\n📊 生成的岗位数据分析：")
    
    sample_job = jobs[0]
    print(f"\n  样本岗位 ID: {sample_job['id']}")
    print(f"  维度示例：")
    for key, value in list(sample_job.items())[:5]:
        if key != 'id' and key != 'generated_at':
            value_str = str(value)[:60]
            print(f"    - {key}: {value_str}")
    
    # 保存到文件
    output_dir = Path("data/generated_demo")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / "resumes_advanced_demo.jsonl", 'w') as f:
        for resume in resumes:
            f.write(json.dumps(resume, ensure_ascii=False) + '\n')
    
    with open(output_dir / "jobs_advanced_demo.jsonl", 'w') as f:
        for job in jobs:
            f.write(json.dumps(job, ensure_ascii=False) + '\n')
    
    print(f"\n✓ 已保存到 {output_dir}")
    
    return output_dir


def demo_matching_config():
    """演示匹配配置生成"""
    print_section("演示3：针对匹配度测试的配置")
    
    print("\n🎯 使用'匹配度'预设配置...")
    config = PresetConfigs.create_matching_config()
    
    # 展示配置维度
    print("\n📝 配置维度（用于测试简历-岗位匹配）：")
    print("\n  简历维度：")
    for name, dim in config.resume_dimensions.items():
        print(f"    - {name}: {dim.values[:5]}...")
    
    print("\n  岗位维度：")
    for name, dim in config.job_dimensions.items():
        print(f"    - {name}: {dim.values[:5]}...")
    
    # 生成小规模数据
    print("\n🚀 生成2000条简历和1000条岗位...")
    
    small_config = PresetConfigs.create_matching_config()
    small_config.resume_count = 2000
    small_config.job_count = 1000
    
    generator = AdvancedDataGenerator(small_config, seed=42)
    resumes = generator.generate_resume_batch(2000)
    jobs = generator.generate_job_batch(1000)
    
    print(f"✓ 生成完成！")
    
    # 示例匹配
    print(f"\n🔍 匹配度示例分析：")
    
    sample_resume = resumes[0]
    sample_job = jobs[0]
    
    resume_skills = set(sample_resume.get('skills', []))
    job_skills = set(sample_job.get('required_skills', []))
    
    if resume_skills and job_skills:
        matched = resume_skills & job_skills
        match_rate = len(matched) / len(job_skills) * 100 if job_skills else 0
        
        print(f"\n  简历技能: {resume_skills}")
        print(f"  岗位要求: {job_skills}")
        print(f"  匹配技能: {matched}")
        print(f"  匹配率: {match_rate:.1f}%")
    
    return Path("data/generated_demo")


def demo_config_management():
    """演示配置管理"""
    print_section("演示4：配置管理")
    
    print("\n💾 保存配置文件...")
    config = PresetConfigs.create_tech_stack_config()
    
    config_dir = Path("data/configs_demo")
    config_dir.mkdir(parents=True, exist_ok=True)
    
    config_file = config_dir / "sample_config.json"
    ConfigManager.save_config(config, str(config_file))
    
    print(f"✓ 配置已保存到: {config_file}")
    
    # 显示配置内容
    print(f"\n📄 配置文件内容 (摘取)：")
    with open(config_file) as f:
        config_data = json.load(f)
    
    print(f"  - resume_dimensions: {len(config_data['resume_dimensions'])} 个维度")
    print(f"  - job_dimensions: {len(config_data['job_dimensions'])} 个维度")
    print(f"  - resume_count: {config_data['resume_count']}")
    print(f"  - job_count: {config_data['job_count']}")
    
    # 加载配置
    print(f"\n📖 加载配置文件...")
    loaded_config = ConfigManager.load_config(str(config_file))
    print(f"✓ 配置已加载，包含 {len(loaded_config.resume_dimensions)} 个维度")


def print_statistics(output_dir: Path):
    """打印统计信息"""
    print_section("生成统计")
    
    total_size = 0
    total_files = 0
    
    for file in output_dir.glob("*.jsonl"):
        size = file.stat().st_size
        lines = sum(1 for _ in open(file))
        total_size += size
        total_files += 1
        
        print(f"✓ {file.name}")
        print(f"  - 行数: {lines:,}")
        print(f"  - 大小: {size/1024/1024:.2f} MB")
        print()
    
    print(f"总计:")
    print(f"  - 文件数: {total_files}")
    print(f"  - 总大小: {total_size/1024/1024:.2f} MB")


def main():
    """主程序"""
    print("\n" + "="*70)
    print("  🎉 VedaAide 数据生成系统演示")
    print("="*70)
    
    try:
        # 演示1：基础生成
        demo_basic_generation()
        
        # 演示2：高级排列组合生成
        demo_advanced_generation()
        
        # 演示3：匹配配置
        demo_matching_config()
        
        # 演示4：配置管理
        demo_config_management()
        
        # 统计
        output_dir = Path("data/generated_demo")
        print_statistics(output_dir)
        
        print("\n" + "="*70)
        print("  ✅ 演示完成！")
        print("="*70)
        
        print("\n📚 下一步：")
        print("  1. 查看生成的数据：")
        print(f"     cat data/generated_demo/resumes_basic.jsonl | head -1 | jq .")
        print()
        print("  2. 生成大规模数据：")
        print("     poetry run python scripts/data/advanced_generator.py \\")
        print("         --preset tech_stack \\")
        print("         --resumes 100000 \\")
        print("         --jobs 50000")
        print()
        print("  3. 查看完整指南：")
        print("     scripts/data/GENERATOR_GUIDE.md")
        print()
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
