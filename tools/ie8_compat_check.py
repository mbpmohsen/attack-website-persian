#!/usr/bin/env python3
"""Check legacy theme JavaScript for syntax and APIs that break IE8.

The ATT&CK site still ships several upstream/vendor scripts. This gate is
focused on the language switching layer by default, because that is the code
this fork owns for Persian support. Pass files or directories explicitly to
scan a wider surface.
"""

# ruff: noqa: D101, D103

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

DEFAULT_FILES = (
    "attack-theme/static/scripts/language.js",
    "attack-theme/static/scripts/stix-translations.js",
)

VENDOR_HINTS = (
    ".min.js",
    "bootstrap",
    "jquery",
    "popper",
    "search_bundle",
    "vendors",
)


@dataclass
class Rule:
    code: str
    message: str
    pattern: re.Pattern[str]
    severity: str = "error"


@dataclass
class Finding:
    path: Path
    line: int
    severity: str
    code: str
    message: str


ERROR_RULES = (
    Rule("syntax.let", "Use var instead of let for IE8.", re.compile(r"\blet\b")),
    Rule("syntax.const", "Use var instead of const for IE8.", re.compile(r"\bconst\b")),
    Rule("syntax.arrow", "Arrow functions are not supported by IE8.", re.compile(r"=>")),
    Rule("syntax.template", "Template literals are not supported by IE8.", re.compile(r"`")),
    Rule("syntax.class", "ES6 class syntax is not supported by IE8.", re.compile(r"\bclass\s+[A-Za-z_$]")),
    Rule("syntax.async", "async functions are not supported by IE8.", re.compile(r"\basync\s+function\b")),
    Rule("syntax.await", "await is not supported by IE8.", re.compile(r"\bawait\b")),
    Rule("syntax.import", "ES module import syntax is not supported by IE8.", re.compile(r"\bimport\s+")),
    Rule("syntax.export", "ES module export syntax is not supported by IE8.", re.compile(r"\bexport\s+")),
    Rule("syntax.spread", "Spread/rest syntax is not supported by IE8.", re.compile(r"\.\.\.")),
    Rule("syntax.optional_chain", "Optional chaining is not supported by IE8.", re.compile(r"\?\.")),
    Rule("syntax.nullish", "Nullish coalescing is not supported by IE8.", re.compile(r"\?\?")),
    Rule(
        "api.array_helpers",
        "ES5+ array helpers need a polyfill in IE8; use an indexed loop here.",
        re.compile(r"\.\s*(forEach|map|filter|reduce|some|every|find|findIndex|includes)\s*\("),
    ),
    Rule("api.string_trim", "String.prototype.trim is not available in IE8.", re.compile(r"\.\s*trim\s*\(")),
    Rule(
        "api.object",
        "Object helper APIs need polyfills in IE8.",
        re.compile(r"\bObject\s*\.\s*(keys|create|assign|defineProperty|freeze|seal|getPrototypeOf)\s*\("),
    ),
    Rule("api.array_isarray", "Array.isArray needs a polyfill in IE8.", re.compile(r"\bArray\s*\.\s*isArray\s*\(")),
    Rule("api.date_now", "Date.now needs a polyfill in IE8.", re.compile(r"\bDate\s*\.\s*now\s*\(")),
    Rule("api.json", "JSON needs a polyfill in IE8 compatibility modes.", re.compile(r"\bJSON\s*\.")),
    Rule("api.bind", "Function.prototype.bind needs a polyfill in IE8.", re.compile(r"\.\s*bind\s*\(")),
)

WARNING_RULES = (
    Rule(
        "dom.add_event_listener",
        "addEventListener is not available in IE8; keep an attachEvent fallback next to it.",
        re.compile(r"\baddEventListener\b"),
        "warning",
    ),
    Rule(
        "dom.text_content",
        "textContent is not available in IE8; keep an innerText fallback next to it.",
        re.compile(r"\btextContent\b"),
        "warning",
    ),
    Rule(
        "dom.query_selector",
        "querySelector support is limited in IE8; prefer getElementById/getElementsByTagName.",
        re.compile(r"\bquerySelector(All)?\b"),
        "warning",
    ),
    Rule("dom.class_list", "classList is not available in IE8.", re.compile(r"\bclassList\b"), "warning"),
    Rule(
        "storage.web_storage",
        "Web Storage is not safe for IE8 compatibility; use cookies for language state.",
        re.compile(r"\b(localStorage|sessionStorage)\b"),
        "warning",
    ),
)


