import numpy as np
import scipy.misc
from databroker.in_memory import BlueskyInMemoryCatalog

from xicam.core.execution.workflow import ingest_result_set, project_intents
from xicam.core.intents import PlotIntent, ImageIntent
from xicam.gui.widgets.imageviewmixins import BetterButtons, LogScaleIntensity

from xicam.core import msg
from xicam.core.execution import Workflow
from xicam.plugins import GUIPlugin, GUILayout
from xicam.gui.widgets.linearworkfloweditor import WorkflowEditor
# TODO: temporary code -- this should live in the views module (after view/model updated with layoutChanged)
from qtpy.QtWidgets import QWidget, QVBoxLayout
from xicam.gui.widgets.views import DataSelectorView, StackedCanvasView
from xicam.core.workspace import Ensemble
from xicam.gui.models import EnsembleModel, IntentsModel


class WorkflowEditorPlugin(GUIPlugin):
    name = 'WorkflowEditor'

    def __init__(self):

        self.workflow = Workflow()
        self.workfloweditor = WorkflowEditor(self.workflow, callback_slot=self.showResult, except_slot=lambda *_: self.workflow._pretty_print())

        self.ensemble_model = EnsembleModel()

        data_selector_view = DataSelectorView()
        data_selector_view.setModel(self.ensemble_model)

        # Our results views' model (should only contain intents)
        intents_model = IntentsModel()
        intents_model.setSourceModel(self.ensemble_model)

        # Our results view widget container
        results_view = StackedCanvasView()
        results_view.setModel(intents_model)


        self.stages = {
            'Testing': GUILayout(results_view, left=None, righttop=data_selector_view, right=self.workfloweditor),

        }
        super(WorkflowEditorPlugin, self).__init__()

    def showResult(self, *result):
        print('result:', result)

        ensemble = Ensemble()
        doc_generator = ingest_result_set(self.workflow, result)

        #### TODO: replace with Dan's push-based
        documents = list(doc_generator)
        catalog = BlueskyInMemoryCatalog()
        # TODO -- change upsert signature to put start and stop as kwargs
        # TODO -- ask about more convenient way to get a BlueskyRun from a document generator
        catalog.upsert(documents[0][1], documents[-1][1], ingest_result_set, [self.workflow, result], {})
        catalog = catalog[-1]
        ####

        ensemble.append_catalog(catalog)
        self.ensemble_model.add_ensemble(ensemble, [project_intents])
