from database.connect_db import db_conn


@db_conn
def test(args, cursor=None):
    """
    """
    sql = 'SELECT * FROM person'
    cursor.execute(sql, args)
    data = cursor.fetchall()
    return data


@db_conn
def stats_data_select(args, cursor=None):
    """
    """
    sql = '''SELECT count(*) AS cnt FROM person'''
    cursor.execute(sql, args)
    person_cnt = cursor.fetchone()

    sql = '''
    SELECT concept.concept_name AS gender, person.cnt as cnt
    FROM concept
    RIGHT JOIN (
        SELECT gender_concept_id, count(*) as cnt
        FROM person
        GROUP BY gender_concept_id
    ) person ON concept.concept_id=person.gender_concept_id
    '''
    cursor.execute(sql, args)
    gender_per_cnt = cursor.fetchall()

    sql = '''
    SELECT concept.concept_name AS race, person.cnt as cnt
    FROM concept
    RIGHT JOIN (
        SELECT race_concept_id, count(*) AS cnt 
        FROM person 
        GROUP BY race_concept_id
    ) person ON concept.concept_id=person.race_concept_id
    '''
    cursor.execute(sql, args)
    race_per_cnt = cursor.fetchall()

    sql = '''
    SELECT concept.concept_name AS ethnicity, person.cnt as cnt
    FROM concept
    RIGHT JOIN (
        SELECT ethnicity_concept_id, count(*) AS cnt 
        FROM person 
        GROUP BY ethnicity_concept_id
    ) person ON concept.concept_id=person.ethnicity_concept_id
    '''
    cursor.execute(sql, args)
    ethnicity_per_cnt = cursor.fetchall()

    sql = '''
    SELECT concept.concept_name AS visit, person.cnt as cnt
    FROM concept
    RIGHT JOIN (
        SELECT visit_concept_id, count(*) as cnt
        FROM visit_occurrence
        GROUP BY visit_concept_id
    ) person ON concept.concept_id=person.visit_concept_id
    '''
    cursor.execute(sql, args)
    visit_cnt = cursor.fetchall()

    sql = '''
    SELECT concept.concept_name AS gender, person.cnt as cnt
    FROM concept
    RIGHT JOIN (
        SELECT person.gender_concept_id, count(*) as cnt
        FROM person
        RIGHT JOIN (
            SELECT person_id
            FROM visit_occurrence
        ) visit ON visit.person_id=person.person_id
        GROUP BY person.gender_concept_id
    ) person ON concept.concept_id=person.gender_concept_id
    '''
    cursor.execute(sql, args)
    gender_visit_cnt = cursor.fetchall()

    sql = '''
    SELECT concept.concept_name AS race, person.cnt as cnt
    FROM concept
    RIGHT JOIN (
        SELECT person.race_concept_id, count(*) as cnt
        FROM person
        RIGHT JOIN (
            SELECT person_id
            FROM visit_occurrence
        ) visit ON visit.person_id=person.person_id
        GROUP BY person.race_concept_id
    ) person ON concept.concept_id=person.race_concept_id
    '''
    cursor.execute(sql, args)
    race_visit_cnt = cursor.fetchall()

    sql = '''
    SELECT concept.concept_name AS ethnicity, person.cnt as cnt
    FROM concept
    RIGHT JOIN (
        SELECT person.ethnicity_concept_id, count(*) as cnt
        FROM person
        RIGHT JOIN (
            SELECT person_id
            FROM visit_occurrence
        ) visit ON visit.person_id=person.person_id
        GROUP BY person.ethnicity_concept_id
    ) person ON concept.concept_id=person.ethnicity_concept_id
    '''
    cursor.execute(sql, args)
    ethnicity_visit_cnt = cursor.fetchall()

    sql = '''
    SELECT ROUND(CAST(EXTRACT(year FROM AGE(CURRENT_DATE, person.birth_datetime)) AS INTEGER), -1) age, count(*) as cnt
    FROM person
    RIGHT JOIN (
        SELECT person_id
        FROM visit_occurrence
    ) visit ON visit.person_id=person.person_id
    GROUP BY age
    '''
    cursor.execute(sql, args)
    birth_visit_cnt = cursor.fetchall()

    data = {
        'person':{
            'total': person_cnt,
            'gender_cnt': gender_per_cnt,
            'race_cnt': race_per_cnt,
            'ethnicity_cnt': ethnicity_per_cnt,
        },
        'visit':{
            'visit_cnt': visit_cnt,
            'gender_cnt': gender_visit_cnt,
            'race_cnt': race_visit_cnt,
            'ethnicity_cnt': ethnicity_visit_cnt,
            'birth_cnt': birth_visit_cnt,
        }
    }

    return data


@db_conn
def concept_id_select(args, cursor=None):
    """
    """
    if args['category']:
        sql = '''SELECT * FROM concept WHERE %(category)s LIKE '%%%(search_keyword)s%%' OFFSET %(offset)s LIMIT %(limit)s'''%args
    else:
        sql = '''SELECT * FROM concept OFFSET %(offset)s LIMIT %(limit)s'''%args
    cursor.execute(sql)
    data = cursor.fetchall()

    return data


@db_conn
def table_select(args, cursor=None):
    """
    """
    if args['category']:
        sql = '''
        SELECT * FROM concept WHERE %(category)s LIKE '%%%(search_keyword)s%%' OFFSET %(offset)s LIMIT %(limit)s'''%args
    else:
        sql = '''
        SELECT * 
        FROM concept
        LEFT JOIN (
            SELECT DISTINCT gender_concept_id as person
            FROM person
        ) person_gender ON person_gender.person=concept.concept_id
        LEFT JOIN (
            SELECT DISTINCT race_concept_id as person
            FROM person
        ) person_race ON person_race.person=concept.concept_id
        LEFT JOIN (
            SELECT DISTINCT ethnicity_concept_id as person
            FROM person
        ) person_ethnicity ON person_ethnicity.person=concept.concept_id
        LEFT JOIN (
            SELECT DISTINCT visit_concept_id as visit
            FROM visit_occurrence
        ) visit ON visit.visit=concept.concept_id
        LEFT JOIN (
            SELECT DISTINCT condition_concept_id as condition
            FROM condition_occurrence
        ) condition ON condition.condition=concept.concept_id
        LEFT JOIN (
            SELECT DISTINCT drug_concept_id as drug
            FROM drug_exposure
        ) drug ON drug.drug=concept.concept_id
        OFFSET %(offset)s LIMIT %(limit)s
        '''%args
        # sql = '''
        # SELECT DISTINCT gender_concept_id as id FROM person;
        # SELECT DISTINCT race_concept_id as id FROM person;
        # SELECT DISTINCT ethnicity_concept_id as id FROM person;
        # '''
    cursor.execute(sql)
    data = cursor.fetchall()

    return data