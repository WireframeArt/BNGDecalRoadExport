#    <Decal Road Export, Blender addon for exporting decal roads to BeamNG.>
#    Copyright (C) <2022> <Damian Paterson>
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Decal Road Export",
    "author": "Damian Paterson / Wireframe Art",
    "version": (1, 0),
    "blender": (3, 2, 0),
    "location": "File > Export > Decal Road Export",
    "description": "A tool for exporting a .json file with the selected decal road that we copy and paste into a items.level.json file",
    "category": "Export",
}

from .ExportRoad import *

def register():
    bpy.utils.register_class(ExportDecalRoad)
    # Register and add to the "file selector" menu (required to use F3 search "Text Export Operator" for quick access).
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportDecalRoad)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()