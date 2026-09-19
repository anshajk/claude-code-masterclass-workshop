from workshop_agent.tools import (
    build_agenda,
    find_module,
    summarize_module_risk,
)


def test_find_known_module_normalizes_input() -> None:
    result = find_module(" Debugging ")

    assert result["status"] == "success"
    assert result["topic"] == "debugging"


def test_find_unknown_module_returns_explicit_error() -> None:
    result = find_module("deployment")

    assert result == {
        "status": "error",
        "error_message": "No module found for 'deployment'.",
    }


def test_build_beginner_agenda() -> None:
    result = build_agenda(" beginner ", 30)

    assert result["status"] == "success"
    assert [module["topic"] for module in result["modules"]] == ["foundations"]


def test_build_agenda_rejects_short_session() -> None:
    result = build_agenda("beginner", 10)

    assert result == {
        "status": "error",
        "error_message": "At least 20 minutes are required.",
    }


def test_summarize_module_risk() -> None:
    result = summarize_module_risk(" Evaluation ")

    assert result == {
        "status": "success",
        "topic": "evaluation",
        "complexity": "intermediate",
        "prerequisites": ["tool calling", "test design"],
        "facilitation_risk": "medium",
    }


def test_summarize_unknown_module_returns_explicit_error() -> None:
    result = summarize_module_risk("deployment")

    assert result["status"] == "error"
    assert "No module found" in result["error_message"]
