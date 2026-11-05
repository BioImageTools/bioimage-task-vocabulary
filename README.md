# bioimage-task-vocabulary

A shared vocabulary for describing bioimage analysis tasks, so that tasks from different tools and pipelines can be named, grouped and chained the same way.

The vocabulary is defined in [task_classification.md](task_classification.md). It describes a task as a sequence of **operations**. Each operation is defined by the **types** and **roles** of the objects it reads and writes.

## What it defines

- **Object types**: Image, Label, Table, Point cloud, Vector, Mesh, Graph and Files. Subtypes (for example an instance Label or a probability Image) are named only where they change what an operation accepts.
- **Roles**: *subject*, *mask*, *reference*, *parameter* and *guide*. A role describes what an input does in an operation, separately from its type.
- **Operations**: about 35 verbs such as *convert*, *estimate*, *apply*, *detect*, *split*, *link*, *measure* and *export*. Each one has its input/output signature and an example, and is mapped to the matching nf-bioimage-spec category where one exists.
- **Categories**: functional groups from the analyst's point of view, aligned with the operation classes of [EDAM-Bioimaging](https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING/?p=classes). Twelve use an EDAM label and ID: Conversion, Image correction, Image enhancement, Image registration, Image segmentation, Spot detection, Object tracking, Filament tracing, Object feature extraction, Classification, Clustering and Validation. Four have no EDAM class and are kept as local categories: Image reshaping, Shape conversion, Data analysis and Export. Each local category names its nearest EDAM class.
- **Compatibility**: when task B can follow task A. The output and input must match in type, subtype and role, and also in name, granularity and scope.
- **Scope**: a separate axis for how much data a task needs at once (FOV, well, plate or time series).

## Status

Draft. OME-Zarr has no adopted format yet for point clouds, vectors, meshes or graphs. A format has to be chosen before any task writes them.

## License

See [LICENSE](LICENSE).
