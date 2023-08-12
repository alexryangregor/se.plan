import pandas as pd
from traitlets import List

from component import parameter as cp
from component.message import cm
from component.model.questionnaire_model import QuestionnaireModel


class ConstraintModel(QuestionnaireModel):
    names = List([]).tag(sync=True)
    ids = List([]).tag(sync=True)
    themes = List([]).tag(sync=True)
    assets = List([]).tag(sync=True)
    descs = List([]).tag(sync=True)
    units = List([]).tag(sync=True)
    values = List([]).tag(sync=True)
    data_type = List([]).tag(sync=True)

    def __init__(self):
        # get the default constraint from the csv file
        _constraint = pd.read_csv(cp.layer_list).fillna("")
        _constraint = _constraint[_constraint.layer_id == "treecover_with_potential"]

        for _, r in _constraint.iterrows():
            self.themes.append(r.subtheme)
            self.names.append(cm.layers[r.layer_id].name)
            self.ids.append(r.layer_id)
            self.assets.append(r.gee_asset)
            self.descs.append(cm.layers[r.layer_id].detail)
            self.units.append(r.unit)
            self.values.append([0, 1])
            self.data_type.append(r.data_type)

        super().__init__()

    def remove(self, id: str, update=True) -> None:
        """Remove a constraint using its name.

        Args:
            id (str): the id of the constraint to remove
            update (bool, optional): trigger the update. Defaults to True.
                I dont' want to update the whole table if one asset failed
                to be added.
        """
        idx = self.get_index(id)

        del self.names[idx]
        del self.ids[idx]
        del self.themes[idx]
        del self.assets[idx]
        del self.descs[idx]
        del self.units[idx]
        del self.values[idx]
        del self.data_type[idx]

        if update:
            self.updated += 1

    def add(
        self,
        theme: str,
        name: str,
        id: str,
        asset: str,
        desc: str,
        unit: str,
        data_type: str,
    ) -> None:
        """add a constraint and trigger the update."""
        self.themes.append(theme)
        self.names.append(name)
        self.ids.append(id)
        self.assets.append(asset)
        self.descs.append(desc)
        self.units.append(unit)
        self.values.append([])
        self.data_type.append(data_type)

        self.updated += 1

    def update(
        self,
        theme: str,
        name: str,
        id: str,
        asset: str,
        desc: str,
        unit: str,
        data_type: str,
    ) -> None:
        """update an existing constraint metadata and trigger the update."""
        idx = self.get_index(id)

        self.themes[idx] = theme
        self.names[idx] = name
        self.ids[idx] = id
        self.assets[idx] = asset
        self.descs[idx] = desc
        self.units[idx] = unit
        self.data_type[idx] = data_type

        self.updated += 1

    def update_value(self, id: str, value: list) -> None:
        """Update the value of a specific constraint."""
        idx = self.get_index(id)
        self.values[idx] = value
