#!/usr/bin/env python3
"""Static validation for repository metadata, documentation, and the Pages site."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlparse

import yaml
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "SUPPORT.md",
    "CITATION.cff",
    "ACKNOWLEDGMENTS.md",
    "ROADMAP.md",
    ".gitignore",
    ".gitattributes",
    ".editorconfig",
    "requirements.txt",
    "config.py",
    "launch.py",
    "run.py",
    "run_all.sh",
    "run_with_dbeaver.sh",
    "db_viewer.py",
    "web_viewer.py",
    "verify_project.py",
    "SRMS_SecureDB.bak",
    "database/srms.db",
    "d_ds.pdf",
    "docs/.nojekyll",
    "docs/robots.txt",
    "docs/sitemap.xml",
    "docs/site.webmanifest",
    "docs/styles.css",
    "docs/script.js",
    ".github/CODEOWNERS",
    ".github/dependabot.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/ci.yml",
    ".github/workflows/release.yml",
    ".github/scripts/check_static.py",
]

SITE_PAGES = [
    "index.html",
    "architecture.html",
    "security.html",
    "database.html",
    "setup.html",
    "testing.html",
    "docs.html",
    "diagrams.html",
    "faq.html",
    "404.html",
]

REQUIRED_ASSETS = [
    "docs/assets/brand/logo.svg",
    "docs/assets/brand/favicon.svg",
    "docs/assets/brand/og-card.svg",
    "docs/assets/brand/apple-touch-icon.png",
    "docs/assets/brand/icon-192.png",
    "docs/assets/brand/icon-512.png",
    "docs/assets/og-image.png",
    "docs/assets/report/d_ds.pdf",
    "docs/assets/diagrams/architecture.svg",
    "docs/assets/diagrams/authentication.svg",
    "docs/assets/diagrams/audit.svg",
    "docs/assets/diagrams/backup-restore.svg",
    "docs/assets/diagrams/deployment.svg",
    "docs/assets/diagrams/encryption.svg",
    "docs/assets/diagrams/erd.svg",
    "docs/assets/diagrams/flow.svg",
    "docs/assets/diagrams/inference.svg",
    "docs/assets/diagrams/mls.svg",
    "docs/assets/diagrams/rbac.svg",
    "docs/assets/diagrams/request-lifecycle.svg",
    "docs/assets/diagrams/role-workflow.svg",
    "docs/assets/diagrams/threat-model.svg",
]

EXTERNAL_SCHEMES = ("http:", "https:", "mailto:", "tel:", "data:", "javascript:")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+['\"][^'\"]*['\"])?\s*\)")
ATTR_RE = re.compile(r"(?:src|href)=[\"']([^\"']+)[\"']", re.IGNORECASE)
FENCE_RE = re.compile(r"```.*?```|~~~.*?~~~", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")

errors: list[str] = []
checks = 0


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        errors.append(message)


def local_target(raw: str) -> str | None:
    raw = raw.strip().strip("<>")
    parsed = urlparse(raw)
    if parsed.scheme in {s.rstrip(":") for s in EXTERNAL_SCHEMES}:
        return None
    if raw.startswith("//") or raw.startswith("#") or not raw:
        return None
    path = unquote(raw.split("#", 1)[0].split("?", 1)[0])
    return path or None


def resolve(base: Path, target: str) -> Path:
    return (base / target).resolve()


for relative in REQUIRED_FILES + REQUIRED_ASSETS:
    check((ROOT / relative).exists(), f"Missing required file: {relative}")

for relative in ("SRMS_SecureDB.bak", "database/srms.db", "d_ds.pdf"):
    path = ROOT / relative
    check(path.exists() and path.stat().st_size > 0, f"Required binary is empty: {relative}")

for page in SITE_PAGES:
    path = DOCS / page
    check(path.exists(), f"Missing website page: docs/{page}")
    if not path.exists():
        continue
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    check(bool(soup.title and soup.title.get_text(strip=True)), f"{page}: missing title")
    description = soup.find("meta", attrs={"name": "description"})
    check(bool(description and description.get("content")), f"{page}: missing meta description")
    if page != "404.html":
        check(bool(soup.find("link", rel="canonical")), f"{page}: missing canonical URL")
        check(len(soup.find_all("h1")) == 1, f"{page}: expected exactly one h1")
    else:
        robots = soup.find("meta", attrs={"name": "robots"})
        check(bool(robots and "noindex" in (robots.get("content") or "")), "404.html: missing noindex")
    ids = [node.get("id") for node in soup.find_all(id=True)]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    check(not duplicates, f"{page}: duplicate ids: {', '.join(duplicates)}")

    for node in soup.find_all(["a", "link", "script", "img", "source"]):
        raw = node.get("href") or node.get("src")
        if not raw:
            continue
        target = local_target(raw)
        if target is None:
            continue
        resolved = resolve(DOCS, target)
        check(resolved.exists(), f"{page}: broken local reference {raw}")
        if resolved.suffix == ".html" and resolved.exists() and "#" in raw:
            anchor = unquote(raw.split("#", 1)[1])
            if anchor:
                target_soup = BeautifulSoup(resolved.read_text(encoding="utf-8"), "html.parser")
                anchor_exists = bool(
                    target_soup.find(id=anchor)
                    or target_soup.find("a", attrs={"name": anchor})
                    or target_soup.find("h1", id=anchor)
                )
                check(anchor_exists, f"{page}: missing anchor #{anchor} in {target}")

markdown_files = sorted(ROOT.glob("*.md")) + sorted((ROOT / "documentation").rglob("*.md"))
for path in markdown_files:
    text = path.read_text(encoding="utf-8")
    stripped = INLINE_CODE_RE.sub("", FENCE_RE.sub("", text))
    targets = set(LINK_RE.findall(stripped))
    targets.update(ATTR_RE.findall(stripped))
    for raw in sorted(targets):
        target = local_target(raw)
        if target is None:
            continue
        resolved = resolve(path.parent, target)
        check(resolved.exists(), f"{path.relative_to(ROOT)}: broken local link {raw}")

for path in sorted((ROOT / ".github").rglob("*.yml")):
    try:
        parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
        check(isinstance(parsed, dict), f"{path.relative_to(ROOT)}: YAML root is not a mapping")
    except yaml.YAMLError as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid YAML: {exc}")

for path in sorted((ROOT / ".github").rglob("*.yaml")):
    try:
        yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid YAML: {exc}")

for path in sorted(DOCS.glob("*.svg")) + sorted((DOCS / "assets").rglob("*.svg")):
    try:
        root = ET.fromstring(path.read_text(encoding="utf-8"))
        check(root.tag.endswith("svg"), f"{path.relative_to(ROOT)}: root element is not svg")
    except ET.ParseError as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid SVG: {exc}")

diagram_svg = sorted((DOCS / "assets" / "diagrams").glob("*.svg"))
diagram_mmd = sorted((ROOT / "documentation" / "diagrams").glob("*.mmd"))
check(len(diagram_svg) >= 14, f"Expected at least 14 rendered diagrams, found {len(diagram_svg)}")
check(len(diagram_mmd) >= 14, f"Expected at least 14 Mermaid sources, found {len(diagram_mmd)}")

manifest_path = DOCS / "site.webmanifest"
if manifest_path.exists():
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for icon in manifest.get("icons", []):
            icon_path = DOCS / icon["src"]
            check(icon_path.exists(), f"Web manifest icon missing: {icon['src']}")
    except json.JSONDecodeError as exc:
        errors.append(f"docs/site.webmanifest: invalid JSON: {exc}")

try:
    sitemap = ET.fromstring((DOCS / "sitemap.xml").read_text(encoding="utf-8"))
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locations = [item.text for item in sitemap.findall("sm:url/sm:loc", namespace)]
    check(len(locations) >= 9, "Sitemap contains fewer than nine URLs")
    site_root = "https://ahmedbakr78.github.io/Secure-Student-Records-Management-Control"
    for location in locations:
        if not location:
            continue
        if location.rstrip("/") == site_root:
            suffix = "index.html"
        else:
            suffix = location.rstrip("/").rsplit("/", 1)[-1]
            if not suffix.endswith(".html"):
                suffix += ".html"
        check((DOCS / suffix).exists(), f"Sitemap target missing: {location}")
except ET.ParseError as exc:
    errors.append(f"docs/sitemap.xml: invalid XML: {exc}")

robots = (DOCS / "robots.txt").read_text(encoding="utf-8") if (DOCS / "robots.txt").exists() else ""
check("Sitemap:" in robots, "robots.txt does not declare a sitemap")

if errors:
    print(f"Static validation failed: {len(errors)} error(s), {checks} checks", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    sys.exit(1)

print(f"Static validation passed: {checks} checks, {len(diagram_svg)} diagrams, {len(markdown_files)} guides.")
