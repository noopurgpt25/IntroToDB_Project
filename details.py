def Details(self):
    sql_script = 'select * from student where Id = ' + str (self.usernmae)
    self.cursor.execute (sql_script)
    details = self.cursor.fetchall ()

    if details:
        for record in details:
            print ('\t'.join ('1', 'Id:', str (record[0])))
            print ('\t'.join ('2', 'Name:', record[1]))
            print ('\t'.join ('3', 'Password:', record[2]))
            print ('\t'.join ('4', 'Address:', record[3]))

    edit_flag = True
    while edit_flag:
        option = raw_input ("Enter 1 to edit information or 0 to go back to main menu:")

        if option == 1:

            edit_code = raw_input ('Enter code to edit any information')
            if edit_code == 1 or edit_code == 2:
                print("Cannot change id or name")
            elif edit_code == 3:
                new_password = raw_input ("Enter new Password:")
                sql_update_pwd = 'update student set Password = ' + new_password + ' where\
                                Id = '+str(self.username)
                try:
                    self.cursor.execute (sql_update_pwd)
                    self.conn.commit ()

                except Error as error:
                    print(error)
                    break;

            elif edit_code == 4:
                new_address = raw_input ("Enter new Address:")
                sql_update_adrs = 'update student set Address = ' + new_address + ' where\
                                    Id = '+str(self.username)
                try:
                    self.cursor.execute (sql_update_adrs)
                    self.conn.commit ()

                except Error as error:
                    print(error)
                    break;
            else:
                print("Invalid option chosen!")

        elif option == 0:
            return
        else:
            print("Enter either 0 or 1")

    return
