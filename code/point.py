"""
The class Point which holds the co-ordinate axis values x and y of a given point on a 2 dimensional plane.
"""
import math
import uuid


class Point:
    """Point class with x and y co-ordinates values"""
    def __init__(self, x=0.0, y=0.0, _uuid=""):
        self.__x = x
        self.__y = y
        if _uuid == "":
            self.__uuid = uuid.uuid4()
        else:
            self.__uuid = _uuid

    """
    Get the x-axis value for the given point
    """
    def get_x(self):
        return self.__x

    """
    Get the y-axis value for the given point
    """
    def get_y(self):
        return self.__y

    """
    Get the UUID value for the given point
    """
    def get_uuid(self):
        return str(self.__uuid)

    """
    Move the given point by delta values of x and y
    """
    def move_by_delta_x_y(self, delta_x=0.0, delta_y=0.0):
        self.__x = round(self.__x + delta_x, 2)
        self.__y = round(self.__y + delta_y, 2)
        return self

    """
    Move the given point provided delta_x and distance
    """
    def move_in_y_by_delta_x_and_given_distance(self, delta_x=0.0, distance=0.0):
        self.move_by_delta_x_y(delta_x, round(math.sqrt(distance ** 2 - delta_x ** 2), 2))
        return self

    """
    Move the given point provided delta_x and distance
    """
    def move_in_minus_y_given_by_delta_x_and_given_distance(self, delta_x=0.0, distance=0.0):
        self.move_by_delta_x_y(delta_x, -round(math.sqrt(distance ** 2 - delta_x ** 2), 2))
        return self

    """
    Move the given point provided delta_y and distance
    """
    def move_in_x_by_delta_y_and_given_distance(self, delta_y=0.0, distance=0.0):
        self.move_by_delta_x_y(round(math.sqrt(distance ** 2 - delta_y ** 2), 2), delta_y)
        return self

    """
    Move the given point provided delta_y and distance
    """
    def move_in_minus_x_given_by_delta_y_and_given_distance(self, delta_y=0.0, distance=0.0):
        self.move_by_delta_x_y(-round(math.sqrt(distance ** 2 - delta_y ** 2), 2), delta_y)
        return self

    def get_distance_from_the_point(self, point):
        """
        Distance from the given Point
        :param point:
        :return: distance
        """
        return round(math.sqrt((self.__x - point.get_x())**2 + (self.__y - point.get_y())**2), 2)

    def copy(self):
        """
        Copy a given Point
        :return:
        """
        return Point(self.__x, self.__y, self.__uuid)

    def __str__(self):
        """
        Convert Point object to string
        :return: string
        """
        return "Point has the value of x co-ordinate:" +\
               str(self.__x) + " and the value of y co-ordinate: " + str(self.__y) + " and a UUID value of " +\
               str(self.__uuid)

