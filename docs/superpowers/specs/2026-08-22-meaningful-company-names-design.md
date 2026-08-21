# Meaningful Multilingual Company Name Generator

## Goal

Replace the current phonetic-only name generator with a hybrid generator that creates pronounceable brand names from meaningful multilingual roots, while preserving the existing domain and web research pipeline.

## Design

The generator will use a small offline semantic lexicon as its reliable foundation and expose an optional online expansion hook for future broader language coverage. Offline generation remains the default so the script works without an API key or network access during name creation.

Each lexicon entry contains:

- `root`: the source fragment used in a candidate
- `language`: the source or inspiration language
- `meaning`: the English meaning
- `concept`: a normalized category such as light, growth, trust, connection, nature, intelligence, or future

The generator will produce three styles:

1. **Direct** — a short root used as a name, such as `Luma`.
2. **Blend** — two compatible roots joined and lightly normalized, such as `Lumora`.
3. **Transform** — a root with a restrained brand spelling change or shortening, such as `Synq` from `sync`.

Every generated candidate will retain metadata describing its roots, meanings, languages, and style. This metadata will be shown in terminal output and written to CSV.

## Generation rules

- Prefer candidates from 5–12 letters; reject candidates longer than 15 letters.
- Keep names lowercase for domain checks and display a title-cased brand form.
- Permit only alphabetic ASCII output for `.com` domain compatibility.
- Avoid arbitrary consonant/vowel syllable assembly as the primary strategy.
- Allow a small set of explicit transformations: vowel removal, safe suffixes, root overlap, and duplicate-letter cleanup.
- Avoid transformations that obscure the source meaning or create difficult pronunciation.
- Prevent duplicate names and duplicate root combinations within one run.

## Semantic scoring

The existing quality score will be extended with:

- semantic traceability: the candidate has known roots and meanings
- pronounceability: reasonable vowel/consonant balance and no difficult clusters
- brandability: concise length and distinctive spelling
- transformation restraint: direct names score higher than heavily distorted names

Domain availability, DNS, website, and search signals remain part of the final opportunity score. The script will not claim trademark or legal availability.

## Optional online expansion

The architecture will isolate vocabulary loading behind a function so a future online provider can add roots without changing generation, scoring, or research code. Online expansion will be optional and must fail back to the offline lexicon when unavailable.

## Output

CSV output will retain the existing research fields and add:

- `display_name`
- `name_style`
- `roots`
- `meanings`
- `languages`

Terminal output will show the candidate’s display name, style, semantic roots, and meanings before the domain research results.

## Testing

Tests will cover:

- deterministic generation with a seeded random source
- valid ASCII/domain-safe output
- direct, blend, and transformed name metadata
- semantic roots and meanings being preserved
- duplicate prevention
- scoring preference for meaningful names
- existing exact-match and research scoring behavior remaining intact

The existing standard-library shadowing regression test will remain passing.

## Scope

This redesign changes name generation, metadata, scoring, and CSV/terminal presentation. It does not add a live translation provider in this iteration; it only establishes the isolated fallback boundary for one.
