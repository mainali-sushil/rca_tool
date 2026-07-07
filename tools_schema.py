BUILD_INCIDENT_TIMELINE_TOOL = {
    "name": "build_incident_timeline",
    "description": (
        "Fetch SIM + Jira + observability data for an incident, normalize events, and "
        "generate a Markdown timeline and narrative summary for RCA/postmortems."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "incidentId": {
                "type": "string",
                "description": "Primary incident identifier from SIM (e.g. SIM-12345).",
            },
            "jiraKeys": {
                "type": "array",
                "description": "Optional list of Jira issue keys linked to the incident.",
                "items": {"type": "string"},
            },
            "jiraIssues": {
                "type": "array",
                "description": (
                    "Pre-fetched Jira issue objects (e.g. from duck_jira). "
                    "When provided, the server uses this data directly — no Jira credentials required. "
                    "Accepts raw Jira REST API format or duck_jira's flattened format."
                ),
                "items": {"type": "object"},
            },
            "timeRange": {
                "type": "object",
                "description": "Optional time window for events.",
                "properties": {
                    "from": {"type": "string", "format": "date-time"},
                    "to": {"type": "string", "format": "date-time"},
                },
                "required": ["from", "to"],
            },
            "includeRawEvents": {
                "type": "boolean",
                "description": "Include normalized event list in response.",
                "default": True,
            },
        },
        "required": ["incidentId"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "incident": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "title": {"type": "string"},
                    "severity": {"type": "string"},
                    "startTime": {"type": "string", "format": "date-time"},
                    "endTime": {"type": "string", "format": "date-time"},
                    "services": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "usersAffected": {"type": "number"},
                },
                "required": ["id", "title"],
            },
            "events": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "timestamp": {"type": "string", "format": "date-time"},
                        "source": {"type": "string"},
                        "entityId": {"type": "string"},
                        "phase": {
                            "type": "string",
                            "enum": [
                                "Detection",
                                "Triage",
                                "Investigation",
                                "Mitigation",
                                "Recovery",
                                "FollowUp",
                            ],
                        },
                        "type": {"type": "string"},
                        "actor": {"type": "string"},
                        "rawText": {"type": "string"},
                        "summary": {"type": "string"},
                    },
                    "required": ["timestamp", "source", "summary"],
                },
            },
            "timelineMarkdown": {
                "type": "string",
                "description": "Markdown formatted incident timeline.",
            },
            "narrativeSummary": {
                "type": "string",
                "description": "Narrative description of how the incident unfolded.",
            },
            "impactSummary": {
                "type": "string",
                "description": "Short summary of duration, affected services, and user impact.",
            },
        },
        "required": ["timelineMarkdown", "narrativeSummary"],
    },
}

GENERATE_5_WHYS_TOOL = {
    "name": "generate_5_whys_questions",
    "description": (
        "Generate 5 Whys starter question chains for an incident RCA, given a "
        "problem statement and timeline."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "problemStatement": {
                "type": "string",
                "description": "Single-sentence incident impact statement.",
            },
            "timelineMarkdown": {
                "type": "string",
                "description": "Incident timeline in Markdown (e.g. from build_incident_timeline).",
            },
            "keyEvents": {
                "type": "array",
                "description": "Optional key events for anchoring questions.",
                "items": {
                    "type": "object",
                    "properties": {
                        "timestamp": {"type": "string", "format": "date-time"},
                        "summary": {"type": "string"},
                        "role": {
                            "type": "string",
                            "enum": [
                                "Trigger",
                                "Detection",
                                "Mitigation",
                                "Recovery",
                                "Contributing",
                            ],
                        },
                    },
                    "required": ["summary", "role"],
                },
            },
            "impact": {
                "type": "object",
                "description": "Optional impact metrics.",
                "properties": {
                    "durationMinutes": {"type": "number"},
                    "usersAffected": {"type": "number"},
                    "severity": {"type": "string"},
                },
            },
            "maxChains": {
                "type": "number",
                "description": "Max number of alternative chains.",
                "default": 2,
            },
        },
        "required": ["problemStatement"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "primaryChain": {
                "type": "array",
                "description": "Primary 5-Whys question chain.",
                "items": {
                    "type": "object",
                    "properties": {
                        "level": {"type": "number"},
                        "question": {"type": "string"},
                        "hint": {"type": "string"},
                    },
                    "required": ["level", "question"],
                },
            },
            "alternativeChains": {
                "type": "array",
                "description": "Alternative chains for different focuses.",
                "items": {
                    "type": "object",
                    "properties": {
                        "focus": {"type": "string"},
                        "chain": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "level": {"type": "number"},
                                    "question": {"type": "string"},
                                    "hint": {"type": "string"},
                                },
                                "required": ["level", "question"],
                            },
                        },
                    },
                    "required": ["focus", "chain"],
                },
            },
            "guidance": {
                "type": "array",
                "description": "Facilitation tips for the 5 Whys session.",
                "items": {"type": "string"},
            },
        },
        "required": ["primaryChain"],
    },
}

ALL_TOOLS = [BUILD_INCIDENT_TIMELINE_TOOL, GENERATE_5_WHYS_TOOL]
