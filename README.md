# Brain Tumor 3D Reconstruction

A Python pipeline for reconstructing and visualizing 3D brain anatomy and tumor regions from MRI volumes and tumor segmentation masks.

The project converts volumetric NIfTI data into polygonal 3D meshes using **Marching Cubes**, followed by optional mesh repair and smoothing. The reconstructed brain and tumor surfaces can be exported as an OBJ model and inspected interactively with PyVista.

## Pipeline

```text
T1-weighted MRI (.nii/.nii.gz)
          │
          ▼
Optional anisotropic diffusion
          │
          ▼
Intensity normalization
          │
          ▼
Brain mask / surface extraction
          │
          ▼
Marching Cubes
          │
          ▼
Mesh repair + optional smoothing
          │
          ├──────────────┐
          ▼              ▼
 Brain mesh        Tumor segmentation
                         │
                         ▼
                   Marching Cubes
                         │
                         ▼
                  Tumor mesh repair
                         │
                         └──────┐
                                ▼
                    Brain + Tumor mesh
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
                 OBJ export            PyVista view
```

## What This Repository Contains

- NIfTI MRI loading with NiBabel
- Optional anisotropic diffusion using MedPy
- Gaussian-filter fallback when MedPy is unavailable
- Intensity normalization
- Brain-surface extraction from the MRI volume
- Tumor-surface extraction from a segmentation mask
- Marching Cubes reconstruction using scikit-image
- Mesh repair with PyMeshFix when available
- Optional Laplacian smoothing with Open3D
- Mesh combination and OBJ export with Trimesh
- Interactive visualization with PyVista

## Research Context

This repository contains the implementation for a research project on **3D visualization of brain tumors from multimodal MRI segmentation**, including reconstruction of anatomical and tumor surfaces for subsequent immersive visualization workflows.

The project includes an implemented AR/VR visualization stage. The reconstructed brain and tumor models were integrated into immersive visualization workflows using Unity/ARCore and Adobe Aero, with the final AR workflow supporting interactive scaling, rotation, and placement in real-world space.

The associated manuscript is **not yet published**. Research descriptions and results should therefore be treated as work associated with the project rather than as published claims.

## Requirements

Recommended Python version: **3.10+**

Core dependencies:

- NumPy
- NiBabel
- Trimesh
- PyVista
- scikit-image
- SciPy

Optional processing dependencies:

- MedPy
- Open3D
- PyMeshFix

Install the core dependencies:

```bash
pip install -r requirements.txt
```

For the optional mesh-processing tools:

```bash
pip install medpy open3d pymeshfix
```

## Input Data

The pipeline expects:

1. A T1-weighted MRI NIfTI volume.
2. A corresponding tumor segmentation NIfTI volume.

Example:

```text
data/
├── patient_t1ce.nii
└── patient_tumor_only.nii
```

**Patient MRI/segmentation data is not included in this repository.** Use datasets for which you have appropriate access and follow the dataset's license and usage conditions.

## Usage

Run the reconstruction script:

```bash
python scripts/reconstruct_brain.py \
  --t1ce /path/to/patient_t1ce.nii \
  --tumor /path/to/patient_tumor_only.nii \
  --output outputs
```

The resulting mesh is written to:

```text
outputs/
└── brain_with_tumor.obj
```

The script also opens an interactive PyVista visualization showing the reconstructed brain and tumor surfaces separately.

## Reconstruction Details

### Brain surface

The supplied implementation optionally applies anisotropic diffusion to the T1-weighted volume. If MedPy is unavailable, a Gaussian filter is used as the fallback.

The normalized volume is thresholded using a percentile-based brain mask before Marching Cubes is applied.

### Tumor surface

The tumor NIfTI volume is converted into a binary mask, lightly smoothed with a Gaussian filter, and converted into a polygonal surface using Marching Cubes.

### Mesh processing

The reconstructed surfaces can optionally be repaired using PyMeshFix and smoothed using Open3D's Laplacian smoothing.

These operations are configurable because aggressive smoothing can remove anatomical detail.

## Output

The pipeline produces a combined OBJ mesh containing the reconstructed brain and tumor surfaces.

For interactive inspection, PyVista renders:

- Brain surface with semi-transparent material
- Tumor surface with higher opacity
- 3D grid for spatial reference

## Important Notes

- The supplied code uses voxel spacing from the MRI NIfTI header when generating meshes.
- MRI and segmentation volumes should be spatially aligned before reconstruction.
- The segmentation mask must correspond to the MRI volume being processed.
- Thresholds and smoothing parameters affect the resulting geometry.
- The reconstructed surface is a visualization mesh and should not be interpreted as a clinical diagnostic output.
- Do not commit patient-identifiable medical data to this repository.

## Project Structure

```text
brain-tumor-3d-reconstruction/
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── outputs/
│   └── README.md
├── configs/
│   └── config.yaml
├── scripts/
│   └── reconstruct_brain.py
├── src/
│   └── brain_reconstruction/
│       ├── __init__.py
│       ├── io.py
│       ├── preprocessing.py
│       ├── reconstruction.py
│       ├── mesh_processing.py
│       └── visualization.py
└── docs/
    └── methodology.md
```

## AR/VR Visualization

The research implementation extends the reconstruction pipeline into an AR visualization workflow. Reconstructed brain and tumor meshes are prepared for immersive visualization and were deployed through Unity with ARCore before transitioning to Adobe Aero to address rendering stability, interaction, and cross-platform deployment considerations. The final workflow supports interactive scaling, rotation, and repositioning of the patient-specific 3D brain model in real-world space.

## Roadmap

- Add support for additional MRI modalities
- Add explicit affine/orientation validation
- Add quantitative mesh-quality measurements
- Add reproducible parameter configuration
- Further refine the existing AR/VR visualization workflow
- Add support for standardized research datasets

## Author

**Sarthak Vishal Luhadia**

Computer Vision • 3D Reconstruction • AR/VR • AI/ML
