from PyQt5.QtCore import QPointF, Qt, QRectF, QSizeF
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QGraphicsItem, QGraphicsView, QGraphicsPixmapItem, QGraphicsScene


class ImageView(QGraphicsView):
    """图片查看控件"""

    def __init__(self, *args, **kwargs):
        image = kwargs.pop('image', None)
        super(ImageView, self).__init__(*args, **kwargs)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.pixmap = QPixmap(image)
        
        self._item = QGraphicsPixmapItem()  # 图元
        self._item.setFlags(QGraphicsPixmapItem.ItemIsFocusable | QGraphicsPixmapItem.ItemIsMovable)
        self._item.setPixmap(self.pixmap)  # 图元放置图像

        self._scene = QGraphicsScene(self)  # 场景
        self._scene.addItem(self._item)  # 场景设置图元

        self.setScene(self._scene)  # 视图设置场景

        rect = QApplication.instance().desktop().availableGeometry(self)  # 窗口大小，不是图像大小
        self.resize(int(rect.width() * 2 / 3), int(rect.height() * 2 / 3))

        self.setPixmap(image)

    def setPixmap(self, pixmap):
        """加载图片
        :param pixmap: 图片或者图片路径
        :param fitIn: 是否适应
        :type pixmap: QPixmap or QImage or str
        :type fitIn: bool
        """
        self.setSceneDims()
        self.fitInView(QRectF(self._item.pos(), QSizeF(self.pixmap.size())), Qt.KeepAspectRatio)

    def fitInView(self, rect, flags=Qt.IgnoreAspectRatio):
        """居中适应
        :param rect: 矩形范围
        :param flags:
        :return:
        """
        viewRect = self.viewport().rect()
        sceneRect = self.transform().mapRect(rect)
        x_ratio = viewRect.width() / sceneRect.width()
        y_ratio = viewRect.height() / sceneRect.height()
        if flags == Qt.KeepAspectRatio:
            x_ratio = y_ratio = min(x_ratio, y_ratio)
        elif flags == Qt.KeepAspectRatioByExpanding:
            x_ratio = y_ratio = max(x_ratio, y_ratio)
        self.scale(x_ratio, y_ratio)
        self.centerOn(rect.center())

    def setSceneDims(self):
        self.setSceneRect(QRectF(QPointF(0, 0), QPointF(self.pixmap.width(), self.pixmap.height())))

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.zoom(1 + 0.1)
        else:
            self.zoom(1 - 0.1)

    def zoom(self, factor):
        """缩放
        :param factor: 缩放的比例因子
        """
        self.transform().scale(factor, factor).mapRect(QRectF(0, 0, 1, 1)).width()
        self.scale(factor, factor)


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(format='text')

    app = QApplication(sys.argv)
    w = ImageView(image='Data/bg.jpg')
    w.show()
    sys.exit(app.exec_())
