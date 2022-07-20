from DataBase import DBHelper
from LoginSignUp import LoginRegistration

class mainn:
    def __init__(self):
        default_tables=DefaultTables()
        user =LoginRegistration()

class DefaultTables:
    def __init__(self):
        cnct=DBHelper()
        # registration data 
        query1='create table if not exists logindata(userId int primary key,first_name varchar(25),last_name varchar(15),email varchar(250) ,password varchar(15),phone varchar(12))'
        
        # exppenses by each group
        query2 = "create table if not exists profileexpenses(userId int)" # Table to track expense of each profile
        
        # groups info 
        query3 = "create table if not exists groupinfo(group_name varchar(50) primary key,created_by varchar(250),created_on varchar(20))"

        # group members table (stores groups created and their user email and phones)
        query4="create table if not exists groupmembers(group_name varchar(50) ,group_members_email varchar(250), group_members_phone varchar(12))"

        query5 =" create table if not exists expenseinfo(group_name varchar(50),expense_name varchar(50),expenser_email varchar(250),expense_date varchar(100))"

        # all members history of collection and expenses

        query = "create table if not exists history (email varchar(250),to_collect float(2),to_pay float(2),date DATE)"

        cur=cnct.con.cursor()
        cur.execute(query1)
        cur.execute(query2)
        cur.execute(query3)
        cur.execute(query4)
        cur.execute(query5)
        # query-1,query-2,query-3 creates default
        
mobj=mainn()
