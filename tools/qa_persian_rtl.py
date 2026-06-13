#!/usr/bin/env python3
"""Run Persian/RTL quality checks against generated ATT&CK output.

This script intentionally uses only the Python standard library so it can run
locally, in GitHub Actions, and during Vercel builds without extra packages.
"""

# ruff: noqa: D101, D102, D103

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

CRITICAL_OUTPUT_DIRS = {
    "analytics",
    "assets",
    "campaigns",
    "datasources",
    "datacomponents",
    "detectionstrategies",
    "groups",
    "matrices",
    "mitigations",
    "software",
    "tactics",
    "techniques",
}

STIX_OBJECT_TYPES = {
    "attack-pattern",
    "campaign",
    "course-of-action",
    "intrusion-set",
    "malware",
    "tool",
    "x-mitre-analytic",
    "x-mitre-asset",
    "x-mitre-data-component",
    "x-mitre-data-source",
    "x-mitre-detection-strategy",
    "x-mitre-tactic",
}


@dataclass
class Issue:
    severity: str
    message: str
    path: Path | None = None
    line: int | None = None


@dataclass
class Coverage:
    total: int = 0
    translated: int = 0

    @property
    def percent(self) -> float:
        if self.total == 0:
            return 100.0
        return (self.translated / self.total) * 100


@dataclass
class DomainCoverage:
    names: Coverage
    descriptions: Coverage


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def line_number(source: str, index: int) -> int:
    return source.count("\n", 0, index) + 1


def has_attr(attrs: str, name: str, value: str) -> bool:
    pattern = r"\b{0}\s*=\s*(['\"]){1}\1".format(re.escape(name), re.escape(value))
    return re.search(pattern, attrs, re.IGNORECASE) is not None


def is_archived_path(path: Path, output_dir: Path) -> bool:
    try:
        parts = path.relative_to(output_dir).parts
    except ValueError:
        parts = path.parts
    return "versions" in parts or "attack-version-archives" in parts


def is_redirect_page(source: str) -> bool:
    head = source[:4096].lower()
    return "http-equiv=\"refresh\"" in head or "http-equiv='refresh'" in head


def is_critical_page(path: Path, output_dir: Path) -> bool:
    try:
        rel = path.relative_to(output_dir)
    except ValueError:
        return False
    if rel.as_posix() == "index.html":
        return True
    return bool(rel.parts and rel.parts[0] in CRITICAL_OUTPUT_DIRS)


def add_issue(
    issues: list[Issue],
    severity: str,
    message: str,
    path: Path | None = None,
    line: int | None = None,
) -> None:
    issues.append(Issue(severity=severity, message=message, path=path, line=line))


def check_required_sources(source_root: Path, issues: list[Issue]) -> None:
    required = (
        "attack-theme/static/scripts/language.js",
        "attack-theme/templates/macros/localized.html",
        "attack-style/base/_base.scss",
        "attack-style/abstracts/_font-faces.scss",
    )
    for raw_path in required:
        path = source_root / raw_path
        if not path.exists():
            add_issue(issues, "error", "Required Persian/RTL source file is missing.", path)


def check_source_markers(source_root: Path, issues: list[Issue]) -> None:
    language_js = source_root / "attack-theme/static/scripts/language.js"
    base_scss = source_root / "attack-style/base/_base.scss"
    fonts_scss = source_root / "attack-style/abstracts/_font-faces.scss"

    if language_js.exists():
        source = read_text(language_js)
        if 'defaultLanguage = "fa"' not in source and "defaultLanguage = 'fa'" not in source:
            add_issue(issues, "error", "Default language is not Persian in language.js.", language_js)
        if "attack_language" not in source:
            add_issue(issues, "error", "Language preference cookie is not present in language.js.", language_js)
        if "attachEvent" not in source:
            add_issue(issues, "error", "IE8 attachEvent fallback is missing from language.js.", language_js)

    if base_scss.exists():
        source = read_text(base_scss)
        if ".language-content-fa" not in source:
            add_issue(issues, "error", "Persian language content CSS hook is missing.", base_scss)
        if 'html[lang="fa"]' not in source and "html[lang='fa']" not in source and "html[lang=fa]" not in source:
            add_issue(issues, "error", "RTL html[lang=fa] CSS rule is missing.", base_scss)

    if fonts_scss.exists():
        source = read_text(fonts_scss)
        if "Vazir" not in source:
            add_issue(issues, "error", "Vazir font-face is missing.", fonts_scss)
        if ".eot" not in source:
            add_issue(issues, "warning", "Vazir font-face does not reference EOT for IE8.", fonts_scss)


