"""
Find all the nearby cells from the given point
"""
import math
from scipy.constants import speed_of_light
from scipy.constants import pi


def get_unique_list_of_cells(filtered, cells_at_point):
    """
    Get unique list of cells
    :param filtered: filtered cells
    :param cells_at_point: new list of cells at a point for intersection
    :return:
    """
    filtered = [cell for cell in cells_at_point if cell in filtered]
    return filtered


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


def print_cells(text, cells):
    """
    Print function to print the list of cells objects
    :param text:
    :param cells:
    :return:
    """
    print(text + ":")
    print("|ENodeB(x, y) | Average serving Rx power (db)")
    for cell in cells:
        print("|(" + str(cell.get_x()) + ", " + str(cell.get_y()) + ")| " + str(cell.get_average_received_power_db())
              + " db |")


def print_cells_at_point(text, _point, cells):
    """
    Print function to print list of point objects
    :param text:
    :param _point:
    :param cells:
    :return:
    """
    print(text + "Cells for the point (" + str(_point.get_x()) + ", " + str(_point.get_y()) + ") are:")
    for cell in cells:
        print("cell: " + cell.__str__() + " with Rx db: " + str(_point.get_received_power_db(cell)))


def calculate_distance_km_given_fspl(acceptable_FSPL_db, radio_frequency):
    """
    Calculate distance given Free-space path loss (FSPL)
    Formula:
    FSPL = (4*Pi*d*f/c)**2
    FSPL(in db) = 20 log(d) + 20 log(f) + 20 log(4*Pi/c))

    distance formula
    d = sqrt(FSPL)*c/(4*Pi*f)
    Distance from DB
    """
    __FSPL = 10 ** (acceptable_FSPL_db / 10)
    return round(math.sqrt(__FSPL) * speed_of_light / (4 * pi * radio_frequency * 1000), 2)


def calculate_fspl_given_distance(distance_km, radio_frequency):
    """
    Calculate the Free Space path loss given following parameters
    :param distance_km: distance from the vehicle to cell
    :param radio_frequency: radio frequency used in the mobile UL and DL
    :return: FSPL (in db)
    """
    return 20 * math.log10(4 * pi * distance_km * 1000 * radio_frequency / speed_of_light)


def calculate_pl_abg_nlos(distance_km, radio_frequency, alpha, beta, gamma, sigma):
    """
    Calculate the path loss for non line of sight with abg generic model given following parameters
    :param distance_km: distance from the vehicle to cell
    :param radio_frequency: radio frequency used in the mobile UL and DL
    :param alpha: alpha
    :param beta: beta (in dB)
    :param gamma: gamma
    :param sigma: sigma (in dB)
    :return: pl_abg_nlos (in db)
    """
    return 10 * alpha * math.log10(distance_km * 1000) + beta + 10 * gamma * math.log10(radio_frequency/1000000000)\
           + sigma


def calculate_distance_km_given_pl_abg_nlos(acceptable_PL_ABG_NLOS, radio_frequency, alpha, beta, gamma, sigma):
    """
    Calculate distance given Free-space path loss (FSPL)
    Formula:
    PL_ABG_NLOS (in dB) = 10 * alpha * log(d) + beta + 10 * gamma * log(f) + sigma

    distance in meters formula
    d = 10 ** (1/(10 * alpha) * (PL_ABG_NLOS - beta - 10 * gamma * log(f) - sigma))
    Distance from path loss in db, radio frequency, alpha, beta, gamma, sigma

    :param acceptable_PL_ABG_NLOS:
    :param radio_frequency:
    :param alpha: alpha
    :param beta: beta (in dB)
    :param gamma: gamma
    :param sigma: sigma (in dB)
    :return:
    """
    return round((10 ** (1 / (10 * alpha) * (acceptable_PL_ABG_NLOS - beta - sigma -
                                             (10 * gamma * math.log10(radio_frequency / 1000000000)))))/1000, 2)


