# Copyright (C) 2013-2014 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import *





class Gravitrax(Boxes):
    """Gravitrax extension"""

    description = "This box is kept simple on purpose. If you need more features have a look at the UniversalBox."

    ui_group = "Alan"

    def __init__(self) -> None:
        Boxes.__init__(self)
        self.argparser.add_argument(
            "--outer_h", action="store", type=float, default=44, help="Height of the outer hex")
        self.argparser.add_argument(
            "--inner_h", action="store", type=float, default=30, help="Height of the inner hex")
        self.argparser.add_argument(
            "--innerer_h", action="store", type=float, default=28, help="Height of the innerer hex")
        self.argparser.add_argument(
            "--outer_snap_h", action="store", type=float, default=2.5, help="Height of the outer hex snap")
        self.argparser.add_argument(
            "--inner_snap_h", action="store", type=float, default=12, help="Height of the outer hex snap")
        self.argparser.add_argument(
            "--stand_l", action="store", type=float, default=7, help="Length of the stand")
        self.argparser.add_argument(
            "--stand_unit_h", action="store", type=float, default=9.525, help="Height of the original stand")
        self.argparser.add_argument(
            "--stand_units_number", action="store", type=float, default=4, help="Height of the stand in form of number of original stands")
        self.argparser.add_argument(
            "--fitness", action="store", type=float, default=0.1, help="Fitness of the model")

    def set_lengths(self):
        self.outer_l = math.sqrt(1/3.0 * self.outer_h *self.outer_h)
        self.inner_l = math.sqrt(1/3.0 * self.inner_h *self.inner_h)
        self.innerer_l = math.sqrt(1/3.0 * self.innerer_h *self.innerer_h)
        self.stand_h = self.stand_unit_h * self.stand_units_number
        self.stand_w = (self.outer_h - self.inner_h) / 2.0
        print(self.stand_w)


    def render(self):
        self.set_lengths()
        self.hexes()
        self.moveTo(100,0)
        self.stand()

    def stand(self):
        neg = 1
        with self.saved_context():
            line = []
            # bottom
            line.append(self.stand_l + self.fitness) #X+
            line.append(-90*neg)
            line.append(self.thickness) #Y-
            line.append(90*neg)
            line.append(self.inner_snap_h -  self.fitness) #X+
            line.append(90*neg)
            # right
            line.append(self.stand_h - self.inner_snap_h - self.thickness) #Y+
            line.append(90*neg)
            # top
            line.extend(self.stand_top())
            # left
            line.append(self.stand_h - self.thickness * 3 - self.inner_snap_h) #Y-
            line.append(-90*neg)
            line.append(self.stand_l+self.inner_snap_h-self.stand_w) #X-
            line.append(90*neg)
            line.append(self.thickness) #Y-
            self.polyline(*line)

    def stand_top(self):
        l = math.sqrt(2*self.inner_snap_h*self.inner_snap_h)
        w = self.outer_snap_h - self.fitness
        h = self.thickness
        line = [0, -45, l, 45]
        line.append(0)
        line.append(-90)
        line.append(self.thickness)
        line.append(90)
        line.append(0)
        line.extend(self.stand_snap(w, h))
        line.append(self.stand_w - 2*w)
        line.extend(self.stand_snap(w, h))
        line.append(0)
        line.append(90)
        line.append(self.thickness)
        line.append(-90)
        line.append(0)
        return line + [135, l, -45]

    def hexes(self):
        with self.saved_context():
            line = []
            for i in range(3):
                line.append(self.outer_l)
                line.append(60)
                line.extend(self.outer_line_with_snap())
                line.append(60)
            self.polyline(*line)
            self.center_inner_hex()
            line = []
            for i in range(3):
                line.extend(self.inner_line_with_snap(self.thickness, self.outer_snap_h, self.inner_l))
                line.append(-60)
                line.append(self.inner_l)
                line.append(-60)
            self.polyline(*line)
            self.center_innerer_hex()
            line = []
            for i in range(6):
                line.append(self.innerer_l)
                line.append(-60)
            self.polyline(*line)

    def center_inner_hex(self):
        d_x = (self.outer_l - self.inner_l) / 2.0
        d_y = (self.outer_h + self.inner_h) / 2.0
        self.moveTo(d_x,d_y)

    def center_innerer_hex(self):
        d_x = (self.inner_l - self.innerer_l) / 2.0
        d_y = -(self.inner_h - self.innerer_h) / 2.0
        self.moveTo(d_x,d_y)

    def snap(self, w, h, reversed=False):
        angle = 90
        pre_snap = []
        post_snap = []
        if reversed:
            pre_snap = [180, 0]
            post_snap = [0, 180, w, 0]
        return pre_snap + [angle, h, -angle, w, -angle, h, angle] + post_snap

    def stand_snap(self, w, h):
        angle = -90
        return [angle, h, -angle, w, -angle, h, angle]

    def outer_line_with_snap(self):
        w = self.thickness +self.fitness
        h = self.outer_snap_h +self.fitness
        l = self.outer_l
        leftover = (l - w) / 2.0
        return [leftover] + self.snap(w, h) + [leftover]

    def inner_line_with_snap(self, w, h, l):
        w = self.thickness+self.fitness
        h1 = self.outer_snap_h+self.fitness
        h2 = self.inner_snap_h+self.fitness
        l = self.inner_l
        leftover = (l - w) / 2.0
        line = [leftover]
        line.extend(self.snap(w, h1))
        line.append(0)
        line.extend(self.snap(w, h2, reversed=True))
        line.append(leftover)
        return line