import bpy
from bpy.types import NodeTree
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem, NodeItemCustom

from .matte import luxcore_material_matte
from .output import luxcore_material_output
from .glossy2 import luxcore_material_glossy2



class LuxCoreMaterialEditor(NodeTree):
    bl_idname = "luxcore_material_nodes"
    bl_label = "LuxCore Material Nodes"
    bl_icon = "MATERIAL"

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == "LUXCORE"

    @classmethod
    def get_from_context(cls, context):
        obj = context.active_object

        if obj and obj.type not in {"LAMP", "CAMERA"}:
            mat = obj.active_material

            if mat:
                # ID pointer
                node_tree = mat.luxcore.node_tree

                if node_tree:
                    return node_tree, mat, mat

        return None, None, None

    # This block updates the preview, when socket links change
    def update(self):
        self.refresh = True

    def acknowledge_connection(self, context):
        while self.refresh:
            self.refresh = False
            break

    refresh = bpy.props.BoolProperty(name='Links Changed',
                                     default=False,
                                     update=acknowledge_connection)


class luxcore_node_category_material(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "luxcore_material_nodes"

luxcore_node_categories_material = [
    luxcore_node_category_material("LUX_MATERIAL", "Material", items=[
        NodeItem("luxcore_material_output", label="Output"),
        NodeItem("luxcore_material_matte", label="Matte"),
        NodeItem("luxcore_material_glossy2", label="Glossy"),
    ]),
]

def register():
    nodeitems_utils.register_node_categories("LUXCORE_MATERIAL", luxcore_node_categories_material)


def unregister():
    nodeitems_utils.unregister_node_categories("LUXCORE_MATERIAL")