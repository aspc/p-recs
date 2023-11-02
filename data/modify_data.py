import ast

def clean_course_info(df):
    format_instructors(df)
    create_schedule(df)

def format_instructors(df):
	def join_faculty(row):
		faculty = ast.literal_eval(row['Faculty'])
		return "; ".join(faculty)
	df["Faculty"] = df.apply(join_faculty, axis=1)
  
def create_schedule(df):
	def join_weekdays_meetimes(row):
		weekdays = ast.literal_eval(row['Weekdays'])
		meettimes = ast.literal_eval(row['MeetTime'])
		# Check if the lengths of both lists are the same
		if len(weekdays) == len(meettimes):
			combined_data = []
			for i in range(len(weekdays)):
				combined_string = weekdays[i] + " " + meettimes[i]
				combined_data.append(combined_string)
			return "\n".join(combined_data)
		# Often To be arranged
		elif len(meettimes) == 1 and weekdays[0] == []:
			return meettimes[0]
		else:
			return "Format Error: " + row['Weekdays'] + row['MeetTime']

	df["Schedule"] = df.apply(join_weekdays_meetimes, axis=1)
    