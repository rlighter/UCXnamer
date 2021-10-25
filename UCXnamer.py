bl_info = {
    "name": "UCX namer",
    "author": "rlighter",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Side Panel > Tools",
    "description": "Renames all selected objects to the following: UCX_'selected object'_N for collision export to UE",
    "category": "Object",
}

import bpy

def main(self, context):
    S = bpy.context.active_object
    S0 = S.name
    i = 0
    # changed indexing from 0,1,2 to 00,01,02
    zero = "0"
    for obj in bpy.context.selected_objects:
        if i > 9:
            zero = ""
        obj.name = (("UCX_")+S.name+("_")+zero+str(i))
        if self.parentToActive:
            if obj != S:
                # parent AND KEEP TRANSFORM
                obj.parent= S
                obj.matrix_parent_inverse = S.matrix_world.inverted()

        i+=1
        S.name = str(S0)

class MESH_OT_UCXnamer(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ucxnamer.id"
    bl_label = "UCX object namer"
    bl_options = {'REGISTER', 'UNDO'}

    #Property declaration
    parentToActive: bpy.props.BoolProperty(
        name="parent all UCX to active",
        description="Will parent (with keep transform) every UCX object to active object",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        return context.active_object
    
   
    


    def execute(self, context):
        print(len(context.selected_objects))
         # Checking if its possible to perform operator using more user friendly error message
        if len(context.selected_objects) <= 1:
            self.report({'ERROR'}, "Please select some objects to name")
            return {'CANCELLED'}
        main(self, context)
        return {'FINISHED'}

class VIEW3D_PT_UCXpanel(bpy.types.Panel):
    """Creates a Panel in the tools side panel window"""
    bl_label = "UCX"
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
        props = row.operator('ucxnamer.id', text="Rename to UCX")
        props.parentToActive = False
        row = layout.row()
        props = row.operator('ucxnamer.id', text="Rename to UCX and parent to active")
        props.parentToActive = True



def menu_func_UCX(self, context):
    self.layout.operator(MESH_OT_UCXnamer.bl_idname)

def register():
    bpy.utils.register_class(MESH_OT_UCXnamer)
    bpy.utils.register_class(VIEW3D_PT_UCXpanel)

    # Added this function to object menu on the top (now this function can be accessed in F3 menu)
    bpy.types.VIEW3D_MT_object.append(menu_func_UCX)

def unregister():
    bpy.utils.unregister_class(MESH_OT_UCXnamer)
    bpy.utils.unregister_class(VIEW3D_PT_UCXpanel)

    bpy.types.VIEW3D_MT_object.remove(menu_func_UCX)


if __name__ == "__main__":
    register()
    
    # test call
    # isn't needed :)
    # bpy.ops.ucxnamer.id()


