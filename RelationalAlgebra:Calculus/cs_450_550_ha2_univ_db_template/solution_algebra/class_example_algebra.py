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

    def is_cs(x):
        return x["dcode"] == "CS"

    # ---------------------------------------------------------------
    # Your queries

    # students who have taken (according to transcript) a CS course


    # Student who have taken all CS courses (i.e. all cs courses must be in transcript)
    transcript_proj = ra.proj(transcript, ['dcode', 'cno', 'ssn'])
    cs_only = ra.sel(course, is_cs)

    cs_only = ra.sel(course,  lambda x: x["dcode"] == "CS")

    cs_only_proj = ra.proj(cs_only, ['dcode', 'cno'])
    student_ssn = ra.proj(student, ['ssn'])
    all_combination = ra.prod(cs_only_proj, student_ssn)
    student_did_not_all_cs = ra.diff(all_combination, transcript_proj)

    query_a = ra.diff(student_ssn, student_did_not_all_cs)

    # Course with highest units
    course2 = ra.ren(ra.proj(course, ['dcode', 'cno', 'units']), {'dcode': 'dcode2', 'cno':'cno2', 'units':'units2'})
    course_x_course2 = ra.prod(course, course2)
    cond_lower_units = lambda x: x['units'] < x['units2']
    course_lower_units = ra.sel(course_x_course2, cond_lower_units)
    course_lower_units = ra.proj(course_lower_units, ['dcode', 'cno'])

    query_b = ra.diff(ra.proj(course, ['dcode', 'cno']), course_lower_units)

    table1 = 
    table2 = 
    ra.div(table1, table2, ["a1", "a2"])
    a1, a2 are attributes in table1 but not in table2


    # ---------------------------------------------------------------
    # Some post-processing which you do not need to worry about
    # It is safe to not change anything after this

    return({
        "query_a": query_a,
        "query_b": query_b
    })


# -------------------------------------------------------------------
# IGNORE CODE AFTER THIS
# YOU DO NOT NEED TO HAVE THIS PART IN YOUR SOLUTION FILE
# -------------------------------------------------------------------

if __name__ == '__main__':
    import json
    f = open("../testDBs/db1.json", "r")
    db1 = json.loads(f.read())
    x = ha2(db1)
