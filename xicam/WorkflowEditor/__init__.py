import numpy as np
from functools import partial
from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from xicam.core.data import NonDBHeader
from xicam.core import msg

from xicam.plugins import GUIPlugin, GUILayout

from xicam.gui.widgets.tabview import TabView
from xicam.gui.widgets.dynimageview import DynImageView
from xicam.gui.widgets.linearworkfloweditor import WorkflowEditor
from .workflows.example import ExampleWorkflow


class WorkflowEditorPlugin(GUIPlugin):
    name = 'WorkflowEditor'

    def __init__(self):

        self.workflow = ExampleWorkflow()

        self.headermodel = QStandardItemModel()
        from .widgets import RAWViewer
        self.rawtabview = TabView(self.headermodel, widgetcls=RAWViewer)

        self.workfloweditor = WorkflowEditor(self.workflow)
        self.workfloweditor.setHidden(True)

        self.processbutton = QPushButton('Process')
        self.processbutton.clicked.connect(self.process)

        self.outputview = DynImageView()

        self.stages = {
            'Testing': GUILayout(self.rawtabview, right=self.workfloweditor, top=self.processbutton,
                                 bottom=self.outputview),

        }
        super(WorkflowEditorPlugin, self).__init__()

    def appendHeader(self, header: NonDBHeader, **kwargs):
        item = QStandardItem(header.startdoc.get('sample_name', '????'))
        item.header = header
        self.headermodel.appendRow(item)
        self.headermodel.dataChanged.emit(QModelIndex(), QModelIndex())

    def process(self):
        currentitem = self.headermodel.item(self.rawtabview.currentIndex())
        if not currentitem: msg.showMessage('Error: You must open files before processing.')
        try:
            msg.showBusy()
            msg.showMessage('Processing frames...', level=msg.INFO)
            currentheader = self.headermodel.item(self.rawtabview.currentIndex()).header
            data = currentheader.meta_array()

            self.workflow.execute_all(None, image=data, callback_slot=self.showResult)

        except Exception as ex:
            msg.logError(ex)
            msg.showReady()
            msg.clearMessage()

    def showResult(self, result):
        print('result:', result)
        self.outputview.setImage(np.absolute(result['out'].value))
        msg.showReady()
