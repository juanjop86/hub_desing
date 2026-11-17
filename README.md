# Hub — visor 3D

Modelo 3D del Hub, para verlo en el navegador: **https://juanjop86.github.io/hub_desing/**

- Arrastra para girar, rueda o pellizco para zoom, clic derecho para desplazar.
- El panel lateral oculta paredes, fachada, techo y luces.

## Actualizar el modelo

Después de cambiar `hub.blend`, desde la carpeta del proyecto:

```
blender -b hub.blend --python docs/exportar_visor.py
```

Eso regenera `docs/hub.glb` sin modificar el `.blend`. Luego haz commit y push.
