-- query_a
drop view query_a;
create view query_a as
select distinct s.ssn as ssn, s.name as name, s.major as major, s.status as status from student s

    order by s.ssn;

-- query_b
drop view query_b;
create view query_b as
select distinct s.ssn as ssn, s.name as name, s.major as major, s.status as status from student s

    order by s.ssn;

-- query_c
drop view query_c;
create view query_c as
select distinct s.ssn as ssn, s.name as name, s.major as major, s.status as status from student s

    order by s.ssn;

-- query_d
drop view query_d;
create view query_d as
select distinct s.ssn as ssn, s.name as name, s.major as major, s.status as status from student s

    order by s.ssn;

-- query_e
drop view query_e;
create view query_e as
select distinct s.ssn as ssn, s.name as name, s.major as major, s.status as status from student s

    order by s.ssn;

-- query_f
drop view query_f;
create view query_f as
select distinct c.dcode, c.cno from course c

    order by c.dcode, c.cno;

-- query_g
drop view query_g;
create view query_g as
select distinct p.dcode, p.cno from prereq p

    order by p.dcode, p.cno;

-- query_h
drop view query_h;
create view query_h as
select distinct c.* from class c

    order by c.class;

-- query_i
drop view query_i;
create view query_i as
select distinct s.* from student s

    order by s.ssn;

-- query_j
drop view query_j;
create view query_j as
select s.* from student s

    order by s.ssn;

-- query_k
drop view query_k;
create view query_k as
select e.ssn from enrollment e

    order by e.ssn

drop view query_l;
create view query_l as
select e.ssn from enrollment e


    order by e.ssn
