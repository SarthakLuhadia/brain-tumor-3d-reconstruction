import numpy as np
import pyvista as pv


def trimesh_to_pyvista(mesh):
    faces = np.hstack([
        np.full((len(mesh.faces), 1), 3, dtype=np.int64),
        mesh.faces,
    ])
    return pv.PolyData(mesh.vertices, faces)


def show_brain_and_tumor(brain_mesh, tumor_mesh):
    plotter = pv.Plotter()
    plotter.add_mesh(
        trimesh_to_pyvista(brain_mesh),
        color="wheat",
        opacity=0.55,
        show_edges=False,
        name="Brain",
    )
    plotter.add_mesh(
        trimesh_to_pyvista(tumor_mesh),
        color="crimson",
        opacity=0.85,
        show_edges=False,
        name="Tumor",
    )
    plotter.show_grid()
    plotter.show()
