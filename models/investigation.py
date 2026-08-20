from dataclasses import dataclass


@dataclass
class Investigation:
    """Domain model for an RCA investigation. Fields grow in later issues."""

    incident_id: str
