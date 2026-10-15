"""ClauseWise legal corpus: rule cards plus load/lookup helpers."""

from clausewise_corpus.loader import CORPUS_VERSION, load_rules, lookup_rule, manifest

__all__ = ["CORPUS_VERSION", "load_rules", "lookup_rule", "manifest"]
