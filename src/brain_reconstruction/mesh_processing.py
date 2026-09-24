import numpy as np
import trimesh

try:
    import open3d as o3d
    USE_OPEN3D = True
except ImportError:
    USE_OPEN3D = False

try:
    from pymeshfix import MeshFix
    USE_MESHFIX = True
except ImportError:
    USE_MESHFIX = False


def repair_mesh(mesh):
    if not USE_MESHFIX:
        return mesh

    fixer = MeshFix(mesh.vertices, mesh.faces)
    fixer.repair(verbose=False)
    return trimesh.Trimesh(fixer.v, fixer.f)


def laplacian_smooth(mesh, iterations=5):
    if not USE_OPEN3D:
        return mesh

    o3d_mesh = o3d.geometry.TriangleMesh(
        o3d.utility.Vector3dVector(mesh.vertices),
        o3d.utility.Vector3iVector(mesh.faces),
    )
    o3d_mesh = o3d_mesh.filter_smooth_laplacian(
        number_of_iterations=iterations
    )
    o3d_mesh.compute_vertex_normals()

    return trimesh.Trimesh(
        np.asarray(o3d_mesh.vertices),
        np.asarray(o3d_mesh.triangles),
    )
