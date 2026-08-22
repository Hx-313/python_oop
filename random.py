"""
company_name_researcher.py

Generate arbitrary brandable company names and research them.

Requirements:
    pip install requests dnspython beautifulsoup4

Run:
    python company_name_researcher.py
"""

import csv
import argparse
import importlib.util
import os
from pathlib import Path
import re
import socket
import string
import sysconfig
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote

# This file is named ``random.py``, which otherwise shadows Python's
# standard-library module of the same name when the script directory is on
# sys.path.  Load the standard-library implementation explicitly so that
# third-party imports (for example requests) can still import Random safely.
_stdlib_random_path = os.path.join(
    sysconfig.get_path("stdlib"),
    "random.py",
)
_stdlib_random_spec = importlib.util.spec_from_file_location(
    "_stdlib_random",
    _stdlib_random_path,
)
if _stdlib_random_spec is None or _stdlib_random_spec.loader is None:
    raise ImportError(
        f"Could not load the standard-library random module from {_stdlib_random_path}"
    )

random = importlib.util.module_from_spec(_stdlib_random_spec)
_stdlib_random_spec.loader.exec_module(random)

# If this file was imported as ``random`` rather than run as a script, expose
# the standard-library names on the in-progress module as well.  This keeps
# dependencies that use ``from random import Random`` working during import.
for _name, _value in vars(random).items():
    globals().setdefault(_name, _value)

import dns.resolver
import requests
from bs4 import BeautifulSoup


# ============================================================
# CONFIGURATION
# ============================================================

TARGET_RESULTS = 25

# How many candidates to generate before stopping.
MAX_CANDIDATES = 10000

TLD = ".com"

OUTPUT_FILE = "company_name_results.csv"

MARKDOWN_OUTPUT_FILE = "company_name_recommendations.md"

LIKED_OUTPUT_FILE = "liked_company_names.md"

REQUEST_TIMEOUT = 8

# Delay between search-engine requests.
SEARCH_DELAY = 1.5

# Number of concurrent domain/DNS checks.
MAX_WORKERS = 10

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/151.0 Safari/537.36"
)


# ============================================================
# PHONETIC GENERATOR
# ============================================================

# These are NOT company names.
#
# They are phonetic building blocks used only to construct
# completely new names algorithmically.

CONSONANTS = list(
    "bcdfghjklmnprstvwxz"
)

VOWELS = list(
    "aeiou"
)

CONSONANT_CLUSTERS = [
    "br", "cr", "dr", "fr", "gr",
    "kr", "pr", "tr", "vr",
    "bl", "cl", "fl", "gl",
    "pl", "sl",
    "ch", "sh",
    "th",
    "qu",
    "sk", "st", "sp",
    "sw",
    "x",
    "z",
]

ENDING_PATTERNS = [
    "a",
    "e",
    "i",
    "o",
    "u",
    "a",
    "o",
    "ia",
    "io",
    "ea",
    "on",
    "en",
    "in",
    "or",
    "ar",
    "er",
    "ix",
    "ex",
    "is",
    "os",
    "us",
    "um",
    "an",
    "en",
    "yn",
    "yx",
]


# ============================================================
# RANDOM HELPERS
# ============================================================

def random_vowel():
    return random.choice(VOWELS)


def random_consonant():
    return random.choice(CONSONANTS)


def random_cluster():
    return random.choice(CONSONANT_CLUSTERS)


# ============================================================
# NAME GENERATION
# ============================================================

def generate_syllable():
    """
    Generate one artificial phonetic syllable.

    Examples:
        va
        zen
        kra
        lo
        pri
    """

    pattern = random.choice([
        "CV",
        "CVC",
        "CCV",
        "CVV",
        "CCVC",
    ])

    result = ""

    for char in pattern:

        if char == "C":
            if random.random() < 0.25:
                result += random_cluster()
            else:
                result += random_consonant()

        elif char == "V":
            result += random_vowel()

    return result


def generate_raw_name():
    """
    Generate a completely artificial name.

    No predefined company names are used.
    """

    syllable_count = random.choice([2, 2, 3, 3, 4])

    name = ""

    for _ in range(syllable_count):
        name += generate_syllable()

    # Occasionally use an artificial ending.
    if random.random() < 0.45:
        name += random.choice(ENDING_PATTERNS)

    return clean_name(name)


def clean_name(name):
    """
    Make the generated name domain-safe.
    """

    name = name.lower()

    name = re.sub(
        r"[^a-z]",
        "",
        name
    )

    # Remove excessive repeated characters.
    name = re.sub(
        r"(.)\1{2,}",
        r"\1",
        name
    )

    return name


