
from sqlite3 import Date
from time import sleep
from DataBase import DBHelper
from datetime import date, datetime
import LoginSignUp
import plotly
import matplotlib.pyplot as plt
import numpy as np




class Group:
    def __init__(self,email):
        self.email=email
        cnct=DBHelper() 
    
    def CreateGroup(self,cnct):
        group_name=input("Give Group name  : ")
        query = "select group_name from groupinfo"
        cur=cnct.con.cursor()
        cur.execute(query)
        ii = cur.fetchall()
        flag=True
        for i in ii:
            if i[0]==group_name:
                flag=False 
                break
        if flag==False:
            print("Create a unique group name")
            return self.CreateGroup(cnct) 
        else:
            query1 = "create table if not exists expenserecord(group_name varchar(30),expense_name varchar(30),group_members_email varchar(250),settlement_status varchar(30),amount_spent float(2) ,settlement_date varchar(50))"
            cur = cnct.con.cursor()
            cur.execute(query1)
            cnct.con.commit()
            cnct.InsertGroupInfo(group_name,self.email)
            print("Group Created")
            query1=f"create table if not exists {group_name}(expense_name varchar(30),total_expense float(2),expenser_email varchar(250),expense_date varchar(20),members_count int)"
            cur=cnct.con.cursor()
            cur.execute(query1) 
            creater_phone=cnct.get_phone_number(self.email)
            query3 = "insert into groupmembers(group_name,group_members_email,group_members_phone) values('{}','{}','{}')".format(group_name,self.email,creater_phone[0]) # Adding group creater in the group
            cur=cnct.con.cursor()
            cur.execute(query3)
            cnct.con.commit()
            return self.ShowMyGroups(cnct)
            
    
       

    def GoInsideGroup(self,cnct):# here we have choice to get inside particular group
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Get inside (Enter group name) or ")
        print("R : To remove Group")
        print("L : Log Out")
        choice=input("Enter your Choice : ")
        if choice=="L":
            return self.Logout(cnct)
        elif choice == "R":
            return self.removeGroup(cnct)
            
        else:
            flag=cnct.CheckGroup(choice)
            print("----------------------------------------------------")
            if flag==False:
                print("Please Write name correctly")
                self.ShowMyGroups(cnct)
                return self.GoInsideGroup(cnct)
            else:
                return self.InsideGroup(cnct,choice)
                
    
    def InsideGroup(self,cnct,group_name):
        print(f"-------------------------{group_name}------------------------")
        print()
        print("1 : Add Member")
        print("2 : Add Expenses")
        print("3 : Show Group Members")
        print("4 : Show Pendings Collections")
        print("5 : Show Pending Payments")
        print("L : Log Out")
        print()
        choice = input("Enter your choice : ")
        if choice=="1":
            return self.AddMember(cnct,group_name)
        elif choice == "2":
            return self.AddExpenses(cnct,group_name)
        elif choice=="4":
            return self.ShowPendingCollections(cnct,self.email,group_name)
        elif choice=="3":
            return self.ShowGroupMembers(cnct,group_name)
        elif choice == "5":
            return self.ShowPendingPayments(cnct,group_name,self.email)
        elif choice=="L":
            return self.Logout(cnct)
        else:
            print("Invalid choice !!!")
            print("Try Again...")
            return self.InsideGroup(cnct,group_name)
        
        # Add Members
        # Create Expense
        # Show Unpaid Expenses

        
