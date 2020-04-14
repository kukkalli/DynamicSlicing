"""
The class ENOdeBCell which extends class Point and holds PL values
"""
from code.point import Point
from code.path_coordinate import PathCoordinate


class GNodeBCell(Point):
    def __init__(self, x, y, transmit_power_db=45, _uuid="", load=0, operator_id="", operator_name="Network Provider",
                 path_coordinates=[], selected=False):
        Point.__init__(self, x, y, _uuid)
        self.__transmit_power_db = transmit_power_db
        self.__load = load
        self.__operator_id = operator_id
        self.__operator_name = operator_name
        self.__path_coordinates = path_coordinates
        self.__selected = selected

    def add_path_coordinates_and_pl(self, path_coordinate: PathCoordinate, pl):
        """
        Add path coordinate and its relative PL from the cell
        :param path_coordinate:
        :param pl:
        :return:
        """
        self.__path_coordinates.append({'path_coordinate': path_coordinate, 'pl': pl})

    def get_average_received_power_db(self):
        """
        Get average of
        :return:
        """
        sum_of_path_loss = 0
        for coordinate in self.__path_coordinates:
            sum_of_path_loss = sum_of_path_loss + coordinate['pl']
        return round(self.get_transmit_power_db() - (sum_of_path_loss / len(self.__path_coordinates)), 3)

    def set_transmit_power_db(self, transmit_power_db):
        """
        Set transmit Power of the ENodeB
        :param transmit_power_db:
        """
        self.__transmit_power_db = transmit_power_db

    def get_transmit_power_db(self):
        """
        Get transmit Power in db
        :return:
        """
        return self.__transmit_power_db

    def set_selected(self):
        """
        Set the ENodeB has been selected
        :return:
        """
        self.__selected = True

    def is_selected(self):
        """
        Return True if the ENodeB has been selected
        :return:
        """
        return self.__selected

    def copy(self):
        """
        Copy the given gNodeB cell
        :return:
        """
        return GNodeBCell(self.__x, self.__y, self.__transmit_power_db, self.__uuid, self.__load,
                          self.__operator_id, self.__operator_name, self.__path_coordinates,
                          self.__selected)

    def __str__(self):
        """
        Convert ENodeBCell object to string
        :return: string
        """
        return "ENodeBCell of " + self.__operator_name + " has (x:" + str(self.get_x()) + ", y: " + str(self.get_y())\
               + "), UUID: "\
               + str(self.get_uuid()) + ", Tx (db): " + str(self.__transmit_power_db)
