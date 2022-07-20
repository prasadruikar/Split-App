
import mysql.connector as connector
from datetime import date

import values
class DBHelper:
    def __init__(self):
        self.con=connector.connect(host='localhost',
                                   port='3306',
                                   user='root',
                                   password='Prasad@1234',
                                   database='splitapp')
        
        
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% CREATE TABLES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    


        



    
    
         
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% GET FUNCTIONS FROM DATABASE%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # gives id to insert dynamically
    def getmaxid(self):
        query="select max(userId) from logindata" 
        cur=self.con.cursor()
        cur.execute(query) 
        a=-1
        for i in cur:
            a = i[0] 
        if a:
            a+=1
        else:
            a=101
        return a
    
    def get_user_name(self,email):
        query=f"select first_name from logindata where email='{email}'";
        cur=self.con.cursor()
        cur.execute(query)
        for i in cur:
            return i[0]
    
    def get_group_names(self,email):
        query=f"select group_name from groupmembers where group_members_email = '{email}'"
        cur=self.con.cursor()
        cur.execute(query)
        return cur.fetchall()
        
        
    def get_phone_by_email(self,email):
        query = f"select phone from logindata where email = '{email}'"
        cur = self.con.cursor()
        cur.execute(query)
        return cur.fetchone()
    
    def get_email_by_Phone(self,phone):
        query=f"select email from logindata where phone='{phone}'" 
        cur = self.con.cursor()
        cur.execute(query)
        return cur.fetchall()
    
    def get_phone_number(self,email):
        query = f"select phone from logindata where email = '{email}'"
        cur = self.con.cursor()
        cur.execute(query)
        return cur.fetchone()

    
    def getMemberCount(self,group_name):
        query=f"select count(group_members_email) from groupmembers where group_name='{group_name}'"
        cur = self.con.cursor()
        cur.execute(query)
        return cur.fetchone()
    
    def GetAllGroupMembers(self,group_name):
        query = f"select logindata.first_name,logindata.last_name,groupmembers.group_members_email from groupmembers,logindata where logindata.email = groupmembers.group_members_email and groupmembers.group_name ='{group_name}'"
        cur=self.con.cursor()
        cur.execute(query)
        return cur.fetchall()
    
    def getMyExpenses(self,email):
        query = f"select expense_name from expenseinfo where expenseinfo.expenser_email = '{email}'"
        cur = self.con.cursor()
        cur.execute(query)
        return cur.fetchall()
    
    def getPendingStatus(self,email,group_name):
        query = f"select expenserecord.group_members_email,expenserecord.expense_name,logindata.first_name,logindata.last_name from expenserecord,logindata where expenserecord.settlement_status = 'Pending' and expenserecord.expense_name in (select expenseinfo.expense_name from expenseinfo where expenseinfo.expenser_email = '{email}') and logindata.email = expenserecord.group_members_email"
        cur = self.con.cursor()
        cur.execute(query)
        return cur.fetchall()
    
    def getMyPendingPayments(self,group_name,email):
        query1 = f"select expenserecord.expense_name from expenserecord,{group_name} where expenserecord.settlement_status = 'Pending' and expenserecord.group_members_email = '{email}' group by expense_name"
        cur = self.con.cursor()
        cur.execute(query1)
        return cur.fetchall()
    def getMemberCountTotalExpense(self,group_name,expense_name):
        query2  = f"select members_count,total_expense,expenser_email from {group_name} where expense_name = '{expense_name}' "
        cur = self.con.cursor()
        cur.execute(query2)
        return cur.fetchall()
    
    def getMyExpense(self,email,group_name):
        query = f"select expense_name from expenseinfo where expenser_email = '{email}' and group_name = '{group_name}'"
        cur=self.con.cursor(query)
        cur.execute(query)
        return cur.fetchall()
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% INSERT FUNCTIONS FOR DATABASE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def InsertforSignUp(self,fname,lname,email,pswrd,phone):
        mId=self.getmaxid()
        query="insert into logindata(userId,first_name,last_name, email,password,phone) values('{}','{}','{}','{}','{}','{}')".format(mId,fname,lname,email,pswrd,phone)
        cur=self.con.cursor(query)
        cur.execute(query)
        self.con.commit()
        return 
    
    def InsertGroupInfo(self,group_name,email):

        query="insert into groupinfo(group_name,created_by,created_on) values('{}','{}','{}')".format(group_name,email,date.today())
        cur=self.con.cursor(query)
        cur.execute(query)
        self.con.commit()
        return
    
    def InsertIntoGroupMembers(self,group_name,email,phone):
        query="insert into groupmembers(group_name,group_members_email,group_members_phone) values('{}','{}','{}')".format(group_name,email,phone)
        cur=self.con.cursor()
        cur.execute(query)
        self.con.commit()
        return 

    def InsertExpense(self,group_name,expense_name,total_expense,expenser_email,expense_date,members_count):
        query = f"insert into {group_name}(expense_name,total_expense,expenser_email,expense_date,members_count) values('{expense_name}','{total_expense}','{expenser_email}','{expense_date}','{int(members_count)}')"
        cur=self.con.cursor()
        cur.execute(query)
        self.con.commit()
        return

    def InsertExpenseRecord(self,group_name,expense_name,email,settlement_status,settlement_date):
        query = "insert into expenserecord(group_name,expense_name,group_members_email,settlement_status,settlement_date) values('{}','{}','{}','{}','{}')".format(group_name,expense_name,email,settlement_status,settlement_date)
        cur=self.con.cursor()
        cur.execute(query)
        self.con.commit()
        return

    def InsertIntoExpenseInfo(self,group_name,expense_name,email,date):
        query = "insert into expenseinfo(group_name,expense_name,expenser_email,expense_date) values('{}','{}','{}','{}')".format(group_name,expense_name,email,date)
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% VERIFICATION FUNCTIONS FROM DATABASE %%%%%%%%%%%%%%%%%%%%%%%%%%
    #function to check if email already exists 
    def CheckEmail(self,email):
        query=f"select Email from logindata where Email ='{email}'";
        cur=self.con.cursor()
        cur.execute(query)
        for c in cur:
            if c[0]==email:
                return True
            else:
                return False

    def CheckEmailPass(self,email,pswrd):
        query=f"select Email,Password from logindata where Email = '{email}' and Password ='{pswrd}'"
        cur=self.con.cursor()
        cur.execute(query)
        for c in cur:
            if c[0]==email and c[1]==pswrd:
                return True 
            else:
                return False
    
    def CheckGroup(self,group_name):# return True if found given group
        query = f"select group_name from groupinfo where group_name = '{group_name}'" 
        cur=self.con.cursor()
        cur.execute(query)
        d = cur.fetchall()
        if(len(d)==0):
            return False
        for c in d:
            if c[0]==group_name:
                return True 
        else:
            return False
        
    def checkGroupMemberByPhone(self,phone):
        query=f"select phone from logindata where phone='{phone}'"
        cur=self.con.cursor()
        cur.execute(query)
        row=cur.fetchall()
        if len(row)==0:
            return False 
        else:
            return True
    
    def CheckUserMembershipIngroupByEmail(self,email,group_name):
        query=f"select group_name,group_members_email from groupmembers where group_name='{group_name}' and group_members_email = '{email}' "
        cur=self.con.cursor()
        cur.execute(query)
        row=cur.fetchall()
        for i in row:
            if i[0]==group_name and i[1]==email:
                return False 
        else:
            return True
    
    def CheckUserMembershipInGroupByPhone(self,phone):
        query=f"select group_members_phone from groupmembers where  group_members_phone = {phone}"
        cur=self.con.cursor()
        cur.execute(query)
        row=cur.fetchall()
        for i in row:
            if i[0]==phone:
                return False 
        else:
            return True
    

# Delete table 
    def delete_for_settlement(self,group_name):
        query = f"truncate table {group_name}"
        cur = self.con.cursor()
        cur.execute(query)
        
    
    