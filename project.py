import random
import matplotlib.pyplot as plt
import numpy as np
import math
from subprocess import Popen, PIPE
import re
import argparse


def main():
    # Parse command-line for programmable args
    parser = argparse.ArgumentParser(description="Create fractal from Chaos Game")

    parser.add_argument(
        "-s",
        "--sides",
        type=int,
        default=argparse.SUPPRESS,
        nargs="?",
        help="Number of sides (vertices) for polygon",
    )
    parser.add_argument(
        "-e",
        type=str,
        default=argparse.SUPPRESS,
        choices=["True", "true", "T", "t", "False", "false", "F", "f"],
        nargs="?",
        help="Equilateral polygon indicator [True/False]",
    )
    parser.add_argument(
        "-m",
        "--multi",
        type=float,
        default=argparse.SUPPRESS,
        nargs="?",
        help="Distance traveled from start point multiplier (AKA ratio)",
    )
    parser.add_argument(
        "-r",
        "--res",
        type=int,
        default=argparse.SUPPRESS,
        nargs="?",
        help="Plot resolution (number of points)",
    )
    parser.add_argument(
        "-x",
        type=float,
        default=argparse.SUPPRESS,
        nargs="?",
        help="x Coordinate start point",
    )
    parser.add_argument(
        "-y",
        type=float,
        default=argparse.SUPPRESS,
        nargs="?",
        help="y Coordinate start point",
    )
    args = parser.parse_args()

    if "s" in args:
        if args.s is not None and args.s > 2:
            sides = args.s

        else:
            sides = get_sides()

    elif "sides" in args:
        if args.sides is not None and args.sides > 2:
            sides = args.sides

        else:
            sides = get_sides()

    else:
        sides = get_sides()

    if "e" in args:
        if args.e is not None:
            if "t" in args.e.lower():
                equilateral_option = True

            elif "f" in args.e.lower():
                equilateral_option = False

            else:
                equilateral_option = get_equilateral()

        else:
            equilateral_option = get_equilateral()

    else:
        equilateral_option = get_equilateral()

    # Create polygon vertices
    start_x, start_y = create_polygon(sides, equilateral=equilateral_option)

    plt.scatter(start_x, start_y, marker=".")

    # Check args for start point (tracepoint default= [0, 0])
    trace_point = [0, 0]

    if "x" in args:
        if args.x is not None:
            trace_point[0] = args.x

    if "y" in args:
        if args.y is not None:
            trace_point[1] = args.y

    plt.scatter(*trace_point, marker=".")

    plt.savefig("initial.png")

    # Get resolution from cl args
    resolution = 15000
    if "r" in args:
        if args.r is not None:
            resolution = args.r

    elif "res" in args:
        if args.res is not None:
            resolution = args.res

    # Create ideal ratio calc
    ratio = get_ideal_ratio(sides)

    # Overwrite ideal ratio if m or multi exists in cl args
    if "m" in args:
        if args.m is not None:
            ratio = args.m

    elif "multi" in args:
        if args.multi is not None:
            ratio = args.multi

    # Create array of tracepoints, assign to x, y
    x, y = create_fractal_array_xy(start_x, start_y, trace_point, resolution, ratio)

    plt.scatter(x, y, marker=".", s=1, color="black")

    plt.savefig("fractal.png")

    # Opens "fractal.png" (modified from users Blender and Travis Cunningham: https://stackoverflow.com/a/12605520)
    process = Popen(["code", "fractal.png"], stdout=PIPE, stderr=PIPE)

    stdout, stderr = process.communicate()


def get_sides():
    while True:
        sides = input("Number of sides: ")
        pattern = r"^\d+$"
        matches = re.search(pattern, sides)

        if matches:
            if int(sides) > 2:
                return int(sides)


def get_equilateral():
    while True:
        response = input("Equilateral? [True/False]: ")
        pattern = r"^(True|true|T|t|False|false|F|f)$"
        matches = re.search(pattern, response)

        if matches:
            if "t" in response.lower():
                return True

            else:
                return False


# Returns polygon vertices (modified from user Jon Betts: https://stackoverflow.com/a/23414895)
def create_polygon(sides, equilateral, radius=1, rotation=0):
    one_segment = math.pi * 2 / sides

    if equilateral:
        points = [
            [
                math.sin(one_segment * i + rotation) * radius,
                math.cos(one_segment * i + rotation) * radius,
            ]
            for i in range(sides)
        ]

    else:
        points = [
            [
                math.sin(one_segment * i + rotation) * radius
                + random.uniform(-1, 1) / sides,
                math.cos(one_segment * i + rotation) * radius
                + random.uniform(-1, 1) / sides,
            ]
            for i in range(sides)
        ]

    return np.array(points).T


# Source: https://computational-discovery-on-jupyter.github.io/Computational-Discovery-on-Jupyter/Contents/chaos-game-representation.html#sec-generalization
def get_ideal_ratio(sides):
    return (1 + math.sin(math.pi / sides)) ** -1


def create_fractal_array_xy(start_x, start_y, trace_point, resolution, multiplier):
    trace_points = []

    for _ in range(resolution):
        # Randomly choose between starter points
        choice = random.choice(range(len(start_x)))

        # Find distance to randomly chosen point and move difference / denominator to new start point (tracepoint)
        trace_point = [
            trace_point[0] - ((trace_point[0] - start_x[choice]) * multiplier),
            trace_point[1] - ((trace_point[1] - start_y[choice]) * multiplier),
        ]

        trace_points.append(trace_point)

    x, y = np.array(trace_points).T

    return x, y


if __name__ == "__main__":
    main()
