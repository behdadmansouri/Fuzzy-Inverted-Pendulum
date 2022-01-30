# -*- coding: utf-8 -*-

from math import degrees
import numpy as np
from fuzzy.storage.fcl.Reader import Reader


class FuzzyController(object):
    def __init__(self, fcl_path):
        self.system = Reader().load_from_file(fcl_path)

    @staticmethod
    def _make_input(world):
        temp = degrees(world.theta)
        if temp < 0:
            temp += 360
        temp2 = degrees(world.omega)
        if temp2 > 200:
            temp2 = 200
        if temp2 < -200:
            temp2 = -200
        return dict(cp=world.x, cv=world.v, pa=temp, pv=temp2)

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
        fuzzy_params = {'pa_up_more_right': self.fuzzification(pa, 'pa_up_more_right'),
                        'pa_up_right': self.fuzzification(pa, 'pa_up_right'),
                        'pa_up': self.fuzzification(pa, 'pa_up'),
                        'pa_up_left': self.fuzzification(pa, 'pa_up_left'),
                        'pa_up_more_left': self.fuzzification(pa, 'pa_up_more_left'),
                        'pa_down_more_left': self.fuzzification(pa, 'pa_down_more_left'),
                        'pa_down_left': self.fuzzification(pa, 'pa_down_left'),
                        'pa_down': self.fuzzification(pa, 'pa_down'),
                        'pa_down_right': self.fuzzification(pa, 'pa_down_right'),
                        'pa_down_more_right': self.fuzzification(pa, 'pa_down_more_right'),
                        'pv_cw_fast': self.fuzzification(pv, 'pv_cw_fast'),
                        'pv_cw_slow': self.fuzzification(pv, 'pv_cw_slow'),
                        'pv_stop': self.fuzzification(pv, 'pv_stop'),
                        'pv_ccw_slow': self.fuzzification(pv, 'pv_ccw_slow'),
                        'pv_ccw_fast': self.fuzzification(pv, 'pv_ccw_fast'),
                        'cp_left_far': self.fuzzification(cp, 'cp_left_far'),
                        'cp_left_near': self.fuzzification(cp, 'cp_left_near'),
                        'cp_stop': self.fuzzification(cp, 'cp_stop'),
                        'cp_right_near': self.fuzzification(cp, 'cp_right_near'),
                        'cp_right_far': self.fuzzification(cp, 'cp_right_far'),
                        'cv_left_fast': self.fuzzification(cv, 'cv_left_fast'),
                        'cv_left_slow': self.fuzzification(cv, 'cv_left_slow'),
                        'cv_stop': self.fuzzification(cv, 'cv_stop'),
                        'cv_right_slow': self.fuzzification(cv, 'cv_right_slow'),
                        'cv_right_fast': self.fuzzification(cv, 'cv_right_fast')}
        return fuzzy_params

    def fuzzification(self, x, belonging):
        y1, y2, y3 = 0, 1, 0
        x1, x2, x3, = 0, 0, 0
        if belonging == 'pa_up_more_right':
            x1, x2, x3 = 0, 30, 60
        elif belonging == 'pa_up_right':
            x1, x2, x3 = 30, 60, 90
        elif belonging == 'pa_up':
            x1, x2, x3 = 60, 90, 120
        elif belonging == 'pa_up_left':
            x1, x2, x3 = 90, 120, 150
        elif belonging == 'pa_up_more_left':
            x1, x2, x3 = 120, 150, 180
        elif belonging == 'pa_down_more_left':
            x1, x2, x3 = 180, 210, 240
        elif belonging == 'pa_down_left':
            x1, x2, x3 = 210, 240, 270
        elif belonging == 'pa_down':
            x1, x2, x3 = 240, 270, 300
        elif belonging == 'pa_down_right':
            x1, x2, x3 = 270, 300, 330
        elif belonging == 'pa_down_more_right':
            x1, x2, x3 = 300, 330, 360
        elif belonging == 'pv_cw_fast':
            x1, x2, x3 = -200, -200, -100
        elif belonging == 'pv_cw_slow':
            x1, x2, x3 = -200, -100, 0
        elif belonging == 'pv_stop':
            x1, x2, x3 = -100, 0, 100
        elif belonging == 'pv_ccw_slow':
            x1, x2, x3 = 0, 100, 200
        elif belonging == 'pv_ccw_fast':
            x1, x2, x3 = 100, 200, 200
        elif belonging == 'cp_left_far':
            x1, x2, x3 = -10, -10, -5
        elif belonging == 'cp_left_near':
            x1, x2, x3 = -10, -2.5, 0
        elif belonging == 'cp_stop':
            x1, x2, x3 = -2.5, 0, 2.5
        elif belonging == 'cp_right_near':
            x1, x2, x3 = 0, 2.5, 10
        elif belonging == 'cp_right_far':
            x1, x2, x3 = 5, 10, 10
        elif belonging == 'cv_left_fast':
            x1, x2, x3 = -5, -5, -2.5
        elif belonging == 'cv_left_slow':
            x1, x2, x3 = -5, -1, 0
        elif belonging == 'cv_stop':
            x1, x2, x3 = -1, 0, 1
        elif belonging == 'cv_right_slow':
            x1, x2, x3 = 0, 1, 5
        elif belonging == 'cv_right_fast':
            x1, x2, x3 = 2.5, 5, 5
        elif belonging == 'force_right_fast':
            x1, x2, x3 = 60, 80, 100
        elif belonging == 'force_right_slow':
            x1, x2, x3 = 0, 60, 80
        elif belonging == 'force_left_fast':
            x1, x2, x3 = -100, -80, -60
        elif belonging == 'force_left_slow':
            x1, x2, x3 = -80, -60, 0
        elif belonging == 'force_Stop':
            x1, x2, x3 = -60, 0, 60
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
        stop = max(min(param['pa_up'], param['pv_stop']),  # 0
                   min(param['pa_up_right'], param['pv_ccw_slow']),  # 0
                   min(param['pa_up_left'], param['pv_cw_slow']),  # 0
                   min(param['pa_down_more_right'], param['pv_cw_slow']),  # 10
                   min(param['pa_down_more_left'], param['pv_ccw_slow']),  # 12
                   min(param['pa_down'], param['pv_ccw_fast']),  # 37
                   min(param['pa_up'], param['pv_stop']),  # 42
                   min(param['pa_down'], param['pv_cw_fast']),  # 36
                   min(param['pa_down_left'], param['pv_cw_fast']),  # 22
                   min(param['pa_down_right'], param['pv_ccw_fast']),  # 21
                   min(param['pa_down_more_right'], param['pv_cw_fast']),  # 14
                   min(param['pa_down_more_right'], param['pv_ccw_fast']),  # 13
                   min(param['pa_down_more_left'], param['pv_cw_fast']),  # 15
                   min(param['pa_down_more_left'], param['pv_ccw_fast']))  # 16
        right_fast = max(min(param['pa_up_more_right'], param['pv_ccw_slow']),  # 1
                         min(param['pa_up_more_right'], param['pv_cw_slow']),  # 2
                         min(param['pa_up_more_right'], param['pv_cw_fast']),  # 6
                         min(param['pa_down_more_right'], param['pv_ccw_slow']),  # 9
                         min(param['pa_down_right'], param['pv_ccw_slow']),  # 17
                         min(param['pa_down_right'], param['pv_cw_slow']),  # 18
                         min(param['pa_up_right'], param['pv_cw_slow']),  # 26
                         min(param['pa_up_right'], param['pv_stop']),  # 27
                         min(param['pa_up_right'], param['pv_cw_fast']),  # 32
                         min(param['pa_up_left'], param['pv_cw_fast']),  # 33
                         min(param['pa_down'], param['pv_stop']),  # 35
                         min(param['pa_up'], param['pv_cw_fast']))  # 41
        left_fast = max(min(param['pa_up_more_left'], param['pv_ccw_slow']),  # 4
                        min(param['pa_up_more_left'], param['pv_cw_slow']),  # 3
                        min(param['pa_up_more_left'], param['pv_ccw_fast']),  # 8
                        min(param['pa_down_more_left'], param['pv_cw_slow']),  # 11
                        min(param['pa_down_left'], param['pv_cw_slow']),  # 19
                        min(param['pa_down_left'], param['pv_ccw_slow']),  # 20
                        min(param['pa_up_left'], param['pv_ccw_slow']),  # 29
                        min(param['pa_up_left'], param['pv_stop']),  # 30
                        min(param['pa_up_left'], param['pv_ccw_fast']),  # 34
                        min(param['pa_up_right'], param['pv_ccw_fast']),  # 31
                        min(param['pa_up'], param['pv_ccw_fast']))  # 39
        left_slow = max(min(param['pa_up_more_right'], param['pv_ccw_fast']),  # 5
                        min(param['pa_down_left'], param['pv_ccw_fast']),  # 24
                        min(param['pa_up_left'], param['pv_cw_slow']),  # 28
                        min(param['pa_up'], param['pv_ccw_slow']))  # 38
        right_slow = max(min(param['pa_up_more_left'], param['pv_cw_fast']),  # 7
                         min(param['pa_down_right'], param['pv_cw_fast']),  # 22
                         min(param['pa_up_right'], param['pv_ccw_slow']),  # 25
                         min(param['pa_up'], param['pv_cw_slow']))  # 40
        # right_slow = param['pa_down_right']
        # left_slow = param['pa_down_left']
        # right_fast = max(param['pa_up_more_right'],
        #                  param['pa_up_right'] * param['pv_cw_slow'],
        #                  param['pv_cw_fast'] * max(param['pa_up_right'], param['pa_up_more_right']))
        # left_fast = max(param['pa_up_more_left'],
        #                 param['pa_up_left'] * param['pv_ccw_slow'],
        #                 param['pv_ccw_fast'] * max(param['pa_up_left'], param['pa_up_more_left']))
        return left_fast, left_slow, right_fast, right_slow, stop

    def defuzzification(self, belonging):
        left_fast, left_slow, right_fast, right_slow, stop = belonging
        points = np.linspace(-100, 100, 1000)
        integral = 0.0
        sums = 0.0
        for i in range(len(points)):
            force_right_fast = min(right_fast, self.fuzzification(points[i], 'force_right_fast'))
            force_right_slow = min(right_slow, self.fuzzification(points[i], 'force_right_slow'))
            force_left_fast = min(left_fast, self.fuzzification(points[i], 'force_left_fast'))
            force_left_slow = min(left_slow, self.fuzzification(points[i], 'force_left_slow'))
            force_Stop = min(stop, self.fuzzification(points[i], 'force_Stop'))
            max_force = max(force_right_fast, force_right_slow, force_left_fast, force_left_slow, force_Stop)
            integral += max_force
            sums += max_force * points[i]
        if integral == 0:
            return 0
        else:
            return sums / integral
