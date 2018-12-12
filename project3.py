from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import getpass
import datetime

def connect():
    db_config = read_db_config()

    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            print('connection established.')
        else:
            print('connection failed.')

    except Error as error:
        print(error)
    return conn




#######################################################################
###########           Notes                             ###############
## 1. No need to call Student menu from subsections explicitely.    ###
##    Automatic return is implemented with while loop               ###
## 2. SQL commands are yet to be written                            ###
#######################################################################

class UserClass:
	def __init__(self,cursor,conn,credentials):
		self.username   = credentials[0]
		self.stdnt_name = credentials[1]
		self.password   = credentials[2]
		self.cursor     = cursor
		self.conn	= conn

	def student_menu(self):
		print ('\n\n~~~~~~~~~~~~~~\n\nStudent Menu\n')
		tryoptions  = True
		while tryoptions:
			print ('Current Courses: \n ------------')
			print ('\n'.join(['\t'.join(item) for item in self.current_courses()]))
			print ('------------ \n\n')
			onscreen = 	'Menu Options \n ------ \n \
					Transcript 	\t 1 \n \
					Enroll		\t 2 \n \
                                        Withdraw        \t 3 \n \
					Personal Info 	\t 4 \n \
					Logout 		\t 0 \n'
			choice   = inputit(onscreen)
			if not choice	: 	tryoptions = False
			elif choice == 1:	self.Transcript()
			elif choice == 2:	self.Enroll()
                        elif choice == 3:       self.Withdraw()
			elif choice == 4:	self.Details()
			else		:	print ('Invalid option. Try again.')

	def current_courses(self):
		dt = datetime.datetime.now()
		cQ = int(round((dt.month-1)/3)+2)
                if cQ>4: cQ-=4
                cQ='Q'+str(cQ)

		sql_script =    'select UoSCode, UoSName from  unitofstudy \
				where UoSCode IN (select distinct UoSCode \
							from transcript \
							where StudId='+str(self.username)+ \
       							' and Semester="'+cQ+ \
        						'" and Year='+str(dt.year)+')'
		self.cursor.execute(sql_script)
		return self.cursor.fetchall()

	def Enroll(self):

		dt = datetime.datetime.now()
		cQ = int(round((dt.month-1)/3)+2)
		nQ = cQ + 1
		if cQ>4: cQ-=4
		if nQ>4: nQ-=4
		cQ='Q'+str(cQ)
		nQ='Q'+str(nQ)
		cYear  = dt.year
		if nQ == "Q2": nYear = dt.year+1
		else: 	dt.year

		sql_script = 'select * from uosoffering\
				where ((Semester="'+cQ+'" and Year='+str(cYear)+') or\
					Semester="'+nQ+'" and Year='+str(nYear)+')'
		self.cursor.execute(sql_script)
		offered_courses = self.cursor.fetchall()
		print('Listing the offered Courses in this quarter and next')
		print('CourseIndex\tCourseCode\tSemester\tYear\tText\tEnrolled\tMaxEnroll\tInstructorID')
		for i,item in enumerate(offered_courses):
			item = [str(jtem) for jtem in item]
			print (str(i+1))+'\t'+'\t'.join(item)
		transcript = self.Transcript(return_courses=True)

		enroll_options = True
		while enroll_options:
			onscreen =      'Options \n ------ \n \
                                         Enter course index number for enrollment \n \
                                         Enter 0 for returning to Student Menu'
			course_idn 	= inputit(onscreen)
			
        		if course_idn <= len(offered_courses) and course_idn>0:
				course_code 	= offered_courses[course_idn-1][0]
				courseQ  	= offered_courses[course_idn-1][1]
				courseY		= offered_courses[course_idn-1][2]
				args 	= (self.username,course_code,courseQ,courseY,0)

				try:
	                		enroll_error = self.cursor.callproc('Check_Enroll',args)[-1]
					if not enroll_error:
						try:
							_ = self.cursor.callproc('Enroll_Student',args)
							self.conn.commit()
							print('Enrolled successfully')
						except:
							self.conn.rollback() 
							print('Eligible to enroll. But some internal error occurred')
					elif enroll_error == 1:
						print('The student has already enrolled/finished/failed this course. Cannot enroll')
					elif enroll_error == 2:
						print('Course is full. Cannot enroll')
					elif enroll_error == 3:
						print('Some prerequisite conditions are not met. Cannot enroll')
						print('Lacking Prerequisites')
						for result in self.cursor.stored_results():
							 print(str(result.fetchall()[0][0]))
				except:
					print('Some internal error occurred. Could not enroll. Try again.')

            		elif course_idn == 0:
                		enroll_options = False
				print ('Returning to Student menu \n\n\n')
        		else:
            			print ('Invalid option/course. Try again.')



	def Withdraw(self):
		dt = datetime.datetime.now()
                cQ = int(round((dt.month-1)/3)+2)
		nQ = cQ + 1
		if cQ>4: cQ-=4
		if nQ>4: nQ-=4
		cQ='Q'+str(cQ)
		nQ='Q'+str(nQ)
		cYear  = dt.year
		if nQ == "Q2": nYear = dt.year+1
                else:   dt.year

		sql_script = 'select UoSCode,Semester,Year from transcript \
				where ((Semester="'+cQ+'" and Year='+str(cYear)+') or\
					Semester="'+nQ+'" and Year='+str(nYear)+')\
					and studId='+str(self.username)
		self.cursor.execute(sql_script)
		current_courses = self.cursor.fetchall()
		print('Listing the offered Courses Enrolled in this quarter and next')
		print('CourseIndex\tCourseCode\tSemester\tYear')
		for i,item in enumerate(current_courses):
			item = [str(jtem) for jtem in item]
			print (str(i+1)+'\t'+'\t'.join(item))

		withdraw_options = True
		while withdraw_options:
			onscreen =      'Options \n ------ \n \
                                         Enter course index number for withdrawal \n \
                                         Enter 0 for returning to Student Menu'
                        course_idn 	= inputit(onscreen)
			
                        if course_idn <= len(current_courses) and course_idn>0:
				course_code 	= current_courses[course_idn-1][0]
				courseQ  	= current_courses[course_idn-1][1]
				courseY		= current_courses[course_idn-1][2]
				args 	= (self.username,course_code,courseQ,courseY,0)
				try:
	                        	enroll_error = self.cursor.callproc('Withdraw',args)[-1]
					self.conn.commit()
					print ('Success. Withdrawn.')

					self.cursor.execute('select @flag')
					flag_sql = self.cursor.fetchone()[0]
                                        self.cursor.execute('set @flag=0')
					self.conn.commit()
					if flag_sql==1:
						print('Enrollment is below 50 percentage')
					if enroll_error == 1:
						print('Grade is assigned for this course. Cannot withdraw')
						self.conn.rollback()
					self.cursor.execute('set @flag=0')
                                        self.conn.commit()
				except Error as error:
					self.conn.rollback()
					print(error)
					#print('Some internal error occurred. Could not withdraw. Try again.')

                       	elif course_idn == 0:
                                withdraw_options = False
				print ('Returning to Student menu \n\n\n')
                        else:
                                print ('Invalid option/course. Try again.')


	def Details(self):
        	sql_script = 'select * from student where Id = ' + str (self.username)
        	self.cursor.execute (sql_script)
        	details = self.cursor.fetchall ()

	        if details:
        	    for record in details:
                	print ('\t'.join (['1', 'Id:', str(record[0])]))
                	print ('\t'.join (['2', 'Name:', str(record[1])]))
                	print ('\t'.join (['3', 'Password:', str(record[2])]))
                	print ('\t'.join (['4', 'Address:', str(record[3])]))

	        edit_flag = True
        	while edit_flag:
            		option = inputit("Enter 1 to edit information or 0 to go back to main menu:")

            		if option == 1:
				edit_code = inputit('Enter code to edit any information')

                		if edit_code == 1 or edit_code == 2:
                    			print("Cannot change id or name")
                    			continue

	                	elif edit_code == 3:
        	        		new_password = raw_input ("Enter new Password:")
                	 		sql_update_pwd = 'update student set Password = "' + new_password + '" where\
                        			                Id = ' + str (self.username)
                 			try:
                        			self.cursor.execute (sql_update_pwd)
                        			self.conn.commit ()
						self.password = new_password
                                                print('Password change successful')

                    			except Error as error:
                		        	print(error)
                     				self.conn.rollback()
        	                		continue
		
                		elif edit_code == 4:
                    			new_address = raw_input ("Enter new Address:")
                    			sql_update_adrs = 'update student set Address = "' + new_address + '" where\
                               			             Id = ' + str (self.username)
                    			try:
                        			self.cursor.execute (sql_update_adrs)
                        			self.conn.commit ()
                                                print('Address change successful')

                    			except Error as error:
                        			print(error)
                        			self.conn.rollback()
                        			continue

                		else:
                    			print("Invalid option chosen!")
                    			continue

         	   	elif option == 0:
                		return

            		else:
                		print("Enter either 0 or 1")

	def Transcript(self, return_courses=False):
		sql_script = 	'select Year,Semester,UoSCode,Grade from transcript \
				where StudId = '+str(self.username)+\
				' order by Year ASC, Semester ASC'
		self.cursor.execute(sql_script)
		transcript = self.cursor.fetchall()
		if return_courses:
			return transcript

		if not transcript:
			print ('No transcript records')
		else:
			print ('\t'.join(['Year','Semester','CourseCode','Grade']))
			for item in transcript:
				item = list(item)
				if not item[-1]:
					item[-1]='Incomplete/Fail'
				item[0] = str(item[0])
				print '\t'.join(item)

			printcourse = True
			while printcourse:
				onscreen =	' Options \n ------ \n \
                                	        Enter course code for course details \n \
                                        	Enter 0 for returning to Student Menu \t'
				course_code = raw_input(onscreen)
				if course_code in [item[2] for item in transcript]:
					sql_script = 'select UosCode, UoSName, Semester, Year, Grade, Enrollment, MaxEnrollment, faculty.Name from  (select * from    (select * from transcript natural join unitofstudy where StudId = "'+str(self.username)+'") as T1   natural join uosoffering) T2 join faculty on T2.InstructorId = faculty.Id'

					self.cursor.execute(sql_script)
					crow = self.cursor.fetchall()
					if not crow:
						print ('Internal error: Course does not exist')
					else:
						tmplist = [crtem[0] for crtem in crow]
						cidx = tmplist.index(course_code)
						crow = [str(jtem) for jtem in list(crow[cidx])]
						print ('\t'.join(crow))
						#print ('Course Code {} \t DeptID {} \t Course_Name {} \t Credits {}'.\
