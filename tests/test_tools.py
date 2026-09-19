from workshop_agent.tools import build_agenda, find_module


def test_find_known_module() -> None:
    result = find_module("debugging")

    assert result["status"] == "success"
    assert result["module"]["title"] == "Debugging with evidence"


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