def collect_translation_keys(source_root: Path) -> set[str]:
    language_js = source_root / "attack-theme/static/scripts/language.js"
    if not language_js.exists():
        return set()
    source = read_text(language_js)
    return set(re.findall(r"['\"]([A-Za-z0-9_.:-]+)['\"]\s*:", source))


def collect_data_i18n_keys(source: str) -> set[str]:
    return set(re.findall(r"data-i18n\s*=\s*['\"]([^'\"]+)['\"]", source))


def check_html_file(
    path: Path,
    output_dir: Path,
    translated_keys: set[str],
    issues: list[Issue],
) -> tuple[int, int]:
    source = read_text(path)
    todo_count = 0
    data_key_count = 0

    for match in re.finditer(r"\[?TODO-FA\]?", source):
        todo_count += 1
        add_issue(issues, "error", "Unresolved TODO-FA marker is present in generated output.", path, line_number(source, match.start()))

    html_match = re.search(r"<html\b([^>]*)>", source[:4096], re.IGNORECASE)
    if html_match and not is_redirect_page(source):
        attrs = html_match.group(1)
        if not (has_attr(attrs, "lang", "fa") and has_attr(attrs, "dir", "rtl")):
            severity = "error" if is_critical_page(path, output_dir) else "warning"
            add_issue(issues, severity, "Generated page is not marked as lang=fa and dir=rtl by default.", path)

    fa_blocks = re.finditer(
        r"<[A-Za-z0-9]+\b([^>]*class\s*=\s*['\"][^'\"]*\blanguage-content-fa\b[^'\"]*['\"][^>]*)>",
        source,
        re.IGNORECASE,
    )
    for match in fa_blocks:
        attrs = match.group(1)
        if not (has_attr(attrs, "lang", "fa") and has_attr(attrs, "dir", "rtl")):
            add_issue(
                issues,
                "error",
                "language-content-fa element is missing lang=fa or dir=rtl.",
                path,
                line_number(source, match.start()),
            )

    for key in collect_data_i18n_keys(source):
        data_key_count += 1
        if key not in translated_keys:
            add_issue(issues, "error", "data-i18n key has no Persian translation: {0}".format(key), path)

    return todo_count, data_key_count


def check_generated_output(
    output_dir: Path,
    source_root: Path,
    include_archives: bool,
    require_output: bool,
    issues: list[Issue],
) -> dict[str, int]:
    stats = {"html_files": 0, "skipped_archives": 0, "todo_markers": 0, "data_i18n_keys": 0}

    if not output_dir.exists():
        severity = "error" if require_output else "warning"
        add_issue(issues, severity, "Output directory does not exist; build the site before running full QA.", output_dir)
        return stats

    translated_keys = collect_translation_keys(source_root)
    for path in sorted(output_dir.rglob("*.html")):
        if not include_archives and is_archived_path(path, output_dir):
            stats["skipped_archives"] += 1
            continue
        stats["html_files"] += 1
        todo_count, key_count = check_html_file(path, output_dir, translated_keys, issues)
        stats["todo_markers"] += todo_count
        stats["data_i18n_keys"] += key_count

    if stats["html_files"] == 0:
        add_issue(issues, "warning", "No HTML files were found in output.", output_dir)

    return stats


