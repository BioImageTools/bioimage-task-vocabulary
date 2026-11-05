# Task classification

A task performs a sequence of operations. An operation is characterized by the types and roles of the objects it reads and writes. Tasks are grouped by functional categories.

## Object types

| Object | Content | Subtypes | nf-bioimage-spec aliases |
|---|---|---|---|
| Image | Pixel intensities, one or more channels. | intensity, probability | `Image` |
| Label | Integers on an image grid. | instance (one ID per object), class map (one value per class), skeleton | `LabelMask`, `ClassMask`, `SkeletonMask` |
| Table | Rows of values under a header. | ROI, masking ROI, feature, condition, parameter | `Tabular`, `Scalar` |
| Point cloud | Points with attributes. | | `Points` |
| Vector | 2D polygons and lines outlining objects. | | `Vector` |
| Mesh | Vertices and faces of an object's surface. | | |
| Graph | Objects as nodes, links as edges. | tree, tracks, tracks with divisions | `SWC`, `Tracks`, `TracksWithDivision` |
| Files | Anything outside OME-Zarr: raw acquisition files, collected metadata, exports. | | |

A subtype is named only where it changes what an operation accepts.

OME-Zarr has no adopted format for point clouds, vectors, meshes or graphs yet: one must be chosen before the first task that writes them.

## Roles

| Role | Meaning | Examples |
|---|---|---|
| *subject* | What the operation acts on. Unmarked. | the image in *enhance*, the label in *split* |
| *mask* | Restricts where the operation works. | a tissue label when cutting superpixels, an organoid label when measuring nuclei |
| *reference* | What the subject is aligned to or compared against. | reference channel in *estimate*, cells in *assign* |
| *parameter* | Values the operation applies. | shifts and flatfield images in *apply* |
| *guide* | Steers the result without being transformed. | the intensity image in watershed, a feature table in *filter* |

A mask is a role, not a type: any Label can play it.

## Operations

Roles in parentheses, optional inputs in brackets.

| Operation | I/O | Example | nf-bioimage-spec |
|---|---|---|---|
| *collect* | Files → Files | acquisition metadata of tiles and channels |  |
| *fix* | Files → Files | correct collected metadata |  |
| *convert* | Files → Image | write OME-Zarr from raw tiles |  |
| *estimate* | Image + Image (reference) → parameter Table | channel shifts | `Stitch` |
| | Image → Image (parameter) | flatfield |  |
| | Point cloud + Point cloud (reference) → parameter Table | point-set registration (ICP) |  |
| *apply* | Image + Table or Image (parameter) → Image | apply shifts, flatfield | `ImgProc` |
| | Point cloud + parameter Table → Point cloud | move spots into the reference frame |  |
| *enhance* | Image → Image | background subtraction, denoising, deconvolution | `ImgProc` |
| *project* | Image → Image | maximum intensity projection |  |
| | Label → Label | 3D label to 2D |  |
| *rearrange* | Image → Image | stitch, move FOVs back to their positions | `Stitch` |
| *crop* | Image [+ ROI Table (parameter)] → Image | crop to ROI |  |
| *rescale* | Image → Image, Label → Label | bin, upscale |  |
| *predict* | Image → probability Image or class map Label | pixel classifier, semantic segmentation | `PixCla` |
| *detect* | Image [+ Label (mask)] → instance Label | thresholding, superpixels, Cellpose | `ObjSeg` |
| | Image [+ Label (mask)] → Point cloud | spot detection | `ObjDet`, `LndDet` |
| *split* | instance Label + Image (guide) → instance Label | watershed |  |
| *filter* | instance Label [+ feature Table (guide)] → instance Label | remove objects by size, shape, position or feature |  |
| *grow / shrink* | instance Label → instance Label | expand, erode, fill holes |  |
| *relabel* | instance Label + Graph (parameter) → instance Label | one ID per track |  |
| *relate* | instance Label + instance Label (reference) → feature Table | nucleus → cell |  |
| *link* | instance Label or Point cloud → Graph | across time, cycles, z planes, FOV borders; with or without divisions | `PrtTrk`, `ObjTrk` |
| *trace* | Image → tree Graph | filament trees | `TreTrc` |
| | Image → skeleton Label | filament networks with loops | `LooTrc` |
| *assign* | Point cloud + instance Label (reference) → feature Table | spots per cell |  |
| *rasterize* | Point cloud or Vector + Image (reference) → instance Label | annotations to labels | `Raster` |
| *vectorize* | instance Label → Vector | object outlines | `Seg2Vec` |
| *mesh* | instance Label → Mesh | marching cubes |  |
| *smooth / simplify* | Mesh → Mesh | |  |
| *measure* | instance Label [+ intensity Image] [+ Label (mask)] → feature Table | intensity, morphology, texture | `FeatExt` |
| | Mesh → feature Table | surface area, curvature |  |
| | Graph → feature Table | speed, displacement, lineage |  |
| *count* | Image → feature Table (per FOV) | objects counted without segmenting | `SptCnt` |
| *cluster* | Point cloud → feature Table, feature Table → feature Table | density, colocalization, phenotypes |  |
| *classify* | feature Table → feature Table | object classifier |  |
| *normalize* | feature Table + condition Table (reference) → feature Table | to controls |  |
| *aggregate* | feature Table → feature Table | objects to wells |  |
| *paint* | instance Label + feature Table (parameter) → class map Label | classes back into a label |  |
| *score* | Image or Label → feature Table | focus, saturation, object counts |  |
| *export* | any → Files | TIFF/PNG, CSV/Parquet, meshes |  |

