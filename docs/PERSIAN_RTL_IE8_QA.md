# Persian, RTL, and IE8 QA

This fork adds Persian content and a legacy-safe language switcher on top of the
static MITRE ATT&CK website build. Use these checks after generating `output/`
so Persian layout problems and IE8-breaking JavaScript are caught before deploy.

## Quick Commands

From the repository root:

```sh
python tools/qa_persian_rtl.py --output-dir output --stix-dir output/stix --require-output --require-stix
python tools/ie8_compat_check.py
```

The default content gate requires 99% `name_fa` coverage and 99.5%
`description_fa` coverage. These thresholds sit just below the measured current
coverage (99.67% and 100%, respectively), so they catch regressions while
allowing the known untranslated names. Override them when auditing another data
source:

```sh
python tools/qa_persian_rtl.py \
  --output-dir output \
  --stix-dir output/stix \
  --require-output \
  --require-stix \
  --min-name-coverage 99 \
  --min-description-coverage 99.5
```

## What The Persian/RTL Gate Checks

`tools/qa_persian_rtl.py` checks the generated static site and the generated STIX
JSON files.

It fails for:

- Missing Persian/RTL source files that the language feature depends on.
- Missing default Persian language setting, language cookie, or IE8 `attachEvent`
  fallback in `attack-theme/static/scripts/language.js`.
- Missing `.language-content-fa`, `html[lang="fa"]`, or Vazir font markers in
  the SCSS source.
- `TODO-FA` markers in generated HTML.
- Critical generated pages that are not emitted as `lang="fa"` and `dir="rtl"`.
- Persian alternate content blocks missing `lang="fa"` or `dir="rtl"`.
- `data-i18n` keys in generated HTML that have no Persian dictionary entry.
- STIX `name_fa` or `description_fa` coverage below the thresholds you pass.

It warns for:

- Missing generated `output/` or `output/stix/` when `--require-output` or
  `--require-stix` is not used.
- Archived version pages skipped by default.
- STIX objects or relationship descriptions that still need Persian fields.

Archived ATT&CK versions are skipped by default because they are copied from
upstream release archives and are not part of the current Persian translation
surface. Use `--include-archives` if you want to audit them too.

## What The IE8 Gate Checks

`tools/ie8_compat_check.py` scans the owned language switching JavaScript by
default:

- `attack-theme/static/scripts/language.js`
- `attack-theme/static/scripts/stix-translations.js`

It fails on ES5+ or ES6+ syntax and APIs that are unsafe for IE8, including
`let`, `const`, arrow functions, template literals, classes, modules,
optional chaining, array helpers, `Object.keys`, `Array.isArray`, `Date.now`,
`JSON.*`, and `.bind()`.

It warns on DOM APIs that can be safe only when feature-detected or paired with
fallbacks, including `addEventListener`, `textContent`, `querySelector`,
`classList`, and Web Storage.

Warnings do not fail the default gate because the current language script uses
feature detection and IE8 fallbacks. To make those warnings fail:

```sh
python tools/ie8_compat_check.py --strict-dom
```

To scan another legacy script:

```sh
python tools/ie8_compat_check.py attack-theme/static/scripts/language.js attack-theme/static/scripts/sidebar-load-all.js
```

To scan a directory and include vendor-like files:

```sh
python tools/ie8_compat_check.py attack-theme/static/scripts --include-vendor
```

## Recommended Build Flow

Use the existing build first, then run the gates:

```sh
cd attack-style
npm run build-copy
cd ..
python update-attack.py --attack-brand --extras --no-test-exitstatus
cd attack-search
npm run build
npm run copy
cd ..
python tools/qa_persian_rtl.py --output-dir output --stix-dir output/stix --require-output --require-stix
python tools/ie8_compat_check.py
```

For Vercel, the same two Python commands can be added to `vercel-build.sh` after
`update-attack.py` generates `output/`. Keep the IE8 gate focused on the owned
language scripts unless you are ready to triage upstream/vendor JavaScript too.

## Manual Persian/RTL Checklist

Run this checklist on a built deployment or local static server:

- Open `/`, `/techniques/enterprise/`, `/techniques/T1659/`, `/groups/`,
  `/software/`, and `/mitigations/`.
- Confirm the first paint is Persian by default, with `html lang="fa"` and
  `dir="rtl"` present before JavaScript runs.
- Confirm the language selector can switch to English and back to Persian.
- Open a second page after switching language and confirm the cookie preserves
  the preference.
- Confirm headings such as Techniques, Platforms, Versions, Procedure Examples,
  Groups, Software, and Mobile Mitigations are Persian in Persian mode.
- Confirm names and descriptions use `name_fa` and `description_fa` when those
  fields exist in the STIX JSON.
- Confirm tables, cards, breadcrumbs, sidebars, and dropdowns align correctly in
  RTL and do not overlap.
- Confirm the Persian font is Vazir, with Tahoma/Arial as fallback.
- Search the rendered page for `TODO-FA`; there should be no visible markers.

## IE8 Authoring Rules

Keep `attack-theme/static/scripts/language.js` and generated translation bundles
compatible with old browsers:

- Use `var`, not `let` or `const`.
- Use function expressions, not arrow functions.
- Use indexed `for` loops, not `forEach`, `map`, `filter`, or `reduce`.
- Use cookies for language persistence; do not use `localStorage`.
- Use `attachEvent` for IE8 and feature-detect any modern DOM API.
- Avoid `JSON.*` unless a tested IE8 polyfill is loaded first.
- Avoid `textContent` without an `innerText` fallback.
- Keep translation data as simple object literals generated at build time.

For CSS, keep the Persian layout compatible with the existing static theme:

- Prefer direction, text alignment, floats, and existing Bootstrap-era classes.
- Do not rely on CSS Grid or Flexbox for required Persian layout behavior.
- Keep the Vazir EOT font source before WOFF/TTF sources so IE8 can load it.

## Troubleshooting

If the Persian/RTL gate reports `TODO-FA`, update the source template or
translation dictionary, then rebuild. Do not edit files under `output/` directly.

If STIX coverage is low, inspect `output/stix/*.json` and add `name_fa` or
`description_fa` to the upstream Persian CTI fork, then rebuild this website.

The September 4, 2026 build scanned 6,442 current HTML files and skipped 41,047
archived files. Its active-STIX coverage was:

| Domain | `name_fa` | `description_fa` |
| --- | ---: | ---: |
| Enterprise | 4,351 / 4,368 (99.61%) | 23,359 / 23,359 (100%) |
| Mobile | 661 / 662 (99.85%) | 2,200 / 2,200 (100%) |
| ICS | 454 / 454 (100%) | 1,057 / 1,057 (100%) |
| PRE-ATT&CK (deprecated) | 7 / 7 (100%) | 28 / 28 (100%) |
| Total | 5,473 / 5,491 (99.67%) | 26,644 / 26,644 (100%) |

The gate reports 29 non-blocking warnings: 28 standalone/upstream changelog or
test pages lack the Persian root attributes, and 18 active named STIX objects
still lack `name_fa`.

If the IE8 gate reports an ES5+ helper, replace it with a simple loop or add a
documented polyfill before using that API. For the language switcher, prefer the
simple loop so Persian switching still works on IE8 without extra dependencies.
