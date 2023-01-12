--Name: Gargi Sontakke
--Gno : G01334018

--query_a
drop view query_a;
create view query_a as
select distinct s.ssn, s.name, s.major, s.status from student s, transcript t
    where s.ssn=t.ssn and t.dcode='CS' and t.cno=530
    order by s.ssn;

-- query_b
drop view query_b;
create view query_b as
select distinct s.ssn, s.name, s.major, s.status from student s, transcript t
    where s.name='John' and s.ssn=t.ssn and t.dcode='CS' and t.cno=530
    order by s.ssn;

-- query_c Students who satisfied all prerequisites of each class they are enrolled in.
drop view query_c;
create view query_c as
  select distinct S.ssn as ssn, S.name as name, S.major as major, S.status as status
  from student S minus ( select S1.ssn as ssn, S1.name as name, S1.major as major, S1.status as status from student S1,
    (select E.ssn, PR.pcode, PR.pno from enrollment E, prereq PR, class C
      where E.class = C.class and C.dcode = PR.dcode and C.cno = PR.cno
      minus select ssn, dcode, cno from transcript
      where grade = 'A' or grade = 'B' ) E where E.ssn = S1.ssn)
      order by ssn;


-- query_d Students who are enrolled in a class for which they have not satisfied all its prerequisites.
drop view query_d;
create view query_d as
  select distinct S.ssn, S.name, S.major, S.status
  from student S, (select E.ssn, PR.pcode, PR.pno from enrollment E, prereq PR,class C
    where E.class = C.class and C.dcode = PR.dcode and C.cno = PR.cno
    minus select ssn,dcode,cno from transcript where grade='A' or grade='B') E
    where E.ssn = S.ssn
    order by S.ssn;

-- query_e Students named John who are enrolled in a class for which they have not satisfied all its prerequisites.
drop view query_e;
create view query_e as
  select distinct S.ssn, S.name, S.major, S.status
  from student S, transcript T
  where T.ssn = S.ssn and (T.grade = 'C' or T.grade = 'F') and S.name = 'John'
  order by S.ssn;

-- query_f Courses which do not have pre-requisites
drop view query_f;
create view query_f as
  select dcode, cno from course
  minus select dcode, cno from prereq
  order by dcode, cno;

-- query_g courses with some pre-requisites
drop view query_g;
create view query_g as
  select distinct PR.dcode, PR.cno from prereq PR
  order by PR.dcode, PR.cno;

-- query_h classes offered this semester and have pre-requisites
drop view query_h;
create view query_h as
  select distinct c.* from class C, prereq PR
  where PR.dcode = C.dcode and PR.cno = C.cno
  order by C.class;

-- query_i Students who received grades A or B in every course they have taken
drop view query_i;
create view query_i as
  select distinct S.ssn, S.name, S.major, S.status from student S
  minus select S1.ssn, S1.name, S1.major, S1.status from student S1, transcript T
  where T.ssn = S1.ssn and T.grade != 'A' and T.grade != 'B'
  order by ssn;

-- query_j Students who are currently enrolled in a class taught by professor Brodsky
drop view query_j;
create view query_j as
  select S.* from student S, enrollment E, class C, faculty F
  where S.ssn = E.ssn and E.class = C.class and F.ssn = C.instr and F.name = 'Brodsky'
  order by S.ssn;

-- query_k Find Students from the enrollment table who are enrolled in all classes
drop view query_k;
create view query_k as
  select distinct E.ssn from enrollment E
  where not exists (select C.class from class C
    where not exists (select E1.class from enrollment E1
      where E1.class = C.class and E1.ssn = E.ssn))
      order by E.ssn;

--query_l CS students from the enrollment table who are enrolled in all math classes.
drop view query_l;
create view query_l as
  select distinct E.ssn from enrollment E, student S
  where E.ssn = S.ssn and S.major = 'CS'
  and not exists (select C.class from class C where C.dcode='MTH'
    and not exists (select E1.class from enrollment E1 where E1.class = C.class and E1.ssn = E.ssn))
    order by E.ssn;
