import json
from pathlib import Path

import ee
from sepal_ui.scripts.warning import SepalWarning
from traitlets import HasTraits, Int, Unicode

import component.parameter as cp
from component import model as cmod
from component.message import cm
from component.model.aoi_model import SeplanAoi
from component.scripts import validation
from component.scripts.seplan import Seplan

ee.Initialize()


class Recipe(HasTraits):
    # Set types
    aoi_model: SeplanAoi
    benefit_model: cmod.BenefitModel
    constraint_model: cmod.ConstraintModel
    cost_model: cmod.CostModel

    new_changes = Int().tag(sync=True)
    """A counter that is incremented every time any of the app model changes. This trait is linked to the app_model, so we can show messaages on the app_bar"""

    recipe_session_path = Unicode("", allow_none=True).tag(sync=True)
    """The path to the recipe session file. This value will come from the recipe view, it will be used by the export csv function and to create the names of the assets to export"""

    def __init__(self):
        super().__init__()
        self.seplan_aoi = None
        self.benefit_model = None
        self.constraint_model = None
        self.cost_model = None
        self.seplan = None

    def load_model(self, **delete_aoi):
        """Define all the models required by the module."""
        self.seplan_aoi = SeplanAoi(**delete_aoi)
        self.benefit_model = cmod.BenefitModel()
        self.constraint_model = cmod.ConstraintModel()
        self.cost_model = cmod.CostModel()
        self.seplan = Seplan(
            self.seplan_aoi, self.benefit_model, self.constraint_model, self.cost_model
        )

        # link the new_changes counter to the models
        self.seplan_aoi.observe(self.update_changes, "updated")
        # Icall them "new_changes" because there's another "updated" trait that is
        # used to trigger the update of the view of these models.
        self.benefit_model.observe(self.update_changes, "new_changes")
        self.constraint_model.observe(self.update_changes, "new_changes")
        self.cost_model.observe(self.update_changes, "new_changes")

        return self

    def update_changes(self, change):
        """Increment the new_changes counter by 1."""
        print(change)
        self.new_changes += 1

    def load(self, recipe_path: str):
        """Load the recipe element in the different element of the app."""
        # This is not necessary since the recipe path is already validated from the origin
        # but I want to keep it here if I want to call the load function from somewhere else
        recipe_path = Path(validation.validate_recipe(recipe_path))
        with recipe_path.open() as f:
            data = json.loads(f.read())

        # load the aoi_model
        self.seplan_aoi.import_data(data["aoi"])
        self.benefit_model.import_data(data["benefits"])
        self.constraint_model.import_data(data["constraints"])
        self.cost_model.import_data(data["costs"])

        self.new_changes = 0

    def save(self, full_recipe_path: str):
        """Save the recipe in a json file with a timestamp."""
        # Raise a sepal_ui.warning if there is no loaded models
        if not self.seplan:
            raise SepalWarning(cm.recipe.error.no_seplan)

        with Path(full_recipe_path).open("w") as f:
            data = {
                "signature": "cc19794c0d420e449f36308ce0ede23d03f14be78490d857fbda3289a1910e75",
                "aoi": self.seplan_aoi.export_data(),
                "benefits": self.benefit_model.export_data(),
                "constraints": self.constraint_model.export_data(),
                "costs": self.cost_model.export_data(),
            }

            json.dump(data, f, indent=4)

        self.new_changes = 0

        return full_recipe_path

    def reset(self):
        """Reset the recipe to its default values."""
        # Each of the models will return to its default values and
        # they'll update their respective views by themselves

        self.seplan_aoi.reset()
        self.benefit_model.reset()
        self.constraint_model.reset()
        self.cost_model.reset()

        self.new_changes = 0

    def get_recipe_path(self, recipe_name: str):
        """generate full recipe path."""
        res_dir = cp.result_dir / "recipes"
        res_dir.mkdir(exist_ok=True)

        recipe_path = Path(recipe_name)

        # add .json if not present
        if recipe_path.suffix != ".json":
            recipe_path = recipe_path.with_suffix(".json")

        # create the json file
        return str(res_dir / recipe_path)
