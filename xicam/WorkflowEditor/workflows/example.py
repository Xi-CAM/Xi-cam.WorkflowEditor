from xicam.core.execution.workflow import Workflow
from ..processing.fft import FFT


class ExampleWorkflow(Workflow):
    def __init__(self):
        super(ExampleWorkflow, self).__init__('Example Workflow')

        fft = FFT()
        fft.axis.value = 1

        # add all processes to the workflow
        for process in [fft]:
            self.addProcess(process)

        # attempt auto-connect all processes
        self.autoConnectAll()
