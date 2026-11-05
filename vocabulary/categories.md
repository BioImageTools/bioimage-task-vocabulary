# Categories

Part of the [task classification](../task_classification.md) · [Object types](object_types.md) · [Roles](roles.md) · [Operations](operations.md) · **Categories**

A category is a functional group from the image analyst's point of view: the step of the analysis a task serves. It groups [operations](operations.md).

Categories follow the operation classes of [EDAM-Bioimaging](https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING/?p=classes) (release alpha06, whose operation tree matches the current development version). A category takes the EDAM label and ID when a matching class exists. Categories with no EDAM class are marked *local*, with the nearest EDAM class in brackets.

| Category | EDAM class | Operations | Task examples |
|---|---|---|---|
| <a id="conversion"></a>Conversion | [`operation_3434`][operation_3434] | [collect](operations.md#collect), [fix](operations.md#fix), [convert](operations.md#convert) | metadata collection, metadata fixes, conversion from Yokogawa, Opera/Operetta, CZI, ND2, … |
| <a id="image-correction"></a>Image correction | [`operation__R7MFwdgojfmkZ07yWbdcda0`][operation__R7MFwdgojfmkZ07yWbdcda0] | [estimate](operations.md#estimate), [apply](operations.md#apply) | illumination correction, flatfield estimation, spectral unmixing, drift correction, chromatic aberration correction, … |
| <a id="image-enhancement"></a>Image enhancement | [`operation_Image_enhancement`][operation_Image_enhancement] | [enhance](operations.md#enhance) | background subtraction, denoising, smoothing, contrast enhancement, deconvolution¹, … |
| <a id="image-registration"></a>Image registration | [`operation_Image_registration`][operation_Image_registration] | [estimate](operations.md#estimate), [apply](operations.md#apply), [crop](operations.md#crop) | channel alignment, shift estimation, multiplex cycle registration, point cloud registration, … |
| <a id="image-reshaping"></a>Image reshaping | *local* (nearest: [Image processing][operation_Image_processing]) | [project](operations.md#project), [rearrange](operations.md#rearrange), [crop](operations.md#crop), [rescale](operations.md#rescale), [link](operations.md#link) | projection², montage², stitching³, crop to ROI ([Image crop][operation__Rhb4iyLUQWY4HnhPpuqNNI]), rescale ([Geometrical transformation][operation_Geometrical_transform]), … |
| <a id="image-segmentation"></a>Image segmentation | [`operation_Image_segmentation`][operation_Image_segmentation] | [predict](operations.md#predict), [detect](operations.md#detect), [split](operations.md#split), [filter](operations.md#filter), [grow / shrink](operations.md#grow-shrink), [relate](operations.md#relate) | threshold segmentation, superpixel segmentation, watershed segmentation, object filtering, Cellpose, StarDist, expand labels, nucleus → cell, … |
| <a id="spot-detection"></a>Spot detection | [`operation_Spot_extraction`][operation_Spot_extraction] | [detect](operations.md#detect) | spots, landmarks, … |
| <a id="object-tracking"></a>Object tracking | [`operation_Image_tracking`][operation_Image_tracking] | [detect](operations.md#detect), [link](operations.md#link), [relabel](operations.md#relabel), [measure](operations.md#measure) | particle tracking, spot tracking, object tracking with divisions, track features, … |
| <a id="filament-tracing"></a>Filament tracing | [`operation__R9Qf06vxvFj2UbAk7pW3IMG`][operation__R9Qf06vxvFj2UbAk7pW3IMG] | [trace](operations.md#trace) | filament trees, filament networks, … |
| <a id="shape-conversion"></a>Shape conversion | *local* (nearest: [Conversion][operation_3434]) | [vectorize](operations.md#vectorize), [rasterize](operations.md#rasterize), [mesh](operations.md#mesh), [smooth / simplify](operations.md#smooth-simplify) | labels to outlines and back, label to mesh, … |
| <a id="object-feature-extraction"></a>Object feature extraction | [`operation_Feature_extraction`][operation_Feature_extraction] | [measure](operations.md#measure), [count](operations.md#count), [assign](operations.md#assign) | intensity, morphology, texture, colocalization⁴, neighbour distances, surface features, object counts⁴, spots per cell, … |
| <a id="classification"></a>Classification | [`operation_2990`][operation_2990] | [classify](operations.md#classify) | object classifier, … |
| <a id="clustering"></a>Clustering | [`operation___Clustering`][operation___Clustering] | [cluster](operations.md#cluster) | spot clusters, density, phenotype clusters, … |
| <a id="data-analysis"></a>Data analysis | *local* (nearest: [Analysis][operation_2945]) | [normalize](operations.md#normalize), [aggregate](operations.md#aggregate), [paint](operations.md#paint), … | normalization to controls, well summaries, hit calling, classes painted back into a label, … |
| <a id="validation"></a>Validation | [`operation___Validation`][operation___Validation] | [score](operations.md#score) | focus, saturation, empty FOVs⁵, segmentation statistics, … |
| <a id="export"></a>Export | *local* (nearest: [Conversion][operation_3434]) | [export](operations.md#export) | thumbnails, tables, meshes, … |

Where EDAM files a task example elsewhere:

1. Deconvolution: [Image reconstruction][operation_Image_reconstruction].
2. Projection and montage: [Image projection][operation_Projection] and [Montage][operation_Montage], both under Visualisation.
3. Stitching: [Image stitching][operation_Image_stitching], under Image reconstruction.
4. Colocalization and object counts: [Colocalisation analysis][operation___Colocalisation_analysis] and [Object counting][operation_Cell_counting], siblings of Object feature extraction under Image analysis.
5. Image-level checks such as focus, saturation and empty FOVs: [Image validation][operation___Image_validation], a child of Validation.

EDAM also places Filament tracing under Image segmentation and Spot detection under Image feature detection; they stay separate categories here because each has its own EDAM class.

An operation can appear in several categories: [*estimate*](operations.md#estimate) and [*apply*](operations.md#apply) in Image correction and Image registration, [*detect*](operations.md#detect) in Image segmentation, Spot detection and Object tracking, [*link*](operations.md#link) in Object tracking and in Image reshaping when merging objects across FOVs.

<!-- EDAM-Bioimaging links. Key = EDAM ID; the URL is the BioPortal page for http://edamontology.org/<ID>. -->
[operation_3434]: https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2Foperation_3434
[operation__R7MFwdgojfmkZ07yWbdcda0]: https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2Foperation__R7MFwdgojfmkZ07yWbdcda0
[operation_Image_enhancement]: https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2Foperation_Image_enhancement
[operation_Image_registration]: https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2Foperation_Image_registration
[operation_Image_processing]: https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2Foperation_Image_processing
[operation__Rhb4iyLUQWY4HnhPpuqNNI]: https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2Foperation__Rhb4iyLUQWY4HnhPpuqNNI
[operation_Geometrical_transform]: https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2Foperation_Geometrical_transform
[operation_Image_segmentation]: https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2Foperation_Image_segmentation
[operation_Spot_extraction]: https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2Foperation_Spot_extraction
[operation_Image_tracking]: https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2Foperation_Image_tracking
[operation__R9Qf06vxvFj2UbAk7pW3IMG]: https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2Foperation__R9Qf06vxvFj2UbAk7pW3IMG
[operation_Feature_extraction]: https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2Foperation_Feature_extraction
[operation_2990]: https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2Foperation_2990
[operation___Clustering]: https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2Foperation___Clustering
[operation_2945]: https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2Foperation_2945
[operation___Validation]: https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2Foperation___Validation
[operation_Image_reconstruction]: https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2Foperation_Image_reconstruction
[operation_Projection]: https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2Foperation_Projection
[operation_Montage]: https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2Foperation_Montage
[operation_Image_stitching]: https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2Foperation_Image_stitching
[operation___Colocalisation_analysis]: https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2Foperation___Colocalisation_analysis
[operation_Cell_counting]: https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2Foperation_Cell_counting
[operation___Image_validation]: https://bioportal.bioontology.org/ontologies/EDAM-BIOIMAGING?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2Foperation___Image_validation
