import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt


class GridWidget(QWidget):
    def __init__(self, rows=20, cols=20, cell_size=20):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = [[False for _ in range(cols)] for _ in range(rows)]
        self.setFixedSize(cols * cell_size, rows * cell_size)
        self.drawing = False

    def paintEvent(self, event):
        painter = QPainter(self)
        for row in range(self.rows):
            for col in range(self.cols):
                rect_x = col * self.cell_size
                rect_y = row * self.cell_size
                painter.setPen(Qt.black)
                if self.grid[row][col]:
                    painter.setBrush(QColor(0, 150, 255))
                else:
                    painter.setBrush(Qt.white)
                painter.drawRect(rect_x, rect_y, self.cell_size, self.cell_size)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self._draw_at(event.x(), event.y())

    def mouseMoveEvent(self, event):
        if self.drawing:
            self._draw_at(event.x(), event.y())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def _draw_at(self, x, y):
        col = x // self.cell_size
        row = y // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = True
            self.update()

    def clear_grid(self):
        self.grid = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.update()

    def to_array(self):
        arr2d = np.array(self.grid, dtype=int)
        return arr2d.ravel()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Desenhe no Grid 20x20")
        self.grid_widget = GridWidget()
        
        self.clear_button = QPushButton("Limpar")
        self.clear_button.clicked.connect(self.grid_widget.clear_grid)
        
        self.test_button = QPushButton("Teste")
        self.test_button.clicked.connect(self.save_as_array)
        
        layout = QVBoxLayout()
        layout.addWidget(self.grid_widget)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.test_button)
        self.setLayout(layout)

    def save_as_array(self):
        arr = self.grid_widget.to_array()
        print("Array do grid:")
        print(arr)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
