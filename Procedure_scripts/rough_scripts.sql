call Check_Enroll(5316,"COMP3419","Q1","Q2",2019,@errorstatus);
select @errorstatus;

call Enroll_Student(3213,"COMP3419","Q1",2019,@errorstatus);
select @errorstatus;

select * from transcript;


select * from uosoffering
where ((Semester="Q1" or Semester="Q2")
		and Year=2019
        and UoSCode="COMP3419"
        and Enrollment < MaxEnrollment);
        
        
select * from student;