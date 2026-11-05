# Roles

Part of the [task classification](../task_classification.md) · [Object types](object_types.md) · **Roles** · [Operations](operations.md) · [Categories](categories.md)

What an input does in an [operation](operations.md), independent of its [type](object_types.md).

| Role | Meaning | Examples |
|---|---|---|
| <a id="subject"></a>*subject* | What the operation acts on. Unmarked. | the image in [*enhance*](operations.md#enhance), the label in [*split*](operations.md#split) |
| <a id="mask"></a>*mask* | Restricts where the operation works. | a tissue label when cutting superpixels, an organoid label when measuring nuclei |
| <a id="reference"></a>*reference* | What the subject is aligned to or compared against. | reference channel in [*estimate*](operations.md#estimate), cells in [*assign*](operations.md#assign) |
| <a id="parameter"></a>*parameter* | Values the operation applies. | shifts and flatfield images in [*apply*](operations.md#apply) |
| <a id="guide"></a>*guide* | Steers the result without being transformed. | the intensity image in watershed, a feature table in [*filter*](operations.md#filter) |

A mask is a role, not a type: any [Label](object_types.md#label) can play it.
