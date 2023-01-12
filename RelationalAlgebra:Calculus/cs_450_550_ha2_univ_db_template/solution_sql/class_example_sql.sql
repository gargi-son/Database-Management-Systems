
/*Student who have taken all CS courses*/
create view query_a as
select s.ssn from student s
	where not exists(select c.dcode, c.cno from course c where c.dcode = 'CS'
			minus select t.dcode, t.cno from transcript t where t.ssn = s.ssn)
	order by s.ssn;

create view query_b as
select c.dcode, c.cno from course c 
	where c.units >= all (select c2.units from course c2)
	order by c.dcode, c.cno;