#							format(crow[0],crow[1],crow[2],crow[3]))
				elif course_code == '0':
					printcourse = False
				else:
					print ('Invalid option/course. Try again.')




def student_login(cursor,conn):
	print ('Student Login\n')
	trylogin = 1
	while trylogin:
		s_username = raw_input("Enter the username: ")
		s_password = getpass.getpass('Enter the Password: ')
		if len(s_username)>0 and len(s_password)>0:
			try:
				sql_script = 	'select Id,Name,Password \
						from student \
						where (Id = '+s_username+\
						' and Password = "'+s_password+'")'
				cursor.execute(sql_script)
				srow = cursor.fetchone()
				if srow:
					print ('Login success')
					trylogin = 0
					return UserClass(cursor,conn,srow)
				else:
					print ('Credentials does not match')
			except:
				print ('Some data access error')
		else:
			print ('credentials were not entered')

		trylogin = inputit('Try again? (1 for yes / 0 for no)\t')
	print ('Could not login. If necessary, contact the admin at dumbledore@hogwarts.edu')
	return

def inputit(onscreen):
	value = raw_input(onscreen)
	while value =="":
		value = raw_input(onscreen)
	return int(value)


def main():
        conn   = connect()
        cursor = conn.cursor()

	trylogin = 1
	while trylogin:
	        user = student_login(cursor,conn)
        	if user:  user.student_menu()
		trylogin = inputit('Continue to login screen again? (yes/no) == (1/0)')
        print ('Exiting the scripts')


        cursor.close()
        #user.cursor.close()
        conn.close()
        print ('connection closed')




main()

