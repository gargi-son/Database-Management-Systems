# Gargi Sontakke
# G01334018

import sys
sys.path.append('..')

import lib.rel_algebra_calculus.rel_algebra_calculus as ra
# note: you can use ra.imply(a,b) which expresses a --> b (a implies b)

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
    # Your set creater functions or other helper functions (if needed)


    # ---------------------------------------------------------------
    # Your queries

    # query_a
    
    query_a = [
        s
        for s in student
        if any([
            (t["dcode"] == "CS" and t["cno"] == 530  and t["ssn"] == s["ssn"])
            for t in transcript
        ])
    ]
   
    # query_b
    def student_t(stu,transcript=transcript):
        return [{'dcode':t['dcode'],'cno':t['cno']} for t in transcript if t['ssn']==stu['ssn']]
    def cs_course(c=course):
        return [{'dcode': co['dcode'], 'cno': co['cno']}       # All CS courses (Sub-set)
                            for co in course if co['dcode'] == 'CS' and co['cno']==530]
    result=[{'ssn':stu['ssn'],'name':stu['name'],'major':stu['major'],'status':stu['status']} for stu in student if all([x in student_t(stu) for x in cs_course()]) and stu["name"]=="John"]
    query_b = ra.distinct(result)

    # query_c
    
    enroll_class=[{**enroll,**clas} for enroll in enrollment for clas in class_ if enroll['class']==clas['class']]
    enroll_class_preq=[{**erc,**pr} for erc in enroll_class for pr in prereq if erc['dcode']==pr['dcode'] and erc['cno']==pr['cno']]
    enroll_class_preq1=[{'ssn':ecp['ssn'],'pcode':ecp['pcode'],'pno':ecp['pno']} for ecp in enroll_class_preq]
    enroll_class_preq2=[{'ssn':ecp2['ssn'],'dcode':ecp2['pcode'],'cno':ecp2['pno']} for ecp2 in enroll_class_preq1]
    t_grade=[t for t in transcript if t['grade']=='A' or t['grade']=='B']
    t_grade1=[{'ssn':tg['ssn'],'dcode':tg['dcode'],'cno':tg['cno']} for tg in t_grade]
    enroll_class_preq_grade=[ecp2 for ecp2 in enroll_class_preq2 if all([ecp2!=tg1 for tg1 in t_grade1])]
    enroll_class_preq_grade_stu=[{**ecpg,**s} for ecpg in enroll_class_preq_grade for s in student if ecpg['ssn']==s['ssn']]
    enroll_class_preq_grade_stu1=[{'ssn':ecpgs['ssn'],'name':ecpgs['name'],'major':ecpgs['major'],'status':ecpgs['status']} for ecpgs in enroll_class_preq_grade_stu]
    enroll_class_preq_grade_stu2=[s for s in student if all([s!=ecpgs1 for ecpgs1 in enroll_class_preq_grade_stu1])]
    resutl=[{'ssn':ecpgs2['ssn'],'name':ecpgs2['name'],'major':ecpgs2['major'],'status':ecpgs2['status']} for ecpgs2 in enroll_class_preq_grade_stu2]
    query_c = ra.distinct(resutl)

    # query_d
    query_d = ra.distinct([ {"tbd": "tbd"} ])

    # query_e
    t_grade=[t for t in transcript if t['grade']=='C' or t['grade']=='F']
    t_grade_stu=[{**tg,**s} for tg in t_grade for s in student if tg['ssn']==s['ssn']]
    t_grade_stu1=[tgs for tgs in t_grade_stu if tgs['name']=='John']
    result=[{'ssn':tgs1['ssn'],'name':tgs1['name'],'major':tgs1['major'],'status':tgs1['status']} for tgs1 in t_grade_stu1]
    query_e = ra.distinct(result)

    # query_f
    def course_preq(c,prq=prereq):
        return [{'dcode':pr['dcode'], 'cno':pr['cno']} for pr in prq if pr['dcode']==c['dcode'] and pr['cno']==c['cno']]
    result=[{'dcode':cors['dcode'], 'cno':cors['cno']} for cors in course if not all([course_preq(cors)])] 
    query_f = ra.distinct(result)

    # query_g
    def course_preq(c,prq=prereq):
        return [{'dcode':pr['dcode'], 'cno':pr['cno']} for pr in prq if pr['dcode']==c['dcode'] and pr['cno']==c['cno']]
    result=[{'dcode':cors['dcode'], 'cno':cors['cno']} for cors in course if all([course_preq(cors)])]
    query_g = ra.distinct(result)

    # query_h
    def class_preq(c,prq=prereq):
        return [{'class':c['class'],'dcode':c['dcode'],'cno':c['cno'],'instr':c['instr']} for pr in prq if pr['dcode']==c['dcode'] and pr['cno']==c['cno']]
    result=[{'class':c['class'],'dcode':c['dcode'],'cno':c['cno'],'instr':c['instr']} for c in class_ if all([class_preq(c)])]
    query_h = ra.distinct(result)

    # query_i
    trans=[{'dcode':tran['dcode'],'cno':tran['cno'],'ssn':tran['ssn'],'grade':tran['grade']} for tran in transcript if tran['grade']!='A' and tran['grade']!='B']
    def transcript_stu(s,tran=trans):
        return [{'ssn':s['ssn'],'name':s['name'],'major':s['major'],'status':s['status']} for tr in tran if tr['ssn']==s['ssn']]
    stu_tran=[{'ssn':s['ssn'],'name':s['name'],'major':s['major'],'status':s['status']} for s in student if not all([transcript_stu(s)])]
    query_i = ra.distinct(stu_tran)

    # query_j
    fac_b=[f for f in faculty if f["name"]=="Brodsky"]
    fac_b1=[{'instr':f['ssn'],'name':f['name'],'dcode':f['dcode'],'rank':f['rank']} for f in fac_b]
    fac_b2=[{'instr':f1['instr']} for f1 in fac_b1]
    fac_class=[{**f2,**c} for f2 in fac_b2 for c in class_ if f2['instr']==c['instr']]
    fac_class_enroll=[{**fc,**enroll} for fc in fac_class for enroll in enrollment if fc['class']==enroll['class']]
    fac_class_enroll1=[{'class':fce['class']} for fce in fac_class_enroll]
    stu_enroll=[{**stu,**enrol} for stu in student for enrol in enrollment if stu['ssn']==enrol['ssn']]
    fac_class_enroll_stu=[{**fce1,**se} for fce1 in fac_class_enroll1 for se in stu_enroll if fce1['class']==se['class']]
    result=[{'ssn':fces['ssn'],'name':fces['name'],'major':fces['major'],'status':fces['status']} for fces in fac_class_enroll_stu]
    query_j = ra.distinct(result)   

    # query_k
    
    def enrollmnt(clas,stu):
        return any([enroll['class']==clas and enroll['ssn']==stu for enroll in enrollment])
    enroll_stu_class=[{'ssn':stu['ssn']} for stu in student 
        if all([enrollmnt(clas['class'],stu['ssn']) for clas in class_]) and len(class_)>0]
    query_k=ra.distinct(enroll_stu_class)

    # query_l
        
    result=[{'ssn':stu['ssn']} for stu in student if stu['major'] == 'CS'
        if all([enrollmnt(clas['class'],stu['ssn']) for clas in class_ if clas['dcode'] == 'MTH']) and len(class_)>0]
    query_l = ra.distinct(result)


    # ---------------------------------------------------------------
    # Some post-processing which you do not need to worry about
    # Do not change anything after this

    ra.sortTable(query_a,["ssn"])
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
        "query_l": query_l,

    })
