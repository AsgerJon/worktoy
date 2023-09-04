"""WorkSide - Style - WorkPainter
Subclass of QPainter implementing direct support for classes in the
WorkSide framwork."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from builtins import str
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPaintDevice, QFont, QPen, QBrush, QColor

from workside.style import Font, Line, Fill
from workside.widgets import CoreWidget
from worktoy.fields import View


class WorkPainter(QPainter):
  """WorkSide - Style - WorkPainter
  Subclass of QPainter implementing direct support for classes in the
  WorkSide framwork."""

  @View('noLine')
  def getEmptyPen(self) -> QPen:
    """Getter-function for the empty pen"""
    pen = QPen()
    pen.setStyle(Qt.PenStyle.NoPen)
    pen.setColor(QColor(255, 255, 255, 0))
    pen.setWidget(1)
    return pen

  @View('noBrush')
  def getEmptyBrush(self) -> QBrush:
    """Getter-function for the empty brush."""
    brush = QBrush()
    brush.setStyle(Qt.BrushStyle.NoBrush)
    brush.setColor(QColor(255, 255, 255, 0))
    return brush

  @View('baseFont')
  def getBaseFont(self) -> QFont:
    """Getter-function for a basic font."""
    raise NotImplementedError

  @View('widget')
  def getWidget(self) -> CoreWidget:
    """Getter-function for the actively painted widget."""
    if isinstance(self.device(), CoreWidget):
      return self.device()
    from worktoy.waitaminute import TypeSupportError
    raise TypeSupportError(CoreWidget, self.device(), 'device')

  def __init__(self, *args, **kwargs) -> None:
    QPainter.__init__(self, *args, **kwargs)

  def begin(self, coreWidget: QPaintDevice) -> None:
    """Implementation of 'begin' to emit begin signal."""
    if not isinstance(coreWidget, CoreWidget):
      from worktoy.waitaminute import TypeSupportError
      raise TypeSupportError(CoreWidget, coreWidget, 'coreWidget')
    coreWidget.paintStart.emit()
    QPainter.begin(self, coreWidget, )

  def device(self) -> CoreWidget:
    """Implementation of the device getter method to specifically
    support the CoreWidget."""
    widget = QPainter.device(self, )
    if isinstance(widget, CoreWidget):
      return widget
    from worktoy.waitaminute import TypeSupportError
    raise TypeSupportError(CoreWidget, widget, 'device')

  def end(self) -> None:
    """Implementation of 'end' to emit 'end' signal."""
    self.device().paintEnd.emit()
    QPainter.end(self)

  def setFont(self, fontData: Any) -> None:
    """Implementation of the font setter function to accept WorkSide
    classes."""
    if isinstance(fontData, CoreWidget):
      return QPainter.setBrush(self, fontData.style.font)

  def setPen(self, lineData: Any) -> None:
    """Implementation of the pen setter function to accept WorkSide
    classes."""
    if isinstance(lineData, CoreWidget):
      return QPainter.setBrush(self, lineData.style.pen)

  def setBrush(self, fillData: Any) -> None:
    """Implementation of the brush setter function to accept WorkSide
    classes."""
    if isinstance(fillData, CoreWidget):
      return QPainter.setBrush(self, fillData.style.brush)

  def __rmatmul__(self, other: Any) -> None:
    if isinstance(other, QBrush):
      return QPainter.setBrush(self, other)
    if isinstance(other, Fill):
      return QPainter.setBrush(self, other.style)
    if isinstance(other, QPen):
      return QPainter.setPen(self, other)
    if isinstance(other, Line):
      return QPainter.setPen(self, other.style)
    if isinstance(other, QFont):
      return QPainter.setFont(self, other)
    if isinstance(other, Font):
      return QPainter.setFont(self, other.style)

  def printText(self, ) -> None:
    """Custom method combining the steps required to print a text field:
    Fill background, draw outline and draw text."""
    if not self.isActive():
      from worktoy.waitaminute import UnexpectedStateError
      raise UnexpectedStateError('isActive')
    text = self.widget.text
    rect = self.widget.rect
    align = self.widget.rect.align
    viewRect = self.viewport()
    textRect = rect.align(viewRect)
    #  Fills the background behind the text
    self.widget.textBackgroundBrush @ self
    self.noPen @ self
    self.drawRect(textRect)
    #  Draws a borderline around the text field
    self.noBrush @ self
    self.widget.borderPen @ self
    self.drawRoundedRect(textRect, 4, 4)
    #  Writes the text
    self.widget.textPen @ self
    self.widget.textFont @ self
    self.drawText(textRect, text)