# ============================================================
# MEANINGFUL NAME GENERATOR
# ============================================================

# The offline vocabulary is intentionally small and curated.  It gives the
# generator semantic anchors while keeping it usable without an API key.
SEMANTIC_ROOTS = [
    {"root": "luma", "language": "Latin-inspired", "meaning": "light", "concept": "light"},
    {"root": "nova", "language": "Latin", "meaning": "new / star", "concept": "future"},
    {"root": "vida", "language": "Spanish/Portuguese", "meaning": "life", "concept": "growth"},
    {"root": "sync", "language": "English", "meaning": "together / coordinated", "concept": "connection"},
    {"root": "kumo", "language": "Japanese", "meaning": "cloud", "concept": "nature"},
    {"root": "dara", "language": "Persian-inspired", "meaning": "wisdom / wealth", "concept": "intelligence"},
    {"root": "navi", "language": "Sanskrit-inspired", "meaning": "guide / ship", "concept": "direction"},
    {"root": "sora", "language": "Japanese", "meaning": "sky", "concept": "nature"},
    {"root": "vivo", "language": "Latin/Italian", "meaning": "alive", "concept": "growth"},
    {"root": "tera", "language": "Greek", "meaning": "earth", "concept": "nature"},
    {"root": "sana", "language": "Arabic/Hindi", "meaning": "brilliance / praise", "concept": "trust"},
    {"root": "amity", "language": "English", "meaning": "friendship", "concept": "trust"},
    {"root": "zeno", "language": "Greek-inspired", "meaning": "stranger / open world", "concept": "future"},
    {"root": "mira", "language": "Latin/Slavic", "meaning": "wonder / peace", "concept": "trust"},
    {"root": "alto", "language": "Italian/Spanish", "meaning": "high", "concept": "future"},
    {"root": "eira", "language": "Welsh", "meaning": "snow", "concept": "nature"},
]


def load_roots(online=False):
    """Return semantic roots, with the offline lexicon as the safe fallback."""

    # The online boundary is deliberate: a translation provider can be added
    # later without coupling network behavior to candidate generation.
    return list(SEMANTIC_ROOTS)


def _candidate_metadata(name, style, roots):
    return {
        "name": clean_name(name),
        "style": style,
        "roots": [root["root"] for root in roots],
        "meanings": [root["meaning"] for root in roots],
        "languages": [root["language"] for root in roots],
        "concepts": [root["concept"] for root in roots],
    }


def generate_direct_candidate(rng, roots):
    root = rng.choice(roots)
    return _candidate_metadata(root["root"], "direct", [root])


def generate_blend_candidate(rng, roots):
    first, second = rng.sample(roots, 2)
    first_root = first["root"]
    second_root = second["root"]

    # Try a clean overlap when the first root ends where the second begins.
    overlap = 0
    for size in range(min(3, len(first_root), len(second_root)), 1, -1):
        if first_root[-size:] == second_root[:size]:
            overlap = size
            break

    name = first_root + second_root[overlap:]
    return _candidate_metadata(name, "blend", [first, second])


def generate_transform_candidate(rng, roots):
    root = rng.choice(roots)
    name = root["root"]

    transformations = [
        lambda value: value.replace("c", "q"),
        lambda value: value + rng.choice(["io", "ra", "ly"]),
        lambda value: value[:-1] if len(value) > 5 else value,
    ]
    name = rng.choice(transformations)(name)
    return _candidate_metadata(name, "transform", [root])


def generate_candidate(rng=None, roots=None):
    """Generate one meaningful candidate with semantic provenance."""

    rng = rng or random
    roots = roots or load_roots()
    generators = [
        generate_direct_candidate,
        generate_blend_candidate,
        generate_transform_candidate,
    ]

    for _ in range(30):
        candidate = rng.choice(generators)(rng, roots)
        candidate["name"] = clean_name(candidate["name"])
        if 5 <= len(candidate["name"]) <= 15:
            return candidate

    raise RuntimeError("Unable to generate a valid meaningful candidate")


# ============================================================
# NAME QUALITY
# ============================================================

def name_quality(name, semantic_bonus=0):
    """
    Basic brandability score.

    This is intentionally heuristic.
    """

    score = 100

    length = len(name)

    # Prefer roughly 5-11 characters.
    if length < 5:
        score -= 25

    elif length > 12:
        score -= 20

    elif length > 10:
        score -= 8

    # Too many consonants together.
    if re.search(r"[bcdfghjklmnpqrstvwxyz]{4,}", name):
        score -= 20

    # Too many vowels together.
    if re.search(r"[aeiou]{4,}", name):
        score -= 15

    # Difficult letter combinations.
    if any(
        sequence in name
        for sequence in [
            "qz",
            "zx",
            "xq",
            "jq",
            "qj",
        ]
    ):
        score -= 20

    # Repeated characters.
    if re.search(r"(.)\1", name):
        score -= 5

    return max(score + min(max(semantic_bonus, 0), 20), 0)


