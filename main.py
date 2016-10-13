import math
import random
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QWidget


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.show()

    def paintEvent(self, QPaintEvent):
        qp = QPainter()

        qp.begin(self)
        for i in range(100):
            self.genfig(qp, 10, 15)
        qp.end()

    def genfig(self, qp, p_count, rad):
        A = self.genpoints(p_count, rad)
        H = self.jarvismarch(A)
        qp.setPen(Qt.black)
        for i in range(len(H) - 1):
            qp.drawLine(A[H[i]][0], A[H[i]][1], A[H[i + 1]][0], A[H[i + 1]][1])
        qp.drawLine(A[H[0]][0], A[H[0]][1], A[H[-1]][0], A[H[-1]][1])

    def genpoints(self, count, rad):
        size = self.size()
        p = [[random.randint(rad, size.width() - rad),
              random.randint(rad, size.height() - rad)]]
        for i in range(1, count):
            while True:
                x = random.randint(p[0][0] - rad, p[0][0] + rad)
                y = random.randint(p[0][1] - rad, p[0][1] + rad)
                if math.sqrt((x - p[0][0]) * (x - p[0][0]) + (y - p[0][1]) * (y - p[0][1])) <= rad:
                    p.append([x, y])
                    break
        return p

    def jarvismarch(self, A):
        n = len(A)
        P = range(n)
        P = list(P)
        # start point
        for i in range(1, n):
            if A[P[i]][0] < A[P[0]][0]:
                P[i], P[0] = P[0], P[i]
        H = [P[0]]
        del P[0]
        P.append(H[0])
        while True:
            right = 0
            for i in range(1, len(P)):
                if self.rotate(A[H[-1]], A[P[right]], A[P[i]]) < 0:
                    right = i
            if P[right] == H[0]:
                break
            else:
                H.append(P[right])
                del P[right]
        return H

    def rotate(self, A, B, C):
        return (B[0] - A[0]) * (C[1] - B[1]) - (B[1] - A[1]) * (C[0] - B[0])

    def mousePressEvent(self, QMouseEvent):
        self.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
