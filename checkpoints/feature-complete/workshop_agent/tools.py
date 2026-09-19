from .catalog import MODULES


def _normalize_topic(topic: str) -> str:
    return topic.strip().lower()


def find_module(topic: str) -> dict:
    """Find a workshop module by its topic.

    Args:
        topic: Topic the learner wants to study.
    """
    normalized_topic = _normalize_topic(topic)
    module = MODULES.get(normalized_topic)
    if module is None:
        return {
            "status": "error",
            "error_message": f"No module found for {topic!r}.",
        }

    return {
        "status": "success",
        "topic": normalized_topic,
        "module": module,
    }


def build_agenda(level: str, duration_minutes: int) -> dict:
    """Build a deterministic workshop agenda.

    Args:
        level: Learner level: beginner or intermediate.
        duration_minutes: Available workshop time in minutes.
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

    selected = [
        {"topic": topic, "title": module["title"], "minutes": module["minutes"]}
        for topic, module in MODULES.items()
        if module["complexity"] == normalized_level
        and module["minutes"] <= duration_minutes
    ]
    return {
        "status": "success",
        "level": normalized_level,
        "duration_minutes": duration_minutes,
        "modules": selected,
    }


def summarize_module_risk(module_name: str) -> dict:
    """Return planning and facilitation risks for a workshop module.

    Args:
        module_name: Module topic to assess.
    """
    normalized_topic = _normalize_topic(module_name)
    module = MODULES.get(normalized_topic)
    if module is None:
        return {
            "status": "error",
            "error_message": f"No module found for {module_name!r}.",
        }

    return {
        "status": "success",
        "topic": normalized_topic,
        "complexity": module["complexity"],
        "prerequisites": module["prerequisites"],
        "facilitation_risk": module["facilitation_risk"],
    }
