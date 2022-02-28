import numpy as np
import time
from read import read_file, write_file
from tabulate import tabulate
from compute_score import compute_score
import os


# There is 3 sorts that are nice to test :
# to_start_before, this is the date to start before to be able to have the maximum points.
# average_point_per_days, this is the nbr of point / days that the project requite, may need to compute one with also how many ressources there is
# average_point_per_days_and_contributor
# maybe also the average or min of skill level ?
def sort_project(projects, print_list):
    sorted_projects = sorted(projects, key=lambda k: (k['to_start_before'], -k['average_point_per_days_and_contributor']))
    if print_list:
        header = sorted_projects[0].keys()
        rows = [x.values() for x in sorted_projects]
        print(tabulate(rows, header))
    return sorted_projects


def increase_skill_contributor(contributor, skill_name, skill_level):
    if 'SergeyU' == contributor['name']:
        print("Increase skill " +skill_name+"for contributor"+ contributor['name'] + " (skill level needed was " + str(skill_level) )

    if skill_name in contributor['skills'] and contributor['skills'][skill_name] <= skill_level:
        contributor['skills'][skill_name] = int(contributor['skills'][skill_name]) + 1
    elif skill_name not in contributor['skills']:
        contributor['skills'][skill_name] = 1


def test_if_contributor_can_be_mentored(contributor, skill_name, skill_level):
    for skill_name_val, skill_level_var in contributor['skills'].items():
        if skill_name_val == skill_name and \
                int(skill_level_var) == int(skill_level) - 1:
            return True
    if skill_level == 1:
        return True
    return False

def look_for_worst_contributor(skill_name, skill_level, contributors, other_skill_needed):
    list_possible_contributor = []
    for contributor in contributors:
        if test_if_contributor_can_be_mentored(contributor, skill_name, skill_level):
            compute_value_contributor(contributor)
            list_possible_contributor.append(contributor)
    if len(list_possible_contributor) == 0:
        return look_for_best_contributor_skill(skill_name, skill_level, contributors, other_skill_needed, False)
    else:
        list_possible_contributor_sorted = sorted(list_possible_contributor, key=lambda k: (k['average_skill_level']))
        best_candidate = list_possible_contributor_sorted[0]
        #print("Candidate will be mentored : " + best_candidate['name'] + " for the skill : " + skill_name + ", level  " + str(skill_name))
        #header = list_possible_contributor_sorted[0].keys()
        #rows = [x.values() for x in list_possible_contributor_sorted]
        #print(tabulate(rows, header))
        contributors.remove(best_candidate)
        return best_candidate


#to be able to select the bext contributor we want, we need to have some input, like to filter on the number of skill he has, the min, average, etc
def compute_value_contributor(contributor):
    contributor['nbr_skill'] = len(contributor['skills'])
    contributor['can_mentor'] = 0  # when a user is candidate, we can reset the can_mentor score
    sum_skill_level = 0
    for skill_name, skill_level in contributor['skills'].items():
        sum_skill_level = int(sum_skill_level) + int(skill_level)
    contributor['sum_skill_level'] = sum_skill_level
    contributor['average_skill_level'] = sum_skill_level


def look_for_best_contributor_skill(skill_name, skill_level, contributors, other_skill_needed, print_list):
    list_possible_contributor = []

    for contributor in contributors:
        if skill_name in contributor['skills'] and contributor['skills'][skill_name] >= skill_level:
            # It has the skill necessary for doing the jobs, and now we check if he can mentor as well !
            compute_value_contributor(contributor)
            for other_skill in other_skill_needed:
                if other_skill['name'] != skill_name and other_skill['name'] in contributor['skills'] and contributor['skills'][other_skill['name']] >= other_skill['level']:
                    # Success
                    #print(contributor['name'] + " can mentor " + other_skill_name)
                    if 'can_mentor' in contributor:
                        contributor['can_mentor'] = contributor['can_mentor'] + 1
                        #print("user" + contributor['name'] + " can mentor " + other_skill['name'])
            list_possible_contributor.append(contributor)
    if len(list_possible_contributor) == 0:
        return None
    else:
        list_possible_contributor_sorted = sorted(list_possible_contributor, key=lambda k: (k['skills'][skill_name], -k['can_mentor'], k['average_skill_level']))
        if print_list:
            header = list_possible_contributor_sorted[0].keys()
        rows = [x.values() for x in list_possible_contributor_sorted]
        #print("Skill needed by project : ")
        #print(other_skill_needed)
        #print("User available")
        #print(tabulate(rows, header))
        best_candidate = list_possible_contributor_sorted[0]
        contributors.remove(best_candidate)
        return best_candidate


