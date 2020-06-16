import matplotlib.pyplot as plt

from code.search_nearby_cells import ComputeENodeBCellsForPath
from code.search_nearby_cells import calculate_pl_abg_nlos, calculate_distance_km_given_pl_abg_nlos
from code.search_nearby_cells import print_path_coordinates
from code.cells_list import GenerateRandomPathData
from code.path_coordinate import PathCoordinate
import numpy as np

# start point of the travel
hospital_location = PathCoordinate(0, 0)
# Seed value for repetition
seed_value = 19841101
# seed_value = 19890111
# seed_value = 20200131
# Transmit Power on ENodeB cell
transmit_power_db = 45

# vehicle travel distance
total_travel_distance = 25
# Number of vehicle paths
path_count = 20
# Maximum distance of travel
max_distance = 15.0
# travelling path's step distance
step_distance = 0.250
# Minimum distance of travel
min_distance = 5.0

# Solution selection
# selection = "DYSOLVE"
selection = "Baseline"

# max acceptable path loss in dB
max_path_loss_db = 135
# Radio operating frequency in Hz
radio_frequency = 2600000000
# alpha, beta, gamma and sigma values for
alpha = 3.6
beta = 7.4
gamma = 2.4
sigma = 8.9

# distance_km = 1

# print("PL_ABG_NLOS: ", calculate_pl_abg_nlos(distance_km, radio_frequency, alpha, beta, gamma, sigma))
# print("Distance: ", calculate_distance_km_given_pl_abg_nlos(135, radio_frequency, alpha, beta, gamma, sigma))
# print(calculate_distance_km_given_fspl(max_path_loss_db, radio_frequency))
# print(calculate_fspl_given_distance(0.9, radio_frequency))

path_generator = GenerateRandomPathData(hospital_location, seed_value)

path_generator.generate_multiple_paths(path_count, max_distance, step_distance, min_distance)
all_paths = path_generator.get_paths_list()

# generate random path
# path_generator.generate_path_data(total_travel_distance, step_distance)
# path_coordinates = path_generator.get_generated_path()
# path_x_coordinate = [point.get_x() for point in path_coordinates]
# path_y_coordinate = [point.get_y() for point in path_coordinates]

# Network Provider A
# Max radius of random cell location creation
cell_max_radius_p_a = 1
# density of cells
cell_density_p_a = 0.20
operator_id_001 = "001"
operator_name_001 = "Network Provider A"
cell_coordinates_provider_a = path_generator.generate_random_cells_data_for_path_list(all_paths,
                                                                                      cell_max_radius_p_a,
                                                                                      cell_density_p_a,
                                                                                      transmit_power_db,
                                                                                      operator_id_001,
                                                                                      operator_name_001)

print("provider A cells count: ", len(cell_coordinates_provider_a))
# cell_coordinates = path_generator.get_random_cells_list()
cell_x_coordinate_a = [cell.get_x() for cell in cell_coordinates_provider_a]
cell_y_coordinate_a = [cell.get_y() for cell in cell_coordinates_provider_a]

# Network Provider 2
# Max radius of random cell location creation
cell_max_radius_p_b = 1
# density of cells
cell_density_p_b = 0.20
operator_id_002 = "002"
operator_name_002 = "Network Provider B"
cell_coordinates_provider_b = path_generator.generate_random_cells_data_for_path_list(all_paths,
                                                                                      cell_max_radius_p_b,
                                                                                      cell_density_p_b,
                                                                                      transmit_power_db,
                                                                                      operator_id_002,
                                                                                      operator_name_002)

print("provider B cells count: ", len(cell_coordinates_provider_b))
# cell_coordinates = path_generator.get_random_cells_list()
cell_x_coordinate_b = [cell.get_x() for cell in cell_coordinates_provider_b]
cell_y_coordinate_b = [cell.get_y() for cell in cell_coordinates_provider_b]

cell_coordinates = np.concatenate((cell_coordinates_provider_a, cell_coordinates_provider_b))
# print_cells("cells: ", cell_coordinates)

# Create object for GetCellsForPath

selected_cells_for_path = []
if selection == "DYSOLVE":
    calculate = ComputeENodeBCellsForPath(all_paths, cell_coordinates, transmit_power_db, max_path_loss_db,
                                          radio_frequency, alpha, beta, gamma, sigma)
    selected_cells_for_path = calculate.get_selected_cells_on_the_path()
    cells_for_print = selected_cells_for_path
