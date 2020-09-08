import numpy as np

from xicam.gui.widgets.imageviewmixins import BetterButtons, LogScaleIntensity

from xicam.core import msg
from xicam.core.execution import Workflow
from xicam.plugins import GUIPlugin, GUILayout
from xicam.gui.widgets.linearworkfloweditor import WorkflowEditor

class ResultsView( BetterButtons, LogScaleIntensity):
    pass


class WorkflowEditorPlugin(GUIPlugin):
    name = 'WorkflowEditor'

    def __init__(self):

        self.workflow = Workflow()
        self.workfloweditor = WorkflowEditor(self.workflow, callback_slot=self.showResult, except_slot=lambda *_: self.workflow._pretty_print())

        self.outputview = ResultsView(log_scale=False)

        self.stages = {
            'Testing': GUILayout(self.outputview, left=None, lefttop=None, right=self.workfloweditor),

        }
        super(WorkflowEditorPlugin, self).__init__()

    def showResult(self, result):
        print('result:', result)
        self.outputview.setImage(next(iter(result.values())), axes={"y":0, "x":1}, autoRange=False)
