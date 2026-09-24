# Methodology

## 1. MRI preprocessing

The supplied implementation loads the T1-weighted MRI using NiBabel and obtains voxel spacing from the NIfTI header.

Anisotropic diffusion is used when MedPy is available. Otherwise, the implementation falls back to Gaussian smoothing.

The processed MRI is normalized to the 0-1 range.

## 2. Brain surface extraction

A percentile threshold of 55 is used to generate a binary brain mask.

The mask is converted to a polygonal surface using scikit-image's Marching Cubes implementation at level 0.25 while preserving the source voxel spacing.

## 3. Tumor surface extraction

The tumor segmentation is converted to a binary mask by testing voxels greater than zero.

A Gaussian filter with sigma 1 is applied before Marching Cubes reconstruction at level 0.30.

## 4. Mesh processing

PyMeshFix can be used to repair the generated meshes.

Open3D can optionally apply five iterations of Laplacian smoothing to the brain surface.

The final brain and tumor meshes are combined and exported as an OBJ file.

## 5. Visualization

PyVista renders the brain and tumor surfaces as separate meshes, allowing interactive inspection of the reconstructed geometry.

## Reproducibility

The reconstruction depends on the input volumes, NIfTI voxel spacing, threshold values, and optional smoothing/repair libraries. Therefore, the exact geometry should be considered input- and parameter-dependent.
