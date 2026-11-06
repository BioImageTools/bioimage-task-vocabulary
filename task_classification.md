# Task classification

A task performs a sequence of operations. An operation is characterized by the types and roles of the objects it reads and writes. Tasks are grouped by functional categories.

The vocabulary is split into one file per table:

| File | Defines |
|---|---|
| [Object types](vocabulary/object_types.md) | Image, Label, Table, Point cloud, Vector, Mesh, Graph, Files, and their subtypes |
| [Roles](vocabulary/roles.md) | *subject*, *mask*, *reference*, *parameter*, *guide* |
| [Operations](vocabulary/operations.md) | each operation's I/O signature, with its EDAM-Bioimaging and nf-bioimage-spec equivalents |
| [Categories](vocabulary/categories.md) | functional groups of operations, aligned with EDAM-Bioimaging |

These pages are generated from YAML sources in [vocabulary/](vocabulary/), which also produce an RDF version, [bioimage_task_vocabulary.ttl](vocabulary/bioimage_task_vocabulary.ttl). See the [README](README.md#maintaining).

## Compatibility

Task B can follow task A when an output of A matches a required input of B in [type](vocabulary/object_types.md), subtype and [role](vocabulary/roles.md): the parameter Table of [*estimate*](vocabulary/operations.md#estimate) feeds [*apply*](vocabulary/operations.md#apply), the instance Label of [*detect*](vocabulary/operations.md#detect) feeds [*split*](vocabulary/operations.md#split), [*filter*](vocabulary/operations.md#filter) and [*measure*](vocabulary/operations.md#measure).

A match is necessary, not sufficient:

- Names must match too: B needs the label A wrote, not any instance label.
- Granularity must match: a per-well feature table cannot feed *filter*.
- Scope must match: [*link*](vocabulary/operations.md#link) needs the whole time series, not one timepoint.

## Scope

How much data a task needs at once is a separate axis: one FOV, a well, a plate, or a whole time series. An image collection input, as in stitching, is scope showing in the I/O.