# ============================================================
# RDAP DOMAIN CHECK
# ============================================================

def check_rdap(domain):
    """
    Check domain registration status using RDAP.

    RDAP:
        200 -> domain exists
        4xx -> domain not found in the RDAP service

    Returns:
        REGISTERED
        POTENTIALLY_AVAILABLE
        UNKNOWN
    """

    url = (
        "https://rdap.org/domain/"
        + quote(domain)
    )

    try:

        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT,
            headers={
                "User-Agent": USER_AGENT
            },
        )

        if response.status_code == 200:

            return {
                "status": "REGISTERED",
                "http_code": response.status_code,
            }

        if 400 <= response.status_code < 500:

            return {
                "status": "POTENTIALLY_AVAILABLE",
                "http_code": response.status_code,
            }

        return {
            "status": "UNKNOWN",
            "http_code": response.status_code,
        }

    except requests.RequestException as error:

        return {
            "status": "ERROR",
            "http_code": "",
            "error": str(error),
        }


# ============================================================
# DNS CHECK
# ============================================================

def check_dns(domain):
    """
    Check whether the domain resolves through DNS.
    """

    try:

        answers = dns.resolver.resolve(
            domain,
            "A",
            lifetime=5,
        )

        addresses = [
            answer.address
            for answer in answers
        ]

        return {
            "dns": True,
            "addresses": addresses,
        }

    except Exception:

        return {
            "dns": False,
            "addresses": [],
        }


# ============================================================
# WEBSITE CHECK
# ============================================================

def check_website(domain):
    """
    Check whether an actual HTTP/HTTPS website responds.
    """

    urls = [
        f"https://{domain}",
        f"http://{domain}",
    ]

    for url in urls:

        try:

            response = requests.get(
                url,
                timeout=REQUEST_TIMEOUT,
                allow_redirects=True,
                headers={
                    "User-Agent": USER_AGENT
                },
            )

            return {
                "website": True,
                "status_code": response.status_code,
                "final_url": response.url,
                "title": extract_title(response.text),
            }

        except requests.RequestException:
            continue

    return {
        "website": False,
        "status_code": "",
        "final_url": "",
        "title": "",
    }


def extract_title(html):
    """
    Extract page title.
    """

    try:

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        if soup.title:
            return soup.title.get_text(
                strip=True
            )[:200]

    except Exception:
        pass

    return ""


# ============================================================
# SEARCH ENGINE RESEARCH
# ============================================================

def search_web(name):
    """
    Search DuckDuckGo HTML for exact-name company results.

    This is intended as a discovery signal, NOT a legal
    trademark/company-name clearance.
    """

    queries = [
        f'"{name}" company',
        f'"{name}" software',
        f'"{name}" startup',
    ]

    results = []

    headers = {
        "User-Agent": USER_AGENT
    }

    for query in queries:

        url = (
            "https://html.duckduckgo.com/html/?q="
            + quote(query)
        )

        try:

            response = requests.get(
                url,
                timeout=REQUEST_TIMEOUT,
                headers=headers,
            )

            if response.status_code != 200:
                continue

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            for result in soup.select(
                ".result"
            ):

                title_element = result.select_one(
                    ".result__a"
                )

                snippet_element = result.select_one(
                    ".result__snippet"
                )

                if not title_element:
                    continue

                title = title_element.get_text(
                    " ",
                    strip=True
                )

                snippet = ""

                if snippet_element:
                    snippet = snippet_element.get_text(
                        " ",
                        strip=True
                    )

                results.append({
                    "title": title,
                    "snippet": snippet,
                })

            time.sleep(SEARCH_DELAY)

        except requests.RequestException:
            continue

    # Remove duplicate titles.
    unique = {}

    for result in results:
        unique[result["title"]] = result

    return list(unique.values())[:15]


# ============================================================
# EXACT NAME MATCH
# ============================================================

def exact_match_score(name, search_results):
    """
    Determine whether search results contain the exact
    generated name.

    This is deliberately conservative.
    """

    name_lower = name.lower()

    matches = 0

    for result in search_results:

        text = (
            result["title"]
            + " "
            + result["snippet"]
        ).lower()

        # Search as a standalone-ish word.
        if re.search(
            rf"\b{re.escape(name_lower)}\b",
            text,
        ):
            matches += 1

    return matches


