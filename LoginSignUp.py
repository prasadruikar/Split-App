import email
from DataBase import DBHelper
import LoginActivities

class LoginRegistration:
    
    def __init__(self):
        print("*****************WELCOME****************")  
        print("Loading....Please wait")
        
        conobj=DBHelper()
        print("Connected.........") 
        self.LR(conobj) 
    
    def LR(self,conobj):
        print("------------------------------------------")
        print("Press - 1 : Login")
        print("Press - 2 : Signup")
        choice=(input()) 
        if choice=="1":
            self.Login(conobj)
        elif choice=="2":
            self.SignUp(conobj)
        else:
            print("ERROR....")
            print("Press valid key") 
            self.LR(conobj) 


#**********************SignUp*************************
    def SignUp(self,conobj):
      
        def innerSign(self,conobj):
            Email = input("Enter Your Email\t:\t")
            #############################################

            f=conobj.CheckEmail(Email)# returns true if email exists

            if f:
                print("xxxxxxxxxxxxxxxxxxxxxxxxxxx")
                print("Something went wrong....")
                print("Try using different Email....")
                print()
                print("Press 1 To Try Login ")
                print("Or")
                print("Press Enter to continue SignUp")
                c=(input())
                if int(c)==1:
                    self.Login(conobj)
                    return
           
                else:
                   
                    return innerSign(self,conobj)
             
            else:
                fname=input("Enter Your First Name \t:\t")
                lname=input("Enter Your Last Name \t:\t")
                Pass =  input("Enter Password\t:\t")
                Phone = input("Enter Your Phone number\t:\t")
                conobj.InsertforSignUp(fname,lname,Email,Pass,Phone)
                print("Sign Up successful !!!") 
                print()
            choice=int(input("Press 1 for Login : "))
            if choice==1:
                self.Login(conobj)
                return
        
        print("----------Sign Up For Split App----------") 
        print()
        innerSign(self,conobj)

        return
        

#**********************Login***********************
    def Login(self,conobj):
        print("------------------ Login -----------------------")
        email=input("Enter your Email \t:\t")
        password=input("Enter your Password \t:\t")
        f=conobj.CheckEmailPass(email,password)
        if f:
            print()
            print("Login Successful")
            loger_name=conobj.get_user_name(email)
            grp_obj=LoginActivities.Group(email) # we are using email of the logger to trace all the activities done by the logger
            print("Welcome {} !!!".format(loger_name))
            print("------------------------------------------")
            self.LoginActivity(grp_obj,conobj)
            return
        else:
            print("Incorrect Email or Password ")
            print("Try again...")
            print()
            self.Login(conobj)
    

    def LoginActivity(self,grp_obj,conobj):
        
            print("1 : Create New Group")
            print("2 : Show My Groups")
            print("3 : Show My Profiles") 
            print("L : Log Out")
            print()
            choice=(input("Enter Your Choice : "))

            if choice=="1":
                grp_obj.CreateGroup(conobj)
            elif choice=="2":
                grp_obj.ShowMyGroups(conobj)
            elif choice=="3":
                grp_obj.ShowProfile(conobj)
            
            elif choice=="L":
                print("You are Logged Out !!")
                print("****************************************")
                self.LR(conobj)
            else:
                print("Press Valid Key")
                self.LoginActivity(conobj)
                 
            # create new group
            # show groups  
            # show my profile


    

                    
