import bpy

def threedify(image_name, mask_color):
    img = bpy.data.images.get(image_name)

    if not img:
        print(f"No image named {image_name} in memory")
        return

    # Get or create mesh
    mesh = bpy.data.meshes.get(image_name)

    if not mesh:
        mesh = bpy.data.meshes.new(image_name)

    mesh.clear_geometry()

    # Get or create object
    obj = bpy.data.objects.get(image_name)

    if not obj:
        obj = bpy.data.objects.new(image_name, object_data=mesh)
        bpy.context.scene.collection.objects.link(obj)

    # Fill verts, faces and colors
    verts = []
    faces = []
    colors = []

    img_width = img.size[0]
    for i, col in enumerate(zip(*[iter(img.pixels)]*4)):
        if col == mask_color:
            continue
        x, y = i % img_width, i // img_width
        verts.extend(((x - 0.5, y - 0.5, 0), (x + 0.5, y - 0.5, 0), (x + 0.5, y + 0.5, 0), (x - 0.5, y + 0.5, 0)))
        verts_amount = len(verts)
        colors.extend((col,)*4)


        faces.append((verts_amount - 4, verts_amount - 3, verts_amount - 2, verts_amount - 1))

    mesh.from_pydata(verts, (), faces)


    # Add modifiers
    obj.modifiers.clear()
    solid = obj.modifiers.new(type='SOLIDIFY', name="solid")
    solid.thickness = 0.5
    bvl = obj.modifiers.new(type='BEVEL', name="bvl")


    # Set vertex colors
    mode = bpy.context.active_object.mode

    if not obj.data.vertex_colors:
       obj.data.vertex_colors.new(name="vcols")
    vcols = obj.data.vertex_colors.get("vcols")
    if vcols is None:
        vcols = obj.data.vertex_colors.new(name="vcols")
    for i, vcol in enumerate(vcols.data):
        vcol.color = colors[i]

    bpy.ops.object.mode_set(mode=mode)

if __name__ == "__main__":
    threedify("example.png", mask_color=(1, 0, 1, 1))
    