# ============================================================
# FINAL SCORE
# ============================================================

def calculate_score(
    name,
    rdap,
    dns,
    website,
    search_results,
    semantic_bonus=0,
):
    """
    Calculate an opportunity score.

    Higher = more interesting.
    """

    score = name_quality(name, semantic_bonus=semantic_bonus)

    # Domain availability is very important.
    if rdap["status"] == "POTENTIALLY_AVAILABLE":
        score += 40

    elif rdap["status"] == "REGISTERED":
        score -= 50

    else:
        score -= 10

    # DNS.
    if dns["dns"]:
        score -= 15

    # Website.
    if website["website"]:
        score -= 20

    # Search presence.
    matches = exact_match_score(
        name,
        search_results
    )

    score -= min(
        matches * 12,
        40
    )

    return max(
        min(score, 100),
        0
    )


# ============================================================
# RESEARCH ONE NAME
# ============================================================

def research_name(candidate):

    if isinstance(candidate, str):
        candidate = _candidate_metadata(
            candidate,
            "direct",
            [],
        )

    name = candidate["name"]

    domain = name + TLD

    print(
        f"\n🔎 Researching: {name}"
        f"  →  {domain}"
    )

    if candidate["roots"]:
        print(
            f"   Meaning:    {candidate['style']} | "
            f"{', '.join(candidate['meanings'])}"
        )

    rdap = check_rdap(domain)

    # If registered, we can still research it,
    # but it is unlikely to be useful.
    dns = check_dns(domain)

    website = check_website(domain)

    search_results = search_web(name)

    score = calculate_score(
        name=name,
        rdap=rdap,
        dns=dns,
        website=website,
        search_results=search_results,
        semantic_bonus=15 if candidate["roots"] else 0,
    )

    exact_matches = exact_match_score(
        name,
        search_results
    )

    result = {
        "name": name,
        "display_name": name.title(),
        "name_style": candidate["style"],
        "roots": " | ".join(candidate["roots"]),
        "meanings": " | ".join(candidate["meanings"]),
        "languages": " | ".join(candidate["languages"]),
        "domain": domain,
        "domain_status": rdap["status"],
        "dns": dns["dns"],
        "website": website["website"],
        "website_status": website["status_code"],
        "website_url": website["final_url"],
        "website_title": website["title"],
        "search_results": len(search_results),
        "exact_matches": exact_matches,
        "brand_score": name_quality(
            name,
            semantic_bonus=15 if candidate["roots"] else 0,
        ),
        "opportunity_score": score,
    }

    print(
        f"   Domain:      {rdap['status']}"
    )

    print(
        f"   DNS:         "
        f"{'YES' if dns['dns'] else 'NO'}"
    )

    print(
        f"   Website:     "
        f"{'YES' if website['website'] else 'NO'}"
    )

    print(
        f"   Search:      "
        f"{len(search_results)} results"
    )

    print(
        f"   Exact hits:  "
        f"{exact_matches}"
    )

    print(
        f"   Score:       "
        f"{score}/100"
    )

    return result


# ============================================================
# SAVE CSV
# ============================================================

def save_results(results):

    if not results:
        return

    fieldnames = [
        "name",
        "display_name",
        "name_style",
        "roots",
        "meanings",
        "languages",
        "domain",
        "domain_status",
        "dns",
        "website",
        "website_status",
        "website_url",
        "website_title",
        "search_results",
        "exact_matches",
        "brand_score",
        "opportunity_score",
    ]

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for result in results:
            writer.writerow(result)


def initialize_markdown_output(path=MARKDOWN_OUTPUT_FILE):
    """Create the Markdown report without erasing earlier recommendations."""

    output_path = Path(path)
    if not output_path.exists() or output_path.stat().st_size == 0:
        output_path.write_text(
            "# Company Name Recommendations\n\n"
            "Generated one candidate at a time by the company name researcher.\n\n",
            encoding="utf-8",
        )


