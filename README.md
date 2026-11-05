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

## Maintaining

EDAM-Bioimaging links are reference-style: a table cell reads `[Label][EDAM ID]`, and the URL for each ID is listed once at the bottom of the file. To add one, use the ID as the key and append `[ID]: https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2FID` with the ID substituted. Table rows carry `<a id="…"></a>` anchors so other files can link to them, e.g. `operations.md#detect`.

## Status

Draft. OME-Zarr has no adopted format yet for point clouds, vectors, meshes or graphs. A format has to be chosen before any task writes them.

## License

See [LICENSE](LICENSE).
