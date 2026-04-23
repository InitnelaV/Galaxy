import sys
import numpy as np
import pyvista as pv
from PyQt5 import QtWidgets, QtCore
from pyvistaqt import QtInteractor

class BlackHoleWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Black Hole & accretion disk")
        self.setGeometry(100, 100, 900, 700)
        self.frame = QtWidgets.QFrame()
        self.layout = QtWidgets.QVBoxLayout()
        self.frame.setLayout(self.layout)
        self.setCentralWidget(self.frame)
        self.plotter = QtInteractor(self.frame)
        self.layout.addWidget(self.plotter.interactor)
        self.plotter.set_background("black")
        self.black_hole = pv.Sphere(radius=0.6)
        self.plotter.add_mesh(self.black_hole, color="black")
        #Disk
        n = 8000
        self.theta = np.random.rand(n) * 6 * np.pi
        self.r = 0.5 + np.random.rand(n) * 3
        x = self.r * np.cos(self.theta)
        y = self.r * np.sin(self.theta)
        z = np.random.randn(n) * 0.05
        self.points = np.vstack([x, y, z]).T
        self.cloud = pv.PolyData(self.points.copy())
        self.plotter.add_mesh(
            self.cloud,
            render_points_as_spheres=True,
            point_size=2,
            scalars=self.r,
            cmap="inferno"
        )
        self.angle = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(20)

    def update(self):
        self.angle += 0.03
        # spinning & rotate
        a = self.angle
        r = self.r * 0.99
        theta = self.theta + a * (1.5 / (r + 0.1))
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        z = self.points[:, 2]
        self.cloud.points = np.vstack([x, y, z]).T
        self.plotter.render()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = BlackHoleWindow()
    window.show()
    sys.exit(app.exec_())