import argparse
import os
from pathlib import Path

from src.brain_reconstruction.io import load_nifti
from src.brain_reconstruction.preprocessing import preprocess_mri, brain_mask, tumor_mask
from src.brain_reconstruction.reconstruction import reconstruct_brain, reconstruct_tumor
from src.brain_reconstruction.mesh_processing import repair_mesh, laplacian_smooth
from src.brain_reconstruction.visualization import show_brain_and_tumor


def main():
    parser = argparse.ArgumentParser(
        description="Reconstruct 3D brain and tumor surfaces from NIfTI volumes."
    )
    parser.add_argument("--t1ce", required=True, help="Path to T1-weighted NIfTI volume.")
    parser.add_argument("--tumor", required=True, help="Path to tumor segmentation NIfTI volume.")
    parser.add_argument("--output", default="outputs", help="Output directory.")
    parser.add_argument("--no-medpy", action="store_true", help="Force Gaussian MRI smoothing.")
    parser.add_argument("--no-mesh-repair", action="store_true")
    parser.add_argument("--no-open3d", action="store_true")
    parser.add_argument("--no-show", action="store_true", help="Skip PyVista visualization.")

    args = parser.parse_args()
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    t1ce_img, t1ce_data, spacing = load_nifti(args.t1ce)
    _, tumor_data, tumor_spacing = load_nifti(args.tumor)

    if len(spacing) != len(tumor_spacing) or any(abs(a - b) > 1e-5 for a, b in zip(spacing, tumor_spacing)):
        raise ValueError("MRI and tumor segmentation voxel spacing do not match.")

    t1ce_data = preprocess_mri(t1ce_data, spacing, use_medpy=not args.no_medpy)

    brain = reconstruct_brain(
        brain_mask(t1ce_data, percentile=55),
        spacing,
        level=0.25,
    )

    tumor = reconstruct_tumor(
        tumor_mask(tumor_data),
        spacing,
        level=0.30,
    )

    if not args.no_mesh_repair:
        brain = repair_mesh(brain)
        tumor = repair_mesh(tumor)

    if not args.no_open3d:
        brain = laplacian_smooth(brain, iterations=5)

    combined = brain + tumor
    combined.export(output_dir / "brain_with_tumor.obj")

    print(f"Saved combined mesh to: {output_dir / 'brain_with_tumor.obj'}")

    if not args.no_show:
        show_brain_and_tumor(brain, tumor)


if __name__ == "__main__":
    main()