# tab_file = ["a.txt","b.txt","c.txt","d.txt","e.txt","f.txt"]
tab_file = [
#    "a_an_example.in.txt",
#    "b_better_start_small.in.txt",
    "c_collaboration.in.txt",
    "d_dense_schedule.in.txt",
    "e_exceptional_skills.in.txt",
    "f_find_great_mentors.in.txt"
]
for file in tab_file:
    start_time = time.time()
    input_folder = "input"
    name_file = file
    projects_done = []
    projects_in_progress = []
    contributors, projects_to_do, list_max_skill_needed, max_iteration = read_file(os.path.join(input_folder, name_file))
    projects_sorted = sort_project(projects_to_do, False)

    iteration = 0
    print("ProjectDone " + str(len(projects_done)))
    print("ProjectInProgress " + str(len(projects_in_progress)))
    print("ProjectToDo " + str(len(projects_sorted)))
    print("iteration " + str(iteration))
    print("contributor available " + str(len(contributors)))
    string_progress = str(len(projects_done)) + "-" + str(len(projects_in_progress)) + "-" + str(len(projects_sorted)) + "-"+ str(len(contributors))
    string_progress_end = ""
    while iteration < max_iteration + 5 or len(projects_to_do) == 0:
        if iteration % 1000 == 0:
            print("ProjectDone " + str(len(projects_done)))
            print("ProjectInProgress " + str(len(projects_in_progress)))
            print("ProjectToDo " + str(len(projects_sorted)))
            print("iteration " + str(iteration))
            print("contributor available " + str(len(contributors)))

        for project_in_progress in list(projects_in_progress):
            if iteration >= project_in_progress['final_date']:
                # Once a project is finished, we had back the contributor in the available one
                projects_done.append(project_in_progress)
                projects_in_progress.remove(project_in_progress)
                for contributor in project_in_progress['contributors']:
                    contributors.append(contributor)
        string_progress = str(len(projects_done)) + "-" + str(len(projects_in_progress)) + "-" + str(len(projects_sorted)) + "-"+ str(len(contributors))
        if string_progress == string_progress_end:
            iteration = iteration + 1
            continue

        for project_sort in list(projects_sorted):
            if (int(project_sort['best_before']) + int(project_sort['score'])) < iteration:
                projects_sorted.remove(project_sort)
                print("Remove : " + project_sort['name'] + " because he can no longer bring any points")
            else:
                skills_sorted = sorted(project_sort['skills'],  key=lambda k: (k['level']))
                #print(skills_sorted)
                skill_left_needed = list(skills_sorted)
                project_contributors = []
                possible_contributor_by_skill = []
                found_all_contributor = True
                skill_to_mentor = {}
                for skill in project_sort['skills']:
                    best_candidate = None
                    if 'DocsNextv2' == project_sort['name']:
                        print("Looking for skill " + skill['name'])

                    skill_name = skill['name']
                    if skill_name in skill_to_mentor and \
                            skill_to_mentor[skill['name']] >= skill['level']:
                        # we can take a bad guy
                        if 'DocsNextv2' == project_sort['name']:
                            print("This skill has a mentor")
                            print(possible_contributor_by_skill)
                        best_candidate_name = look_for_worst_contributor(skill['name'], skill['level'], contributors, skill_left_needed)
                    else:
                        if 'DocsNextv2' == project_sort['name']:
                            print("Looking for user with enough level : ")
                        best_candidate_name = look_for_best_contributor_skill(skill['name'], skill['level'], contributors, skill_left_needed, False)
                        if 'DocsNextv2' == project_sort['name']:
                            print(best_candidate_name)
                    if best_candidate_name is not None:
                        #print(skill_left_needed)
                        #print("we found the best candidate for skill " + skill['name'] + " that  " + best_candidate_name['name'])
                        possible_contributor_by_skill.append(best_candidate_name)
                        skill_left_needed.pop(0)
                        for contributor_skill_name, contributor_skill_level in best_candidate_name['skills'].items():
                            for skill_bis in project_sort['skills']:
                                if skill_bis['name'] == contributor_skill_name \
                                        and contributor_skill_level >= skill_bis['level']:
                                    if contributor_skill_name not in skill_to_mentor or contributor_skill_level > skill_to_mentor[contributor_skill_name]:
                                        skill_to_mentor[contributor_skill_name] = contributor_skill_level
                    else:
                        #print("No contributor found for the project")
                        found_all_contributor = False

                if found_all_contributor:
                    project_contributors = []

                    for idx, contributor in enumerate(possible_contributor_by_skill):
                        increase_skill_contributor(contributor, project_sort['skills'][idx]['name'], project_sort['skills'][idx]['level'])
                        project_contributors.append(contributor)
                    project_sort['final_date'] = int(iteration) + int(project_sort['nbr_days'])
                    project_sort['contributors'] = project_contributors
                    projects_sorted.remove(project_sort)
                    projects_in_progress.append(project_sort)
                else:
                    for contributor in possible_contributor_by_skill:
                        contributors.append(contributor)
        iteration = iteration + 1
        string_progress_end = str(len(projects_done)) + "-" + str(len(projects_in_progress)) + "-" + str(len(projects_sorted)) + "-"+ str(len(contributors))

    write_file(file, projects_done)
#
#
#
#    print("duration algo = ", time.time() - start_time)
#