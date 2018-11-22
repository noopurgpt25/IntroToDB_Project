CREATE DEFINER=`root`@`localhost` PROCEDURE `Withdraw`(
	IN studentID 	varchar(20),
    IN CourseCode 	varchar(20),
    IN courseQ 	varchar(10),
    IN cYear		varchar(10),
    OUT FinalStatus varchar(10))
withdraw_proc:BEGIN
DECLARE Grade_Status INT DEFAULT 0;
set FinalStatus = Null;

select count(*) into Grade_Status
from transcript
	where 	StudId=studentID
    and 	UoSCode=CourseCode
    and 	Semester=courseQ
	and 	Year=cYear
	and 	Grade is null;

if Grade_Status=0 then
	set FinalStatus = 1;
    LEAVE 	withdraw_proc;
end if;


delete
from 	transcript
	where 	StudId =studentID
    and 	UoSCode	=CourseCode
    and 	Semester=courseQ
	and 	Year=cYear
	and 	Grade is NULL;


update 	uosoffering
set Enrollment = Enrollment-1
	where 	UoSCode	=CourseCode
	and 	Semester=courseQ
    and 	Year	=cYear;

set 	FinalStatus = 0;

END