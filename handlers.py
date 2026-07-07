from typing import Any, Dict, List


def _jira_issues_to_events(
    jira_issues: List[Dict[str, Any]], incident_id: str
) -> List[Dict[str, Any]]:
    """Convert pre-fetched Jira issues (passed in by Mallard via duck_jira) into normalized events.

    Accepts both raw Jira REST API format (fields nested under 'fields') and
    the flattened format duck_jira may return.
    """
    events: List[Dict[str, Any]] = []
    for issue in jira_issues:
        fields = issue.get("fields", issue)
        key = issue.get("key", "")

        created = fields.get("created") or fields.get("createdAt", "")
        creator = (fields.get("creator") or {}).get("displayName", "unknown")
        events.append(
            {
                "timestamp": created,
                "source": "JIRA",
                "entityId": key,
                "phase": None,
                "type": "IssueCreated",
                "actor": creator,
                "rawText": f"[{key}] {fields.get('summary', '')}",
                "summary": fields.get("summary"),
            }
        )

        resolved = fields.get("resolutiondate") or fields.get("resolvedAt")
        if resolved:
            assignee = (fields.get("assignee") or {}).get("displayName", "unknown")
            resolution = (fields.get("resolution") or {}).get("name", "")
            events.append(
                {
                    "timestamp": resolved,
                    "source": "JIRA",
                    "entityId": key,
                    "phase": "Recovery",
                    "type": "IssueResolved",
                    "actor": assignee,
                    "rawText": f"[{key}] Resolved: {resolution}",
                    "summary": f"Jira issue {key} resolved.",
                }
            )

        for comment in (fields.get("comment") or {}).get("comments", []):
            events.append(
                {
                    "timestamp": comment.get("created", ""),
                    "source": "JIRA",
                    "entityId": key,
                    "phase": None,
                    "type": "Comment",
                    "actor": (comment.get("author") or {}).get("displayName", "unknown"),
                    "rawText": comment.get("body", ""),
                    "summary": None,
                }
            )

    return events


def call_build_incident_timeline(args: Dict[str, Any]) -> Dict[str, Any]:
    incident_id: str = args["incidentId"]
    jira_issues: List[Dict[str, Any]] = args.get("jiraIssues", [])

    # Stub incident metadata — replace with SIM/PagerDuty fetch when available.
    incident = {
        "id": incident_id,
        "title": f"Incident {incident_id}",
        "severity": args.get("severity", "unknown"),
        "startTime": args.get("startTime"),
        "endTime": args.get("endTime"),
        "services": args.get("services", []),
        "usersAffected": args.get("usersAffected"),
    }

    normalized_events: List[Dict[str, Any]] = []

    if jira_issues:
        normalized_events.extend(_jira_issues_to_events(jira_issues, incident_id))
        normalized_events.sort(key=lambda e: e.get("timestamp") or "")

    return {
        "incident": incident,
        "events": normalized_events,
        "_task": (
            "You have the normalized incident events above. Now:\n"
            "1. Summarize each event into a concise description.\n"
            "2. Assign each event a phase: Detection, Triage, Investigation, Mitigation, Recovery, or FollowUp.\n"
            "3. Write a Markdown incident timeline (chronological, phase-grouped).\n"
            "4. Write a 1–3 paragraph narrative summary of how the incident unfolded.\n"
            "5. Write a short impact summary (duration, affected services, user impact).\n"
            "Do not invent events or timestamps. Focus on technical/process facts, not individuals."
        ),
    }


def call_generate_5_whys_questions(args: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "problemStatement": args["problemStatement"],
        "timelineMarkdown": args.get("timelineMarkdown", ""),
        "keyEvents": args.get("keyEvents", []),
        "impact": args.get("impact", {}),
        "maxChains": args.get("maxChains", 2),
        "_task": (
            "Using the context above, generate a 5 Whys analysis:\n"
            "1. One primary chain of 5 successive 'Why?' questions starting from the problem statement.\n"
            f"2. Up to {args.get('maxChains', 2)} alternative chains (e.g. technical focus, process focus).\n"
            "3. A short list of facilitation tips for the 5 Whys session.\n"
            "Rules: never blame an individual — focus on systems, processes, culture. "
            "Aim for a specific, actionable, changeable root cause. "
            "Stop when further 'Why' leads to uncontrollable causes."
        ),
    }
