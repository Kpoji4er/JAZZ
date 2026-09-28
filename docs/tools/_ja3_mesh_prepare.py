# -*- coding: utf-8 -*-
"""JA3 mesh prepare/audit: never keep custom or split normals.

Successful FBX / AssetsProcessor output is not a PASS. A bad weld can explode
into a screen-sized polygon once the mesh is animated (Doctor_Leevsy / Kpoji4er).
Always recalculate normals. Do not author, keep, or write custom split normals.
"""
from __future__ import annotations

import math
from typing import Iterable, Mapping, MutableMapping, Sequence

AREA_EPS_REL = 1e-12
ZERO_NORMAL = 1e-10
SPIKE_EDGE_RATIO = 40.0
# Triangle longer than the mesh itself: leftover weld to a stray vertex.
SPIKE_BBOX_FRAC = 0.9
FINITE_LIMIT = 1e20

Issue = MutableMapping[str, object]


def _sub(a: Sequence[float], b: Sequence[float]) -> tuple[float, float, float]:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _cross(a: Sequence[float], b: Sequence[float]) -> tuple[float, float, float]:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _length(v: Sequence[float]) -> float:
    return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])


def _finite(v: Sequence[float]) -> bool:
    return all(math.isfinite(c) and abs(c) < FINITE_LIMIT for c in v)


def audit_triangles(
    vertices: Sequence[Sequence[float]],
    faces: Sequence[Sequence[int]],
    *,
    name: str = "mesh",
) -> list[Issue]:
    """Flag empty meshes, n-gons, NaNs, zero-area tris, zero normals, weld spikes."""
    issues: list[Issue] = []
    if not vertices or not faces:
        issues.append({"kind": "empty", "detail": f"{name}: no geometry", "triangle": None})
        return issues

    xs = [v[0] for v in vertices if _finite(v)]
    ys = [v[1] for v in vertices if _finite(v)]
    zs = [v[2] for v in vertices if _finite(v)]
    if not xs:
        issues.append({"kind": "nan", "detail": f"{name}: no finite vertices", "triangle": None})
        return issues
    diag = math.sqrt(
        (max(xs) - min(xs)) ** 2 + (max(ys) - min(ys)) ** 2 + (max(zs) - min(zs)) ** 2
    )
    area_eps = AREA_EPS_REL * max(diag * diag, 1e-8)

    for index, face in enumerate(faces):
        if len(face) < 3:
            issues.append(
                {"kind": "degenerate", "detail": f"{name}: face {index} has {len(face)} verts", "triangle": index}
            )
            continue
        if len(face) > 3:
            issues.append(
                {"kind": "ngon", "detail": f"{name}: face {index} is an n-gon ({len(face)})", "triangle": index}
            )
            continue
        try:
            a, b, c = vertices[face[0]], vertices[face[1]], vertices[face[2]]
        except IndexError:
            issues.append(
                {"kind": "degenerate", "detail": f"{name}: face {index} index out of range", "triangle": index}
            )
            continue
        if not (_finite(a) and _finite(b) and _finite(c)):
            issues.append({"kind": "nan", "detail": f"{name}: face {index} has non-finite verts", "triangle": index})
            continue
        e1, e2, e3 = _length(_sub(b, a)), _length(_sub(c, b)), _length(_sub(a, c))
        normal = _cross(_sub(b, a), _sub(c, a))
        area = 0.5 * _length(normal)
        if area < area_eps or min(e1, e2, e3) < ZERO_NORMAL:
            issues.append(
                {
                    "kind": "degenerate",
                    "detail": f"{name}: face {index} area={area:.3e} edges=({e1:.3e},{e2:.3e},{e3:.3e})",
                    "triangle": index,
                }
            )
        elif _length(normal) < ZERO_NORMAL:
            issues.append({"kind": "zero_normal", "detail": f"{name}: face {index} zero-length normal", "triangle": index})
        longest = max(e1, e2, e3)
        shortest = min(e1, e2, e3)
        if (
            shortest > 0
            and longest / shortest >= SPIKE_EDGE_RATIO
            and longest >= SPIKE_BBOX_FRAC * max(diag, 1e-8)
        ):
            issues.append(
                {
                    "kind": "spike",
                    "detail": f"{name}: face {index} weld-spike {longest:.4f} / {shortest:.4f}",
                    "triangle": index,
                }
            )
    return issues


