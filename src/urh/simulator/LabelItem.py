from PySide2.QtGui import QPainter, QPen

from urh.simulator.GraphicsItem import GraphicsItem
from urh.simulator.SimulatorProtocolLabel import SimulatorProtocolLabel

from urh import constants

from PySide2.QtWidgets import QGraphicsTextItem
from PySide2.QtCore import Qt


class LabelItem(GraphicsItem):
    font_bold_italic = None

    def __init__(self, model_item: SimulatorProtocolLabel, parent=None):
        assert isinstance(model_item, SimulatorProtocolLabel)
        super().__init__(model_item=model_item, parent=parent)

        self.name = QGraphicsTextItem(self)
        self.name.setFont(self.font)

    def update_flags(self):
        if self.scene().mode == 1:
            self.set_flags(is_selectable=True, accept_hover_events=True)

    def update_numbering(self):
        pass

    def paint(self, painter: QPainter, option, widget):
        style = Qt.DotLine if self.model_item.has_live_input else Qt.SolidLine
        pen = QPen(constants.LINECOLOR, 1, style)
        painter.setPen(pen)
        painter.setBrush(constants.LABEL_COLORS[self.model_item.color_index])
        painter.drawRect(self.boundingRect())

        if self.scene().mode == 1:
            super().paint(painter, option, widget)

    def boundingRect(self):
        return self.childrenBoundingRect()

    def refresh(self):
        self.name.setPlainText(self.model_item.name)
        if self.model_item.is_checksum_label:
            value_type = "Checksum"
        else:
            value_type = SimulatorProtocolLabel.VALUE_TYPES[self.model_item.value_type_index]
        tooltip = "Value type:<br><b>{}</b>".format(value_type)
        self.setToolTip(tooltip)
