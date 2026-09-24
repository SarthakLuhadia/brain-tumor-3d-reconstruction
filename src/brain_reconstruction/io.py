from pathlib import Path
import nibabel as nib


def load_nifti(path: str | Path):
    """Load a NIfTI volume and return image, floating-point data, and voxel spacing."""
    image = nib.load(str(path))
    data = image.get_fdata()
    spacing = image.header.get_zooms()[:3]
    return image, data, spacing
