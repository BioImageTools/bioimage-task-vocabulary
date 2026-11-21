"""Build the vocabulary: validate the YAML sources and generate Markdown and RDF.

Sources (edit these):   vocabulary/*.yaml, templates/*.md.j2, schema/*.yaml
Generated (do not edit): vocabulary/*.md, vocabulary/bioimage_task_vocabulary.ttl

Usage:
    python scripts/build.py                 # validate and regenerate
    python scripts/build.py --check         # validate; fail if generated files are stale
    python scripts/build.py --edam-owl PATH_OR_URL   # also check EDAM ids and labels
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader
from linkml.generators.pythongen import PythonGenerator
from linkml.validator import validate
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import rdflib_dumper
from rdflib import RDF, SKOS, Graph, URIRef
from rdflib.compare import to_canonical_graph

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schema" / "bioimage_task_vocabulary.yaml"
VOCAB = ROOT / "vocabulary"
TEMPLATES = ROOT / "templates"
SOURCES = ["terms", "object_types", "roles", "operations", "categories"]
PAGES = ["object_types", "roles", "operations", "categories"]
TTL = VOCAB / "bioimage_task_vocabulary.ttl"
BIOPORTAL = "https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid="
SUPERSCRIPT = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def fail(errors: list[str]) -> None:
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)


# --------------------------------------------------------------------------- load + validate

def load() -> dict:
    data = {}
    for name in SOURCES:
        part = yaml.safe_load((VOCAB / f"{name}.yaml").read_text())
        if set(part) != {name}:
            fail([f"vocabulary/{name}.yaml must have exactly one top-level key, '{name}'"])
        data.update(part)
    return data


def check_schema(data: dict) -> None:
    report = validate(data, str(SCHEMA), "Vocabulary")
    if report.results:
        fail([r.message for r in report.results])


def check_references(data: dict, sv: SchemaView) -> dict[str, dict]:
    """Ids are unique, and every reference points to an existing id of the right class."""
    ids: dict[str, str] = {}  # id -> class name
    errors: list[str] = []
    refs: list[tuple[str, str, str]] = []  # (where, value, expected class)

    def walk(obj: dict, cls: str, where: str) -> None:
        id_slot = sv.get_identifier_slot(cls)
        if id_slot and obj.get(id_slot.name):
            where = obj[id_slot.name]
            if where in ids:
                errors.append(f"duplicate id {where}")
            ids[where] = cls
        for slot in sv.class_induced_slots(cls):
            if slot.identifier or obj.get(slot.name) is None:
                continue
            value = obj[slot.name]
            rng = slot.range
            if rng not in sv.all_classes():
                continue
            values = value if isinstance(value, list) else [value]
            inlined = slot.inlined or slot.inlined_as_list or sv.get_identifier_slot(rng) is None
            for v in values:
                if inlined:
                    # A list item's own class may be a subclass; ObjectType.subtypes -> Subtype etc.
                    walk(v, rng, where)
                else:
                    refs.append((where, v, rng))

    walk(data, "Vocabulary", "root")
    for where, value, rng in refs:
        allowed = {rng, *sv.class_descendants(rng)}
        if value not in ids:
            errors.append(f"{where}: unknown reference {value}")
        elif ids[value] not in allowed:
            errors.append(f"{where}: {value} is a {ids[value]}, expected {rng}")
    if errors:
        fail(errors)
    return ids


def check_edam(data: dict, source: str) -> None:
    raw = urllib.request.urlopen(source).read() if "://" in source else Path(source).read_bytes()
    ns = {
        "owl": "http://www.w3.org/2002/07/owl#",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    }
    about = "{%s}about" % ns["rdf"]
    labels = {}
    for c in ET.fromstring(raw).findall("owl:Class", ns):
        label = c.find("rdfs:label", ns)
        if c.get(about) and label is not None and c.find("owl:deprecated", ns) is None:
            labels[c.get(about).rsplit("/", 1)[-1]] = label.text
    errors = []
    for term in (t for t in data["terms"] if t["id"].startswith("edam:")):
        local = term["id"].split(":", 1)[1]
        if local not in labels:
            errors.append(f"{term['id']} not found (or deprecated) in {source}")
        elif labels[local] != term["label"]:
            errors.append(f"{term['id']}: label is '{labels[local]}' in EDAM, '{term['label']}' here")
    if errors:
        fail(errors)


# --------------------------------------------------------------------------- RDF

def to_turtle(data: dict, sv: SchemaView) -> str:
    module = PythonGenerator(str(SCHEMA)).compile_module()
    graph = rdflib_dumper.as_rdf_graph(module.Vocabulary(**data), sv)
    # Type every concept as skos:Concept too, so SKOS tools see it without the schema.
    concept_classes = [sv.get_uri(c, expand=True) for c in sv.class_descendants("Concept", reflexive=False)]
    for cls in concept_classes:
        for s in list(graph.subjects(RDF.type, URIRef(cls))):
            graph.add((s, RDF.type, SKOS.Concept))
    canonical = Graph()  # stable blank-node labels, so --check is reliable
    for triple in to_canonical_graph(graph):
        canonical.add(triple)
    for prefix, ns in graph.namespaces():
        canonical.bind(prefix, ns, replace=True)
    return canonical.serialize(format="turtle")


# --------------------------------------------------------------------------- Markdown

def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


class Renderer:
    """Helpers available in templates. Records the ontology terms used, for the link definitions."""

    def __init__(self, data: dict, prefixes: dict[str, str]):
        self.data = data
        self.prefixes = prefixes
        self.by_id: dict[str, dict] = {}
        self.parent: dict[str, dict] = {}
        for t in data["terms"]:
            self.by_id[t["id"]] = t
        for t in data["object_types"]:
            self.by_id[t["id"]] = t
            for s in t.get("subtypes") or []:
                self.by_id[s["id"]] = s
                self.parent[s["id"]] = t
        for key in ("roles", "operations", "categories"):
            for c in data[key]:
                self.by_id[c["id"]] = c
        self.edam_used: list[str] = []

    # -- links
    def anchor(self, concept: dict) -> str:
        return f'<a id="{slug(concept["label"])}"></a>'

    def op_link(self, op_id: str, italic: bool = False, page: str = "operations.md") -> str:
        label = self.by_id[op_id]["label"]
        text = f"*{label}*" if italic else label
        return f"[{text}]({page}#{slug(label)})"

    @staticmethod
    def ref_key(term_id: str) -> str:
        """Reference-link key: the bare EDAM ID for EDAM terms, the CURIE for others."""
        return term_id.split(":", 1)[1] if term_id.startswith("edam:") else term_id

    def edam(self, term_id: str, text: str | None = None) -> str:
        """Link to an ontology term (EDAM or other), labelled with its label unless text is given."""
        if term_id not in self.edam_used:
            self.edam_used.append(term_id)
        return f"[{text or self.by_id[term_id]['label']}][{self.ref_key(term_id)}]"

    def term(self, term_id: str) -> str:
        """Link labelled with the term's label and its ontology, e.g. "table (IAO)"."""
        prefix = term_id.split(":", 1)[0]
        source = "EDAM" if prefix == "edam" else prefix
        return self.edam(term_id, f"{self.by_id[term_id]['label']} ({source})")

    def edam_id(self, term_id: str) -> str:
        key = term_id.split(":", 1)[1]
        return self.edam(term_id, f"`{key}`")

    def edam_definitions(self) -> str:
        lines = ["<!-- Ontology term links. EDAM: key = EDAM ID, URL = BioPortal page for "
                 "http://edamontology.org/<ID>. Others: key = CURIE, URL = the term IRI. -->"]
        for term_id in self.edam_used:
            prefix, local = term_id.split(":", 1)
            iri = self.prefixes[prefix] + local
            url = BIOPORTAL + urllib.parse.quote(iri, safe="") if prefix == "edam" else iri
            lines.append(f"[{self.ref_key(term_id)}]: {url}")
        return "\n".join(lines) + "\n"

    # -- object type mappings
    MATCHES = [("exact_match", "exact"), ("close_match", "close"), ("broad_match", "broad"),
               ("narrow_match", "narrow"), ("related_match", "related")]

    def mappings(self, concept: dict) -> str:
        parts = []
        for slot, word in self.MATCHES:
            if concept.get(slot):
                parts.append(f"*{word}*: " + ", ".join(self.term(t) for t in concept[slot]))
        return "; ".join(parts)

    @staticmethod
    def models(concept: dict) -> str:
        return ", ".join(f"{m['model']} [{m['element']}]({m['url']})"
                         for m in concept.get("data_model_equivalents") or [])

    # -- operations
    def kind(self, kind_id: str) -> str:
        if kind_id in self.parent:
            return f"{self.by_id[kind_id]['label']} {self.parent[kind_id]['label']}"
        return self.by_id[kind_id]["label"]

    def port(self, p: dict) -> str:
        text = " or ".join(self.kind(k) for k in p.get("accepts") or []) or "any"
        if p.get("role"):
            text += f" ({self.by_id[p['role']]['label']})"
        if p.get("qualifier"):
            text += f" ({p['qualifier']})"
        return text

    def ports(self, ps: list[dict]) -> str:
        out = ""
        for i, p in enumerate(ps):
            if i == 0:
                out = self.port(p)
            elif p.get("optional"):
                out += f" [+ {self.port(p)}]"
            else:
                out += f" + {self.port(p)}"
        return out

    def io(self, sig: dict) -> str:
        return f"{self.ports(sig.get('inputs') or [])} → {self.ports(sig['outputs'])}"

    @staticmethod
    def codes(names: list[str] | None) -> str:
        return ", ".join(f"`{n}`" for n in names or [])

    # -- categories
    def footnotes(self) -> list[dict]:
        """One footnote per EDAM class used by a task example, numbered in order of appearance."""
        notes: dict[str, dict] = {}
        for c in self.data["categories"]:
            for ex in c.get("task_examples") or []:
                if ex.get("close_match"):
                    n = notes.setdefault(ex["close_match"], {"term": ex["close_match"], "examples": [],
                                                             "note": ex.get("edam_note")})
                    n["examples"].append(ex["label"])
        for i, n in enumerate(notes.values(), 1):
            n["number"] = i
        return list(notes.values())

    def task_examples(self, category: dict, footnotes: list[dict]) -> str:
        number = {n["term"]: n["number"] for n in footnotes}
        parts = []
        for ex in category.get("task_examples") or []:
            mark = str(number[ex["close_match"]]).translate(SUPERSCRIPT) if ex.get("close_match") else ""
            parts.append(ex["label"] + mark)
        return ", ".join(parts + ["…"])

    @staticmethod
    def cap(text: str) -> str:
        return text[:1].upper() + text[1:]

    @staticmethod
    def join_and(items: list[str]) -> str:
        return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def render_pages(data: dict, sv: SchemaView) -> dict[Path, str]:
    prefixes = {k: v.prefix_reference for k, v in sv.schema.prefixes.items()}
    env = Environment(loader=FileSystemLoader(TEMPLATES),
                      keep_trailing_newline=True, trim_blocks=True, lstrip_blocks=True)
    out = {}
    for page in PAGES:
        r = Renderer(data, prefixes)
        body = env.get_template(f"{page}.md.j2").render(data=data, r=r)
        header = (f"<!-- GENERATED by scripts/build.py from vocabulary/{page}.yaml (and the other YAML files in vocabulary/) and "
                  f"templates/{page}.md.j2. Do not edit this file; edit those and rebuild. -->\n\n")
        text = header + body
        while "|  |" in text:  # empty table cells: "| |", not "|  |"
            text = text.replace("|  |", "| |")
        if r.edam_used:
            text = text.rstrip("\n") + "\n\n" + r.edam_definitions()
        out[VOCAB / f"{page}.md"] = text
    return out


# --------------------------------------------------------------------------- main

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="fail if generated files are out of date")
    ap.add_argument("--edam-owl", help="EDAM-Bioimaging OWL file or URL to check EDAM ids and labels")
    args = ap.parse_args()

    sv = SchemaView(str(SCHEMA))
    data = load()
    check_schema(data)
    check_references(data, sv)
    if args.edam_owl:
        check_edam(data, args.edam_owl)

    outputs = render_pages(data, sv)
    outputs[TTL] = to_turtle(data, sv)

    stale = [p for p, text in outputs.items() if not p.exists() or p.read_text() != text]
    if args.check:
        if stale:
            fail([f"{p.relative_to(ROOT)} is out of date; run python scripts/build.py" for p in stale])
        print("OK: sources valid, generated files up to date")
        return
    for p in stale:
        p.write_text(outputs[p])
        print(f"wrote {p.relative_to(ROOT)}")
    print("OK")


if __name__ == "__main__":
    main()
