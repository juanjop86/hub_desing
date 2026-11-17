# Exporta hub.blend al visor web (docs/hub.glb) sin modificar el .blend.
# Separa el objeto "Muros" en una pieza por pared para poder ocultarlas en el visor.
# Uso, desde la carpeta del proyecto:
#   blender -b hub.blend --python docs/exportar_visor.py
import os
import bpy
import bmesh

out = os.path.join(os.path.dirname(bpy.data.filepath), "docs", "hub.glb")

# Límites interiores del recinto (m): x 0..5.66, y 0..7.81
def pared(c):
    if c.x < 0.01:
        return "Muro_Izquierdo"
    if c.x > 5.65:
        return "Muro_Derecho"
    if c.y > 7.79:
        return "Muro_Fondo"
    if c.y < 0.01:
        return "Muro_Frontal"
    return "Muro_Otros"

src = bpy.data.objects.get("Muros")
if src:
    bm = bmesh.new()
    bm.from_mesh(src.data)
    grupos = {}
    for f in bm.faces:
        grupos.setdefault(pared(src.matrix_world @ f.calc_center_median()), set()).add(f.index)
    for nombre, caras in grupos.items():
        b = bm.copy()
        b.faces.ensure_lookup_table()
        bmesh.ops.delete(b, geom=[f for f in b.faces if f.index not in caras], context="FACES")
        me = src.data.copy()
        b.to_mesh(me)
        b.free()
        o = bpy.data.objects.new(nombre, me)
        o.matrix_world = src.matrix_world.copy()
        for col in src.users_collection:
            col.objects.link(o)
    bm.free()
    bpy.data.objects.remove(src)

# No se guarda el .blend: los cambios de arriba solo existen durante la exportación.
bpy.ops.export_scene.gltf(filepath=out, export_format="GLB", use_visible=True,
                          export_apply=True, export_yup=True)
print("Visor exportado en", out)
