import sepal_ui.sepalwidgets as sw

import component.parameter as cp
from component.message import cm
from component.model.recipe import Recipe
from component.widget.alert_state import AlertState
from component.widget.custom_widgets import Tabs
from component.widget.questionaire_table import Table


class QuestionnaireTile(sw.Layout):
    def __init__(self):
        # name the tile
        self._metadata = {"mount_id": "questionnaire_tile"}
        self.class_ = "d-block"

        super().__init__()

    def build(self, recipe: Recipe, alert: AlertState):
        """Build the questionnaire tile."""
        alert.set_state("new", "questionnaire", "building")

        benefit_table = Table(model=recipe.benefit_model)

        constraint_table = Table(
            model=recipe.constraint_model, aoi_model=recipe.seplan_aoi
        )

        cost_table = Table(model=recipe.cost_model)

        tabs = Tabs(
            titles=[cm[theme].tab_title for theme in cp.themes],
            content=[benefit_table, constraint_table, cost_table],
            class_="mt-5",
            fixed_tabs=True,
            centered=True,
        )

        self.set_children([tabs], position="last")

        alert.set_state("new", "questionnaire", "done")