else:
    calculate = ComputeENodeBCellsForPath(all_paths, cell_coordinates_provider_a, transmit_power_db, max_path_loss_db,
                                          radio_frequency, alpha, beta, gamma, sigma)
    selected_cells_for_path = cell_coordinates_provider_a  # calculate.get_selected_cells_on_the_path()
    cells_for_print = calculate.get_selected_cells_on_the_path()

selected_cells_x_coordinate = [cells.get_x() for cells in selected_cells_for_path]
selected_cells_y_coordinate = [cells.get_y() for cells in selected_cells_for_path]

print("Selected number of cells: ", len(selected_cells_for_path))
# print_cells("Average serving received power by each ENodeB cell: ", cells_for_print)

no_signal_points = calculate.get_no_signal_points()
# print_path_coordinates("no_signal_points: ", no_signal_points)
no_signal_points_x_coordinate = [point.get_x() for point in no_signal_points]
no_signal_points_y_coordinate = [point.get_y() for point in no_signal_points]
print("No signal points: ", len(no_signal_points))


point_of_handover = calculate.get_point_of_handover()
# print_path_coordinates("point_of_handover: ", point_of_handover)
point_of_handover_x_coordinate = [point.get_x() for point in point_of_handover]
point_of_handover_y_coordinate = [point.get_y() for point in point_of_handover]

# Plot the graph
# fig = plt.figure()
# frequency_text = '3.6 GHz'
# if radio_frequency == 2600000000:
#     frequency_text = '2.6 GHz'
frequency_text = '2.6 GHz' if radio_frequency == 2600000000 else '3.6 GHz'
plt.figure(figsize=[16, 9])
plt.title("Cell Selection using " + selection + " (Freq.: " + frequency_text + ")", fontsize=30, fontweight='bold')

# Plot axes label
ax = plt.gca()
ax.set_aspect('equal', adjustable='box')
ax.set_xlabel(r'x-distance (km)', fontsize=20, labelpad=0, fontweight='bold')
ax.set_ylabel(r'y-distance (km)', fontsize=20, labelpad=0, rotation=90, fontweight='bold')

# Plot the grid
plt.grid(b=True, which='major', color='#666666', linestyle='-')
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

number_of_points = 0
for i, l in enumerate(all_paths):
    # print_path_coordinates(str(i) + ": ", l)
    number_of_points = number_of_points + len(l)
    l_x_coordinate = [point.get_x() for point in l]
    l_y_coordinate = [point.get_y() for point in l]
    plt.plot(l_x_coordinate, l_y_coordinate, 'black', label='Path of the Vehicle', linewidth=1, )

print("number of kilometers: ", (number_of_points - len(all_paths)))

# Plot the path of the vehicle
# plt.plot(path_x_coordinate, path_y_coordinate, 'black', label='Path of the Vehicle', linewidth=2, )

# Plot the selected cells
plt.scatter(selected_cells_x_coordinate, selected_cells_y_coordinate, c='#e58b88', s=150, label='Selected Cells')

# Plot the no coverage points
plt.scatter(no_signal_points_x_coordinate, no_signal_points_y_coordinate, c='red', s=100,
            label='No availability of Cells')

# Plot handover points
if selection == "DYSOLVE":
    plt.scatter(point_of_handover_x_coordinate, point_of_handover_y_coordinate, c='green', marker='x', s=50,
                label='Point of handover')

# Plot Network Provider 1
plt.scatter(cell_x_coordinate_a, cell_y_coordinate_a, s=40, c='blue', label=operator_name_001)
# plot Network Provider 2
plt.scatter(cell_x_coordinate_b, cell_y_coordinate_b, s=40, c='#a02c2d', label=operator_name_002)

# Plot legend
# plt.legend(prop={"size": 20, "weight": 'bold'})

# plt.ylim(-5, 5)
# plt.xlim(20, 25)

# Show plot
# plt.show()

filename = selection + "_" + frequency_text.replace('.', ',').replace(' ', '') + "_" \
           + str(cell_density_p_a).replace('.', ',') \
           + "_" + str(cell_density_p_b).replace('.', ',') + ".pdf"

plt.savefig("../images/" + filename, bbox_inches='tight')
