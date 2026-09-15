#!/usr/bin/env python3
"""
Hacker News Show HN Idea & Open-Source Code Miner Pipeline
Leverages the 100% Free, Zero-Auth Official Algolia HN API.
Mines Show HN projects, open-source GitHub repositories, architecture patterns, and founder launch texts.
"""

import sys
import os
import json
import re
import argparse
import urllib.request
import urllib.parse
from datetime import datetime
from typing import List, Dict, Any, Optional

ALGOLIA_SEARCH_URL = "https://hn.algolia.com/api/v1/search"
ALGOLIA_DATE_URL = "https://hn.algolia.com/api/v1/search_by_date"
HN_ITEM_URL = "https://hn.algolia.com/api/v1/items/"

class HNIdeaMiner:
    def __init__(self):
        self.headers = {"User-Agent": "HNIdeaMiner/1.0"}

    def search_show_hn(
        self,
        query: str = "",
        min_points: int = 15,
        min_comments: int = 0,
        github_only: bool = False,
        sort_by_date: bool = False,
        limit: int = 25
    ) -> List[Dict[str, Any]]:
        """
        Queries the free Algolia HN API for Show HN projects.
        """
        base_url = ALGOLIA_DATE_URL if sort_by_date else ALGOLIA_SEARCH_URL
        
        numeric_filters = []
        if min_points > 0:
            numeric_filters.append(f"points>={min_points}")
        if min_comments > 0:
            numeric_filters.append(f"num_comments>={min_comments}")

        params = {
            "tags": "show_hn",
            "hitsPerPage": min(limit * 3, 100),
        }
        if query:
            params["query"] = query
        if numeric_filters:
            params["numericFilters"] = ",".join(numeric_filters)

        url = f"{base_url}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers=self.headers)
        
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"Error connecting to HN API: {e}", file=sys.stderr)
            return []

        results = []
        github_pattern = re.compile(r"https?://github\.com/[a-zA-Z0-9_\-\.]+/[a-zA-Z0-9_\-\.]+")

        for hit in data.get("hits", []):
            title = hit.get("title", "")
            raw_url = hit.get("url", "")
            story_text = hit.get("story_text") or ""
            object_id = hit.get("objectID")
            points = hit.get("points") or 0
            num_comments = hit.get("num_comments") or 0
            author = hit.get("author", "")
            created_at = hit.get("created_at", "")

            # Detect GitHub links in url or story_text
            github_matches = set(github_pattern.findall(raw_url) + github_pattern.findall(story_text))
            github_url = list(github_matches)[0] if github_matches else (raw_url if "github.com" in raw_url else None)

            if github_only and not github_url:
                continue

            cleaned_title = title.replace("Show HN: ", "").replace("Show HN : ", "")

            results.append({
                "hn_id": object_id,
                "title": cleaned_title,
                "project_url": raw_url or f"https://news.ycombinator.com/item?id={object_id}",
                "github_url": github_url,
                "points": points,
                "num_comments": num_comments,
                "author": author,
                "created_at": created_at,
                "founder_pitch": story_text[:500] + "..." if len(story_text) > 500 else story_text,
                "hn_discussion_url": f"https://news.ycombinator.com/item?id={object_id}"
            })

            if len(results) >= limit:
                break

        return results

    def fetch_top_comments(self, hn_id: str, limit: int = 3) -> List[str]:
        """Fetches top insightful community comments for a given HN submission."""
        url = f"{HN_ITEM_URL}{hn_id}"
        req = urllib.request.Request(url, headers=self.headers)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                item = json.loads(resp.read().decode("utf-8"))
            
            comments = []
            for child in item.get("children", [])[:limit]:
                text = child.get("text", "")
                if text:
                    clean = re.sub(r"<[^>]+>", " ", text)
                    comments.append(clean.strip())
            return comments
        except Exception:
            return []

    def export_markdown_report(self, items: List[Dict[str, Any]], query: str, output_path: str):
        """Generates a clean markdown briefing of mined ideas and repos."""
        topic = query if query else "Top Trending Show HN"
        lines = [
            f"# Hacker News Show HN Intelligence Report: {topic}",
            f"Generated on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC",
            f"Total Projects Mined: {len(items)}\n",
            "| Points | Comments | Project Title | Open Source GitHub | Live Demo / Discussion |",
            "| :---: | :---: | :--- | :--- | :--- |"
        ]

        for it in items:
            gh_link = f"[GitHub Repo]({it['github_url']})" if it['github_url'] else "Proprietary / Closed"
            lines.append(
                f"| **{it['points']}** | {it['num_comments']} | **{it['title']}** | {gh_link} | [HN Discussion]({it['hn_discussion_url']}) |"
            )

        lines.append("\n---\n## Project Deep Dives & Founder Launch Pitches\n")
        for it in items:
            lines.append(f"### {it['title']}")
            lines.append(f"- **Points:** {it['points']} | **Comments:** {it['num_comments']} | **Author:** `{it['author']}` | **Date:** {it['created_at'][:10]}")
            if it['github_url']:
                lines.append(f"- **Code Repository:** {it['github_url']}")
            lines.append(f"- **Project URL:** {it['project_url']}")
            lines.append(f"- **Discussion:** {it['hn_discussion_url']}")
            if it['founder_pitch']:
                lines.append(f"\n> **Founder Launch Pitch:**\n> {it['founder_pitch']}\n")
            lines.append("---\n")

        with open(output_path, "w") as f:
            f.write("\n".join(lines))
        print(f"Report successfully saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Mine Hacker News Show HN projects, ideas, and open source code.")
    parser.add_argument("-q", "--query", type=str, default="", help="Keyword to search (e.g. satellite, carbon, procurement, rust, agent)")
    parser.add_argument("-p", "--min-points", type=int, default=15, help="Minimum HN points/upvotes (default: 15)")
    parser.add_argument("-c", "--min-comments", type=int, default=0, help="Minimum comments count (default: 0)")
    parser.add_argument("--github-only", action="store_true", help="Only show projects with open-source GitHub repos")
    parser.add_argument("--latest", action="store_true", help="Sort by latest submissions instead of popularity")
    parser.add_argument("-l", "--limit", type=int, default=10, help="Max results to return (default: 10)")
    parser.add_argument("-o", "--output", type=str, default="", help="Path to export Markdown report")

    args = parser.parse_args()

    miner = HNIdeaMiner()
    print(f"\n🔍 Mining Hacker News Show HN for query: '{args.query or 'ALL'}' (Min Points: {args.min_points}, GitHub only: {args.github_only})...\n")
    
    results = miner.search_show_hn(
        query=args.query,
        min_points=args.min_points,
        min_comments=args.min_comments,
        github_only=args.github_only,
        sort_by_date=args.latest,
        limit=args.limit
    )

    if not results:
        print("No matching projects found with current filters.")
        return

    print(f"✅ Found {len(results)} high-signal projects:\n")
    for idx, r in enumerate(results, 1):
        print(f"{idx}. [{r['points']} pts | {r['num_comments']} comments] {r['title']}")
        if r['github_url']:
            print(f"   📦 GitHub: {r['github_url']}")
        print(f"   🌐 URL: {r['project_url']}")
        print(f"   💬 Discussion: {r['hn_discussion_url']}")
        if r['founder_pitch']:
            print(f"   💡 Pitch snippet: {r['founder_pitch'][:150]}...")
        print()

    if args.output:
        miner.export_markdown_report(results, args.query, args.output)

if __name__ == "__main__":
    main()