def append_markdown_recommendation(result, path=MARKDOWN_OUTPUT_FILE, strong=False):
    """Append one researched candidate so it is visible immediately."""

    output_path = Path(path)
    if not output_path.exists() or output_path.stat().st_size == 0:
        initialize_markdown_output(output_path)

    def value(field, fallback="Not available"):
        current = result.get(field, fallback)
        return current if current not in (None, "") else fallback

    section = (
        f"## {value('display_name', result.get('name', 'Unnamed'))}\n\n"
        "- [ ] Keep this name\n"
        f"- **Strong candidate:** {'Yes' if strong else 'No'}\n"
        f"- **Style:** {value('name_style')}\n"
        f"- **Roots:** {value('roots')}\n"
        f"- **Meanings:** {value('meanings')}\n"
        f"- **Languages:** {value('languages')}\n"
        f"- **Domain:** `{value('domain')}`\n"
        f"- **Domain status:** {value('domain_status')}\n"
        f"- **DNS:** {'Yes' if result.get('dns') else 'No'}\n"
        f"- **Website:** {'Yes' if result.get('website') else 'No'}\n"
        f"- **Search results:** {value('search_results', 0)}\n"
        f"- **Exact matches:** {value('exact_matches', 0)}\n"
        f"- **Brand score:** {value('brand_score', 0)}/100\n"
        f"- **Opportunity score:** {value('opportunity_score', 0)}/100\n\n"
        "---\n\n"
    )

    with output_path.open("a", encoding="utf-8") as file:
        file.write(section)


def collect_liked_names(
    source=MARKDOWN_OUTPUT_FILE,
    output=LIKED_OUTPUT_FILE,
):
    """Copy manually checked recommendation sections into a separate file."""

    source_text = Path(source).read_text(encoding="utf-8")
    sections = re.split(r"(?=^## )", source_text, flags=re.MULTILINE)
    liked_sections = [
        section
        for section in sections
        if re.search(r"^- \[[xX]\] Keep this name$", section, re.MULTILINE)
    ]

    liked_text = (
        "# Liked Company Names\n\n"
        "Names manually marked with `[x]` in the recommendations file.\n\n"
    )
    if liked_sections:
        liked_text += "\n".join(liked_sections).rstrip() + "\n"
    else:
        liked_text += "No names have been marked yet.\n"

    Path(output).write_text(liked_text, encoding="utf-8")
    return len(liked_sections)


# ============================================================
# MAIN
# ============================================================

def main():

    initialize_markdown_output()

    print()
    print("=" * 70)
    print("       AUTOMATED COMPANY NAME RESEARCHER")
    print("=" * 70)
    print()

    print(
        f"Target strong candidates: {TARGET_RESULTS}"
    )

    print(
        f"Maximum candidates:       {MAX_CANDIDATES}"
    )

    print(
        f"TLD:                      {TLD}"
    )

    print()

    generated_names = set()

    strong_results = []

    all_results = []

    candidates_checked = 0

    while (
        candidates_checked < MAX_CANDIDATES
        and len(strong_results) < TARGET_RESULTS
    ):

        # ----------------------------------------------------
        # Generate a new arbitrary name
        # ----------------------------------------------------

        candidate = generate_candidate(random)
        name = candidate["name"]

        # Validate.
        if not name:
            continue

        if name in generated_names:
            continue

        if len(name) < 5:
            continue

        if len(name) > 15:
            continue

        generated_names.add(name)

        candidates_checked += 1

        # ----------------------------------------------------
        # Research
        # ----------------------------------------------------

        result = research_name(candidate)

        all_results.append(result)

        # ----------------------------------------------------
        # Keep promising names
        # ----------------------------------------------------

        is_strong_candidate = (
            result["domain_status"]
            == "POTENTIALLY_AVAILABLE"
            and result["opportunity_score"] >= 70
            and result["exact_matches"] == 0
        )

        append_markdown_recommendation(
            result,
            strong=is_strong_candidate,
        )

        if is_strong_candidate:

            print(
                "   ⭐ STRONG CANDIDATE"
            )

            strong_results.append(result)

            # Save immediately.
            save_results(strong_results)

    # ========================================================
    # FINAL OUTPUT
    # ========================================================

    strong_results.sort(
        key=lambda x: x["opportunity_score"],
        reverse=True,
    )

    save_results(strong_results)

    print()
    print("=" * 70)
    print("                    RESULTS")
    print("=" * 70)
    print()

    print(
        f"Names generated: {candidates_checked}"
    )

    print(
        f"Strong candidates: {len(strong_results)}"
    )

    print(
        f"Saved to: {OUTPUT_FILE}"
    )

    print()

    for index, result in enumerate(
        strong_results,
        start=1,
    ):

        print(
            f"{index:02d}. "
            f"{result['name']:<15} "
            f"{result['domain']:<20} "
            f"{result['opportunity_score']}/100"
        )

    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate and research meaningful company names."
    )
    parser.add_argument(
        "--collect-liked",
        action="store_true",
        help="copy names marked [x] into liked_company_names.md",
    )
    args = parser.parse_args()

    if args.collect_liked:
        count = collect_liked_names()
        print(f"Collected {count} liked name(s) into {LIKED_OUTPUT_FILE}")
    else:
        main()
