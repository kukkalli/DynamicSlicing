import math
from random import Random
from code.path_coordinate import PathCoordinate
from code.gnodeb_cell import GNodeBCell
from scipy.constants import pi


def print_path_coordinates(text, path_coordinates):
    """
    Print function to print the list of path coordinate objects
    :param text:
    :param path_coordinates:
    :return:
    """
    print(text + ":")
    for path_coordinate in path_coordinates:
        print("Path: " + path_coordinate.__str__())


class GenerateRandomPathData:
    """
    A class to generate random path and random cell points on the given path
    """

    def __init__(self, start_point=PathCoordinate(0, 0), seed=19841101):
        """
        Constructor of the Class GenerateRandomPathData
        :param start_point:
        :param seed:
        """
        self.__random = Random()
        self.__random.seed(seed)
        self.__start_point = start_point
        self.__current_point_position = start_point
        self.__random_path_points = []
        self.__random_cells_list = []
        self.__seed = seed
        self.__cell_density = 0
        self.__paths = []

    def __generate_random_cells(self, radius, density, transmit_power_db=45, operator_id="",
                                operator_name="Network Provider"):
        """
        Generate random cell values
        :param radius:
        :param density:
        :param transmit_power_db:
        :param operator_id:
        :param operator_name:
        :return:
        """
        for i in range(density):
            cell_point_x = round(self.__current_point_position.get_x() + self.__random.uniform(-radius, radius), 2)
            cell_point_y = round(self.__current_point_position.get_y() + self.__random.uniform(-radius, radius), 2)
            cell_point = GNodeBCell(cell_point_x, cell_point_y, transmit_power_db=transmit_power_db,
                                    operator_id=operator_id,
                                    operator_name=operator_name)
            self.__random_cells_list.append(cell_point)

    def __cell_density_iteration_value(self, cell_max_radius, transmit_power_db, operator_id, operator_name):
        """
        Check if the count of cell density is more than 1 to create a random cell
        :param cell_max_radius:
        :param transmit_power_db:
        :param operator_id:
        :param operator_name:
        :return:
        """
        if self.__cell_density >= 1:
            iteration_value = math.floor(self.__cell_density)
            self.__cell_density -= iteration_value
            self.__generate_random_cells(cell_max_radius, iteration_value, transmit_power_db, operator_id,
                                         operator_name)

    def __generate_random_path(self, total_travel_distance, cell_max_radius, step_distance, cell_density,
                               transmit_power_db, operator_id, operator_name):
        """
        function to generate random path given,
        :param total_travel_distance:
        :param cell_max_radius:
        :param step_distance:
        :param cell_density:
        :param transmit_power_db:
        :param operator_id:
        :param operator_name:
        """
        # print("total_travel_distance: ", total_travel_distance)
        travel_distance = 0
        self.__random_path_points.append(PathCoordinate(self.__start_point.get_x(), self.__start_point.get_y()))
        self.__cell_density = cell_density
        self.__cell_density_iteration_value(cell_max_radius, transmit_power_db, operator_id, operator_name)
        while travel_distance < total_travel_distance:
            travel_distance = round(travel_distance + step_distance, 2)
            delta_x = round(self.__random.uniform(-step_distance * 0.8, step_distance * 0.8), 2)
            current_point = self.__current_point_position.move_in_x_by_delta_y_and_given_distance(
                delta_x, step_distance)
            self.__random_path_points.append(PathCoordinate(current_point.get_x(), current_point.get_y()))
            self.__cell_density = round(self.__cell_density + cell_density, 2)
            self.__cell_density_iteration_value(cell_max_radius, transmit_power_db, operator_id, operator_name)
        self.__paths.append(self.__random_path_points)

    def generate_path_data(self, total_travel_distance=10.0, step_distance=0.2, angle_of_path=0.0):
        """
        Generate path co-ordinates from the given
        :param total_travel_distance:
        :param step_distance:
        :param angle_of_path:
        :return:
        """
        factor = 2 * pi / 10
        # print("total_travel_distance: ", total_travel_distance)
        travel_distance = 0
        self.__current_point_position = PathCoordinate(self.__start_point.get_x(), self.__start_point.get_y())
        self.__random_path_points = []
        self.__random_path_points.append(PathCoordinate(self.__start_point.get_x(), self.__start_point.get_y()))
        # print((angle_of_path - factor) * 360 / (2 * pi), angle_of_path * 360 / (2 * pi),
        #       (angle_of_path + factor) * 360 / (2 * pi))
        # print("Cos of angle: ", math.cos(angle_of_path - factor), math.cos(angle_of_path + factor))
        # print("Sin of angle: ", math.sin(angle_of_path - factor), math.sin(angle_of_path + factor))
        while travel_distance < total_travel_distance:
            travel_distance = round(travel_distance + step_distance, 2)
            if math.sin(angle_of_path - factor) < math.sin(angle_of_path + factor):
                delta_y = round(self.__random.uniform(step_distance * math.sin(angle_of_path - factor),
                                                      step_distance * math.sin(angle_of_path + factor)), 2)
            else:
                delta_y = round(self.__random.uniform(step_distance * math.sin(angle_of_path + factor),
                                                      step_distance * math.sin(angle_of_path - factor)), 2)

            if math.cos(angle_of_path - factor) < math.cos(angle_of_path + factor):
                delta_x = round(self.__random.uniform(step_distance * math.cos(angle_of_path - factor),
                                                      step_distance * math.cos(angle_of_path + factor)), 2)
            else:
                delta_x = round(self.__random.uniform(step_distance * math.cos(angle_of_path + factor),
                                                      step_distance * math.cos(angle_of_path - factor)), 2)

            if (angle_of_path <= pi / 4) and (angle_of_path >= -pi / 4):
                current_point = self.__current_point_position.move_in_x_by_delta_y_and_given_distance(delta_y,
                                                                                                      step_distance)
            elif (angle_of_path > pi / 4) and (angle_of_path < 3 * pi / 4):
                current_point = self.__current_point_position.move_in_y_by_delta_x_and_given_distance(
                    delta_x, step_distance)
            elif (angle_of_path >= 3 * pi / 4) and (angle_of_path <= 5 * pi / 4):
                current_point = self.__current_point_position.move_in_minus_x_given_by_delta_y_and_given_distance(
                    delta_y, step_distance)
            else:
                current_point = self.__current_point_position.move_in_minus_y_given_by_delta_x_and_given_distance(
                    delta_x, step_distance)
            self.__random_path_points.append(PathCoordinate(current_point.get_x(), current_point.get_y()))
        # print("len: ", len(self.__random_path_points))
        return self.__random_path_points.copy()

    def generate_multiple_paths(self, paths_count=1, max_distance=15.0, step_distance=0.2, min_distance=5.0):
        """
        Generate multiple paths given,
        :param paths_count:
        :param max_distance:
        :param step_distance:
        :param min_distance:
        :return:
        """
        self.__random.seed(self.__seed)
        angle_of_path = 2 * pi / paths_count
        for i, count in enumerate(range(paths_count)):
            self.__paths.append(self.generate_path_data(self.__random.randint(min_distance, max_distance),
                                                        step_distance, i * angle_of_path))

    def generate_random_cells_data_for_given_path(self, path_coordinates, cell_max_radius=1, cell_density=1,
                                                  transmit_power_db=45, operator_id="",
                                                  operator_name="Network Provider"):
        """
        Generate Random
        :param path_coordinates:
        :param cell_max_radius:
        :param cell_density:
        :param transmit_power_db:
        :param operator_id:
        :param operator_name:
        :return:
        """
        self.__cell_density = 0
        # print(len(path_coordinates))
        # print_path_coordinates("Hello: ", path_coordinates)
        for _point in path_coordinates:
            self.__current_point_position = _point
            self.__cell_density = round(self.__cell_density + cell_density, 2)
            self.__cell_density_iteration_value(cell_max_radius, transmit_power_db, operator_id, operator_name)

    def generate_random_cells_data_for_path_list(self, paths, cell_max_radius=1, cell_density=1, transmit_power_db=45,
                                                  operator_id="", operator_name="Network Provider"):
        """
        Generate Random
        :param paths:
        :param cell_max_radius:
        :param cell_density:
        :param transmit_power_db:
        :param operator_id:
        :param operator_name:
        :return:
        """
        self.__cell_density = 0
        self.__random_cells_list = []
        for path in paths:
            self.generate_random_cells_data_for_given_path(path, cell_max_radius, cell_density, transmit_power_db,
                                                           operator_id,
                                                           operator_name)
        return self.get_random_cells_list()

    def get_paths_list(self):
        """
        get list of all randomly generated paths
        :return:
        """
        return self.__paths

    def get_random_cells_list(self):
        """
        Get randomly generated list of Random ENodeB Cells
        :return:
        """
        return self.__random_cells_list

    def get_generated_path(self):
        """
        Get randomly generated list of Path Coordinates
        :return:
        """
        return self.__random_path_points
