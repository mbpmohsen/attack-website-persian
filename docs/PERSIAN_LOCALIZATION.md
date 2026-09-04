# Persian Localization Pipeline

This fork keeps English as the canonical ATT&CK content and overlays Persian
fields when they are available. Missing translations therefore fall back to
English without removing content or stopping the build.

## Data Flow

1. `modules/site_config.py` resolves each English STIX source from
   `STIX_LOCATION_*` and each optional Persian source from
   `STIX_TRANSLATIONS_*`.
2. `modules.util.stixhelpers.get_stix_memory_stores()` downloads or copies the
   English bundle into `output/stix/`.
3. `overlay_stix_translations()` loads the Persian source and matches objects by
   STIX `id`. It copies only non-empty `name_fa` and `description_fa`; it never
   replaces `name` or `description`.
4. The merged bundle is loaded into the normal STIX `MemoryStore`, so existing
   Python modules and Jinja templates receive both languages.
5. `generate_stix_translation_javascript()` emits plain ES3 object literals for
   legacy text replacement. The explicit `localized` macros remain the primary
   rendering path.
6. Pelican renders both language blocks. `language.js` chooses Persian by
   default and switches visibility using `?lang=`, the `attack_language` cookie,
   and the language selector.
7. The search module strips tags from the rendered bilingual HTML, so both
   English and Persian terms are present in `output/search/*.json`.

Translation sources may be HTTP(S) bundle URLs, local bundle files, or local
directories containing single-object bundles. Directory input is scanned
recursively. A missing or invalid Persian source logs a warning and leaves the
English bundle usable.

## Configuration

`CTI_PERSIAN_BASE_URL` defaults to the Persian CTI fork independently of
`CTI_RAW_BASE_URL`. `STIX_TRANSLATIONS_ENTERPRISE` defaults to its aggregate
Enterprise bundle. Mobile, ICS, and PRE translation overrides default to empty
because their configured primary bundles currently already contain Persian
fields.

For a local tree of single-object bundles:

```sh
STIX_TRANSLATIONS_ENTERPRISE=/path/to/cti-persian/enterprise-attack \
uv run python update-attack.py --attack-brand --extras --no-test-exitstatus
```

## Measured Coverage

Measured on September 4, 2026 against active objects in the generated STIX:

| Domain | `name_fa` | `description_fa` |
| --- | ---: | ---: |
| Enterprise | 4,351 / 4,368 (99.61%) | 23,359 / 23,359 (100%) |
| Mobile | 661 / 662 (99.85%) | 2,200 / 2,200 (100%) |
| ICS | 454 / 454 (100%) | 1,057 / 1,057 (100%) |
| PRE-ATT&CK (deprecated) | 7 / 7 (100%) | 28 / 28 (100%) |
| Total | 5,473 / 5,491 (99.67%) | 26,644 / 26,644 (100%) |

The source described in the original localization brief has changed since that
brief was written. The current `cti-persian` master branch stores translated
single-object bundles directly under `enterprise-attack/<type>/` and also ships
an aggregate `enterprise-attack.json`. It now contains Persian data for more
than the three object types named in the brief. Coverage above records the
actual current build rather than the older estimate.

The 18 untranslated active names are 10 Enterprise campaigns, 6 Enterprise
intrusion sets, 1 Enterprise malware object, and 1 Mobile campaign. Objects
without descriptions (for example detection-strategy objects) are not counted
as missing description translations.

## Template And Search Audit

`techniques-domain-index.html` already uses the `localized` macro for its
description and counters, and its table macro receives bilingual technique
data. The ATT&CK-backed modules (`analytics`, `assets`, `campaigns`, data
components and sources, detection strategies, groups, matrices, mitigations,
software, tactics, and techniques) carry Persian fields into their templates.

No STIX-field wiring was added to `benefactors`, `blog`, `contribute`, `tour`,
`versions`, `redirections`, `random_page`, or `subdirectory`: they generate
static/editorial pages, redirects, routing helpers, or archived upstream output
rather than current ATT&CK objects. Search needed no schema change because its
rendered HTML index already contains both language blocks; a generated
Enterprise technique entry was verified to contain its Persian name and body.

## Reproduction And QA

```sh
uv pip install -r requirements.txt
uv run python update-attack.py --attack-brand --extras --no-test-exitstatus
uv run python -m unittest tests/test_stix_translation_overlay.py
uv run python tools/qa_persian_rtl.py --require-output --require-stix
python tools/ie8_compat_check.py
```

The generated translation script is about 17 MB after eliminating duplicate
description entries. Splitting by domain was considered, but Enterprise owns
most of the payload and several pages combine objects from multiple domains, so
simple domain splitting would add requests without materially reducing the
default download. A future optimization should generate page/type-specific
chunks with conditional loading rather than merely dividing the same payload.

The source translations still require editorial review. Examples observed
during this work include malformed bracket-heavy campaign text in `C0033` and
inconsistent security-context translations of “adversary” (`دشمنان`, `حریف`,
and related variants). This work intentionally preserves upstream translation
content and only fixes its delivery pipeline.
