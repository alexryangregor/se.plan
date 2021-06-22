from datetime import datetime
from pathlib import Path

from sepal_ui import sepalwidgets as sw
from sepal_ui.scripts import utils as su
import ipyvuetify as v

from component import scripts as cs
from component.message import cm
from component import widget as cw
from component import parameter as cp

class ValidationTile(sw.Tile):
    
    def __init__(self, aoi_tile, questionnaire_tile, layer_tile):
        
        # gather the io 
        self.layer_model = layer_tile.model
        self.aoi_model = aoi_tile.view.model
        self.question_model = questionnaire_tile.model
        
        # gather the tiles that need to be filled
        self.layer_tile = layer_tile
        self.aoi_tile = aoi_tile
        self.questionnaire_tile = questionnaire_tile
        
        # add the naming textField
        self.w_name = v.TextField(
            label = cm.custom.recipe.name,
            v_model = None
        )
        
        # create the layer list widget 
        self.layers_recipe = cw.layerRecipe().hide()
        mkd = sw.Markdown('  \n'.join(cm.valid.txt)) 
        
        # add the recipe loader
        self.reset_to_recipe = sw.Btn(text=cm.custom.recipe.apply,icon='mdi-download', class_='ml-2')
        self.file_select = sw.FileInput(['.json'], cp.result_dir, cm.custom.recipe.file)
        ep = v.ExpansionPanels(class_="mt-5", children=[v.ExpansionPanel(children=[
            v.ExpansionPanelHeader(
                disable_icon_rotate = True,
                children=[cm.custom.recipe.title],
                v_slots = [{
                    'name': 'actions',
                    'children' : v.Icon(children=['mdi-download'])
                }]
            ),
            v.ExpansionPanelContent(children=[self.file_select, self.reset_to_recipe])
        ])])
        
        # create the tile 
        super().__init__(
            id_ = "compute_widget",
            inputs= [ep, mkd, self.w_name, self.layers_recipe],
            title = cm.valid.title,
            btn = sw.Btn(cm.valid.display, class_ = 'ma-1'),
            alert = sw.Alert()
        )
        
        # js behaviours 
        aoi_tile.view.observe(self._recipe_placeholder, 'updated')
        self.btn.on_event('click', self._validate_data)
        self.reset_to_recipe.on_event('click', self.load_recipe)
        
    def _recipe_placeholder(self, change):
        """name the recipe with the date"""
        
        now = datetime.now()
        
        self.w_name.v_model = f'recipe_{now.strftime("%Y-%m-%d")}'
        
        return self
    
    @su.loading_button(debug=True)
    def _validate_data(self, widget, event, data):
        """validate the data and release the computation btn"""
    
        # watch the inputs
        self.layers_recipe.digest_layers(self.layer_model, self.question_model)
        self.layers_recipe.show()
        
        # save the inputs in a json
        cs.save_recipe(self.layer_model, self.aoi_model, self.question_model, self.w_name.v_model)
        
        return self
    
    @su.loading_button(debug=True)
    def load_recipe(self, widget, event, data, path=None):
        """load the recipe file into the different io, then update the display of the table"""

        # check if path is set, if not use the one frome file select 
        path = path or self.file_select.v_model
            
        cs.load_recipe(self.layer_tile, self.aoi_tile, self.questionnaire_tile, path)
        self.w_name.v_model = Path(path).stem

        # automatically validate them 
        self.btn.fire_event('click', None)

        self.alert.add_msg('loaded', 'success')

        return self