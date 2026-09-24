import numpy as np
import trimesh
from skimage import measure


def marching_cubes_mesh(volume, level, spacing):
    """Convert a volumetric mask into a Trimesh surface using Marching Cubes."""
    vertices, faces, _, _ = measure.marching_cubes(
        volume,
        level=level,
        spacing=spacing,
    )
    return trimesh.Trimesh(vertices=vertices, faces=faces)


def reconstruct_brain(mask, spacing, level=0.25):
    return marching_cubes_mesh(mask.astype(np.float32), level, spacing)


def reconstruct_tumor(mask, spacing, level=0.30):
    return marching_cubes_mesh(mask, level, spacing)
