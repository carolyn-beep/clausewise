"""Primary-source domain allowlist (PLAN.md §7.4, §11.5).

A rule card's ``source_url`` must point at an official government source. Any ``*.gov`` host
is allowed, plus a short list of non-``.gov`` open-data sources we explicitly trust.
"""

from urllib.parse import urlparse

# Non-.gov sources that are still authoritative open data. Every official legislature site in
# scope (CA, NY, TX, WA, IL, MA) is already a *.gov host and is covered by the .gov rule.
EXTRA_ALLOWLISTED_HOSTS: tuple[str, ...] = (
    "courtlistener.com",
    "api.legiscan.com",
)


def is_allowlisted(url: str) -> bool:
    """Return True if ``url``'s host is a ``.gov`` domain or an explicitly trusted host."""
    host = (urlparse(url).hostname or "").lower()
    if not host:
        return False
    if host == "gov" or host.endswith(".gov"):
        return True
    return any(
        host == allowed or host.endswith("." + allowed) for allowed in EXTRA_ALLOWLISTED_HOSTS
    )
