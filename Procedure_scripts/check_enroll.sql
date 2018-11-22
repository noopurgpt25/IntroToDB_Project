CREATE DEFINER=`root`@`localhost` PROCEDURE `Check_Enroll`(
	IN studentID 	varchar(20),
    IN CourseCode 	varchar(20),
    IN courseQ 	varchar(10),
    IN courseY		varchar(10),
    OUT FinalStatus int)
enroll_proc:BEGIN
DECLARE CourseStatus INT DEFAULT 0;
set FinalStatus = Null;




select count(*) into CourseStatus from transcript 
where (	StudId=StudentID
        and UoSCode = CourseCode);
        
if CourseStatus <> 0 then
	set FinalStatus = 1;
    LEAVE enroll_proc;
end if;




set CourseStatus=0;
select count(*) into CourseStatus from uosoffering 
where (Semester =courseQ
		and Year=courseY
        and UoSCode = CourseCode
        and Enrollment < MaxEnrollment);
        
if CourseStatus=0 then
	set FinalStatus = 2;
    LEAVE enroll_proc;
end if;




set CourseStatus=0;
select count(*) into CourseStatus
from (select PrereqUoSCode from requires
where UoSCode=CourseCode) PREQ
	where PREQ.PrereqUoSCode not in 
		(select UoSCode from transcript
		where StudId=studentID 
		and Grade is not null);

if CourseStatus <> 0 then
	set FinalStatus = 3;
    select *
	from (select PrereqUoSCode from requires
	where UoSCode=CourseCode) PREQ
	where PREQ.PrereqUoSCode not in 
		(select UoSCode from transcript
		where StudId=studentID 
		and Grade is not null);
    LEAVE enroll_proc;
end if;

set FinalStatus = 0;

END