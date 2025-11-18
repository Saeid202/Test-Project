import sys
from pathlib import Path

# Allow running this test file directly (conftest isn't loaded when run as a script)
try:
    from scraper.normalize import normalize_product
except ModuleNotFoundError:
    ROOT = Path(__file__).resolve().parents[1] / "python-product-AIBot"
    sys.path.insert(0, str(ROOT))
    from scraper.normalize import normalize_product


def test_normalize_with_source():
    raw = {"title": "USB Power Bank", "price": "$10", "source": "Alibaba"}
    norm = normalize_product(raw)
    assert norm["title"] == "USB Power Bank"
    assert norm["price"] == "$10"
    assert norm["source"] == "Alibaba"


def test_normalize_without_source():
    raw = {"title": "Cable", "price": "$2"}
    norm = normalize_product(raw)
    assert norm["title"] == "Cable"
    assert norm["price"] == "$2"
    assert norm["source"] == "Alibaba"
