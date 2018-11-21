DROP TRIGGER IF EXISTS enrollmentConstraint;

delimiter $$

create trigger enrollmentConstraint after update on uosoffering 
for each row
begin
	if exists(select enrollment from uosoffering where UoSCode = NEW.UoSCode and NEW.enrollment < floor(MaxEnrollment/2))
	then 
		SIGNAL SQLSTATE '12345' SET MESSAGE_TEXT = 'Enrollment below 50%';
	end if;
end

delimiter $$
