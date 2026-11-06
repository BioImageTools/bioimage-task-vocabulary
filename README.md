# bioimage-task-vocabulary

A shared vocabulary for describing bioimage analysis tasks, so that tasks from different tools and pipelines can be named, grouped and chained the same way.

The overview is [task_classification.md](task_classification.md), and each table lives in its own file under [vocabulary/](vocabulary/). The vocabulary describes a task as a sequence of **operations**. Each operation is defined by the **types** and **roles** of the objects it reads and writes.

## What it defines

- **[Object types](vocabulary/object_types.md)**: Image, Label, Table, Point cloud, Vector, Mesh, Graph and Files. Subtypes (for example an instance Label or a probability Image) are named only where they change what an operation accepts.
- **[Roles](vocabulary/roles.md)**: *subject*, *mask*, *reference*, *parameter* and *guide*. A role describes what an input does in an operation, separately from its type.
- **[Operations](vocabulary/operations.md)**: about 35 verbs such as *convert*, *estimate*, *apply*, *detect*, *split*, *link*, *measure* and *export*. Each one has its input/output signature and an example, and is mapped to the closest EDAM-Bioimaging operation and the matching nf-bioimage-spec category where they exist.
- **[Categories](vocabulary/categories.md)**: functional groups from the analyst's point of view, aligned with the operation classes of [EDAM-Bioimaging](https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING/?p=classes). Twelve use an EDAM label and ID: Conversion, Image correction, Image enhancement, Image registration, Image segmentation, Spot detection, Object tracking, Filament tracing, Object feature extraction, Classification, Clustering and Validation. Four have no EDAM class and are kept as local categories: Image reshaping, Shape conversion, Data analysis and Export. Each local category names its nearest EDAM class.
- **[Compatibility](task_classification.md#compatibility)**: when task B can follow task A. The output and input must match in type, subtype and role, and also in name, granularity and scope.
- **[Scope](task_classification.md#scope)**: a separate axis for how much data a task needs at once (FOV, well, plate or time series).

## RDF

The vocabulary is modelled in [LinkML](https://linkml.io) and published as RDF in [vocabulary/bioimage_task_vocabulary.ttl](vocabulary/bioimage_task_vocabulary.ttl). Every type, subtype, role, operation and category is a `skos:Concept`. Mappings to EDAM-Bioimaging use `skos:exactMatch` (a category named after an EDAM class), `skos:broadMatch` (the nearest broader EDAM class of a local category) and `skos:closeMatch` (operations and task examples). I/O signatures use `btv:signature`, `btv:input`, `btv:output`, `btv:accepts` and `btv:role`. Object types map to EDAM-Bioimaging, IAO, SIO and NCIt terms with `skos:exactMatch`, `skos:closeMatch`, `skos:narrowMatch` and `skos:relatedMatch`. Their equivalents in SpatialData and the BioImage Archive's MIFA annotation types are linked with `btv:dataModelEquivalent`, because those data models have no IRIs.

The namespace is a local placeholder, `https://example.org/bioimage-task-vocabulary/`. It is declared once, in the schema's `prefixes`.

[queries/next_operations.rq](queries/next_operations.rq) implements the [compatibility rule](task_classification.md#compatibility) in SPARQL. It lists the operations that can follow a given one.

## Maintaining

The YAML files are the source of truth. The Markdown tables and the Turtle file are generated from them, so don't edit those by hand.

| To change | Edit |
|---|---|
| a type, role, operation or category | `vocabulary/<table>.yaml` |
| prose around a table | `templates/<table>.md.j2` |
| an EDAM or other ontology ID or label | `vocabulary/terms.yaml` |
| the model itself (classes, slots, RDF properties) | [schema/bioimage_task_vocabulary.yaml](schema/bioimage_task_vocabulary.yaml) |

Then rebuild:

```sh
python -m venv .venv && .venv/bin/pip install -r requirements.txt   # once
.venv/bin/python scripts/build.py           # validate and regenerate
.venv/bin/python scripts/query.py queries/next_operations.rq
```

`build.py` validates the YAML against the schema and checks that every id is unique and every reference points to an existing id of the right class. It then writes the Markdown and Turtle. With `--edam-owl <file or URL>` it also checks every EDAM ID and label against the ontology. `--check` writes nothing and fails if a generated file is out of date, so it can run in CI.

In the generated Markdown, table rows carry anchors such as `operations.md#detect`, and EDAM IDs link to BioPortal.

## Status

Draft. OME-Zarr has no adopted format yet for point clouds, vectors, meshes or graphs. A format has to be chosen before any task writes them.

## License

See [LICENSE](LICENSE).
