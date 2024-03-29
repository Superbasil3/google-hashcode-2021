import numpy as np
import time
from read import read_file, write_file, write_file_normer
from compute_score import compute_score
import os


def compute_length_path_car(list_cars, streets):
    tab_time_cars = []
    for car in list_cars:
        total_time = 0
        for street_name in car[1:]:
            time_travel_street = streets[street_name][2]
            total_time += time_travel_street
        tab_time_cars.append(total_time)
    return np.array(tab_time_cars)

def compute_length_path_car_with_solution(list_cars, streets, dict_schedule_solution):
    tab_time_cars = []
    for car in list_cars:
        total_time = 0
        for ind_street_name in range(len(car)):
            street_name = car[ind_street_name]
            id_inters_end_street = streets[street_name][1]
            if ind_street_name > 0:
                time_travel_street = streets[street_name][2]
                total_time += time_travel_street
            if id_inters_end_street in dict_schedule_solution:
                current_dict_inters = dict_schedule_solution[id_inters_end_street]
                magic_number_wait = 0.05
                total_time += magic_number_wait*len(current_dict_inters)

        tab_time_cars.append(total_time)
    return np.array(tab_time_cars)

def build_dict_inters_car(list_cars, streets):
    full_dict_inters_car = {}
    for car in list_cars:
        for street_name in car[:-1]:
            id_inters_end_street = streets[street_name][1]
            if not id_inters_end_street in full_dict_inters_car:
                full_dict_inters_car[id_inters_end_street] = {}
            if street_name in full_dict_inters_car[id_inters_end_street]:
                full_dict_inters_car[id_inters_end_street][street_name] += 1
            else:
                full_dict_inters_car[id_inters_end_street][street_name] = 1

    return full_dict_inters_car

# def compute_schedule(dict_dict_street_time_arrived, schedule_inters):


def build_dummy_schedule(full_dict_inters_car):

    dict_schedule_solution = {}
    for inters in full_dict_inters_car.keys():
        tab_nb_car = []
        list_name_street = list(full_dict_inters_car[inters].keys())
        for name_street in list_name_street:
            current_nb_car = full_dict_inters_car[inters][name_street]
            tab_nb_car.append(current_nb_car)

        minimum_nb_car = np.min(tab_nb_car)
        tab_nb_car_normalized = tab_nb_car/minimum_nb_car
        schedule = tab_nb_car_normalized.astype(np.int32)
        assert len(schedule) == len(list_name_street)
        dict_schedule_solution[inters] = []
        for ind_schedule in range(len(schedule)):
            current_street_name = list_name_street[ind_schedule]
            current_time_schedule = schedule[ind_schedule]
            dict_schedule_solution[inters].append((current_street_name, current_time_schedule))

    return dict_schedule_solution

#tab_file = ["a.txt","b.txt","c.txt","d.txt","e.txt","f.txt"]
tab_file = ["a.txt"]
for file in tab_file:
    input_folder = "input"
    name_file = file
    streets, cars, duration, nb_inters, nb_streets, nb_cars, bonus = read_file(os.path.join(input_folder, name_file))
    duration = int(duration)
    list_cars = cars
    print("duration = ", duration)
    start_time = time.time()
    # print("time starting build_dict_inters_car = ", start_time)
    tab_time_cars = compute_length_path_car(list_cars, streets)
    indice_cars_usefull = np.where(tab_time_cars <= duration)[0]
    list_cars_usefull = [list_cars[indice_car_usefull] for indice_car_usefull in indice_cars_usefull]

    full_dict_inters_car = build_dict_inters_car(list_cars_usefull, streets)
    print("duration build_dict_inters_car = ", time.time()-start_time)
    start_time = time.time()
    dict_schedule_solution = build_dummy_schedule(full_dict_inters_car)
    print("duration build_dummy_schedule = ", time.time()-start_time)

    nb_iter = 0
    for iter in range(nb_iter):
        tab_time_cars_with_solution = compute_length_path_car_with_solution(list_cars_usefull, streets, dict_schedule_solution)

        indice_cars_usefull = np.where(tab_time_cars_with_solution <= duration)[0]
        list_cars_usefull = [list_cars_usefull[indice_car_usefull] for indice_car_usefull in indice_cars_usefull]

        full_dict_inters_car = build_dict_inters_car(list_cars_usefull, streets)
        print("duration build_dict_inters_car = ", time.time() - start_time)
        start_time = time.time()
        dict_schedule_solution = build_dummy_schedule(full_dict_inters_car)
        print("duration build_dummy_schedule = ", time.time() - start_time)

    # print("dict_schedule_solution = ", dict_schedule_solution)
    write_file(name_file, dict_schedule_solution)
