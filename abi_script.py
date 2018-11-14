from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import getpass

 
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
 


class UserClass:
	def __init__(self,cursor,credentials):
		self.username   = credentials[0]
		self.stdnt_name = credentials[1]
		self.password   = credentials[2]
		self.cursor     = cursor
	def main_menu():
		tryoptions  = True
		course_list = self.current_courses()
		while tryoptions:
			print ('Current Courses: \t'+', '.join(course_list)+'\n')

			onscreen = 	'Transcript 	\t 1 \n \
					Enroll		\t 2 \n \
					Personal Info 	\t 3 \n \
					Logout 		\t 0 \n'
			choice   = input(onscreen)
			if not choice	: 	tryoptions = False
			elif choice == 1:	self.Transcript()
			elif choice == 2:	self.Enroll()
			elif choice == 3:	self.Details()
			else		:	print ('Invalid option. Try again.')

	def current_courses()
		sql_script =    'select * from -----------'
		
	def Enroll():
		sql_script = 	'select * from -----------'


	def Details():
                sql_script =    'select * from -----------'
		

	def Transcript()
		sql_script = 	'select * from transcript \
				where StudId = '+str(self.username)+\
				' order by Year ASC, Semester ASC'
		self.cursor.execute(sql_script)
		transcript = self.cursor.fetchall()
		if not transcript:
			print ('No transcript records')
		else:
			for item in transcript:
				print '\t'.join(item[1:])



def student_login(cursor):
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
					return (srow)
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
	        credentials = student_login(cursor)
        	if credentials:
                	user = UserClass(cursor,credentials)
                	user.main_menu()
		trylogin = input('Continue to login screen again? (yes/no) == (1/0)')
        print ('Exiting the scripts')


        cursor.close()
        user.cursor.close()
        conn.close()
        print ('connection closed')




main()