def calculate_pl_ci(distance_km, radio_frequency):
    """
    Calculate the Free Space path loss given following parameters
    :param distance_km: distance from the vehicle to cell
    :param radio_frequency: radio frequency used in the mobile UL and DL
    :return: FSPL (in db)
    """
    return 20 * math.log10(4 * pi * distance_km * 1000 * radio_frequency / speed_of_light)


def get_nearby_cells(traversing_path_point, cells, acceptable_PL_db, radio_frequency, alpha, beta, gamma, sigma):
    """
    private function to get nearby cells in a given square from the list of cells
    This search function can be replaced by SQL query to return cells around a given point
    """
#    maximum_signal_distance_km = calculate_distance_km_given_fspl(acceptable_FSPL_db, radio_frequency)
    maximum_signal_distance_km = calculate_distance_km_given_pl_abg_nlos(acceptable_PL_db, radio_frequency,
                                                                         alpha, beta, gamma, sigma)
    nearby_cells_in_square = get_nearby_cells_in_square(traversing_path_point, cells, maximum_signal_distance_km)
    nearby_cells = []

    for cell in nearby_cells_in_square:
        distance_km = math.sqrt((cell.get_x() - traversing_path_point.get_x()) ** 2 +
                                (cell.get_y() - traversing_path_point.get_y()) ** 2)

        if distance_km <= maximum_signal_distance_km:
            # path_loss = calculate_fspl_given_distance(distance_km, radio_frequency)
            path_loss = calculate_distance_km_given_pl_abg_nlos(distance_km, radio_frequency, alpha, beta, gamma, sigma)
            cell.add_path_coordinates_and_pl(traversing_path_point, path_loss)
            traversing_path_point.add_available_enodeb(cell, path_loss)
            nearby_cells.append(cell)

    return nearby_cells


def get_nearby_cells_in_square(point, cells, maximum_distance_km):
    """
    get nearby cells based on distance
    :param point: point coordinate on the road
    :param cells: all cells
    :param maximum_distance_km: maximum acceptable distance
    :return: get cells within the coordinates
    """
    nearby_cells_in_square = []
    x1, x2 = point.get_x() - maximum_distance_km, point.get_x() + maximum_distance_km
    y1, y2 = point.get_y() - maximum_distance_km, point.get_y() + maximum_distance_km
    for cell in cells:
        if x1 <= cell.get_x() <= x2 and y1 <= cell.get_y() <= y2:
            nearby_cells_in_square.append(cell)
    return nearby_cells_in_square


def get_max_average_receiving_power_cell(filtered_enodeb_cells):
    """
    Get the best cell serving highest received power at the given path point
    :param filtered_enodeb_cells:
    :return:
    """
    average_received_power = float('-inf')
    best_enodeb_cell = None
    for enodeb in filtered_enodeb_cells:
        if average_received_power < enodeb.get_average_received_power_db():
            average_received_power = enodeb.get_average_received_power_db()
            best_enodeb_cell = enodeb
    return best_enodeb_cell