#***************************************************************
    # From Home Screen
    def ShowMyGroups(self,cnct):
        l=cnct.get_group_names(self.email) # fetch all the My groups created
        if len(l)==0:
            print()
            print("No Groups Created Yet....")
            print()
            print("1 : To create Group")
            choice=input()
            if choice=="1":
                self.CreateGroup(cnct)
        else:
            for i in l:
                print("> ",i[0])
        return self.GoInsideGroup(cnct)



    def ShowProfile(self,cnct):

        query = f"select first_name,last_name from logindata where email = '{self.email}'"
        cur = cnct.con.cursor()
        cur.execute(query)
        data = cur.fetchall()
        name = data[0][0].upper()
        surname = data[0][1].upper()
        print(f"------------------------{name} {surname}-------------------------------")
        def count_total_spent(email,group_name):
            query = f" select sum(amount_spent) from expenserecord where group_name = '{group_name}' and group_members_email = '{email}'"
            cur = cnct.con.cursor()
            cur.execute(query)
            data = cur.fetchall()
            return data[0][0]
        def create_piechart(list1,list2):
            y = np.array(list2)
            mylabels = list1
            plt.pie(y, labels = mylabels)
            plt.show() 
            if(input()=="Q"):
                plt.close()
        
        def show_expense_charts_inside_group(cnct,email,group_name):
            query = f"select expense_name,amount_spent from expenserecord where group_name = '{group_name}' and group_members_email = '{email}'"
            cur = cnct.con.cursor()
            cur.execute(query)
            data = cur.fetchall()
            expense = []
            amount = []
            for i in data:
                expense.append(i[0])
                amount.append(i[1])
           
            create_piechart(expense,amount)
            return show_my_expenses
        def getin(choice):
            flag=cnct.CheckGroup(choice)
            print("----------------------------------------------------")
            if flag==False:
                print("Please Write name correctly")
            else:
                query = f"select expense_name ,amount_spent from expenserecord where group_name = '{choice}' and group_members_email = '{self.email}'"
                cur = cnct.con.cursor()
                cur.execute(query)
                data = cur.fetchall()
                print("Expense\t  |  Spent\t  |")
                print("---------------------------")
                for i in data:
                    print(i[0],"\t  |  ",i[1])
                print("----------------------------------------------------")
                print("Type B to back")
                print("Type G to show graph")
                inn = input()
                if(inn == "B"):
                    return 
                return show_expense_charts_inside_group(cnct,self.email,choice)

        def show_my_expenses(email):
            l=cnct.get_group_names(email)
            if len(l)!=0:
                print("Group Name\t  |  Amount Spent\t  |")
                print("---------------------------")
                expense = []
                spentmoney = []
                for i in l:
                    spent = count_total_spent(email,i[0])
                    expense.append(i[0])
                    spentmoney.append(spent)
                    print(i[0],"\t\t  |  ",spent)
                    print("---------------------------")
                print("Type G to print Graph\n")
                print("Type Group name to get in\n")
                choice =input()
                if(choice == "G"):
                    create_piechart(expense,spentmoney)
                    show_my_expenses(email)
                else:
                    flag=cnct.CheckGroup(choice)
                    print("----------------------------------------------------")
                    if flag==False:
                        print("Please Write name correctly")
                    else:
                        getin(choice)
                        print("Type B to back")
                        return 

        print("1.show my Group expenses")
        choice = input()
        if(choice == '1'):
            show_my_expenses(self.email)
        print("1.Show my expenses")
        print("This is profile")

    
    def Logout(self,cnct):
        obj=LoginSignUp.LoginRegistration()
        print("You are Logged Out !!")
        print("****************************************") 
        print()
        obj.LR(cnct)
    
