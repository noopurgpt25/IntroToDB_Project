CREATE DEFINER=`root`@`localhost` PROCEDURE `Enroll_Student`(
	IN studentID 	varchar(20),
    IN CourseCode 	varchar(20),
    IN courseQ 	varchar(10),
    IN cYear		varchar(10),
    OUT FinalError varchar(64))
enrolling:BEGIN
set FinalError = 1;

insert into transcript
values(studentID,CourseCode,courseQ,cYear,Null);

update uosoffering
set Enrollment=Enrollment+1
where UoSCode=CourseCode
	and Semester=courseQ
    and Year=cYear;
set FinalError=0;
    
END