from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import getpass
import time
 
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
	def student_menu():
		print ('\n\n~~~~~~~~~~~~~~\n\nStudent Menu\n')
		tryoptions  = True
		while tryoptions:
			print ('Current Courses: \n ------------')
			print ('\n'.join(['\t'.join(item) for item in self.current_courses()]))
			print ('------------ \n\n')
			onscreen = 	'Menu Options \n ------ \n \
					Transcript 	\t 1 \n \
					Enroll		\t 2 \n \
					Personal Info 	\t 3 \n \
					Logout 		\t 0 \n'
			choice   = input(onscreen)
			if not choice	: 	tryoptions = False
			elif choice == 1:	self.Transcript()
			elif choice == 2:	self.Enroll()
			elif choice == 3:	self.Details()
                        elif choice == 4:       self.Withdraw()
			else		:	print ('Invalid option. Try again.')

	def current_courses(self):
		dt = datetime.datetime.now()
		current_Q = 'Q'+str(int(round(dt.month/3 + min([1,(dt.month%3)]))))
		sql_script =    'select UoSCode, UoSName from  unitofstudy \
				where UoSCode IN (select distinct UoSCode \
							from transcript \
							where StudId='+self.username+ \
       							'and Semester='+current_Q+ \
        						'and Year='+str(dt.year)+')'
		self.cursor.execute(sql_script)
		return self.cursor.fetchall()
		
	def Enroll(self):
		dt = datetime.datetime.now()
                current_Q = 'Q'+str(int(round(dt.month/3 + min([1,(dt.month%3)]))))
		next_Q = 'Q'+str(int(round(dt.month/3 + min([1,(dt.month%3)]))+1.))
		sql_script = 	'select * from uosoffering
				where ((Semester='+current_Q+ \
					'or Semester='+next_Q+ \ 
					')and Year='+str(dt.year)+')'
		self.cursor.execute(sql_script)
		offered_courses = self.cursor.fetchall()
		transcript = self.Transcript(return_courses=True)
		
		enroll_options = True
		while enroll_courses:
			onscreen =      ' Options \n ------ \n \
                                         Enter course code for enrollment \n \
                                         Enter 0 for returning to Student Menu'
                        course_code = raw_input(onscreen)
                        if course_code in [item[0] for item in offered_courses]:
				proceed_enroll = True
				crow = offered_courses[ [item[0] for item in offered_courses] \
								.index(course_code)]
				if int(crow[4]) >= int(crow[5]): 
					print ('The course is already registered in full')
					proceed_enroll = False
				if proceed_enroll:
                        		sql_script = 'select PrereqUoSCode from requires \
                                        	      where UoSCode='+course_code
                                	self.cursor.execute(sql_script)
                                	prows = self.cursor.fetchall()
				

################# Current Checkpoint ######



	
                       	elif course_code == '0':
                                enroll_options = False
                        else:
                                print ('Invalid option/course. Try again.')





		self.conn.commit()



        def Withdraw(self):
                sql_script =    'select * from -----------'
                self.cursor.execute(sql_script)
                self.conn.commit()

	def Details(self):
                sql_script =    'select * from -----------'
		self.cursor.execute(sql_script)

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
				if not item[-1]: 
					item[-1]='Incomplete/Fail'
				print '\t'.join(item[1:])
			
			printcourse = True
			while printcourse:
				onscreen =	' Options \n ------ \n \
                                	        Enter course code for course details \n \
                                        	Enter 0 for returning to Student Menu'
				course_code = raw_input(onscreen)
				if course_code in [item[0] for item in transcript]:
					sql_script = 'select * from unitofstudy \
							where UoSCode='+course_code
					self.cursor.execute(sql_script)
					crow = self.cursor.fetchall()
					if not crow:
						print ('Internal error: Course does not exist')
					else:
						print ('Course Code {} \t DeptID {} \t Course_Name {} \t Credits {}'.\
							format(crow[0],crow[1],crow[2],crow[3]))
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
						' and Password = '+s_password+')'
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

		trylogin = input('Try again? (1 for yes / 0 for no)')
	print ('Could not login. If necessary, contact the admin at dumbledore@hogwarts.edu')
	return




def main():
        conn   = connect()
        curosr = conn.cursor()

	trylogin = 1
	while trylogin:
	        user = student_login(cursor,conn)
        	if user:  user.student_menu()
		trylogin = input('Continue to login screen again? (yes/no) == (1/0)')
        print ('Exiting the scripts')


        cursor.close()
        #user.cursor.close()
        conn.close()
        print ('connection closed')




main()

