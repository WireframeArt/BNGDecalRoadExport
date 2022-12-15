import bpy
from bpy.props import (
    IntProperty, 
    BoolProperty, 
    StringProperty, 
    FloatProperty
    )

# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator

class ExportDecalRoad(Operator, ExportHelper):
    """Exports a .json file containing the selected decal road"""
    bl_idname = "decal_road_export.export_road"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export Decal Road"
    bl_options = {'PRESET'}

    # ExportHelper mixin class uses this
    filename_ext = ".json"

    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    road_detail: FloatProperty(
    name="Detail",
    description="Decal Road Detail",
    default=0.1,
    )

    road_radius: FloatProperty(
        name="Road Radius",
        description="Decal Road Radius",
        default=10,
    )

    road_smoothness: FloatProperty(
        name="Smoothness",
        description="Decal Road smoothness",
        default=0.5,
    )

    road_drivability: FloatProperty(
        name="Drivability",
        description="Decal Road Drivability",
        default=-1,
    )

    texture_length: FloatProperty(
        name="Texture Length",
        description="Decal Road texture length",
        default=10,
    )

    end_overlap: BoolProperty(
        name="Overlap Ends",
        description="When splitting is enabled this will add an extra node to each decal road that overlaps the previous, this helps with blending as well as avoiding any gaps where the decal road splits",
        default=False,
    )

    start_fade: FloatProperty(
        name="Start Fade",
        description="size of fade at the start of the decal road",
        default=0,
    )

    end_fade: FloatProperty(
        name="End Fade",
        description="size of fade at the end of the decal road",
        default=0,
    )   

    improved_spline: BoolProperty(
        name="Improved Spline",
        description="Use Improved Spline on decal road",
        default=True,
    )
    
    over_object: BoolProperty(
        name="Over Object",
        description="Snap decal road to objects",
        default=False,
    )

    flip_road: BoolProperty(
        name="Flip Road",
        description="Reverses the direction of the road",
        default=False,
    )

    road_material: StringProperty(
        name="Material",
        description="Material to use on the decal road",
        default="",
    )

    parent_name: StringProperty(
        name="Parent Name",
        description="The folder in the level editor that the decal road will be placed in",
        default="",
    )

    split_road: BoolProperty(
        name="Split Road",
        description="Automatically splits decal road into smaller segments to avoid rendering errors",
        default=False,
    )

    split_iter: IntProperty(
        name="Nodes per road segment",
        description="When road splitting is enabled this is the number of nodes a segment will be allowed to have before it splits into a new decal road",
        default=21,
    )

    lanes_left: IntProperty(
        name="Lanes Left",
        description="amount of lanes on the left side",
        default=1,
    )
    lanes_right: IntProperty(
        name="Lanes Right",
        description="amount of lanes on the right side",
        default=1,
    )
    one_way: BoolProperty(
        name="One Way",
        description="road is only one way",
        default=False,
    )
    flip_ai_direction: BoolProperty(
        name="Flip Ai Direction",
        description="road direction is inverted",
        default=False,
    )
    gated_road: BoolProperty(
        name="Gated Road",
        description="road is open to the public",
        default=False,       
    )
    use_subdivison: BoolProperty(
        name="Use Subdivison",
        description="generate high detail ai road",
        default=True,       
    )
    start_tangent: BoolProperty(
        name="Start Tangent",
        description="use the first point as tangent marker",
        default=False,       
    )
    end_tangent: BoolProperty(
        name="End Tangent",
        description="use the last point as tangent marker",
        default=False,       
    )
    looped: BoolProperty(
        name="Looped",
        description="loop the road?",
        default=False,       
    )   
    distance_fade_start: FloatProperty(
        name="Distance Fade Start",
        description="distance at which the decalroad will fade, and size of the fade. First value should be bigger than the second value",
        default=0,       
    )  
    distance_fade_size: FloatProperty(
        name="Distance Fade Size",
        description="distance at which the decalroad will fade, and size of the fade. First value should be bigger than the second value",
        default=0,       
    ) 
    break_angle: FloatProperty(
        name="Break Angle",
        description="Angle in degrees - decal road will subdivide the spline if its curve is greater than the threshold",
        default=3,       
    ) 
    render_priority: IntProperty(
        name="Render Priority",
        description="Decal roads are rendered in descending render priority order",
        default=10,       
    ) 
    z_bias: FloatProperty(
        name="Z Bias",
        description="render order, -1 to top most, 1 for bottom most",
        default=0,       
    ) 
    decal_bias: FloatProperty(
        name="Decal Bias",
        description="the hovering height of the decal over the terrain",
        default=0.001,       
    ) 
    hidden_in_navi: BoolProperty(
        name="Hidden In Navi",
        description="whether this road is hidden in the navigation app",
        default=False,       
    ) 


    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.use_property_split=True
        box.label(text="Export Options")
        box.prop(self, 'road_radius')
        box.prop(self, 'end_overlap')
        box.prop(self, 'flip_road')
        box.prop(self, 'parent_name')
        box.prop(self, 'split_road')
        box.prop(self, 'split_iter')

        box=layout.box()
        box.use_property_split=True
        box.label(text="Pathfinding Options")
        box.prop(self, 'road_drivability')
        box.prop(self, 'lanes_left')
        box.prop(self, 'lanes_right')
        box.prop(self, 'one_way')
        box.prop(self, 'flip_ai_direction')
        box.prop(self, 'gated_road')
        box.prop(self, 'use_subdivison')

        box=layout.box()
        box.use_property_split=True
        box.label(text="Improved Spline Options")
        box.prop(self, 'improved_spline')
        box.prop(self, 'start_tangent')
        box.prop(self, 'end_tangent')
        box.prop(self, 'looped')
        box.prop(self, 'road_smoothness')
        box.prop(self, 'road_detail')

        box=layout.box()
        box.use_property_split=True
        box.label(text="Decal Road Options")
        box.prop(self, 'over_object')
        box.prop(self, 'road_material')
        box.prop(self, 'texture_length')
        box.prop(self, 'break_angle')
        box.prop(self, 'render_priority')
        box.prop(self, 'z_bias')
        box.prop(self, 'decal_bias')
        row = box.row()
        row.prop(self, 'distance_fade_start', text="DistanceFade")
        row.prop(self, 'distance_fade_size', text="")

        row = box.row()
        row.prop(self, 'start_fade', text="StartEndFade")
        row.prop(self, 'end_fade', text="")
        box.prop(self, 'hidden_in_navi')

    def execute(self, context):
        self.exportdecalroad(
            detail=self.road_detail, 
            smoothness=self.road_smoothness, 
            drivability=self.road_drivability, 
            t_length=self.texture_length, 
            s_fade=self.start_fade, 
            e_fade=self.end_fade, 
            i_spline=self.improved_spline, 
            o_object=self.over_object, 
            flip=self.flip_road, 
            material=self.road_material, 
            p_name=self.parent_name, 
            s_road=self.split_road, 
            s_iter=self.split_iter, 
            radius=self.road_radius,
            e_overlap=self.end_overlap,
            lanes_left=self.lanes_left,
            lanes_right=self.lanes_right,
            one_way=self.one_way,
            flip_ai_direction=self.flip_ai_direction,
            gated_road=self.gated_road,
            use_subdivison=self.use_subdivison,
            start_tangent=self.start_tangent,
            end_tangent=self.end_tangent,
            distance_fade_start=self.distance_fade_start,
            distance_fade_size=self.distance_fade_size,
            break_angle=self.break_angle,
            render_priority=self.render_priority,
            z_bias=self.z_bias,
            decal_bias=self.decal_bias,
            hidden_in_navi=self.hidden_in_navi,
            looped=self.looped,
            filepath=self.filepath
        )
        self.report({'INFO'}, "Decal road exported")
        return {'FINISHED'}
    def exportdecalroad(context, detail, smoothness, drivability, t_length, s_fade, e_fade, i_spline, o_object, flip, material, p_name, s_road, s_iter, radius, e_overlap, filepath,lanes_left,lanes_right,one_way,flip_ai_direction,gated_road,use_subdivison,start_tangent,end_tangent,distance_fade_start,distance_fade_size,break_angle,render_priority,z_bias,decal_bias,hidden_in_navi,looped):

        dg = bpy.context.evaluated_depsgraph_get()
        obj = bpy.context.object.evaluated_get(dg)
        if obj == None:

            raise Exception("ERROR - No decal road was selected, export canceled")
        
        active_obj = obj.to_mesh(preserve_all_data_layers=True, depsgraph=dg)
        i = 0
        vertslen = len(active_obj.vertices)
        items = ""

        ispline = "false"
        if i_spline:
            ispline = "true"

        oobject = "false"
        if o_object:
            oobject = "true"

        s_fade_int = 0
        if s_fade:
            s_fade_int = 1
        
        e_fade_int = 0
        if e_fade:
            e_fade_int = 1

        if not s_road:
            s_iter = vertslen
            e_overlap = False

        while i < vertslen:

            splititer = 0
            firstvert = True

            #First chunk of text for the decal road, parent is the folder the decal road is placed in, in the editor.

            items += "{"
            items += f'"class":"DecalRoad","persistentId":"","__parent":"{p_name}","position":['
            #adds positon value to decal road

            startadded = False
            cur_index = i
            if flip:
                cur_index= (vertslen - 1) - i

            split_index= i - 1
            if flip:
                split_index= (vertslen - 1) - i + 1

            overlap_index= i - 2
            if flip:
                overlap_index= (vertslen - 1) - i + 2

            if e_overlap:
                try:
                    v= active_obj.vertices[overlap_index]
                    co = obj.matrix_world @ v.co
                    items += f'{round(co.x, 5)},{round(co.y, 5)},{round(co.z, 5)}'
                    startadded = True 
                    print(f'Decal road start pos set to overlap')  
                except:
                    pass

            if startadded == False:
                try:
                    v= active_obj.vertices[split_index]
                    co= obj.matrix_world @ v.co
                    items += f'[{round(co.x, 5)},{round(co.y, 5)},{round(co.z, 5)}]'
                    startadded = True
                    print(f'Decal road start pos set to split')  
                except:
                    pass

            if startadded == False:
                v = active_obj.vertices[cur_index]
                co = obj.matrix_world @ v.co
                items += f"{round(co.x, 5)},{round(co.y, 5)},{round(co.z, 5)}"
                startadded = True
                print(f'Decal road start pos set to default')      
            items += "],"
            items +=f'"breakAngle":{break_angle},"decalBias":{decal_bias},"detail":{detail},"distanceFade":[{round(distance_fade_start, 2)},{round(distance_fade_size, 2)}],"drivability":{drivability},'

            if end_tangent:
                items+=f'"endTangent":true,'
            if flip_ai_direction:
                items+=f'"flipDirection":true,'
            if gated_road:
                items+=f'"gatedRoad":true,'
            if hidden_in_navi:
                items+=f'"hiddenInNavi":true,'
            if i_spline:
                items+=f'"improvedSpline":true,'

            items +=f'"lanesLeft":{lanes_left},"lanesRight":{lanes_right},'
            if looped:
                items+=f'"looped":true,'

            items +=f'"material":"{material}","nodes":['

            #If we enabled overlap and there is a vertex at 2 indices back in the verts list we'll add that as the first position node

            if e_overlap:
                try:
                    v= active_obj.vertices[overlap_index]
                    co = obj.matrix_world @ v.co
                    items += f'[{round(co.x, 5)},{round(co.y, 5)},{round(co.z, 5)},{round(radius, 2)}]'
                    splititer += 1
                    firstvert = False
                    print(f'overlap node added to decal road')  
                except:
                    pass

            #Trys to get previous node if there is one, this won't work on the first loop but should work on every loop after

            try:
                if firstvert == False:
                    items +=","

                v= active_obj.vertices[split_index]
                co= obj.matrix_world @ v.co
                items += f'[{round(co.x, 5)},{round(co.y, 5)},{round(co.z, 5)},{round(radius, 2)}]'
                splititer += 1
                firstvert = False
                print(f'split node added to decal road')  
            except:
                pass

            while splititer < s_iter and i < vertslen:
                v = None
                if flip:
                    ii = (vertslen - 1) - i
                    v = active_obj.vertices[ii]

                else:
                    v = active_obj.vertices[i]

                co = obj.matrix_world @ v.co
                if firstvert:
                    items += f'[{round(co.x, 5)},{round(co.y, 5)},{round(co.z, 5)},{round(radius, 2)}]'
                    firstvert = False
                else:
                    items += f',[{round(co.x, 5)},{round(co.y, 5)},{round(co.z, 5)},{round(radius, 2)}]'
                i += 1
                splititer += 1
            
            print(f"decal road split at {splititer} nodes")
            print("\n")
            items += f'],'

            if one_way:
                items+=f'"oneWay":true,'
            if o_object:
                items+=f'"overObjects":true,'

            items+=f'"renderPriority":{render_priority},"smoothness":{smoothness},"startEndFade":[{round(s_fade, 2)},{round(e_fade, 2)}],'

            if start_tangent:
                items+=f'"startTangent":true,'

            items+=f'"textureLength":{t_length},"zBias":{z_bias}'


            items += "}\n"

        print(f"Path is {filepath}")
        
        file = open(filepath, 'w')
        file.write(items)
        file.close()

        return


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportDecalRoad.bl_idname, text="Decal Road Export (.json)")