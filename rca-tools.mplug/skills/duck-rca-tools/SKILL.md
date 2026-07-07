---
name: duck-rca-tools
description: RCA Tools MCP — build incident timelines and 5 Whys question chains for postmortems. Use when asked to write an RCA, build a timeline, generate 5 Whys, or analyse an incident. Works with Jira ticket keys — fetch the issue via duck_jira first, then pass it in.
---

# RCA Tools MCP

You have access to an **rca-tools** MCP server. These tools structure and normalise incident data — **you** (Mallard/Claude) do the generation. No external LLM or API key required.

## How it works

The tools return structured event data plus a `_task` field with instructions for you to follow. Read the `_task` and complete it using your own reasoning. The tools handle data wrangling; you handle the writing.

## Jira integration — no token needed

This server never talks to Jira directly. Instead:

1. Use `duck_jira(action="get_issue", key="CESG-XXXXX")` to fetch the ticket
2. Pass the result as `jiraIssues` to `build_incident_timeline`

Mallard holds the Jira auth — the RCA server just normalises what you hand it.

## Workflow

```
1. duck_jira → get_issue(key="CESG-XXXXX")            # fetch ticket + linked issues
2. build_incident_timeline(incidentId, jiraIssues=[…]) # normalise events
3. Read _task from response → write timeline + narrative yourself
4. generate_5_whys_questions(problemStatement, timelineMarkdown)
5. Read _task from response → write 5 Whys chains yourself
```

## Tools

### `build_incident_timeline`

Returns normalised events and incident metadata. You generate the Markdown timeline, narrative summary, and impact summary from the output.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `incidentId` | ✅ | Primary incident ID (e.g. SIM-48282) |
| `jiraIssues` | — | Pre-fetched Jira issue objects from `duck_jira` |
| `severity` | — | Incident severity (P1, P2…) |
| `startTime` | — | ISO timestamp of incident start |
| `endTime` | — | ISO timestamp of resolution |
| `services` | — | Affected service names |
| `usersAffected` | — | Approximate user impact count |

### `generate_5_whys_questions`

Returns structured context. You generate the primary chain, alternative chains, and facilitation tips.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `problemStatement` | ✅ | Single-sentence incident impact statement |
| `timelineMarkdown` | — | Timeline from `build_incident_timeline` |
| `keyEvents` | — | Key events with role (Trigger, Detection, Mitigation…) |
| `impact` | — | `{ durationMinutes, usersAffected, severity }` |
| `maxChains` | — | Max alternative Why chains (default 2) |

## Generation rules (follow these when writing from `_task`)

**Timeline:**
- Assign each event a phase: Detection / Triage / Investigation / Mitigation / Recovery / FollowUp
- Present chronologically, grouped by phase
- Do not invent events or change timestamps
- Focus on technical/process facts, not individuals

**5 Whys:**
- Start from the problem statement, ask "Why did that happen?" at each level
- Never identify a person or "human error" as the root cause — focus on systems, processes, culture
- Aim for a specific, actionable, changeable root cause
- Stop when further "Why" leads to uncontrollable causes

## Prerequisites

- Run `python3 install.py` from the `rca_mcp` repo once to register this plugin
- No API key needed — Mallard's existing Claude session does all generation
