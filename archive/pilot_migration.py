#!/usr/bin/env python3
"""
Pilot Migration Script: AI-Assisted Development Category
Tests unified taxonomy approach on high-impact category
"""
import json
import re
from pathlib import Path
from typing import Dict, List

def load_reddit_posts() -> List[Dict]:
    """Load and parse Reddit classification data"""
    reddit_file = Path("reddit_classifications.md")
    content = reddit_file.read_text()
    
    posts = []
    # Split by post headers (numbered entries)
    post_sections = re.split(r'\n\d+\. \*\*([^*]+)\*\* \(([^)]+)\)', content)[1:]  # Skip first empty section
    
    for i in range(0, len(post_sections), 3):  # Title, ID, Content groups
        if i + 2 < len(post_sections):
            title = post_sections[i]
            post_id = post_sections[i + 1] 
            content_block = post_sections[i + 2]
            
            # Extract current classifications
            topics_match = re.search(r'   - Topics: `([^`]+)`(?:, `([^`]+)`)?(?:, `([^`]+)`)?', content_block)
            domain_match = re.search(r'   - Domain: `([^`]+)`', content_block)
            audience_match = re.search(r'   - Audience: `([^`]+)`(?:, `([^`]+)`)?(?:, `([^`]+)`)?', content_block)
            summary_match = re.search(r'   - \*\*Summary\*\*: (.+)', content_block)
            
            # Parse topics
            topics = []
            if topics_match:
                for j in range(1, 4):  # Up to 3 topics
                    if topics_match.group(j):
                        topics.append(topics_match.group(j))
            
            # Parse audiences  
            audiences = []
            if audience_match:
                for j in range(1, 4):  # Up to 3 audiences
                    if audience_match.group(j):
                        audiences.append(audience_match.group(j))
            
            posts.append({
                'title': title,
                'id': post_id,
                'summary': summary_match.group(1) if summary_match else '',
                'topics': topics,
                'domain': domain_match.group(1) if domain_match else '',
                'audiences': audiences,
                'content_block': content_block,
                'platform': 'reddit'
            })
    
    return posts

def load_youtube_chapters() -> List[Dict]:
    """Load and parse YouTube classification data"""
    youtube_file = Path("youtube_classifications.md")
    content = youtube_file.read_text()
    
    chapters = []
    # Split by chapter headers
    chapter_sections = re.split(r'\n### Chapter \d+: ([^[]+)\[([^\]]+)\]', content)[1:]
    
    for i in range(0, len(chapter_sections), 3):
        if i + 2 < len(chapter_sections):
            title = chapter_sections[i].strip()
            timestamp = chapter_sections[i + 1]
            content_block = chapter_sections[i + 2]
            
            # Extract classifications
            topic_match = re.search(r'\*\*Topic\*\*: (.+)', content_block)
            domain_match = re.search(r'\*\*Domain\*\*: (.+)', content_block)
            audience_match = re.search(r'\*\*Audience\*\*: (.+)', content_block)
            summary_match = re.search(r'\*\*Summary\*\*: (.+)', content_block)
            
            chapters.append({
                'title': title,
                'timestamp': timestamp,
                'summary': summary_match.group(1) if summary_match else '',
                'topic': topic_match.group(1) if topic_match else '',
                'domain': domain_match.group(1) if domain_match else '',
                'audience': audience_match.group(1) if audience_match else '',
                'content_block': content_block,
                'platform': 'youtube'
            })
    
    return chapters

def is_ai_assisted_development(item: Dict) -> bool:
    """Determine if content should be classified as ai-assisted-development"""
    
    # For Reddit posts
    if item['platform'] == 'reddit':
        topics = item['topics']
        summary = item['summary'].lower()
        title = item['title'].lower()
        
        # Check for AI/ML development indicators
        ai_keywords = ['llm', 'language model', 'ai', 'chatbot', 'prompt', 'rag', 'embedding', 'neural', 'nlp']
        development_keywords = ['build', 'develop', 'implement', 'deploy', 'code', 'tool', 'application', 'project']
        
        has_ai = any(keyword in summary + title for keyword in ai_keywords)
        has_development = any(keyword in summary + title for keyword in development_keywords)
        has_nlp_topic = 'nlp-applications' in topics
        
        return (has_ai and has_development) or has_nlp_topic
    
    # For YouTube chapters
    else:
        return item['topic'] == 'AI-Assisted Development'

