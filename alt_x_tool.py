bl_info = {
    "name": "Transparent-Tool-Blender",
    "description": "A tool",
    "author": "Jozef,
    "blender": (2, 7, 8),
    "location": "View 3D > Tool Shelf",
    "category": "3D View",
}

import bpy
from bpy.props import *



class Opacity(bpy.types.Operator):
    bl_idname = "object.make_transparent"
    bl_label = "Make Transparent"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):

        #Set property transparent on Object bpy.data.Objects['id'].show_transparent = true
        # set value of material : bpy.data.materials['material index'].alpha
        return {'FINISHED'}


class RegWire(bpy.types.Operator):
    """Selected Wireframe"""
    bl_idname = "object.regester_wire_on_selected"
    bl_label = "Wireframe"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.app.handlers.scene_update_pre.append(wire)

        return {'FINISHED'}

#---------------------

class UnregWire(bpy.types.Operator):
	"""Selected Wireframe"""
	bl_idname = "object.unregester_wire_on_selected"
	bl_label = "Wireframe"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		for list in selected:
			obj = list[0]
			obj.show_wire = list[1]
			obj.show_all_edges = list[2]
		bpy.app.handlers.scene_update_pre.remove(wire)

		return {'FINISHED'}

#---------------------
selected = []

def wire(scene):
	global selected
	
	for list in selected:
		obj = list[0]
		obj.show_wire = list[1]
		obj.show_all_edges = list[2]

	selected = []

	for obj in scene.objects:
		if obj.select:
			selected.append([
				obj,
				obj.show_wire,
				obj.show_all_edges
			])
			
			obj.show_wire = True
			obj.show_all_edges = True

bpy.types.Scene.myTransparency = FloatProperty(
    name="Level", 
    min = 0.0, max = 1.000,
    default = 0.500)
	
class ToolShelfMenu(bpy.types.Panel):
    """enabile and disabile wireframe on the select objects"""
    bl_category = "Tools"
    bl_label = "Selected Transparency"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.prop(context.scene, 'myTransparency');
        split = layout.split()
        col = split.column(align=True)
        col.operator("object.make_transparent");
        

def register():
    bpy.utils.register_class(ToolShelfMenu)

    bpy.utils.register_class(Opacity)

def unregister():
    bpy.utils.unregister_class(ToolShelfMenu)

    bpy.utils.unregister_class(Opacity)


if __name__ == "__main__":
    register()