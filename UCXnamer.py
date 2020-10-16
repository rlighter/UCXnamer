bl_info = {
    "name": "UCX namer",
    "author": "rlighter",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "description": "Renames all selected objects to the following: UCX_'selected object'_N for collision export to UE",
    "category": "Object",
}

import bpy

def main(context):
    S = bpy.context.active_object
    S0 = S.name
    i = 0
    for obj in bpy.context.selected_objects:
        obj.name = (("UCX_")+S.name+("_")+str(i))
        if obj != S:
            obj.parent = S
        i+=1
        S.name = str(S0)

class UCXnamer(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ucxnamer.id"
    bl_label = "UCX object namer"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}

class UCXpanelGen(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "UCX"
    bl_idname = "PT_UCXnames"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="UCX object namer", icon='SNAP_VERTEX')

        row = layout.row()

        row = layout.row()
        row.operator("ucxnamer.id", text="Rename to UCX")

def register():
    bpy.utils.register_class(UCXnamer)
    bpy.utils.register_class(UCXpanelGen)


def unregister():
    bpy.utils.unregister_class(UCXnamer)
    bpy.utils.register_class(UCXpanelGen)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.ucxnamer.id()