class ComputeENodeBCellsForPath:

    def __init__(self, path_coordinates, cell_coordinates, transmit_power_db=45, acceptable_FSPL_db=100,
                 radio_frequency=2600000000, alpha=1, beta=0, gamma=1, sigma=0):
        """
        Constructor which calculates the eNodeB cells to be selected in the given vehicle path
        :param path_coordinates: step co-ordinates in vehicles path
        :param cell_coordinates: retrieved list of eNodeB cells in the given path
        :param transmit_power_db: default 45 db
        :param acceptable_FSPL_db: default 100 db
        :param radio_frequency: default 2.6 Ghz
        :param alpha: alpha
        :param beta: beta (in dB)
        :param gamma: gamma
        :param sigma: sigma (in dB)
        """
        self.__cells_for_given_path = set()
        self.__no_cells_point = []
        self.__point_of_handover = []
        self.__average_power_loss_db = 0
        self.__path_coordinates_fspl = []
        self.__transmit_power_db = transmit_power_db

        # Compute the cell selection on the paths list
        self.__compute_cells_for_path_list(path_coordinates, cell_coordinates, acceptable_FSPL_db, radio_frequency,
                                           alpha, beta, gamma, sigma)

    def __compute_cells_for_path_list(self, paths, cell_coordinates, acceptable_FSPL_db, radio_frequency,
                                      alpha=1, beta=0, gamma=1, sigma=0):
        """

        :param paths:
        :param cell_coordinates:
        :param acceptable_FSPL_db:
        :param radio_frequency:
        :param alpha: alpha
        :param beta: beta (in dB)
        :param gamma: gamma
        :param sigma: sigma (in dB)
        :return:
        """
        for path in paths:
            self.__compute_cells_for_given_path(path, cell_coordinates, acceptable_FSPL_db, radio_frequency, alpha,
                                                beta, gamma, sigma)

    def __compute_cells_for_given_path(self, path_coordinates, cell_coordinates, acceptable_FSPL_db, radio_frequency,
                                       alpha, beta, gamma, sigma):
        """
        The main algorithm to calculate the best possible cells for the given path of the vehicle
        get cells for the given path
        :param path_coordinates: point coordinates in the vehicle path
        :param cell_coordinates: nearby cell coordinates on the given vehicular path
        :param acceptable_FSPL_db: acceptable maximum Free Space Path Loss
        :param radio_frequency: Radio frequency used in mobile communication
        """
        old_cells_list = []
        old_filtered_cells_list = []
        new_filtered_cells_list = []
        previous_point = path_coordinates[0]
        # print("---------------------------------------------\nThe algorithm starts here.")
        for index, point in enumerate(path_coordinates):
            current_cells_list = get_nearby_cells(point, cell_coordinates, acceptable_FSPL_db, radio_frequency,
                                                  alpha, beta, gamma, sigma)
            if len(current_cells_list) == 0:
                self.__no_cells_point.append(point)
                if index > 0 and len(old_filtered_cells_list) > 0:
                    self.__cells_for_given_path.add(get_max_average_receiving_power_cell(old_filtered_cells_list))

            # print("***********************************************************")
            # print_cells_at_point("List: ", point, current_cells_list)
            if len(new_filtered_cells_list) > 0:
                new_filtered_cells_list = get_unique_list_of_cells(new_filtered_cells_list, current_cells_list)
                # print("===================================================")
                # print("index: ", index, len(new_filtered_cells_list))
                # print_cells_at_point("Intersection: ", point, new_filtered_cells_list)
                if len(new_filtered_cells_list) == 0:
                    self.__cells_for_given_path.add(get_max_average_receiving_power_cell(old_filtered_cells_list))
                    self.__point_of_handover.append(previous_point)
                    # print_cells("Path cell added: ", list(self.__cells_for_given_path))
                    new_filtered_cells_list = get_unique_list_of_cells(old_cells_list, current_cells_list)
            else:
                new_filtered_cells_list = current_cells_list
            # print("***********************************************************")
            old_cells_list = current_cells_list
            old_filtered_cells_list = new_filtered_cells_list
            previous_point = point

        if len(old_filtered_cells_list) > 0:
            # print_cells("Final Intersection cells: ", old_filtered_cells_list)
            self.__cells_for_given_path.add(get_max_average_receiving_power_cell(old_filtered_cells_list))
            # print("===================================================")
            # print_cells("Path cell added: ", list(self.__cells_for_given_path))
            # print("***********************************************************")

    def get_selected_cells_on_the_path(self):
        """
        :return: get computed cells on the path
        """
        return self.get_sorted_list_enodeb()

    def get_no_signal_points(self):
        """
        :return: get list of point on the path with no signal
        """
        return self.__no_cells_point

    def get_point_of_handover(self):
        """
        :return: get list of all handover points
        """
        return self.__point_of_handover

    def get_average_power_loss_db(self):
        """
        Get average power loss across the path
        :return: average power loss in db
        """
        return self.__average_power_loss_db

    def get_sorted_list_enodeb(self):
        list_to_sort = list(self.__cells_for_given_path)
        return sorted(list_to_sort, key=lambda cell: cell.get_x())
