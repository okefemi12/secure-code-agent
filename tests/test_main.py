from src.main import analyze_code

def test_analyze_import():
    code = "import os"
    result = analyze_code(code)
    assert result == "Code contains imports."

def test_analyze_simple():
    code = "x = 1"
    result = analyze_code(code)
    assert result == "Code is simple."