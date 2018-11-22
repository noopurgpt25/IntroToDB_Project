call Check_Enroll(3213,"COMP3419","Q1","Q2",2019,@errorstatus);
select @errorstatus;

call Enroll_Student(3213,"COMP3419","Q1",2019,@errorstatus);
select @errorstatus;

select * from transcript
where StudId=3213 and Year=2018;
call Withdraw(3213,"INFO3402","Q1",2018,@errorstatus);

select * from transcript;

select * from uosoffering
where ((Semester="Q1" or Semester="Q2")
		and Year=2019
        and UoSCode="COMP3419"
        and Enrollment < MaxEnrollment);
select * from student;

select * from uosoffering
where UoSCode="COMP3615";
        
select * from student;
select * from unitofstudy;
select * from whenoffered;
select * from uosoffering;


select * from transcript;