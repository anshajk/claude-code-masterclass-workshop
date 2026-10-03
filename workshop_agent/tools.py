from .catalog import MODULES


def find_module(topic: str) -> dict:
    """Find a workshop module by its topic.

    Args:
        topic: Topic the learner wants to study.
    """
    module = MODULES.get(topic)
    if module is None:
        return {
            "status": "error",
            "error_message": f"No module found for {topic!r}.",
        }

    return {
        "status": "success",
        "topic": topic,
        "module": module,
    }


def build_agenda(
    level: str,
    duration_minutes: int,
    completed_prerequisites: list[str] | None = None,
) -> dict:
    """Build a deterministic workshop agenda.

    Args:
        level: Learner level: beginner or intermediate.
        duration_minutes: Available workshop time in minutes.
        completed_prerequisites: Optional prerequisites the learner has
            completed. When provided, only modules whose prerequisites are
            all covered are selected. When omitted, no filtering is applied.
    """
    normalized_level = level.strip().lower()
    if normalized_level not in {"beginner", "intermediate"}:
        return {
            "status": "error",
            "error_message": "Level must be beginner or intermediate.",
        }
    if duration_minutes < 20:
        return {
            "status": "error",
            "error_message": "At least 20 minutes are required.",
        }

    completed = (
        None
        if completed_prerequisites is None
        else {item.strip().lower() for item in completed_prerequisites}
    )
    selected = [
        {"topic": topic, "title": module["title"], "minutes": module["minutes"]}
        for topic, module in MODULES.items()
        if module["complexity"] == normalized_level
        and module["minutes"] <= duration_minutes
        and (
            completed is None
            or all(p.lower() in completed for p in module["prerequisites"])
        )
    ]
    return {
        "status": "success",
        "level": normalized_level,
        "duration_minutes": duration_minutes,
        "modules": selected,
    }