def parse_obj(text: str) -> tuple[list[tuple[float, float, float]], list[tuple[int, int, int]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, int, int]] = []
    for raw in text.splitlines():
        if raw.startswith("v "):
            parts = raw.split()
            vertices.append((float(parts[1]), float(parts[2]), float(parts[3])))
        elif raw.startswith("f "):
            idxs = [int(tok.split("/")[0]) - 1 for tok in raw.split()[1:]]
            if len(idxs) == 3:
                faces.append((idxs[0], idxs[1], idxs[2]))
            else:
                for i in range(1, len(idxs) - 1):
                    faces.append((idxs[0], idxs[i], idxs[i + 1]))
    return vertices, faces


def audit_hgm_json(data: Mapping[str, object], *, name: str = "hgm") -> list[Issue]:
    issues: list[Issue] = []
    meshes = data.get("meshes")
    if not isinstance(meshes, list) or not meshes:
        return [{"kind": "empty", "detail": f"{name}: no meshes[]", "triangle": None}]
    for i, mesh in enumerate(meshes):
        if not isinstance(mesh, Mapping):
            continue
        verts = mesh.get("vertices") or []
        faces = mesh.get("faces") or []
        issues.extend(audit_triangles(verts, faces, name=f"{name}[{i}]"))
    return issues


def mesh_has_custom_normals(mesh) -> bool:
    if getattr(mesh, "has_custom_normals", False):
        return True
    attrs = getattr(mesh, "attributes", None)
    if attrs is not None and "custom_normal" in attrs:
        return True
    return False


def _ensure_object_mode(obj) -> None:
    import bpy

    if bpy.context.view_layer.objects.active != obj:
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
    if obj.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")


def clear_custom_normals(obj) -> None:
    import bpy

    _ensure_object_mode(obj)
    mesh = obj.data
    try:
        bpy.ops.mesh.customdata_custom_splitnormals_clear()
    except Exception:
        pass
    if hasattr(mesh, "free_normals_split"):
        try:
            mesh.free_normals_split()
        except Exception:
            pass
    attrs = getattr(mesh, "attributes", None)
    if attrs is not None and "custom_normal" in attrs:
        try:
            attrs.remove(attrs["custom_normal"])
        except Exception:
            pass


def recalc_normals(obj) -> None:
    import bpy

    _ensure_object_mode(obj)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    try:
        bpy.ops.mesh.customdata_custom_splitnormals_clear()
    except Exception:
        pass
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode="OBJECT")
    clear_custom_normals(obj)
    # shade_auto_smooth / shade_smooth_by_angle write custom split normals in
    # Blender 4.1+. JA3 export must not create that layer.
    bpy.ops.object.shade_smooth()


def triangulate_without_custom_normals(obj) -> None:
    import bpy

    _ensure_object_mode(obj)
    clear_custom_normals(obj)
    tri = obj.modifiers.new("JA3_Triangulate", "TRIANGULATE")
    if hasattr(tri, "keep_custom_normals"):
        tri.keep_custom_normals = False
    bpy.ops.object.modifier_apply(modifier=tri.name)


def audit_blender_object(obj) -> list[Issue]:
    mesh = obj.data
    mesh.calc_loop_triangles()
    vertices = [tuple(v.co) for v in mesh.vertices]
    faces = [tuple(tri.vertices) for tri in mesh.loop_triangles]
    issues = audit_triangles(vertices, faces, name=obj.name)
    if mesh_has_custom_normals(mesh):
        issues.append(
            {
                "kind": "custom_normals",
                "detail": f"{obj.name}: custom/split normals still present",
                "triangle": None,
            }
        )
    return issues


def prepare_export_mesh(obj, *, strict: bool = True) -> list[Issue]:
    """Triangulate without custom normals, recalc, then fail on weld/normal defects."""
    triangulate_without_custom_normals(obj)
    recalc_normals(obj)
    issues = audit_blender_object(obj)
    fatal = {"degenerate", "zero_normal", "spike", "nan", "custom_normals", "empty"}
    bad = [issue for issue in issues if issue["kind"] in fatal]
    if strict and bad:
        summary = "; ".join(str(issue["detail"]) for issue in bad[:8])
        raise RuntimeError(f"JA3 mesh rejected (recalc-only, no custom normals): {summary}")
    return issues


def load_tools_path(path_like: Iterable[str] | None = None) -> None:
    """Insert docs/tools onto sys.path so Blender scripts can import this module."""
    import sys
    from pathlib import Path

    extra = list(path_like or ())
    extra.append(str(Path(__file__).resolve().parent))
    for item in extra:
        if item not in sys.path:
            sys.path.insert(0, item)