#****************************************************************
    # From Group Screen
    def AddMember(self,cnct,group_name):
        # Add by Email 
        # Add by Phone
        print("1 : Add Member by Phone")
        print("2 : Add Member by Email")
        choice = input("Enter your Choice : ")
        if choice == "1":
            member_phn = input("Enter the Member Phone Number\t:\t")
            flag=cnct.checkGroupMemberByPhone(member_phn)# checks is user in logindata
            if flag==True:
                l=cnct.get_email_by_Phone(member_phn)
                f=cnct.CheckUserMembershipInGroupByPhone(member_phn)
                if f:
                    for i in l:
                        email=i[0]
                        cnct.InsertIntoGroupMembers(group_name,email,member_phn)
                        print()
                        print("User Added Successfully.....")
                        return self.InsideGroup(cnct,group_name)
                else:
                    print("User Already exists...")
                    print()
                    self.InsideGroup(cnct,group_name)
            else:
                print("User not on split app...")
                print("Ask to sign in")
                self.AddMember(cnct,group_name)

        elif choice == "2":
            member_email = input("Enter the Member Email\t:\t")
            f=cnct.CheckEmail(member_email)
            if f:
                l=cnct.get_phone_by_email(member_email)
                flag=cnct.CheckUserMembershipIngroupByEmail(member_email,group_name) # check is member already inside a group
                
                if flag:
                    phone=l[0]
                    cnct.InsertIntoGroupMembers(group_name,member_email,phone) 
                    print()
                    print("User Added Successfully.....")
                    return self.InsideGroup(cnct,group_name)
                else:
                    print("User Already exists...")
                    print()
                    self.InsideGroup(cnct,group_name)
            else:
                print("No User Not Found...")
                return self.InsideGroup(cnct,group_name)


        else:
            print("Invalid Choice....")
            print("Try Again")
            return self.AddMember(cnct,group_name)
        
    
    def AddExpenses(self,cnct,group_name):
        expense_name=input("Name Expense : ")
        query = f"select expense_name from {group_name} where expense_name = '{expense_name}'";
        cur=cnct.con.cursor()
        cur.execute(query)
        d = cur.fetchall();
        exp = []
   
        for ex in d:
            exp.append(ex[0])
        if(expense_name in exp):
            print("Try Using different expense name")
            return self.AddExpenses(cnct,group_name)
        spent = input("Spent (Rs.) : ") 
        date=str(Date.today())
        total_members = cnct.getMemberCount(group_name)
        cnct.InsertExpense(group_name,expense_name,spent,self.email,date,total_members[0])
        row = cnct.GetAllGroupMembers(group_name)
        for r in row:
            cnct.InsertExpenseRecord(group_name,expense_name,r[2],"Pending",date)
        print("Expense added successfully...")
        # This query updates the login user data as there is no pendings for self paid
        status = "Completed"
        amount_spent = 0;
        query = f"select members_count from {group_name} where expense_name = '{expense_name}'"
        cur=cnct.con.cursor()
        cur.execute(query)
        data = cur.fetchall()
        
        email = self.email
        query = f"update expenserecord set settlement_status = '{status}',settlement_date = '{date}' where group_members_email = '{email}' and expense_name = '{expense_name}'"
        cur=cnct.con.cursor()
        cur.execute(query)
        cnct.con.commit()
        amount_spent = int(spent)/int(data[0][0])
        query = f"update expenserecord set amount_spent = {amount_spent} where expense_name = '{expense_name}' and group_name = '{group_name}'"
        cur=cnct.con.cursor()
        cur.execute(query)
        cnct.con.commit()



        #*****************************************************************************
        # this query add expense info like who have spent on expense and when
        cnct.InsertIntoExpenseInfo(group_name,expense_name,self.email,str(datetime.today()))
        return self.InsideGroup(cnct,group_name)


    def ShowGroupMembers(self,cnct,group_name):
        def remove_member():
            print("Press : R to remove Group Member")
            inpt = input()
            if inpt == "R":
                em = input("Enter email id to remove member : ")
                self.RemoveGroupMember(cnct,group_name,em)
                
            else:
                print("Invalid Choice ....")
                return remove_member();
        row = cnct.GetAllGroupMembers(group_name)
        for i in row:
            print(i[0],i[1])
        print()
        print("-------------------------------------")
        #only the group owner can remove the member
        query = f"select created_by,group_name from groupinfo where group_name = '{group_name}' and created_by = '{self.email}'";
        cur=cnct.con.cursor()
        cur.execute(query)
        d = cur.fetchall()
        if(len(d)!=0):
           remove_member()
        return self.InsideGroup(cnct,group_name)
    
    

    def ShowPendingCollections(self,cnct,email,group_name):
        expenses = []
        data = cnct.getMyExpense(email,group_name)#gives the expenses made my email 
        for d in data:
            expenses.append(d[0]) 
        if(len(expenses)==0):#if no expenses are made by me
            print("All collections are settled")
            return self.InsideGroup(cnct,group_name)
        else:
            netpay = 0
            data = []
            for ex in expenses:
                query = f"select expenserecord.group_members_email, expenserecord.expense_name from expenserecord where expense_name = '{ex}' and settlement_status = 'Pending' and group_name = '{group_name}'"
                cur=cnct.con.cursor()
                cur.execute(query)
                d = cur.fetchall()
                for dd in d:
                    data.append(dd)
            data.sort()
            print()
            print("---------------------------------------------------------------")
            print("Payer Name\t\t","|","\t Amount to be paid")
            print("---------------------------------------------------------------")
            for d in data:
                query = f"select total_expense,members_count from {group_name} where expense_name ='{d[1]}'"
                cur=cnct.con.cursor()
                cur.execute(query)
                memcnt_expnm = cur.fetchall()
                query1 =f"select first_name,last_name from logindata where email = '{d[0]}'" 
                cur1=cnct.con.cursor()
                cur1.execute(query1)
                fl_name = cur1.fetchall()
                print(fl_name[0][0]," ",fl_name[0][1],"(",d[1],")","\t\t\t","|",memcnt_expnm[0][0]/memcnt_expnm[0][1])
                netpay+=memcnt_expnm[0][0]/memcnt_expnm[0][1]
            print("---------------------------------------------------------------")
            print("Total Collection Remaining : ",netpay)
            print("---------------------------------------------------------------")
            input()
            return self.InsideGroup(cnct,group_name)
       
    
        
    def settlePendingPayments(self,cnct,group_name):
        choice = input("1 : To settle all Payments \n 2 : Back\n") 
        if choice =="1":
            # cnct.delete_for_settlement(group_name)
            status = "Completed"
            date = str(datetime.today())
            email = self.email
            query = f"update expenserecord set settlement_status = '{status}',settlement_date = '{date}' where group_members_email = '{email}'"
            cur=cnct.con.cursor()
            cur.execute(query)
            cnct.con.commit()
            print()
            print("Settled all.....")
            return
        elif choice=="2":
            return self.InsideGroup(cnct,group_name)
        else:
            print("Please Press the valid keys")
            return self.settlePendingPayments(cnct,group_name)


    def ShowPendingPayments(self,cnct,group_name,email):
        row = cnct.getMyPendingPayments(group_name,email)
        if len(row)!=0:
            total_amt = 0
            
            print("------------------ My Pendings ----------------")
            print("---------------------------------------------------------------")
            print("Expense Name \t  | Amt")
            print("---------------------------------------------------------------")
            for i in row:
                rr = cnct.getMemberCountTotalExpense(group_name,i[0])
                for r in rr:
                    que = f"select first_name,last_name from logindata where email = '{r[2]}'"
                    cur=cnct.con.cursor()
                    cur.execute(que)
                    fl = cur.fetchall();
                    name = fl[0][0]
                    surname = fl[0][1]
                    print(i[0]," (",name,surname,") "," \t  | ",r[1]/r[0])
                    total_amt+=r[1]/r[0]
            print("---------------------------------------------------------------")
            print("Total amount to Pay : ",total_amt)
            print("---------------------------------------------------------------")
            print()
            self.settlePendingPayments(cnct,group_name)
            
        else:
            print("----------------No More Pending Payments-----------------------")
        print()
        return self.InsideGroup(cnct,group_name)

    def removeGroup(self,cnct):
        #check logger email with group owner email
        #if mathched then only group can be removed
        # the group can be removed only if all the paymenents are settled
        query = f"select group_name from groupinfo where created_by = '{self.email}'";
        cur=cnct.con.cursor()
        cur.execute(query)
        data = cur.fetchall();
        
        if(len(data)==0):
            print("Group not found or you don't own a group")
        else:
            def verifygroup(groups):
                group_name = input("Enter group name to remove : ")
                if group_name in groups:
                    return group_name
                else:
                    print("Please enter a valid group name")
                    return verifygroup(groups)
            
            print("Groups create by you !!!")
            groups = []
            for i in data:
                groups.append(i[0])
                print("--> ",i[0])
            
            group_name =  verifygroup(groups) #return correct inputed group_name
            
            #check for settlements
            status = "Pending"
            query = f"select group_members_email from expenserecord where group_name = '{group_name}' and settlement_status = '{status}'"
            cur=cnct.con.cursor()
            cur.execute(query)
            d = cur.fetchall()
            data = set()
            for i in d:
                data.add(i[0])
            if(len(data) == 0): # if all the pending payments are setteled
                query = f"drop table {group_name}"
                cur=cnct.con.cursor()
                cur.execute(query)
                cnct.con.commit()
                query = f"delete from groupmembers where group_name = '{group_name}'"
                cur=cnct.con.cursor()
                cur.execute(query)
                cnct.con.commit()
                query = f"delete from groupinfo where group_name = '{group_name}'"
                cur=cnct.con.cursor()
                cur.execute(query)
                cnct.con.commit()
                print("Group removed Successfully")
                return 
            else: # if settlement is not clear
                print()
                print("Cannot remove groups")
                print("Below members settlement is pending")
                print()
                for mem in data:
                    print("-> ",mem)
                self.ShowMyGroups;
            
           
    

    def RemoveGroupMember(self,cnct,group_name,member_email):# call this function after watching member list
        #Only group owner can remove the member
        #check is member is having any pending payments is not then removes;
        if(self.email == member_email):
            print("Maybe you are trying to remove yourself...")
            print("Error.........")
        else:
           
            
            #1 -> Checks is their any pending payments to make by email 
            #2 -> Checks is their any collection is left for email

            #--------------------------1----------------------------# 
            flag1 = False #for unpaid payments 
            flag2 = False #for ungot payments 
            
            query = f"select expense_name from expenserecord where group_members_email = '{member_email}' and settlement_status ='Pending' and group_name = '{group_name}'";
            cur=cnct.con.cursor()
            cur.execute(query)
            data = cur.fetchall() 
            print(data,"from line no.415")
            unpaid_exp = []
            for exp in data:
                unpaid_exp.append(exp) 
            if(len(unpaid_exp)==0):#no remaining payments to made for email
                flag1 = True
            else: # remaining payments are left for email
                print("Cannot remove user...")
                print("User have unpaid payments for below expenses")
                for e in unpaid_exp:
                    print(" --> ",e[0]); 
                return self.InsideGroup(cnct,group_name)


            #-----------------------------2---------------------------# 
            query = f"select expense_name from {group_name} where expenser_email = '{member_email}'"#checks for expenses made by email 
            cur=cnct.con.cursor()
            cur.execute(query)
            data = cur.fetchall() 
            print(data,"from line no.434")
            if(len(data)==0):# email has made no expenses for others
                flag2 = True
            else: # email has made expenses for others
                #check is their any collection left from others 
                exp_by_email_notPaid = []
                for exp in data:
                    ex = exp[0]
                    query = f"select group_members_email from expenserecord where settlement_status = 'Pending' and expense_name = '{ex}' and group_name = '{group_name}'"
                    cur=cnct.con.cursor()
                    cur.execute(query)
                    d = cur.fetchall()
                    print(d,"from line no.445")
                    for i in d:
                        exp_by_email_notPaid.append(i)
                    if(len(exp_by_email_notPaid)!=0):
                        print("Cannot remove user ....")
                        print("User not got complete settlement from")
                        for e in exp_by_email_notPaid:
                            query = f"select first_name,last_name from logindata where email = '{e[0]}'"
                            cur=cnct.con.cursor()
                            cur.execute(query)
                            info = cur.fetchall()
                            print(" --> ",info[0][0],info[0][1])
                        return self.InsideGroup(cnct,group_name)
                    else:
                        flag2 = True 
            if(flag1 and flag2):
                query = f"delete from groupmembers where group_members_email = '{member_email}' and group_name = '{group_name}'"
                cur=cnct.con.cursor()
                cur.execute(query)
                cnct.con.commit()
                print("User removed successfully....")
                print()




                        

                
                
                
                
                