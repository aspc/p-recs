import ast

def clean_course_info(df):
    format_instructors(df)
    create_schedule(df)

def format_instructors(df):
	def join_faculty(row):
		faculty = list(row['Faculty'])
		return "; ".join(faculty)
	df["Faculty"] = df.apply(join_faculty, axis=1)
  
def create_schedule(df):
	def join_weekdays_meetimes(row):
		weekdays = row['Weekdays']
		meettimes = row['MeetTime']
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
			str_weekdays = ''.join(str(x) for x in row['Weekdays'])
			str_meetdays = ''.join(str(x) for x in row['MeetTime'])

			return "Format Error: " + str_weekdays + " " + str_meetdays

	df["Schedule"] = df.apply(join_weekdays_meetimes, axis=1)
    