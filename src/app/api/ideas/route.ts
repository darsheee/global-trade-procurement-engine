import { NextResponse } from "next/server";

const ALGOLIA_SEARCH_URL = "https://hn.algolia.com/api/v1/search";
const ALGOLIA_DATE_URL = "https://hn.algolia.com/api/v1/search_by_date";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const query = searchParams.get("q") || "";
  const minPoints = Number(searchParams.get("minPoints") || "15");
  const githubOnly = searchParams.get("githubOnly") === "true";
  const sortByDate = searchParams.get("sortByDate") === "true";
  const limit = Math.min(Number(searchParams.get("limit") || "20"), 50);

  const baseUrl = sortByDate ? ALGOLIA_DATE_URL : ALGOLIA_SEARCH_URL;
  const numericFilters = [`points>=${minPoints}`];

  const params = new URLSearchParams({
    tags: "show_hn",
    hitsPerPage: String(limit * 2),
    numericFilters: numericFilters.join(",")
  });

  if (query) {
    params.set("query", query);
  }

  try {
    const res = await fetch(`${baseUrl}?${params.toString()}`, {
      headers: { "User-Agent": "HNIdeaMiner/NextApp" }
    });

    if (!res.ok) {
      return NextResponse.json({ error: "Failed to fetch from HN API" }, { status: 502 });
    }

    const data = await res.json();
    const githubRegex = /https?:\/\/github\.com\/[a-zA-Z0-9_\-\.]+\/[a-zA-Z0-9_\-\.]+/;

    const results = [];
    for (const hit of data.hits || []) {
      const rawUrl = hit.url || "";
      const storyText = hit.story_text || "";
      const ghMatch = rawUrl.match(githubRegex) || storyText.match(githubRegex);
      const githubUrl = ghMatch ? ghMatch[0] : null;

      if (githubOnly && !githubUrl) continue;

      results.push({
        hnId: hit.objectID,
        title: (hit.title || "").replace(/^Show HN:\s*/i, ""),
        projectUrl: rawUrl || `https://news.ycombinator.com/item?id=${hit.objectID}`,
        githubUrl,
        points: hit.points || 0,
        numComments: hit.num_comments || 0,
        author: hit.author,
        createdAt: hit.created_at,
        founderPitch: storyText.length > 350 ? storyText.slice(0, 350) + "..." : storyText,
        hnDiscussionUrl: `https://news.ycombinator.com/item?id=${hit.objectID}`
      });

      if (results.length >= limit) break;
    }

    return NextResponse.json({ total: results.length, hits: results });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