def mask_comments_and_strings(source: str) -> str:
    """Return code with comments and quoted strings blanked, preserving lines."""
    output: list[str] = []
    state = "code"
    quote = ""
    i = 0

    while i < len(source):
        char = source[i]
        nxt = source[i + 1] if i + 1 < len(source) else ""

        if state == "code":
            if char == "/" and nxt == "/":
                output.extend((" ", " "))
                state = "line_comment"
                i += 2
                continue
            if char == "/" and nxt == "*":
                output.extend((" ", " "))
                state = "block_comment"
                i += 2
                continue
            if char in ("'", '"'):
                output.append(" ")
                quote = char
                state = "string"
                i += 1
                continue
            output.append(char)
            i += 1
            continue

        if state == "line_comment":
            if char == "\n":
                output.append("\n")
                state = "code"
            else:
                output.append(" ")
            i += 1
            continue

        if state == "block_comment":
            if char == "*" and nxt == "/":
                output.extend((" ", " "))
                state = "code"
                i += 2
                continue
            output.append("\n" if char == "\n" else " ")
            i += 1
            continue

        if state == "string":
            if char == "\\" and i + 1 < len(source):
                output.append("\n" if char == "\n" else " ")
                output.append("\n" if nxt == "\n" else " ")
                i += 2
                continue
            if char == quote:
                output.append(" ")
                state = "code"
                i += 1
                continue
            if char == "\n":
                output.append("\n")
                state = "code"
            else:
                output.append(" ")
            i += 1

    return "".join(output)


def line_for_index(source: str, index: int) -> int:
    return source.count("\n", 0, index) + 1


def should_skip(path: Path, include_vendor: bool) -> bool:
    if include_vendor:
        return False
    lowered = str(path).lower()
    return any(hint in lowered for hint in VENDOR_HINTS)


def collect_files(paths: list[str], include_vendor: bool) -> tuple[list[Path], list[Path]]:
    files: list[Path] = []
    missing: list[Path] = []

    for raw_path in paths:
        path = Path(raw_path)
        if not path.exists():
            missing.append(path)
            continue
        if path.is_file():
            if path.suffix == ".js" and not should_skip(path, include_vendor):
                files.append(path)
            continue
        for root, _, names in os.walk(path):
            for name in names:
                candidate = Path(root) / name
                if candidate.suffix == ".js" and not should_skip(candidate, include_vendor):
                    files.append(candidate)

    return sorted(set(files)), missing


def scan_file(path: Path) -> list[Finding]:
    source = path.read_text(encoding="utf-8", errors="replace")
    masked = mask_comments_and_strings(source)
    findings: list[Finding] = []

    for rule in ERROR_RULES + WARNING_RULES:
        for match in rule.pattern.finditer(masked):
            findings.append(
                Finding(
                    path=path,
                    line=line_for_index(masked, match.start()),
                    severity=rule.severity,
                    code=rule.code,
                    message=rule.message,
                )
            )

    return findings


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check owned legacy JavaScript for IE8 compatibility.")
    parser.add_argument(
        "paths",
        nargs="*",
        help="JavaScript files or directories to scan. Defaults to the Persian language-switching layer.",
    )
    parser.add_argument(
        "--include-vendor",
        action="store_true",
        help="Do not skip minified/vendor-like files when a directory is scanned.",
    )
    parser.add_argument(
        "--strict-dom",
        action="store_true",
        help="Treat DOM compatibility warnings as failures.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    scan_paths = args.paths or list(DEFAULT_FILES)
    files, missing = collect_files(scan_paths, args.include_vendor)
    findings: list[Finding] = []

    for path in files:
        findings.extend(scan_file(path))

    errors = [finding for finding in findings if finding.severity == "error"]
    warnings = [finding for finding in findings if finding.severity == "warning"]

    print("IE8 compatibility gate")
    print("Scanned {0} JavaScript file(s).".format(len(files)))

    for path in missing:
        print("ERROR missing: {0}".format(path))
    for finding in sorted(findings, key=lambda item: (str(item.path), item.line, item.code)):
        print(
            "{0}:{1}: {2} {3}: {4}".format(
                finding.path,
                finding.line,
                finding.severity.upper(),
                finding.code,
                finding.message,
            )
        )

    if not missing and not errors and not (args.strict_dom and warnings):
        if warnings:
            print("PASS with {0} warning(s).".format(len(warnings)))
        else:
            print("PASS")
        return 0

    print(
        "FAIL: {0} error(s), {1} warning(s), {2} missing file(s).".format(
            len(errors),
            len(warnings),
            len(missing),
        )
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
