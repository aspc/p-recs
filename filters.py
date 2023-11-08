def get_filters(course_area, campus_list, selected_days):
    filters = []
    filters.append(course_area)
    filters.append(set_campus(campus_list))
    filters.append(set_days(selected_days))
    return filters

def set_days(selected_days):
    days = ['M', 'T', 'W', 'R', 'F']
    selected_days = set(selected_days)
    days_is_checked = []
    for day in days:
        if day in selected_days:
            days_is_checked.append("1")
        else:
            days_is_checked.append("0")
    return days_is_checked

def set_campus(campus_list):
    campuses = ['PO Campus', 'CM Campus', 'HM Campus', 'SC Campus', 'PZ Campus']
    campus_list = set(campus_list)
    campus_is_checked = []
    for campus in campuses:
        if campus in campus_list:
            campus_is_checked.append("1")
        else:
            campus_is_checked.append("0")
    return campus_is_checked