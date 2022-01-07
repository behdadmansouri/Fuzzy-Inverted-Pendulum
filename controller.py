# -*- coding: utf-8 -*-

from math import degrees
import numpy as np
from fuzzy.storage.fcl.Reader import Reader


class FuzzyController(object):
    def __init__(self, fcl_path):
        self.system = Reader().load_from_file(fcl_path)

    @staticmethod
    def _make_input(world):
        return dict(cp=world.x, cv=world.v, pa=degrees(world.theta), pv=degrees(world.omega))

    @staticmethod
    def _make_output():
        return dict(force=0.)

    def decide(self, world):
        # output = self._make_output()
        # self.system.calculate(self._make_input(world), output)
        # return output['force']
        return self.my_decide_function(world)

    def my_decide_function(self, world):
        # fuzzify parameters
        fuzzy_params = self.fuzzify(self._make_input(world))
        # calculating belonging to force
        belonging = self.inference(fuzzy_params)
        # defuzzify to find force
        force = self.defuzzification(belonging)
        return force

    def fuzzify(self, world):
        pa, pv, cv, cp = world['pa'], world['pv'], world['cv'], world['cp']
        fuzzy_params = {'pa_up_more_right': self.fuzzification(pa, (0, 0), (30, 1), (60, 0)),
                        'pa_up_right': self.fuzzification(pa, (30, 0), (60, 1), (90, 0)),
                        'pa_up': self.fuzzification(pa, (60, 0), (90, 1), (120, 0)),
                        'pa_up_left': self.fuzzification(pa, (90, 0), (120, 1), (150, 0)),
                        'pa_up_more_left': self.fuzzification(pa, (120, 0), (150, 1), (180, 0)),
                        'pa_down_more_left': self.fuzzification(pa, (180, 0), (210, 1), (240, 0)),
                        'pa_down_left': self.fuzzification(pa, (210, 0), (240, 1), (270, 0)),
                        'pa_down': self.fuzzification(pa, (240, 0), (270, 1), (300, 0)),
                        'pa_down_right': self.fuzzification(pa, (270, 0), (300, 1), (330, 0)),
                        'pa_down_more_right': self.fuzzification(pa, (300, 0), (330, 1), (360, 0)),
                        'pv_cw_fast': self.fuzzification(pv, (-200, 0), (-200, 1), (-100, 0)),
                        'pv_cw_slow': self.fuzzification(pv, (-200, 0), (-100, 1), (0, 0)),
                        'pv_stop': self.fuzzification(pv, (-100, 0), (0, 1), (100, 0)),
                        'pv_ccw_slow': self.fuzzification(pv, (0, 0), (100, 1), (200, 0)),
                        'pv_ccw_fast': self.fuzzification(pv, (100, 0), (200, 1), (200, 0)),
                        'cp_left_far': self.fuzzification(cp, (-10, 0), (-10, 1), (-5, 0)),
                        'cp_left_near': self.fuzzification(cp, (-10, 0), (-2.5, 1), (0, 0)),
                        'cp_stop': self.fuzzification(cp, (-2.5, 0), (0, 1), (2.5, 0)),
                        'cp_right_near': self.fuzzification(cp, (0, 0), (2.5, 1), (10, 0)),
                        'cp_right_far': self.fuzzification(cp, (5, 0), (10, 1), (10, 0)),
                        'cv_left_fast': self.fuzzification(cv, (-5, 0), (-5, 1), (-2.5, 0)),
                        'cv_left_slow': self.fuzzification(cv, (-5, 0), (-1, 1), (0, 0)),
                        'cv_stop': self.fuzzification(cv, (-1, 0), (0, 1), (1, 0)),
                        'cv_right_slow': self.fuzzification(cv, (0, 0), (1, 1), (5, 0)),
                        'cv_right_fast': self.fuzzification(cv, (2.5, 0), (5, 1), (5, 0))}
        return fuzzy_params

    def fuzzification(self, x, beginning, middle, end):
        (x1, y1), (x2, y2), (x3, y3) = beginning, middle, end
        if x1 <= x <= x2:
            return self.linear_equation(x1, y1, x2, y2, x)
        elif x2 < x <= x3:
            return self.linear_equation(x3, y3, x2, y2, x)
        else:
            return 0

    @staticmethod
    def linear_equation(x1, y1, x2, y2, x):
        if x1 == x2:
            y = float((max(y1, y2)))
        else:
            slope = (y2 - y1) / float((x2 - x1))
            offset = y1 - slope * x1
            y = slope * x + offset
        return y

    @staticmethod
    def inference(param):
        stop = max(max(min(param['pa_up'], param['pv_stop']),
                       min(param['pa_up_right'], param['pv_ccw_slow']),
                       min(param['pa_up_left'], param['pv_cw_slow'])),
                   min(param['pa_down_more_right'], param['pv_cw_slow']),
                   min(param['pa_down_more_left'], param['pv_ccw_slow']),
                   min(param['pa_down'], param['pv_ccw_fast']),
                   min(param['pa_up'], param['pv_stop']),
                   min(param['pa_down'], param['pv_cw_fast']),
                   min(param['pa_down_left'], param['pv_cw_fast']),
                   min(param['pa_down_right'], param['pv_ccw_fast']),
                   min(param['pa_down_more_right'], param['pv_cw_fast']),
                   min(param['pa_down_more_right'], param['pv_ccw_fast']),
                   min(param['pa_down_more_left'], param['pv_cw_fast']),
                   min(param['pa_down_more_left'], param['pv_ccw_fast']),
                   min(param['cv_stop'], param['pv_stop'], param['pa_up']))
        right_fast = max(min(param['pa_up_more_right'], param['pv_ccw_slow']),
                         min(param['pa_up_more_right'], param['pv_cw_slow']),
                         min(param['pa_up_more_right'], param['pv_cw_fast']),
                         min(param['pa_down_more_right'], param['pv_ccw_slow']),
                         min(param['pa_down_right'], param['pv_ccw_slow']),
                         min(param['pa_down_right'], param['pv_cw_slow']),
                         min(param['pa_up_right'], param['pv_cw_slow']),
                         min(param['pa_up_right'], param['pv_stop']),
                         min(param['pa_up_right'], param['pv_cw_fast']),
                         min(param['pa_up_left'], param['pv_cw_fast']),
                         min(param['pa_down'], param['pv_stop']),
                         min(param['pa_up'], param['pv_cw_fast']),
                         min(param['cv_left_fast'], param['pv_stop']),
                         min(param['cv_left_fast'], param['pv_cw_fast']),
                         min(param['cv_left_fast'], param['pv_cw_slow']),
                         min(param['cv_stop'], param['pv_ccw_fast']))
        left_fast = max(min(param['pa_up_more_left'], param['pv_ccw_slow']),
                        min(param['pa_up_more_left'], param['pv_cw_slow']),
                        min(param['pa_up_more_left'], param['pv_ccw_fast']),
                        min(param['pa_down_more_left'], param['pv_cw_slow']),
                        min(param['pa_down_left'], param['pv_cw_slow']),
                        min(param['pa_down_left'], param['pv_ccw_slow']),
                        min(param['pa_up_left'], param['pv_ccw_slow']),
                        min(param['pa_up_left'], param['pv_stop']),
                        min(param['pa_up_left'], param['pv_ccw_fast']),
                        min(param['pa_up_right'], param['pv_ccw_fast']),
                        min(param['pa_up'], param['pv_ccw_fast']),
                        min(param['cv_right_fast'], param['pv_stop']),
                        min(param['cv_right_fast'], param['pv_ccw_fast']),
                        min(param['cv_right_fast'], param['pv_ccw_slow']),
                        min(param['cv_stop'], param['pv_ccw_fast']))
        left_slow = max(min(param['pa_up_more_right'], param['pv_ccw_fast']),
                        min(param['pa_down_left'], param['pv_ccw_fast']),
                        min(param['pa_up_left'], param['pv_cw_slow']),
                        min(param['pa_up'], param['pv_ccw_slow']),
                        min(param['cv_right_fast'], param['pv_cw_slow']),
                        min(param['cv_left_slow'], param['pv_ccw_fast']),
                        min(param['cv_left_fast'], param['pv_ccw_fast']))
        right_slow = max(min(param['pa_up_more_left'], param['pv_cw_fast']),
                         min(param['pa_down_right'], param['pv_cw_fast']),
                         min(param['pa_up_right'], param['pv_ccw_slow']),
                         min(param['pa_up'], param['pv_cw_slow']),
                         min(param['cv_left_slow'], param['pv_ccw_slow']),
                         min(param['cv_right_slow'], param['pv_cw_slow']),
                         min(param['cv_right_slow'], param['pv_cw_fast']))
        return left_fast, left_slow, right_fast, right_slow, stop

    def defuzzification(self, belonging):
        left_fast, left_slow, right_fast, right_slow, stop = belonging
        points = np.linspace(-100, 100, 1000)
        integral = 0.0
        sums = 0.0
        for i in range(len(points)):
            force_right_fast = min(right_fast, self.fuzzification(points[i], (60, 0), (80, 1), (100, 0)))
            force_right_slow = min(right_slow, self.fuzzification(points[i], (0, 0), (60, 1), (80, 0)))
            force_left_fast = min(left_fast, self.fuzzification(points[i], (-100, 0), (-80, 1), (-60, 0)))
            force_left_slow = min(left_slow, self.fuzzification(points[i], (-80, 0), (-60, 1), (0, 0)))
            force_Stop = min(stop, self.fuzzification(points[i], (-60, 0), (0, 1), (60, 0)))
            max_force = max(force_right_fast, force_right_slow, force_left_fast, force_left_slow, force_Stop)
            integral += max_force
            sums += max_force * points[i]
        if integral == 0:
            return 0
        else:
            return sums / integral
