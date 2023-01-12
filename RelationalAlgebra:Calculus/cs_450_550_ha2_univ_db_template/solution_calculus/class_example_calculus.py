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
    # Your set creater functions or other helper functions (if needed)

    def student_transcript(s, transcript=transcript):
        return [{'dcode':t['dcode'], 'cno':t['cno']} for t in transcript
                    if t['ssn'] == s['ssn']]

    def cs_courses(course=course):
        return [{'dcode': co['dcode'], 'cno': co['cno']}       # All CS courses (Sub-set)
                            for co in course if co['dcode'] == 'CS']

    # ---------------------------------------------------------------
    # Your queries

    # Student(s) who has taken all CS courses
               # col : val
    query_a = [  { 'ssn': s['ssn'] }
        for s in student
        if all([x in student_transcript(s)          # Superset
                 for x in cs_courses()
        ])         # Subset
    ]


    # Course(s) which has the highest units
    query_b = [{'dcode':co['dcode'], 'cno':co['cno']} for co in course
                    if all([co['units']>= c['units'] for c in course])
    ]

    # ---------------------------------------------------------------
    # Some post-processing which you do not need to worry about
    # It is safe to not change anything after this

    return({
        "query_a": query_a,
        "query_b": query_b
    })


# -----------------------------------------------------
# IGNORE CODE AFTER THIS
# YOU DO NOT NEED TO HAVE THIS PART IN YOUR SUBMISSION
# -----------------------------------------------------

if __name__ == '__main__':
    import json
    f = open("../testDBs/db1.json", "r")
    db1 = json.loads(f.read())
    x = ha2(db1)
