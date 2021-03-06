import numpy as np
import time
from read import read_file, write_file
from compute_score import find_waiting_time, car_timings, compute_score
import os


input_folder = "input"
name_file = "d.txt"
streets, cars, duration, nb_inters, nb_streets, nb_cars, bonus = read_file(os.path.join(input_folder, name_file))
duration = int(duration)
nb_inters= int(nb_inters)
bonus = int(bonus)

list_cars = cars

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


def build_dict_inters_car_list(list_cars, streets, schedule):
    inters_car_list = {}
    for car in list_cars:
        timings = car_timings(car, schedule=schedule, streets=streets)

        for timing in timings[:-1]:
            inter=timing[1]
            street= timing[0]
            if inter not in inters_car_list:
                inters_car_list[inter] = {}
            if street not in inters_car_list:
                inters_car_list[inter][street] = [timing[2]]
            else:
                inters_car_list[inter][street].append(timing[2])

    return inters_car_list





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


#
# def find_best_schedule(street_to_arrival_times_map: dict):
#     street_names = street_to_arrival_times_map.keys()
#
#
#     generated_schedule = np.ones(street_names)
#
#     for street in street_names:
#         alea = np.random.randint(5)
#
#
#



























start_time = time.time()
# print("time starting build_dict_inters_car = ", start_time)
full_dict_inters_car = build_dict_inters_car(list_cars, streets)
print("duration build_dict_inters_car = ", time.time()-start_time)
start_time = time.time()
dict_schedule_solution = build_dummy_schedule(full_dict_inters_car)
print("duration build_dummy_schedule = ", time.time()-start_time)

print("dict_schedule_solution = ", dict_schedule_solution)

score =compute_score(cars,dict_schedule_solution,streets,bonus,duration)
print("hey score", score)

print("hey dict arrivals")
print(build_dict_inters_car_list(list_cars, streets, dict_schedule_solution))






write_file(name_file, dict_schedule_solution)
