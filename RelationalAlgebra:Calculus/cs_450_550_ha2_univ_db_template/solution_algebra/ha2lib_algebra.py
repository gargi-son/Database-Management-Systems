import sys
sys.path.append('..')

import lib.rel_algebra_calculus.rel_algebra_calculus as ra


def ha2(univDB):
    tables = univDB["tables"]
    department = tables["department"]
    course = tables["course"]
    prereq = tables["prereq"]
    # class may be a reserved word - check
    class_ = tables["class"]
    faculty = tables["faculty"]
    student = tables["student"]
    enrollment = tables["enrollment"]
    transcript = tables["transcript"]

    # ---------------------------------------------------------------
    # Your condition functions or other helper functions (if needed)

    def is_cs530(x):
        return x["dcode"] == "CS" and x["cno"] == "530"

    # ---------------------------------------------------------------
    # Your queries

    #query_a
    #Find students (ssn, name, major, status) who have taken the course “cs530” (must be in transcripts)
    select_course = ra.sel(transcript,  lambda x: (x["cno"] == 530 and x["dcode"] == "CS"))
    query_a = ra.proj(ra.join(select_course, student), ['ssn', 'name', 'major', 'status'])

    # query_b
    #Find students (ssn, name, major, status) named “John” (i.e., name = "John" in student) who have taken the course “CS 530”
    select_course = ra.sel(transcript,  lambda x: (x["cno"] == 530 and x["dcode"] == "CS"))
    select_name = ra.sel(ra.join(select_course,student), lambda y: y["name"] == "John")

    query_b = ra.proj(select_name, ['ssn', 'name', 'major', 'status'])

    # query_c

    enroll_c = ra.join(enrollment, class_)
    pre_c1 = ra.proj(ra.join(enroll_c,prereq), ['ssn','pcode','pno'])
    pre_c2 = ra.ren(pre_c1,{'pcode':'dcode','pno':'cno'})
    pre_c3 = lambda x: x['grade'] == 'A' or x['grade'] == 'B'
    grades_c1 = ra.proj(ra.sel(transcript,pre_c3),['ssn','dcode','cno'])
    temp_c = ra.diff(pre_c2,grades_c1)
    temp_c1 = ra.join(temp_c,student)
    temp_c2 = ra.proj(temp_c1,['ssn','name','major','status'])
    temp_c3 = ra.diff(student,temp_c2)
    query_c = ra.proj(temp_c3,['ssn','name','major','status'])

    # query_d
    
    enroll_j = ra.join(enrollment, class_)
    pre_j = ra.join(enroll_j,prereq)
    pre_a = ra.proj(pre_j,['ssn','pcode','pno'])
    pre_a1 = ra.ren(pre_a,{'pcode':'dcode','pno':'cno'})
    grades = ra.sel(transcript,lambda y: y['grade'] == 'A' or y['grade'] == 'B')
    grade_proj = ra.proj(grades,['ssn','dcode','cno'])
    tmp_d = ra.diff(pre_a1,grade_proj)
    tmp_d1 = ra.join(tmp_d,student)
    query_d = ra.proj(tmp_d1,['ssn','name','major','status'])

    # query_e
    #Find students (ssn, name, major, status) named “John” who are enrolled in a class 
    # for which they have not satisfied all its prerequisites. 
    # To satisfy the prerequisite, the student needs to have obtained 
    # the grade “B” or higher. Order the result by ssn.
    select_grade = ra.sel(transcript, lambda x: (x["grade"] == "C" and x["grade"] == "F"))
    select_name = ra.sel(ra.join(select_grade,student), lambda y: y["name"] == "John")
    query_e = ra.proj(select_name, ['ssn', 'name', 'major', 'status'])


    # query_f
    #Find courses (dcode, cno) that do not have prerequisites. 
    # Order the result by dcode, cno
    prereq_select = ra.proj(prereq,['dcode', 'cno'])
    course_proj = ra.proj(course, ['dcode', 'cno'])

    query_f = ra.diff(course_proj,prereq_select)

    # query_g
    #Find courses (dcode, cno) that do have some prerequisites. 
    # Order the result by dcode, cno.
    prereq_select = ra.proj(prereq, ['dcode', 'cno'])
    course_select = ra.proj(course, ['dcode', 'cno'])
    combine_table = ra.join(prereq_select, course_select)
    query_g = ra.proj(combine_table, ['dcode', 'cno'])

    # query_h
    #Find classes (class, dcode, cno, instr) that are offered this 
    # semester and have prerequisites. Order the result by class.
    prereq_proj = ra.proj(prereq, ['dcode','cno'])
    combine_table = ra.join(prereq_proj,class_)

    query_h = ra.proj(combine_table,['class', 'dcode', 'cno', 'instr'])

    # query_i
    #Find students (ssn, name, major, status) who received only the grades “A” or “B” 
    # in every course they have taken (must appear in Transcripts).
    # Order the results by ssn.
    non_AB = ra.proj(ra.sel(transcript,lambda x:x["grade"]!= 'A' and x["grade"] != 'B'),["ssn"])
    diff_tables = ra.diff(ra.proj(student,["ssn"]),non_AB)
    query_i = ra.proj(ra.join(diff_tables,student), ['ssn', 'name', 'major','status'])

    # query_j
    #Find students (ssn, name, major, status) who are currently enrolled 
    # in a class taught by professor Brodsky (name = “Brodsky” in faculty). 
    # Order the result by ssn
    sel_prof = ra.sel(faculty,lambda x: x["name"] == "Brodsky")
    faculties = ra.proj(ra.ren(sel_prof,{'ssn':'instr'}),['instr'])
    fac_class = ra.join(faculties,class_)
    fac_class_enroll = ra.join(fac_class,enrollment)
    class_num = ra.proj(fac_class_enroll,['class'])
    stud_enroll = ra.join(student,enrollment)
    class_stud_enroll = ra.join(class_num, stud_enroll)
    query_j = ra.proj(class_stud_enroll,['ssn','name','major','status'])

    # query_k
    #Find students (ssn) from the enrollment table who are enrolled in all classes. 
    # Order the result by ssn
    class_proj = ra.proj(class_, ['class'])

    query_k = ra.div(enrollment, class_proj,["class"])


    #query_l

    cs_stud = ra.sel(student, lambda x: x["major"] == "CS")
    cs_stud_proj = ra.proj(ra.join(cs_stud, enrollment),['class','ssn'])
    math_class = ra.sel(class_, lambda x: x["dcode"] == "MTH")
    math_class_proj = ra.proj(math_class, ['class'])
    query_l = ra.div(cs_stud_proj, math_class_proj, ['class'])

    # ---------------------------------------------------------------
    # Some post-processing which you do not need to worry about
    # Do not change anything after this

    query_a = ra.distinct(query_a)
    query_b = ra.distinct(query_b)
    query_c = ra.distinct(query_c)
    query_d = ra.distinct(query_d)
    query_e = ra.distinct(query_e)
    query_f = ra.distinct(query_f)
    query_g = ra.distinct(query_g)
    query_h = ra.distinct(query_h)
    query_i = ra.distinct(query_i)
    query_j = ra.distinct(query_j)
    query_k = ra.distinct(query_k)
    query_l = ra.distinct(query_l)


    ra.sortTable(query_a,["ssn"])
    ra.sortTable(query_b,["ssn"])
    ra.sortTable(query_c, ['ssn'])
    ra.sortTable(query_d, ['ssn'])
    ra.sortTable(query_e, ['ssn'])
    ra.sortTable(query_f, ['dcode', 'cno'])
    ra.sortTable(query_g, ['dcode', 'cno'])
    ra.sortTable(query_h, ['class'])
    ra.sortTable(query_i, ['ssn'])
    ra.sortTable(query_j, ['ssn'])
    ra.sortTable(query_k, ['ssn'])
    ra.sortTable(query_l, ['ssn'])

    return({
        "query_a": query_a,
        "query_b": query_b,
        "query_c": query_c,
        "query_d": query_d,
        "query_e": query_e,
        "query_f": query_f,
        "query_g": query_g,
        "query_h": query_h,
        "query_i": query_i,
        "query_j": query_j,
        "query_k": query_k,
        "query_l": query_l
    })
