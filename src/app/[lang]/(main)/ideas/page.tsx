"use client";

import React, { useState, useEffect } from "react";
import { Page, PageContent, Section, H1, H2, Intro, P } from "@/components/Layout";
import { Search, Github, Globe, MessageSquare, Flame, Sparkles, Filter, ExternalLink, Code2 } from "lucide-react";

const PRESET_TOPICS = [
  { label: "All Trending", query: "" },
  { label: "Satellite & GIS", query: "satellite" },
  { label: "Carbon & Climate", query: "carbon" },
  { label: "Procurement & Tenders", query: "procurement" },
  { label: "Trade & ERP", query: "trade" },
  { label: "AI Agents", query: "agent" },
  { label: "Defense & Drone", query: "drone" },
];

export default function IdeasPage() {
  const [query, setQuery] = useState("");
  const [minPoints, setMinPoints] = useState(20);
  const [githubOnly, setGithubOnly] = useState(false);
  const [sortByDate, setSortByDate] = useState(false);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any[]>([]);

  const fetchIdeas = async (targetQuery = query) => {
    setLoading(true);
    try {
      const params = new URLSearchParams({
        q: targetQuery,
        minPoints: String(minPoints),
        githubOnly: String(githubOnly),
        sortByDate: String(sortByDate),
        limit: "24"
      });
      const res = await fetch(`/api/ideas?${params.toString()}`);
      const data = await res.json();
      setResults(data.hits || []);
    } catch (err) {
      console.error("Error fetching HN ideas:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchIdeas();
  }, [minPoints, githubOnly, sortByDate]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchIdeas();
  };

  const handlePresetClick = (topicQuery: string) => {
    setQuery(topicQuery);
    fetchIdeas(topicQuery);
  };

  return (
    <Page>
      <PageContent>
        <Section>
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b pb-6">
            <div>
              <H1>Show HN Idea & Open-Source Code Radar</H1>
              <Intro>
                Mine validated startup concepts, architecture patterns, and open-source GitHub repositories from 550,000+ Hacker News Show HN launches.
              </Intro>
            </div>
            <div className="flex items-center gap-2 bg-amber-50 text-amber-900 border border-amber-200 px-4 py-2 rounded-lg text-sm font-medium">
              <Sparkles className="w-5 h-5 text-amber-600" />
              100% Free Live Algolia HN Pipeline
            </div>
          </div>

          {/* Preset Topics Bar */}
          <div className="flex flex-wrap gap-2 my-6">
            {PRESET_TOPICS.map((t) => (
              <button
                key={t.label}
                onClick={() => handlePresetClick(t.query)}
                className={`px-3.5 py-1.5 rounded-full text-xs font-semibold transition-colors ${
                  query === t.query
                    ? "bg-black text-white"
                    : "bg-muted text-muted-foreground hover:bg-muted/80 hover:text-black"
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>

          {/* Search & Filter Bar */}
          <form onSubmit={handleSearchSubmit} className="flex flex-col md:flex-row gap-3 items-center justify-between mb-8 p-4 rounded-xl border bg-card">
            <div className="relative w-full md:flex-1">
              <Search className="absolute left-3.5 top-3 text-muted-foreground w-4 h-4" />
              <input
                type="text"
                placeholder="Search by keyword (e.g. satellite, carbon, procurement, rust, agent, drone)..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 rounded-lg border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-black/10"
              />
            </div>

            <div className="flex flex-wrap items-center gap-4 w-full md:w-auto text-xs">
              <div className="flex items-center gap-2">
                <label className="font-medium text-muted-foreground">Min Points:</label>
                <select
                  value={minPoints}
                  onChange={(e) => setMinPoints(Number(e.target.value))}
                  className="px-2.5 py-1.5 border rounded-lg bg-background font-medium"
                >
                  <option value={10}>10+ pts</option>
                  <option value={25}>25+ pts</option>
                  <option value={50}>50+ pts (High signal)</option>
                  <option value={100}>100+ pts (Top trending)</option>
                </select>
              </div>

              <label className="flex items-center gap-1.5 cursor-pointer select-none font-medium">
                <input
                  type="checkbox"
                  checked={githubOnly}
                  onChange={(e) => setGithubOnly(e.target.checked)}
                  className="rounded border-gray-300 text-black focus:ring-black"
                />
                <Code2 className="w-3.5 h-3.5" />
                GitHub Repos Only
              </label>

              <label className="flex items-center gap-1.5 cursor-pointer select-none font-medium">
                <input
                  type="checkbox"
                  checked={sortByDate}
                  onChange={(e) => setSortByDate(e.target.checked)}
                  className="rounded border-gray-300 text-black focus:ring-black"
                />
                Latest First
              </label>

              <button
                type="submit"
                className="bg-black text-white hover:bg-neutral-800 px-4 py-2 rounded-lg font-semibold text-xs transition-colors"
              >
                Search
              </button>
            </div>
          </form>

          {/* Loading Indicator */}
          {loading && (
            <div className="text-center py-16 text-muted-foreground text-sm">
              Mining Hacker News submissions...
            </div>
          )}

          {/* Results Grid */}
          {!loading && results.length === 0 && (
            <div className="text-center py-16 text-muted-foreground text-sm">
              No projects found matching current criteria. Try lowering the minimum points or expanding your query.
            </div>
          )}

          {!loading && results.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              {results.map((item: any) => (
                <div
                  key={item.hnId}
                  className="p-5 rounded-2xl border bg-card hover:shadow-md transition-all flex flex-col justify-between"
                >
                  <div>
                    {/* Header badge */}
                    <div className="flex items-center justify-between gap-2 mb-2">
                      <div className="flex items-center gap-1.5 text-xs font-bold text-amber-700 bg-amber-50 px-2.5 py-0.5 rounded-full border border-amber-200">
                        <Flame className="w-3.5 h-3.5" />
                        {item.points} pts
                      </div>
                      <span className="text-[11px] text-muted-foreground">
                        {item.createdAt?.slice(0, 10)}
                      </span>
                    </div>

                    {/* Title */}
                    <h3 className="font-bold text-base leading-snug hover:text-blue-600 transition-colors line-clamp-2">
                      <a href={item.projectUrl} target="_blank" rel="noreferrer">
                        {item.title}
                      </a>
                    </h3>

                    {/* Founder pitch preview */}
                    {item.founderPitch && (
                      <p className="text-xs text-muted-foreground mt-2 line-clamp-3 leading-relaxed">
                        {item.founderPitch.replace(/<[^>]+>/g, " ")}
                      </p>
                    )}
                  </div>

                  {/* Actions & Links */}
                  <div className="mt-5 pt-3 border-t flex items-center justify-between gap-2 text-xs">
                    <div className="flex items-center gap-3">
                      {item.githubUrl ? (
                        <a
                          href={item.githubUrl}
                          target="_blank"
                          rel="noreferrer"
                          className="flex items-center gap-1 font-semibold text-black hover:underline"
                        >
                          <Github className="w-4 h-4" />
                          Code Repo
                        </a>
                      ) : (
                        <a
                          href={item.projectUrl}
                          target="_blank"
                          rel="noreferrer"
                          className="flex items-center gap-1 text-muted-foreground hover:text-black"
                        >
                          <Globe className="w-3.5 h-3.5" />
                          Demo Link
                        </a>
                      )}
                    </div>

                    <a
                      href={item.hnDiscussionUrl}
                      target="_blank"
                      rel="noreferrer"
                      className="flex items-center gap-1 text-muted-foreground hover:text-blue-600 font-medium"
                    >
                      <MessageSquare className="w-3.5 h-3.5" />
                      {item.numComments} comments
                    </a>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Section>
      </PageContent>
    </Page>
  );
}
