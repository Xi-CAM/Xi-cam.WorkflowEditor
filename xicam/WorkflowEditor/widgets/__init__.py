from xicam.gui.widgets.dynimageview import DynImageView
from xicam.plugins import QWidgetPlugin
from xicam.core.data import NonDBHeader
from xicam.core import msg


class RAWViewer(DynImageView, QWidgetPlugin):
    def __init__(self, header, field):
        super(RAWViewer, self).__init__()
        self.setPredefinedGradient('grey')

        self.setHeader(header, field)

    def setHeader(self, header: NonDBHeader, field: str, *args, **kwargs):
        self.header = header
        # make lazy array from document
        data = None
        try:
            data = header.meta_array(field)
        except IndexError as ex:
            msg.logMessage(f'Header object contained no frames with field "{field}".', level=msg.ERROR)
            msg.logError(ex)

        if data:
            # kwargs['transform'] = QTransform(0, -1, 1, 0, 0, data.shape[-2])
            super(RAWViewer, self).setImage(img=data, *args, **kwargs)