The last column gives the matching category of nf-bioimage-spec, whose categories 3–11 come from the [NEUBIAS / BIAFLOWS problem classes](https://neubias-wg5.github.io/problem_class_ground_truth.html). `ObjTrk` is *detect* and *link* together.

## Categories

A category is a functional group from the image analyst's point of view: the step of the analysis a task serves.

Categories follow the operation classes of [EDAM-Bioimaging](https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING/?p=classes) (release alpha06, whose operation tree matches the current development version). A category takes the EDAM label and ID when a matching class exists; IDs are relative to `http://edamontology.org/`. Categories with no EDAM class are marked *local*, with the nearest EDAM class in brackets.

| Category | EDAM class | Operations | Task examples |
|---|---|---|---|
| Conversion | `operation_3434` | collect, fix, convert | metadata collection, metadata fixes, conversion from Yokogawa, Opera/Operetta, CZI, ND2, … |
| Image correction | `operation__R7MFwdgojfmkZ07yWbdcda0` | estimate, apply | illumination correction, flatfield estimation, spectral unmixing, drift correction, chromatic aberration correction, … |
| Image enhancement | `operation_Image_enhancement` | enhance | background subtraction, denoising, smoothing, contrast enhancement, deconvolution¹, … |
| Image registration | `operation_Image_registration` | estimate, apply, crop | channel alignment, shift estimation, multiplex cycle registration, point cloud registration, … |
| Image reshaping | *local* (nearest: Image processing, `operation_Image_processing`) | project, rearrange, crop, rescale, link | projection², montage², stitching³, crop to ROI (Image crop), rescale (Geometrical transformation), … |
| Image segmentation | `operation_Image_segmentation` | predict, detect, split, filter, grow / shrink, relate | threshold segmentation, superpixel segmentation, watershed segmentation, object filtering, Cellpose, StarDist, expand labels, nucleus → cell, … |
| Spot detection | `operation_Spot_extraction` | detect | spots, landmarks, … |
| Object tracking | `operation_Image_tracking` | detect, link, relabel, measure | particle tracking, spot tracking, object tracking with divisions, track features, … |
| Filament tracing | `operation__R9Qf06vxvFj2UbAk7pW3IMG` | trace | filament trees, filament networks, … |
| Shape conversion | *local* (nearest: Conversion, `operation_3434`) | vectorize, rasterize, mesh, smooth / simplify | labels to outlines and back, label to mesh, … |
| Object feature extraction | `operation_Feature_extraction` | measure, count, assign | intensity, morphology, texture, colocalization⁴, neighbour distances, surface features, object counts⁴, spots per cell, … |
| Classification | `operation_2990` | classify | object classifier, … |
| Clustering | `operation___Clustering` | cluster | spot clusters, density, phenotype clusters, … |
| Data analysis | *local* (nearest: Analysis, `operation_2945`) | normalize, aggregate, paint, … | normalization to controls, well summaries, hit calling, classes painted back into a label, … |
| Validation | `operation___Validation` | score | focus, saturation, empty FOVs⁵, segmentation statistics, … |
| Export | *local* (nearest: Conversion, `operation_3434`) | export | thumbnails, tables, meshes, … |

Where EDAM files a task example elsewhere:

1. Deconvolution: Image reconstruction (`operation_Image_reconstruction`).
2. Projection and montage: Image projection (`operation_Projection`) and Montage (`operation_Montage`), both under Visualisation.
3. Stitching: Image stitching (`operation_Image_stitching`), under Image reconstruction.
4. Colocalization and object counts: Colocalisation analysis (`operation___Colocalisation_analysis`) and Object counting (`operation_Cell_counting`), siblings of Object feature extraction under Image analysis.
5. Image-level checks such as focus, saturation and empty FOVs: Image validation (`operation___Image_validation`), a child of Validation.

EDAM also places Filament tracing under Image segmentation and Spot detection under Image feature detection; they stay separate categories here because each has its own EDAM class.

An operation can appear in several categories: *estimate* and *apply* in Image correction and Image registration, *detect* in Image segmentation, Spot detection and Object tracking, *link* in Object tracking and in Image reshaping when merging objects across FOVs.

## Compatibility

Task B can follow task A when an output of A matches a required input of B in type, subtype and role: the parameter Table of *estimate* feeds *apply*, the instance Label of *detect* feeds *split*, *filter* and *measure*.

A match is necessary, not sufficient:

- Names must match too: B needs the label A wrote, not any instance label.
- Granularity must match: a per-well feature table cannot feed *filter*.
- Scope must match: *link* needs the whole time series, not one timepoint.

## Scope

How much data a task needs at once is a separate axis: one FOV, a well, a plate, or a whole time series. An image collection input, as in stitching, is scope showing in the I/O.
