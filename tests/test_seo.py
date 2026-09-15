from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_generate_and_seo() -> None:
    subprocess.check_call([sys.executable, str(ROOT / "generate_site.py")])
    rc = subprocess.call([sys.executable, str(ROOT / "check_seo.py")])
    assert rc == 0
    assert (ROOT / "docs" / "sensor-hoof-boot.html").exists()
    html = (ROOT / "docs" / "sensor-hoof-boot.html").read_text(encoding="utf-8")
    assert "Sensor Hoof Boot" in html
    assert "application/ld+json" in html