def is_active_stix_object(item: dict[str, Any]) -> bool:
    return not item.get("revoked") and not item.get("x_mitre_deprecated")


def has_value(item: dict[str, Any], field: str) -> bool:
    value = item.get(field)
    return isinstance(value, str) and bool(value.strip())


def update_coverage(coverage: Coverage, translated: bool) -> None:
    coverage.total += 1
    if translated:
        coverage.translated += 1


def load_stix_json(path: Path, issues: list[Issue]) -> dict[str, Any] | None:
    try:
        return json.loads(read_text(path))
    except ValueError as exc:
        add_issue(issues, "error", "Invalid STIX JSON: {0}".format(exc), path)
        return None


def check_stix_coverage(
    stix_dir: Path,
    require_stix: bool,
    min_name_coverage: float,
    min_description_coverage: float,
    issues: list[Issue],
) -> dict[str, DomainCoverage]:
    domains: dict[str, DomainCoverage] = {}
    total = DomainCoverage(names=Coverage(), descriptions=Coverage())

    if not stix_dir.exists():
        severity = "error" if require_stix else "warning"
        add_issue(issues, severity, "STIX directory does not exist; translation coverage was not measured.", stix_dir)
        return domains

    for path in sorted(stix_dir.glob("*.json")):
        data = load_stix_json(path, issues)
        if not data:
            continue
        domain = path.stem
        coverage = DomainCoverage(names=Coverage(), descriptions=Coverage())
        for item in data.get("objects", []):
            if not isinstance(item, dict) or not is_active_stix_object(item):
                continue
            item_type = item.get("type")
            if item_type in STIX_OBJECT_TYPES:
                if has_value(item, "name"):
                    update_coverage(coverage.names, has_value(item, "name_fa"))
                    update_coverage(total.names, has_value(item, "name_fa"))
                if has_value(item, "description"):
                    update_coverage(coverage.descriptions, has_value(item, "description_fa"))
                    update_coverage(total.descriptions, has_value(item, "description_fa"))
            elif item_type == "relationship" and has_value(item, "description"):
                update_coverage(coverage.descriptions, has_value(item, "description_fa"))
                update_coverage(total.descriptions, has_value(item, "description_fa"))
        domains[domain] = coverage

    if not domains:
        add_issue(issues, "warning", "No STIX JSON files were found for translation coverage.", stix_dir)
        return domains

    domains["_total"] = total
    if total.names.percent < min_name_coverage:
        add_issue(
            issues,
            "error",
            "STIX name_fa coverage {0:.1f}% is below required {1:.1f}%.".format(
                total.names.percent,
                min_name_coverage,
            ),
            stix_dir,
        )
    if total.descriptions.percent < min_description_coverage:
        add_issue(
            issues,
            "error",
            "STIX description_fa coverage {0:.1f}% is below required {1:.1f}%.".format(
                total.descriptions.percent,
                min_description_coverage,
            ),
            stix_dir,
        )

    if total.names.percent < 100.0:
        add_issue(issues, "warning", "Some active STIX objects are missing name_fa.", stix_dir)
    if total.descriptions.percent < 100.0:
        add_issue(issues, "warning", "Some active STIX descriptions are missing description_fa.", stix_dir)

    return domains


