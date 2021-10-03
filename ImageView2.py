from PyQt5.QtCore import QPointF, Qt, QRectF, QSizeF, QEvent, QRect
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5.QtWidgets import QApplication, QGraphicsItem, QGraphicsView, QGraphicsPixmapItem, QGraphicsScene

import numpy as np
import cv2
from PIL import Image, ImageQt

class ImageView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        image = kwargs.pop('image', None)
        super(ImageView, self).__init__(*args, **kwargs)
        self.setGeometry(QRect(0, 0, 800, 600))

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


        # func 1
        # self.pixmap = QPixmap(image)

        # func2
        arr = cv2.imread(image)
        arr = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
        pil = Image.fromarray(arr)
        qimage = ImageQt.toqimage(pil)
        qimage = qimage.scaled(self.width(), self.height(), Qt.KeepAspectRatio)
        self.pixmap = QPixmap.fromImage(qimage)

        # func3
        # ppp = Image.open(image).convert("RGB")
        # self.pixmap = ImageQt.toqpixmap(ppp)

        self._scene = QGraphicsScene()  # 场景
        self._scene.addPixmap(self.pixmap)

        self.setScene(self._scene)

        # self.fitInView(QRectF(QPointF(0, 0), QSizeF(self.pixmap.size())), Qt.KeepAspectRatio)
        # self.fitInView(QRectF(QPointF(0, 0), QSizeF(self.pixmap.size())), Qt.KeepAspectRatioByExpanding)
        # self.fitInView(QRectF(QPointF(0, 0), QSizeF(self.pixmap.size())), Qt.IgnoreAspectRatio)

    def fitInView(self, rect, flags=Qt.IgnoreAspectRatio):
        """居中适应
        :param rect: 矩形范围
        :param flags:
        """
        viewRect = self.viewport().rect()

        sceneRect = self.transform().mapRect(rect)

        print(f"view:{viewRect.size()}")
        print(f"scene:{sceneRect.size()}")

        x_ratio = viewRect.width() / sceneRect.width()
        y_ratio = viewRect.height() / sceneRect.height()

        if flags == Qt.KeepAspectRatio:  # 保持原来的形状
            x_ratio = y_ratio = min(x_ratio, y_ratio)
        elif flags == Qt.KeepAspectRatioByExpanding:  # 保持原来的形状，但是有些部分会看不到
            x_ratio = y_ratio = max(x_ratio, y_ratio)
        elif flags == Qt.IgnoreAspectRatio:  # 直接填满，但是会产生形变
            x_ratio, y_ratio = x_ratio, y_ratio

        self.scale(x_ratio, y_ratio)
        self.centerOn(rect.center())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.middleMouseButtonPress(event)
        else:
            super().mousePressEvent(event)
    # 判断鼠标松开的类型
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.middleMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)
     # 拖拽功能 - 按下 的实现 
    def middleMouseButtonPress(self, event):
        # 设置画布拖拽
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), 
                            event.screenPos(),
                            Qt.LeftButton, event.buttons() | Qt.LeftButton, 
                            event.modifiers())
        super().mousePressEvent(fakeEvent)
    # 拖拽功能 - 松开 的实现 
    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), 
                              event.screenPos(),
                              Qt.LeftButton, event.buttons() & ~Qt.LeftButton, 
                              event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        # 取消拖拽
        self.setDragMode(QGraphicsView.NoDrag)

    # 滚轮缩放的实现
    def wheelEvent(self, event):
        # 放大触发
        if event.angleDelta().y() > 0:
            zoomFactor = 1 + 0.1
        # 缩小触发
        else:
            zoomFactor = 1 - 0.1
        self.scale(zoomFactor, zoomFactor)


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(format='text')

    app = QApplication(sys.argv)
    w = ImageView(image='Data/bg.jpg')
    # w = ImageView(image='D:/594870.jpg')
    w.show()
    sys.exit(app.exec_())
