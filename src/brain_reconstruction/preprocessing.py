import numpy as np
from scipy.ndimage import gaussian_filter

try:
    from medpy.filter.smoothing import anisotropic_diffusion
    USE_MEDPY = True
except ImportError:
    USE_MEDPY = False


def preprocess_mri(data, spacing, use_medpy=True):
    """Apply the supplied MRI smoothing strategy and normalize intensities to 0-1."""
    data = np.asarray(data, dtype=np.float32)

    if use_medpy and USE_MEDPY:
        data = anisotropic_diffusion(
            data,
            niter=15,
            kappa=30,
            gamma=0.2,
            voxelspacing=spacing,
        )
    else:
        data = gaussian_filter(data, sigma=0.7)

    minimum = float(np.min(data))
    maximum = float(np.max(data))
    if maximum == minimum:
        return np.zeros_like(data)

    return (data - minimum) / (maximum - minimum)


def brain_mask(data, percentile=55):
    """Create the percentile-based brain mask used by the supplied pipeline."""
    return data > np.percentile(data, percentile)


def tumor_mask(data):
    """Convert a tumor segmentation volume to a binary mask."""
    return gaussian_filter((data > 0).astype(np.float32), sigma=1.0)
