#!/usr/bin/env python3
# encoding: utf-8
"""
BrachFitness.py

Module with a bunch of functions to calculate fitness for a GA evolving
a brachistochrone curve. Fancy words.

To use in your project, simply put this file in the project's working directory
and in your python code - from BrachFitness import *

Created by Miguel Tavares.
Copyright (c) 2011 Miguel Tavares under Creative Commons 3.0 BY-SA.
http://creativecommons.org/licenses/by-sa/3.0/
"""
import math

G_ACC = 9.80655

"""
Returns the time needed for a point to travel with frictionless motion through the line segments passed as argument.
If the point cannot reach the final destination, -1 is returned. In case the individual is mis-represented, -1 is returned.

The individual passed as argument should be in the following
format: [ x0,y0, x1,y1, x2,y2, ... ,xi,yi ] - Assure that for every j < i, xj < xi.
Don't forget that (x0,y0) should be the starting point and (xi,yi) the final point in the brachistochrone curve.
"""
def calcBrachTime(indiv, debug=False):
    x_i = indiv[0]
    y_i = maxHeight = indiv[1]
    v_i = time = 0

    if len(indiv) < 4:
        return -1

    for i in range(2, len(indiv), 2):
        # Consistency checking. This wasn't done in a separate function for quickness
        if indiv[i] < x_i:
            return -1
        elif indiv[i] == x_i:
            return -1
        if indiv[i + 1] >= maxHeight:
            return -1
        # Calculate accelaration based on segment slope. Open question - would be using cos() faster?
        # Since the angle had to be calculated beforehand, I don't think so
        dx = indiv[i] - x_i
        dy = indiv[i + 1] - y_i
        li = math.sqrt(dx * dx + dy * dy)
        ai = -G_ACC * dy / li

        # Energy conservation. You really needn't be reading this, but if you have doubts, tell me
        v_j = math.sqrt(2 * (-G_ACC * dy + v_i ** 2 / 2))
        if v_j <= 0.0:
            return -1
        dv = v_j - v_i

        # The speed variation over the acceleration gives us the time. Voila
        time += dv / ai if ai != 0 else li / v_j

        if debug:
            print(f"Segment {i // 2}")
            print(f"dX: {dx} dY: {dy}")
            print(f"Distance Travelled: {li}")
            print(f"Gained velocity: {dv}")
            print(f"Acceleration: {ai}")
            print(f"Time to travel: {dv / ai if ai != 0 else li / v_j}\n")

        # Update the positions and current speed
        v_i = v_j
        x_i = indiv[i]
        y_i = indiv[i + 1]

    return time

"""
Checks for errors in the individual representation. Returns false when:
- There is an height (yj) higher than the starting height.
- The points are not ordered in the x-coordinate or there are duplicate points in x.

This is actually not used by the function above, but if you wish to use it, go on. It can
save you some trouble.
"""
def checkIndiv(indiv):
    x_i = indiv[0]
    maxHeight = indiv[1]

    if len(indiv) < 4:
        return [False, indiv]

    for i in range(2, len(indiv), 2):
        if indiv[i] <= x_i:
            return [False, indiv]
        if indiv[i + 1] > maxHeight:
            return [False, indiv]
        x_i = indiv[i]

    return [True, indiv]

# if __name__ == '__main__':
#     test_indiv = [1,2,2,1,3,0,4,1.5,5,1,6,0,7,1.9,8,0]
#     print(calcBrachTime(test_indiv, True))
