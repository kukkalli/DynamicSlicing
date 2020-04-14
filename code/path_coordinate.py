"""
The class ENOdeBCell which extends class Point and holds FSPL values
"""
from code.point import Point


class PathCoordinate(Point):
    def __init__(self, x=0.0, y=0.0, _uuid="", reachable_enodeb_cells={},
                 selected_enodeb_received_power_db=float('-inf'), selected_enodeb_cell=None, has_coverage=False):
        Point.__init__(self, x, y, _uuid)
        self.__reachable_enodeb_cells = reachable_enodeb_cells
        self.__selected_enodeb_received_power_db = selected_enodeb_received_power_db
        self.__selected_enodeb_cell = selected_enodeb_cell
        self.__has_coverage = has_coverage

    def add_available_enodeb(self, enodeb, fspl):
        """
        Add ENodeB to list of reachable ENodeB cells with its received power
        :param enodeb:
        :param fspl:
        :return:
        """
        self.__reachable_enodeb_cells.update({str(enodeb.get_uuid()): {'enodeb': enodeb, 'fspl': fspl}})

    def set_selected_enodeb_cell(self, selected_enodeb_cell):
        """
        Set selected eNodeB
        :param selected_enodeb_cell:
        :return:
        """
        self.__selected_enodeb_cell = selected_enodeb_cell
        self.__selected_enodeb_received_power_db = selected_enodeb_cell.get_transmit_power_db() \
                                                   - self.get_fspl_from_selected_enodeb()

    def get_selected_enodeb_cell(self):
        """
        Get selected eNodeB
        :return:
        """
        return self.__selected_enodeb_cell

    def get_fspl_from_selected_enodeb(self):
        """
        Get FSPL from selected ENodeB
        :return:
        """
        print('FSPL from selected ENodeB: ',
              self.__reachable_enodeb_cells[str(self.get_selected_enodeb_cell().get_uuid())]['fspl'])
        return self.__reachable_enodeb_cells[str(self.get_selected_enodeb_cell().get_uuid())]['fspl']

    def get_received_power_db(self, enodeb):
        """
        Get received power in db at this path coordinate
        :return:
        """
        return enodeb.get_transmit_power_db() - self.__reachable_enodeb_cells[str(enodeb.get_uuid())]['fspl']

    def set_has_coverage(self):
        """
        Set this point has at least one cell to offer service
        """
        self.__has_coverage = True

    def has_coverage(self):
        """
        Return if this point coordinate has acceptable mobile network coverage
        :return:
        """
        return self.__has_coverage

    def copy(self):
        """
        Copy a given Point
        :return:
        """
        return PathCoordinate(self.__x, self.__y, self.__uuid, self.__reachable_enodeb_cells,
                              self.__selected_enodeb_received_power_db, self.__selected_enodeb_cell,
                              self.__has_coverage)

    def __str__(self):
        """
        Convert ENodeBCell object to string
        :return: string
        """
        return "Path has (x:" + str(self.get_x()) + ", y: " + str(self.get_y()) + "), UUID: "\
               + str(self.get_uuid()) + ", Rx (db): " + str(self.__selected_enodeb_cell)
