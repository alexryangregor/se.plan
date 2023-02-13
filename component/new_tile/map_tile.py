from sepal_ui import mapping as sm
from sepal_ui import sepalwidgets as sw

from .export_control import ExportControl
from .about_control import AboutControl


class MapTile(sw.Tile):
    def __init__(self):

        # set the map in the center
        self.map = sm.SepalMap()

        # create the controls
        full_control = sm.FullScreenControl(self.map, True, True, position="topright")
        val_control = sm.InspectorControl(self.map, False, position="bottomleft")
        export_control = ExportControl(position="bottomleft")
        about_control = AboutControl(position="bottomleft")

        # add them on the map
        self.map.add(full_control)
        self.map.add(val_control)
        self.map.add(export_control)
        self.map.add(about_control)

        super().__init__(id_="map_tile", title="", inputs=[self.map])
