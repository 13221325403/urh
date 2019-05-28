from PySide2.QtCore import pyqtSignal
from PySide2.QtGui import QDragEnterEvent, QDropEvent

from urh.signalprocessing.ProtocolAnalyzer import ProtocolAnalyzer
from urh.signalprocessing.IQSignal import IQSignal
from urh.ui.painting.SignalSceneManager import SignalSceneManager
from urh.ui.views.ZoomableGraphicView import ZoomableGraphicView


class ZoomAndDropableGraphicView(ZoomableGraphicView):
    signal_loaded = pyqtSignal(ProtocolAnalyzer)

    def __init__(self, parent=None):
        self.signal_tree_root = None  # type: ProtocolTreeItem
        self.scene_manager = None

        self.signal = None  # type: IQSignal
        self.proto_analyzer = None  # type: ProtocolAnalyzer

        super().__init__(parent)

    def dragEnterEvent(self, event: QDragEnterEvent):
        event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        mime_data = event.mimeData()
        data_str = str(mime_data.text())
        indexes = list(data_str.split("/")[:-1])

        signal = None
        proto_analyzer = None
        for index in indexes:
            row, column, parent = map(int, index.split(","))
            if parent == -1:
                parent = self.signal_tree_root
            else:
                parent = self.signal_tree_root.child(parent)
            node = parent.child(row)
            if node.protocol is not None and node.protocol.signal is not None:
                signal = node.protocol.signal
                proto_analyzer = node.protocol
                break

        if signal is None:
            return

        self.draw_signal(signal, proto_analyzer)

    def draw_signal(self, signal, proto_analyzer):
        if signal is None:
            return

        self.signal = signal  # type: IQSignal
        self.proto_analyzer = proto_analyzer  # type: ProtocolAnalyzer

        self.scene_manager = SignalSceneManager(signal, self)
        self.plot_data(self.signal.real_plot_data)
        self.show_full_scene()
        self.auto_fit_view()

        self.signal_loaded.emit(self.proto_analyzer)

    def eliminate(self):
        # Do _not_ call eliminate() for self.signal and self.proto_analyzer
        # as these are references to the original data!
        self.signal = None
        self.proto_analyzer = None
        self.signal_tree_root = None
        super().eliminate()