def issue_to_text(issue: Issue) -> str:
    location = ""
    if issue.path:
        location = str(issue.path)
        if issue.line:
            location += ":{0}".format(issue.line)
        location += ": "
    return "{0}{1}: {2}".format(location, issue.severity.upper(), issue.message)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Persian/RTL QA checks for generated ATT&CK output.")
    parser.add_argument("--source-root", default=".", help="Repository root containing theme/style source files.")
    parser.add_argument("--output-dir", default="output", help="Generated static site output directory.")
    parser.add_argument("--stix-dir", default="output/stix", help="Generated STIX JSON directory.")
    parser.add_argument("--include-archives", action="store_true", help="Include archived version pages in HTML checks.")
    parser.add_argument("--require-output", action="store_true", help="Fail if the generated output directory is missing.")
    parser.add_argument("--require-stix", action="store_true", help="Fail if generated STIX JSON is missing.")
    parser.add_argument("--min-name-coverage", type=float, default=0.0, help="Minimum total name_fa coverage percentage.")
    parser.add_argument(
        "--min-description-coverage",
        type=float,
        default=0.0,
        help="Minimum total description_fa coverage percentage.",
    )
    parser.add_argument("--max-issues", type=int, default=50, help="Maximum issue lines to print before truncating.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON instead of text.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    source_root = Path(args.source_root)
    output_dir = Path(args.output_dir)
    stix_dir = Path(args.stix_dir)
    issues: list[Issue] = []

    check_required_sources(source_root, issues)
    check_source_markers(source_root, issues)
    output_stats = check_generated_output(output_dir, source_root, args.include_archives, args.require_output, issues)
    stix_coverage = check_stix_coverage(
        stix_dir,
        args.require_stix,
        args.min_name_coverage,
        args.min_description_coverage,
        issues,
    )

    errors = [issue for issue in issues if issue.severity == "error"]
    warnings = [issue for issue in issues if issue.severity == "warning"]

    if args.json:
        print(
            json.dumps(
                {
                    "ok": not errors,
                    "errors": len(errors),
                    "warnings": len(warnings),
                    "output": output_stats,
                    "stix": {
                        domain: {
                            "name_fa": {
                                "translated": coverage.names.translated,
                                "total": coverage.names.total,
                                "percent": round(coverage.names.percent, 2),
                            },
                            "description_fa": {
                                "translated": coverage.descriptions.translated,
                                "total": coverage.descriptions.total,
                                "percent": round(coverage.descriptions.percent, 2),
                            },
                        }
                        for domain, coverage in stix_coverage.items()
                    },
                    "issues": [
                        {
                            "severity": issue.severity,
                            "message": issue.message,
                            "path": str(issue.path) if issue.path else None,
                            "line": issue.line,
                        }
                        for issue in issues
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0 if not errors else 1

    print("Persian/RTL QA gate")
    print(
        "HTML scanned: {0}; archived skipped: {1}; TODO-FA markers: {2}; data-i18n keys seen: {3}".format(
            output_stats["html_files"],
            output_stats["skipped_archives"],
            output_stats["todo_markers"],
            output_stats["data_i18n_keys"],
        )
    )

    if stix_coverage:
        print("STIX translation coverage:")
        for domain in sorted(name for name in stix_coverage if name != "_total"):
            coverage = stix_coverage[domain]
            print(
                "  {0}: name_fa {1}/{2} ({3:.1f}%), description_fa {4}/{5} ({6:.1f}%)".format(
                    domain,
                    coverage.names.translated,
                    coverage.names.total,
                    coverage.names.percent,
                    coverage.descriptions.translated,
                    coverage.descriptions.total,
                    coverage.descriptions.percent,
                )
            )
        total = stix_coverage.get("_total")
        if total:
            print(
                "  total: name_fa {0}/{1} ({2:.1f}%), description_fa {3}/{4} ({5:.1f}%)".format(
                    total.names.translated,
                    total.names.total,
                    total.names.percent,
                    total.descriptions.translated,
                    total.descriptions.total,
                    total.descriptions.percent,
                )
            )

    for issue in issues[: args.max_issues]:
        print(issue_to_text(issue))
    if len(issues) > args.max_issues:
        print("... {0} more issue(s) not shown".format(len(issues) - args.max_issues))

    if errors:
        print("FAIL: {0} error(s), {1} warning(s).".format(len(errors), len(warnings)))
        return 1

    if warnings:
        print("PASS with {0} warning(s).".format(len(warnings)))
    else:
        print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
