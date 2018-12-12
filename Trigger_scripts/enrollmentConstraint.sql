DROP PROCEDURE IF EXISTS enrollmentWarning;
DROP TRIGGER IF EXISTS enrollmentConstraint;

delimiter $$

create procedure enrollmentWarning(out flag int)
begin
	set flag = 1;
end

delimiter $$

create trigger enrollmentConstraint after update on uosoffering 
for each row
begin
	if  (NEW.enrollment < NEW.MaxEnrollment*0.5)
	then 
		call enrollmentWarning(@flag);
	end if;
end

delimiter $$
