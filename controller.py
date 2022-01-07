# -*- coding: utf-8 -*-

from math import degrees
import numpy as np
from fuzzy.storage.fcl.Reader import Reader


class FuzzyController:

    def __init__(self, fcl_path):
        self.system = Reader().load_from_file(fcl_path)

    def _make_input(self, world):
        return dict(
            cp=world.x,
            cv=world.v,
            pa=degrees(world.theta),
            pv=degrees(world.omega)
        )

    def _make_output(self):
        return dict(force=0.)

    def decide(self, world):
        # output = self._make_output()
        # self.system.calculate(self._make_input(world), output)
        # return output['force']
        return self.my_decide_function(world)

    def my_decide_function(self, world):
        # calculating belonging to each
        left_fast, left_slow, right_fast, right_slow, stop = self.inference(self._make_input(world))
        # defuzzify to find force
        force = self.defuzzification(left_fast, left_slow, right_fast, right_slow, stop)
        return force

    def defuzzification(self, left_fast, left_slow, right_fast, right_slow, stop):
        points = np.linspace(-100, 100, 1000)
        integral = 0.0
        sums = 0.0
        for i in range(len(points)):
            force_right_fast = min(right_fast, self.force_right_fast(points[i]))
            force_right_slow = min(right_slow, self.force_right_slow(points[i]))
            force_left_fast = min(left_fast, self.force_left_fast(points[i]))
            force_left_slow = min(left_slow, self.force_left_slow(points[i]))
            force_Stop = min(stop, self.force_stop(points[i]))
            max_force = max(force_right_fast, force_right_slow, force_left_fast, force_left_slow, force_Stop)
            integral += max_force
            sums += max_force * points[i]
        if integral == 0:
            return 0
        else:
            return sums / integral

    def inference(self, world):
        pa, pv, cv = world['pa'], world['pv'], world['cv']
        stop = max(max(min(self.pa_up(pa), self.pv_stop(pv)),
                       min(self.pa_up_right(pa), self.pv_ccw_slow(pv)),
                       min(self.pa_up_left(pa), self.pv_cw_slow(pv))),
                   min(self.pa_down_more_right(pa), self.pv_cw_slow(pv)),
                   min(self.pa_down_more_left(pa), self.pv_ccw_slow(pv)),
                   min(self.pa_down(pa), self.pv_ccw_fast(pv)),
                   min(self.pa_up(pa), self.pv_stop(pv)),
                   min(self.pa_down(pa), self.pv_cw_fast(pv)),
                   min(self.pa_down_left(pa), self.pv_cw_fast(pv)),
                   min(self.pa_down_right(pa), self.pv_ccw_fast(pv)),
                   min(self.pa_down_more_right(pa), self.pv_cw_fast(pv)),
                   min(self.pa_down_more_right(pa), self.pv_ccw_fast(pv)),
                   min(self.pa_down_more_left(pa), self.pv_cw_fast(pv)),
                   min(self.pa_down_more_left(pa), self.pv_ccw_fast(pv)),
                   min(self.cv_stop(cv), self.pv_stop(pv), self.pa_up(pa)))
        right_fast = max(min(self.pa_up_more_right(pa), self.pv_ccw_slow(pv)),
                         min(self.pa_up_more_right(pa), self.pv_cw_slow(pv)),
                         min(self.pa_up_more_right(pa), self.pv_cw_fast(pv)),
                         min(self.pa_down_more_right(pa), self.pv_ccw_slow(pv)),
                         min(self.pa_down_right(pa), self.pv_ccw_slow(pv)),
                         min(self.pa_down_right(pa), self.pv_cw_slow(pv)),
                         min(self.pa_up_right(pa), self.pv_cw_slow(pv)),
                         min(self.pa_up_right(pa), self.pv_stop(pv)),
                         min(self.pa_up_right(pa), self.pv_cw_fast(pv)),
                         min(self.pa_up_left(pa), self.pv_cw_fast(pv)),
                         min(self.pa_down(pa), self.pv_stop(pv)),
                         min(self.pa_up(pa), self.pv_cw_fast(pv)),
                         min(self.cv_left_fast(cv), self.pv_stop(pv)),
                         min(self.cv_left_fast(cv), self.pv_cw_fast(pv)),
                         min(self.cv_left_fast(cv), self.pv_cw_slow(pv)),
                         min(self.cv_stop(cv), self.pv_ccw_fast(pv)))
        left_fast = max(min(self.pa_up_more_left(pa), self.pv_ccw_slow(pv)),
                        min(self.pa_up_more_left(pa), self.pv_cw_slow(pv)),
                        min(self.pa_up_more_left(pa), self.pv_ccw_fast(pv)),
                        min(self.pa_down_more_left(pa), self.pv_cw_slow(pv)),
                        min(self.pa_down_left(pa), self.pv_cw_slow(pv)),
                        min(self.pa_down_left(pa), self.pv_ccw_slow(pv)),
                        min(self.pa_up_left(pa), self.pv_ccw_slow(pv)),
                        min(self.pa_up_left(pa), self.pv_stop(pv)),
                        min(self.pa_up_left(pa), self.pv_ccw_fast(pv)),
                        min(self.pa_up_right(pa), self.pv_ccw_fast(pv)),
                        min(self.pa_up(pa), self.pv_ccw_fast(pv)),
                        min(self.cv_right_fast(cv), self.pv_stop(pv)),
                        min(self.cv_right_fast(cv), self.pv_ccw_fast(pv)),
                        min(self.cv_right_fast(cv), self.pv_ccw_slow(pv)),
                        min(self.cv_stop(cv), self.pv_ccw_fast(pv)))
        left_slow = max(min(self.pa_up_more_right(pa), self.pv_ccw_fast(pv)),
                        min(self.pa_down_left(pa), self.pv_ccw_fast(pv)),
                        min(self.pa_up_left(pa), self.pv_cw_slow(pv)),
                        min(self.pa_up(pa), self.pv_ccw_slow(pv)),
                        min(self.cv_right_fast(cv), self.pv_cw_slow(pv)),
                        min(self.cv_left_slow(cv), self.pv_ccw_fast(pv)),
                        min(self.cv_left_fast(cv), self.pv_ccw_fast(pv)))
        right_slow = max(min(self.pa_up_more_left(pa), self.pv_cw_fast(pv)),
                         min(self.pa_down_right(pa), self.pv_cw_fast(pv)),
                         min(self.pa_up_right(pa), self.pv_ccw_slow(pv)),
                         min(self.pa_up(pa), self.pv_cw_slow(pv)),
                         min(self.cv_left_slow(cv), self.pv_ccw_slow(pv)),
                         min(self.cv_right_slow(cv), self.pv_cw_slow(pv)),
                         min(self.cv_right_slow(cv), self.pv_cw_fast(pv)))
        return left_fast, left_slow, right_fast, right_slow, stop

    def linear_equation(self, x1, y1, x2, y2, x):
        if x1 == x2:
            y = float((max(y1, y2)))
        else:
            slope = (y2 - y1) / float((x2 - x1))
            offset = y1 - slope * x1
            y = slope * x + offset
        return y

    def fuzzification(self, x, beginning, middle, end):
        (x1, y1), (x2, y2), (x3, y3) = beginning, middle, end
        if x1 <= x <= x2:
            return self.linear_equation(x1, y1, x2, y2, x)
        elif x2 < x <= x3:
            return self.linear_equation(x3, y3, x2, y2, x)
        else:
            return 0

    def pa_up_more_right(self, x):
        return self.fuzzification(x, (0, 0), (30, 1), (60, 0))

    def pa_up_right(self, x):
        return self.fuzzification(x, (30, 0), (60, 1), (90, 0))

    def pa_up(self, x):
        return self.fuzzification(x, (60, 0), (90, 1), (120, 0))

    def pa_up_left(self, x):
        return self.fuzzification(x, (90, 0), (120, 1), (150, 0))

    def pa_up_more_left(self, x):
        return self.fuzzification(x, (120, 0), (150, 1), (180, 0))

    def pa_down_more_left(self, x):
        return self.fuzzification(x, (180, 0), (210, 1), (240, 0))

    def pa_down_left(self, x):
        return self.fuzzification(x, (210, 0), (240, 1), (270, 0))

    def pa_down(self, x):
        return self.fuzzification(x, (240, 0), (270, 1), (300, 0))

    def pa_down_right(self, x):
        return self.fuzzification(x, (270, 0), (300, 1), (330, 0))

    def pa_down_more_right(self, x):
        return self.fuzzification(x, (300, 0), (330, 1), (360, 0))

    def pv_cw_fast(self, x):
        return self.fuzzification(x, (-200, 0), (-200, 1), (-100, 0))

    def pv_cw_slow(self, x):
        return self.fuzzification(x, (-200, 0), (-100, 1), (0, 0))

    def pv_stop(self, x):
        return self.fuzzification(x, (-100, 0), (0, 1), (100, 0))

    def pv_ccw_slow(self, x):
        return self.fuzzification(x, (0, 0), (100, 1), (200, 0))

    def pv_ccw_fast(self, x):
        return self.fuzzification(x, (100, 0), (200, 1), (200, 0))

    def cp_left_far(self, x):
        return self.fuzzification(x, (-10, 0), (-10, 1), (-5, 0))

    def cp_left_near(self, x):
        return self.fuzzification(x, (-10, 0), (-2.5, 1), (0, 0))

    def cp_stop(self, x):
        return self.fuzzification(x, (-2.5, 0), (0, 1), (2.5, 0))

    def cp_right_near(self, x):
        return self.fuzzification(x, (0, 0), (2.5, 1), (10, 0))

    def cp_right_far(self, x):
        return self.fuzzification(x, (5, 0), (10, 1), (10, 0))

    def cv_left_fast(self, x):
        return self.fuzzification(x, (-5, 0), (-5, 1), (-2.5, 0))

    def cv_left_slow(self, x):
        return self.fuzzification(x, (-5, 0), (-1, 1), (0, 0))

    def cv_stop(self, x):
        return self.fuzzification(x, (-1, 0), (0, 1), (1, 0))

    def cv_right_slow(self, x):
        return self.fuzzification(x, (0, 0), (1, 1), (5, 0))

    def cv_right_fast(self, x):
        return self.fuzzification(x, (2.5, 0), (5, 1), (5, 0))

    def force_left_fast(self, x):
        return self.fuzzification(x, (-100, 0), (-80, 1), (-60, 0))

    def force_left_slow(self, x):
        return self.fuzzification(x, (-80, 0), (-60, 1), (0, 0))

    def force_stop(self, x):
        return self.fuzzification(x, (-60, 0), (0, 1), (60, 0))

    def force_right_slow(self, x):
        return self.fuzzification(x, (0, 0), (60, 1), (80, 0))

    def force_right_fast(self, x):
        return self.fuzzification(x, (60, 0), (80, 1), (100, 0))
