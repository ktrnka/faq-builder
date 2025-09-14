#!/usr/bin/env python3
"""
Script to analyze classifications from Reddit and YouTube data
"""
import re
from collections import Counter
from pathlib import Path

def extract_reddit_classifications():
    """Extract all classifications from Reddit data"""
    reddit_file = Path("reddit_classifications.md")
    content = reddit_file.read_text()
    
    topics = []
    domains = []
    audiences = []
    
    # Extract all Topics lines
    topic_matches = re.findall(r'   - Topics: `([^`]+)`(?:, `([^`]+)`)?(?:, `([^`]+)`)?', content)
    for match in topic_matches:
        for topic in match:
            if topic:  # Skip empty matches
                topics.append(topic)
    
    # Extract all Domain lines
    domain_matches = re.findall(r'   - Domain: `([^`]+)`', content)
    domains.extend(domain_matches)
    
    # Extract all Audience lines
    audience_matches = re.findall(r'   - Audience: `([^`]+)`(?:, `([^`]+)`)?(?:, `([^`]+)`)?', content)
    for match in audience_matches:
        for audience in match:
            if audience:  # Skip empty matches
                audiences.append(audience)
    
    return topics, domains, audiences

def extract_youtube_classifications():
    """Extract all classifications from YouTube data"""
    youtube_file = Path("youtube_classifications.md")
    content = youtube_file.read_text()
    
    topics = []
    domains = []
    audiences = []
    
    # Extract all Topic lines
    topic_matches = re.findall(r'\*\*Topic\*\*: (.+)', content)
    topics.extend(topic_matches)
    
    # Extract all Domain lines
    domain_matches = re.findall(r'\*\*Domain\*\*: (.+)', content)
    domains.extend(domain_matches)
    
    # Extract all Audience lines
    audience_matches = re.findall(r'\*\*Audience\*\*: (.+)', content)
    audiences.extend(audience_matches)
    
    return topics, domains, audiences

def main():
    print("=== REDDIT ANALYSIS ===")
    reddit_topics, reddit_domains, reddit_audiences = extract_reddit_classifications()
    
    print(f"Reddit posts: {len(reddit_domains)}")
    print(f"Reddit total topics: {len(reddit_topics)}")
    print(f"Reddit total audiences: {len(reddit_audiences)}")
    
    print("\nReddit Topic Distribution:")
    topic_counts = Counter(reddit_topics)
    for topic, count in topic_counts.most_common():
        print(f"  {topic}: {count}")
    
    print("\nReddit Domain Distribution:")
    domain_counts = Counter(reddit_domains)
    for domain, count in domain_counts.most_common():
        print(f"  {domain}: {count}")
    
    print("\nReddit Audience Distribution:")
    audience_counts = Counter(reddit_audiences)
    for audience, count in audience_counts.most_common():
        print(f"  {audience}: {count}")
    
    print("\n\n=== YOUTUBE ANALYSIS ===")
    youtube_topics, youtube_domains, youtube_audiences = extract_youtube_classifications()
    
    print(f"YouTube chapters: {len(youtube_domains)}")
    print(f"YouTube total topics: {len(youtube_topics)}")
    print(f"YouTube total audiences: {len(youtube_audiences)}")
    
    print("\nYouTube Topic Distribution:")
    topic_counts = Counter(youtube_topics)
    for topic, count in topic_counts.most_common():
        print(f"  {topic}: {count}")
    
    print("\nYouTube Domain Distribution:")
    domain_counts = Counter(youtube_domains)
    for domain, count in domain_counts.most_common():
        print(f"  {domain}: {count}")
    
    print("\nYouTube Audience Distribution:")
    audience_counts = Counter(youtube_audiences)
    for audience, count in audience_counts.most_common():
        print(f"  {audience}: {count}")

if __name__ == "__main__":
    main()