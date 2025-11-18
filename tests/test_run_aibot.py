import builtins
from types import SimpleNamespace
import sys
from pathlib import Path

# Allow running this test file directly (conftest isn't loaded when run as a script)
try:
    import scraper.connector.run_aibot as run_mod
except ModuleNotFoundError:
    ROOT = Path(__file__).resolve().parents[1] / "python-product-AIBot"
    sys.path.insert(0, str(ROOT))
    # If `requests` isn't installed in the environment, provide a minimal stub so
    # importing `run_aibot` (which imports `website_api`) won't fail.
    import types
    import types as _types
    fake_requests = _types.ModuleType("requests")
    def _fake_post(*args, **kwargs):
        class R:
            def raise_for_status(self):
                return None
            def json(self):
                return {}
        return R()
    fake_requests.post = _fake_post
    sys.modules["requests"] = fake_requests
    import scraper.connector.run_aibot as run_mod


def test_run_bot_happy_path(monkeypatch, capsys):
    # Mock AlibabaScraper.run
    class DummyScraper:
        def run(self, query, max_results=5):
            return [{"title": "Item A", "price": "$1"}]

    monkeypatch.setattr(run_mod, "AlibabaScraper", DummyScraper)

    # Mock website_api functions
    monkeypatch.setattr(run_mod, "start_import_job", lambda q, m, r: "job-xyz")
    inserted = {}

    def fake_insert(job_id, products):
        inserted["job_id"] = job_id
        inserted["products"] = products

    monkeypatch.setattr(run_mod, "insert_imported_products", fake_insert)
    monkeypatch.setattr(run_mod, "complete_import_job", lambda jid: None)

    run_mod.run_bot(query="x", max_results=1)

    captured = capsys.readouterr()
    assert "Scraping products" in captured.out
    assert inserted["job_id"] == "job-xyz"
    assert len(inserted["products"]) == 1
