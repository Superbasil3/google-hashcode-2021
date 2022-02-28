
def read_file(filename):
    with open(filename, 'r') as f:
        nbr_contributors, nbr_projects = f.readline().rstrip("\n").split(' ')

        contributors = []
        for i in range(int(nbr_contributors)):
            contributor = {}
            name, nbr_skill = f.readline().rstrip("\n").split(' ')
            skills = {}
            for j in range(int(nbr_skill)):
                name_skill, level_skill = f.readline().rstrip("\n").split(' ')
                skills[name_skill] = int(level_skill)
            contributor['name'] = name
            contributor['skills'] = skills
            contributor['can_mentor'] = 0  # is computed later, juste to have default value
            contributors.append(contributor)

        projects = []
        list_max_skill_needed = {}
        #max_time_to_do is the max iteration in order to have any point. This is the max of ( best_before + score )
        max_iteration = 0
        for i in range(int(nbr_projects)):
            project = {}
            project_name, nbr_days, score, best_before, nbr_roles = f.readline().rstrip("\n").split(' ')
            skills = []
            for j in range(int(nbr_roles)):
                skill = {}
                name_skill, level_needed = f.readline().rstrip("\n").split(' ')
                skill['name'] = name_skill
                skill['level'] = int(level_needed)
                skills.append(skill)
            project['nbr_days'] = int(nbr_days)
            project['score'] = int(score)
            project['best_before'] = int(best_before)
            project['to_start_before'] = int(best_before) - int(nbr_days)
            project['average_point_per_days'] = float(score) / float(nbr_days)
            project['average_point_per_days_and_contributor'] = float(score) / float(nbr_days) / float(nbr_roles)
            project['skills'] = skills
            project['name'] = project_name
            if (int(best_before) + int(score)) > max_iteration:
                max_iteration = int(best_before) + int(score)
            projects.append(project)
        print("max_iteration" + str(max_iteration))
        return contributors, projects, list_max_skill_needed, max_iteration

def write_file(filename, projects):
    with open("output/{0}".format(filename), 'a') as the_file:
        the_file.truncate(0)
        the_file.write("{0} \n".format(len(projects))) # nbr projects done
        for project in projects:
            the_file.write("{0} \n".format(project['name'])) # name project

            list_contributor_name = []
            for contributor in project['contributors']:
                list_contributor_name.append(contributor['name'])
            the_file.write("{0} \n".format((' ').join(list_contributor_name))) # list contributors










