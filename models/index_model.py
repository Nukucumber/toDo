import pandas


def create(conn):

    cur = conn.cursor()
    
    cur.execute('''

        create table if not exists knowledge (
            knowledge_id integer primary key autoincrement,
            knowledge_title varchar(100),
            knowledge_source text
        )
                
    ''')
    
    cur.execute('''
                    
        create table if not exists activity_sphere(
            activity_sphere_id integer primary key autoincrement,
            activity_sphere_name varchar(30)
        )   
                
    ''')
    
    cur.execute('''

        create table if not exists task_category(
            task_category_id integer primary key autoincrement,
            task_category_name varchar(30)
        )
           
    ''')

    cur.execute('''
                         
        create table if not exists subject(
            subject_id integer primary key autoincrement,
            subject_name varchar(30),
            subject_description text
        )

    ''')

    cur.execute('''
                
        create table if not exists task (
            task_id integer primary key autoincrement,
            task_category_id int,
            activity_sphere_id int,
            subject_id int,
            task_name varchar(100),
            task_description text, 
            task_dateline date,
            foreign key (task_category_id) references task_category (task_category_id) on delete cascade,
            foreign key (activity_sphere_id) references activity_sphere (activity_sphere_id) on delete cascade,
            foreign key (subject_id) references subject (subject_id) on delete cascade
        )
                    
    ''')

    cur.execute('''
                
        create table if not exists task_knowledge (
            task_knowledge_id integer primary key autoincrement,
            knowledge_id int,
            task_id int,
            foreign key (knowledge_id) references knowledge (knowledge_id) on delete cascade,
            foreign key (task_id) references task (task_id) on delete cascade
        )
                    
    ''')

    cur.execute('''

        create table if not exists teacher_category (
            teacher_category_id integer primary key autoincrement,
            teacher_category_name
        )

    ''')

    cur.execute('''

        create table if not exists teacher (
            teacher_id integer primary key autoincrement,
            teacher_category_id int,
            teacher_name varchar(35),
            teacher_phone_number varchar(11),
            teacher_mail varchar(50),
            foreign key (teacher_category_id) references teacher_category (teacher_category_id) on delete cascade
        )

    ''')

    cur.execute('''

        create table if not exists subject_teacher (
            subject_teacher_id integer primary key autoincrement,
            teacher_id int,
            subject_id int,
            foreign key (teacher_id) references teacher (teacher_id) on delete cascade,
            foreign key (subject_id) references subject (subject_id) on delete cascade
        )
        
    ''')
    
    cur.close()

    return

def insert(conn):

    cur = conn.cursor()

    cur.execute('''
                    
        insert into activity_sphere (activity_sphere_name) values
        ("Учебная"),   
        ("Внеучебная")   
                
    ''')
        
    cur.execute('''

        insert into task_category (task_category_name) values
        ("Сложно"),
        ("Средне"),
        ("Просто")
           
    ''')

    cur.execute('''
                         
        insert into subject (subject_name, subject_description) values
        ("ПП", "Параллельное программирование"),
        ("СиИТ", "Сетевые и интернет технологии")        

    ''')

    cur.execute('''
                
        insert into task (task_category_id, activity_sphere_id, subject_id, task_name, task_description, task_dateline) values
        (2, 1, 1, "lab_1", "lab_1 description", date()),
        (2, 2, null, "Сходить за хлебом", "Сходить за белым резанным хлебом", date()),
        (3, 1, 2, "lab_1", "lab_1 description", "2024-02-12")
                    
    ''')

    cur.execute('''

        insert into knowledge (knowledge_title, knowledge_source) values
        ("css", "что-то о css"),
        ("html", "что-то о html"),
        ("ООП", "что-то об ООП"),
        ("c++", "что-то о c++"),
        ("Структуры данных", "что-то о структурах данных")
                
    ''')

    cur.execute('''
                
        insert into task_knowledge (knowledge_id, task_id) values
        (1, 3),
        (5, 3),
        (5, 1),
        (3, 1)
                    
    ''')

    cur.execute('''

        insert into teacher_category (teacher_category_name) values
        ("Допускающий сдачу заданий невовремя"),
        ("Не допускающий сдачу заданий невовремя")

    ''')

    cur.execute('''

        insert into teacher (teacher_category_id, teacher_name, teacher_phone_number, teacher_mail) values
        (1, "Озерова Галина Павловна", 89999999999, null),
        (2, "Чусов Андрей Александрович", null, null)

    ''')

    cur.execute('''

        insert into subject_teacher (teacher_id, subject_id) values
        (1, 2),
        (2, 1)
        
    ''')

    conn.commit()

    cur.close()

    return

def get_request_1_1(conn):

    df = pandas.read_sql('''

        select teacher_name, teacher_phone_number, teacher_category_name from teacher join teacher_category using(teacher_category_id)

    ''', conn)

    return df

        # select task_name, task_description, task_dateline, knowledge_title, knowledge_source from task left join task_knowledge using (task_id) left join knowledge using (knowledge_id)
        # where knowledge_title = 'Структуры данных'
        # order by task_dateline  
def get_request_1_2(conn):
    
    df = pandas.read_sql('''

        select teacher.* from teacher left join subject_teacher using (teacher_id) left join subject using (subject_id)
        where subject_name != 'ПП' and (teacher_phone_number not null and teacher_mail not null) 
        order by teacher_name
    ''', conn)

    return df

def get_request_2_1(conn):
    
    df = pandas.read_sql('''

        select subject.*, count() from subject left join task using(subject_id)
        group by subject_name

    ''', conn)

    return df    

def get_request_2_2(conn):
    
    df = pandas.read_sql('''

        select activity_sphere.*, count() from activity_sphere left join task using(activity_sphere_id)
        group by activity_sphere_name
                         
    ''', conn)

    return df 

def get_request_3_1(conn):
    
    df = pandas.read_sql('''

        with task_knowledge_count
        as(
            select distinct task_id, count() as knowledge_count from task left join task_knowledge using(task_id) join knowledge using(knowledge_id)
            group by task_id
        )
        select task.* from task left join task_knowledge_count using(task_id)
        where knowledge_count is null
                         
    ''', conn)

    return df 
    
def get_request_3_2(conn):
    
    df = pandas.read_sql('''

        select task.* from task
        where task_id not in (
            select task_id from task_knowledge
        )
    
    ''', conn)

    return df

def get_request_4_1(conn):

    cur = conn.cursor()
    
    cur.execute('''

        insert into task (task_category_id, activity_sphere_id, subject_id, task_name, task_description, task_dateline) values
        (2, 1, 1, "lab_2", "lab_2 description", date("2024-01-28"))
    
    ''')

    # conn.commit()

    cur.close()

    return

def get_request_4_2(conn):

    cur = conn.cursor()
    
    cur.execute('''

        delete from task 
        where task_id = 4
    
    ''')

    # conn.commit()

    cur.close()

    return

def get_request_5(conn):

    return pandas.read_sql('''

        select * from teacher

    ''', conn)