def migrate_to_unified_taxonomy(item: Dict) -> Dict | None:
    """Migrate item to unified taxonomy if it qualifies"""
    
    if not is_ai_assisted_development(item):
        return None
    
    migrated = item.copy()
    
    # Unified topic
    migrated['unified_topic'] = 'ai-assisted-development'
    
    # Unified domain mapping
    if item['platform'] == 'reddit':
        if item['domain'] == 'general-tech':
            migrated['unified_domain'] = 'ai-ml'
        else:
            migrated['unified_domain'] = item['domain']  # Keep specific domains
    else:  # YouTube
        if item['domain'] in ['AI/ML', 'Technology/AI Industry', 'Technology/AI Applications']:
            migrated['unified_domain'] = 'ai-ml'
        elif 'Software Engineering' in item['domain']:
            migrated['unified_domain'] = 'software-engineering'
        else:
            migrated['unified_domain'] = 'ai-ml'  # Default for AI-assisted content
    
    # Unified audience mapping  
    if item['platform'] == 'reddit':
        audiences = item['audiences']
        unified_audiences = []
        for audience in audiences:
            if audience == 'practitioners':
                unified_audiences.append('practitioners')
            elif audience == 'beginners':
                unified_audiences.append('beginners') 
            elif audience == 'researchers':
                unified_audiences.append('researchers-academics')
            elif audience == 'managers':
                unified_audiences.append('managers-leads')
            else:
                unified_audiences.append(audience)  # Keep others as-is
        migrated['unified_audiences'] = unified_audiences
    else:  # YouTube
        audience = item['audience']
        if 'AI Engineers' in audience:
            migrated['unified_audiences'] = ['practitioners', 'developers']
        elif 'Software Engineers' in audience:
            migrated['unified_audiences'] = ['practitioners', 'developers']
        elif 'Professional/Developer' in audience:
            migrated['unified_audiences'] = ['practitioners']
        elif 'Students' in audience:
            migrated['unified_audiences'] = ['beginners']
        else:
            migrated['unified_audiences'] = ['practitioners']  # Default
    
    return migrated

def generate_migration_report(reddit_posts: List[Dict], youtube_chapters: List[Dict], 
                            migrated_reddit: List[Dict], migrated_youtube: List[Dict]):
    """Generate detailed migration report"""
    
    report = []
    report.append("# AI-Assisted Development Pilot Migration Report")
    report.append("*Generated on September 14, 2025*\n")
    
    report.append("## Migration Summary")
    report.append(f"- **Reddit Posts Analyzed**: {len(reddit_posts)}")
    report.append(f"- **Reddit Posts Migrated**: {len(migrated_reddit)} ({len(migrated_reddit)/len(reddit_posts)*100:.1f}%)")
    report.append(f"- **YouTube Chapters Analyzed**: {len(youtube_chapters)}")
    report.append(f"- **YouTube Chapters Migrated**: {len(migrated_youtube)} ({len(migrated_youtube)/len(youtube_chapters)*100:.1f}%)")
    report.append(f"- **Total Unified Content**: {len(migrated_reddit) + len(migrated_youtube)}\n")
    
    report.append("## Reddit Migrations")
    for item in migrated_reddit:
        report.append(f"### {item['title']} ({item['id']})")
        report.append(f"**Original Topics**: {', '.join(item['topics'])}")
        report.append(f"**Unified Topic**: {item['unified_topic']}")
        report.append(f"**Original Domain**: {item['domain']}")
        report.append(f"**Unified Domain**: {item['unified_domain']}")
        report.append(f"**Original Audiences**: {', '.join(item['audiences'])}")
        report.append(f"**Unified Audiences**: {', '.join(item['unified_audiences'])}")
        report.append(f"**Summary**: {item['summary'][:100]}...\n")
    
    report.append("## YouTube Migrations")
    for item in migrated_youtube:
        report.append(f"### {item['title']}")
        report.append(f"**Original Topic**: {item['topic']}")
        report.append(f"**Unified Topic**: {item['unified_topic']}")
        report.append(f"**Original Domain**: {item['domain']}")
        report.append(f"**Unified Domain**: {item['unified_domain']}")
        report.append(f"**Original Audience**: {item['audience']}")
        report.append(f"**Unified Audiences**: {', '.join(item['unified_audiences'])}")
        report.append(f"**Summary**: {item['summary'][:100]}...\n")
    
    return '\n'.join(report)

def main():
    print("Starting AI-Assisted Development Pilot Migration...")
    
    # Load data
    print("Loading Reddit posts...")
    reddit_posts = load_reddit_posts()
    print(f"Loaded {len(reddit_posts)} Reddit posts")
    
    print("Loading YouTube chapters...")
    youtube_chapters = load_youtube_chapters()
    print(f"Loaded {len(youtube_chapters)} YouTube chapters")
    
    # Run migration
    print("Analyzing content for AI-assisted development classification...")
    migrated_reddit = []
    migrated_youtube = []
    
    for post in reddit_posts:
        migrated = migrate_to_unified_taxonomy(post)
        if migrated:
            migrated_reddit.append(migrated)
    
    for chapter in youtube_chapters:
        migrated = migrate_to_unified_taxonomy(chapter)
        if migrated:
            migrated_youtube.append(migrated)
    
    print(f"Migrated {len(migrated_reddit)} Reddit posts and {len(migrated_youtube)} YouTube chapters")
    
    # Generate report
    report = generate_migration_report(reddit_posts, youtube_chapters, migrated_reddit, migrated_youtube)
    
    # Save report
    report_file = Path("pilot_migration_report.md")
    report_file.write_text(report)
    print(f"Migration report saved to {report_file}")
    
    # Save migrated data as JSON for further analysis
    migration_data = {
        'reddit': migrated_reddit,
        'youtube': migrated_youtube,
        'summary': {
            'total_reddit_analyzed': len(reddit_posts),
            'total_youtube_analyzed': len(youtube_chapters),
            'reddit_migrated': len(migrated_reddit),
            'youtube_migrated': len(migrated_youtube),
            'unified_content_count': len(migrated_reddit) + len(migrated_youtube)
        }
    }
    
    json_file = Path("pilot_migration_data.json")
    json_file.write_text(json.dumps(migration_data, indent=2))
    print(f"Migration data saved to {json_file}")

if __name__ == "__main__":
    main()