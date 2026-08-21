# Meaningful Company Names Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace phonetic-only name generation with meaningful multilingual roots, restrained brand transformations, semantic metadata, and meaning-aware scoring.

**Architecture:** Keep the existing research pipeline in `random.py`. Replace the phonetic generator with isolated vocabulary, candidate-generation, metadata, and semantic-scoring helpers. Candidate generation will use the offline lexicon by default and expose a loader boundary for future online expansion without requiring network access.

**Tech Stack:** Python 3.10+, `unittest`, existing `requests`, `dnspython`, and `beautifulsoup4` dependencies.

## Global Constraints

- Offline generation must work without an API key or online translation service.
- Candidate names must be ASCII alphabetic strings suitable for `.com` checks.
- Candidate metadata must preserve roots, meanings, languages, and generation style.
- Existing RDAP, DNS, website, and search behavior must remain available.
- No trademark or legal-availability claims may be added.

---

### Task 1: Add failing tests for meaningful candidate generation

**Files:**
- Create: `tests/test_name_generation.py`
- Test: `tests/test_name_generation.py`

**Interfaces:**
- Consumes: `generate_candidate`, `clean_name`, `name_quality` from `random.py` loaded by file path.
- Produces: executable expectations for candidate metadata, domain-safe output, and semantic scoring.

- [ ] **Step 1: Write the failing tests**

```python
import importlib.util
import random as stdlib_random
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "random.py"
SPEC = importlib.util.spec_from_file_location("company_name_researcher", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class NameGenerationTests(unittest.TestCase):
    def test_seeded_candidate_has_meaningful_metadata(self):
        candidate = MODULE.generate_candidate(stdlib_random.Random(7))

        self.assertRegex(candidate["name"], r"^[a-z]{5,15}$")
        self.assertIn(candidate["style"], {"direct", "blend", "transform"})
        self.assertTrue(candidate["roots"])
        self.assertEqual(len(candidate["roots"]), len(candidate["meanings"]))
        self.assertEqual(len(candidate["roots"]), len(candidate["languages"]))

    def test_semantic_score_rewards_known_roots(self):
        meaningful = MODULE.name_quality("lumora", semantic_bonus=15)
        phonetic = MODULE.name_quality("brxqzt", semantic_bonus=0)

        self.assertGreater(meaningful, phonetic)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `py -m unittest -v tests/test_name_generation.py`

Expected: FAIL because `generate_candidate` and the `semantic_bonus` parameter do not yet exist.

### Task 2: Implement vocabulary and candidate generation

**Files:**
- Modify: `random.py` in the generator section
- Test: `tests/test_name_generation.py`

**Interfaces:**
- Consumes: seeded `random.Random`-compatible object and offline semantic lexicon.
- Produces: `generate_candidate(rng) -> dict`, `generate_direct_candidate`, `generate_blend_candidate`, `generate_transform_candidate`, and `load_roots(online=False) -> list[dict]`.

- [ ] **Step 1: Add the offline semantic lexicon**

Add entries with `root`, `language`, `meaning`, and `concept` fields for concepts including light, growth, trust, connection, nature, intelligence, and future. Include roots such as `luma`, `nova`, `vida`, `syn`, `kumo`, `dara`, `navi`, `sora`, `vivo`, and `tera`.

- [ ] **Step 2: Add `load_roots` with offline fallback**

```python
def load_roots(online=False):
    """Return offline roots; reserve an optional online expansion hook."""
    return list(SEMANTIC_ROOTS)
```

- [ ] **Step 3: Add direct, blend, and transform generators**

Each function must return a dictionary containing `name`, `style`, `roots`, `meanings`, and `languages`. Blends must use two roots, preserve at least one recognizable root segment, and transform only through explicit rules such as removing a vowel or adding a safe suffix.

- [ ] **Step 4: Add `generate_candidate`**

Select one of the three styles using the supplied random object, normalize with `clean_name`, reject names outside the configured length range, and retry a bounded number of times before raising a clear `RuntimeError`.

- [ ] **Step 5: Run the focused tests**

Run: `py -m unittest -v tests/test_name_generation.py`

Expected: PASS.

### Task 3: Integrate metadata into research, scoring, and CSV output

**Files:**
- Modify: `random.py` in `name_quality`, `research_name`, `save_results`, and `main`
- Test: `tests/test_name_generation.py`

**Interfaces:**
- Consumes: candidate dictionaries from `generate_candidate`.
- Produces: research result rows with semantic metadata and a semantic bonus in scoring.

- [ ] **Step 1: Extend `name_quality`**

Change the signature to `name_quality(name, semantic_bonus=0)` and add the bounded bonus after existing heuristic deductions.

- [ ] **Step 2: Update `research_name`**

Accept a candidate dictionary, research `candidate["name"]`, and add `display_name`, `name_style`, `roots`, `meanings`, and `languages` to the returned result. Keep compatibility by allowing a string input to be wrapped as a direct candidate.

- [ ] **Step 3: Update CSV fields and terminal output**

Serialize root, meaning, and language lists with `" | "`. Print the candidate style and semantic explanation before domain checks.

- [ ] **Step 4: Update `main` to use candidate metadata**

Generate candidates using one seeded-capable random object, deduplicate by normalized name, and pass the candidate dictionary into `research_name`.

- [ ] **Step 5: Run focused tests and compile checks**

Run: `py -m unittest -v tests/test_name_generation.py test_random_startup.py`

Run: `py -m py_compile random.py`

Expected: all tests pass and compilation succeeds.

### Task 4: Verify the researcher behavior and document setup

**Files:**
- Modify: `requirements.txt` if dependency constraints need pinning
- Test: `tests/test_name_generation.py`, `test_random_startup.py`

**Interfaces:**
- Consumes: complete meaningful generator and existing research functions.
- Produces: verified local run path and reproducible dependency instructions.

- [ ] **Step 1: Run the full local test suite**

Run: `py -m unittest discover -v`

Expected: all tests pass.

- [ ] **Step 2: Run a bounded offline generation smoke test**

Run:

```powershell
py -c "import random as m; print(m.generate_candidate(m.random.Random(11)))"
```

Expected: a dictionary containing a domain-safe name and non-empty semantic metadata.

- [ ] **Step 3: Review the diff for accidental behavior changes**

Run: `git diff --check; git diff -- random.py tests/test_name_generation.py requirements.txt`

Expected: no whitespace errors and only generator redesign changes.
