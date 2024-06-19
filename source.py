import mysql.connector
from tabulate import tabulate
from prettytable import PrettyTable
import datetime
def contact_no():
  while True:
    try:
     NO=int(input("PLEASE ENTER CONTACT NO."))
     if len(str(NO))==10:
         return NO
         break
     else :
        print("PLEASE ENTER 10 DIGIT ")
    except:
        print("PLEASE ENTER VALID NO.")
def option_input(x):
    while True:
     try:
        options=int(input("ENTER YOUR CHOICE"))
        if options in x:
            break
        else:
            print("PLEASE ENTER VALID NO.")
     except:
         print("PLEASE ENTER VALID NO.")
    return(options)
def name_changer(N):
 c=""
 i=0
 for i in range(0,len(N)):
  if N[i].isspace():
      c=c+"_"
      i=i+1
  else:
    c=c+N[i]
    i=i+1
 return c
def year_input():
 while True:
     try:
        y=int(input("ENTER YEAR"))
        if y in range(2020,int(now.strftime('%Y'))+1):
                break
        else:
            print("PLEASE ENTER VALID YEAR")
     except:
            print("PLEASE ENTER VALID YEAR")
 return (y)
def month_input() :
 while True:
  try:
    m=int(input("ENTER MONTH IN NO."))
    if m in [1,2,3,4,5,6,7,8,9,10,11,12]:
        break
    else:
        print("PLEASE ENTER VALID MONTH")
  except:
        print("PLEASE ENTER MONTH IN NO.")
 return(m)
i=1
while True:
 now = datetime.datetime.now()
 print("CHOOSE")
 print("")
 print("   ____________________________________________________________________________________________")
 print("  |                                                                                            |")
 print("  |           ___________        ____________________________      _________________           |")
 print("  |          |           |      |                            |     |                |          |")
 print("  |          | 1) BILL   |      |  2)  ADMINISTRATION        |     |  3)  EXIT      |          |")
 print("  |          |___________|      |____________________________|     |________________|          |")
 print("  |                                                                                            |")
 print("  |____________________________________________________________________________________________|")
 print("")
 l1=[1,2,3]
 option=option_input(l1)
 if option==3:
  break
 if option==1:
    mydb=mysql.connector.connect(host="localhost",user="root",password="1234",database="admin",)
    mycursor = mydb.cursor()
    mycursor.execute("select bill_no from sale")
    data=mycursor.fetchall()
    l=[]
    for row in data:
       l.append(row[0])    
    bill_no=max(l)+1
    mycursor.close()
    mydb.close()
    mydb=mysql.connector.connect(host="localhost",user="root",password="1234",database="customer",)
    mycursor = mydb.cursor()
    while True:
     print("")
     customer_name=input("ENTER CUSTOMER NAME")
     print("")
     if all(x.isalpha() or x.isspace() for x in customer_name):
         if len(customer_name)==0:
             print("NAME CAN'T BE EMPTY")
         else:
          break
     else:
         print("PLEASE ENTER VALID NAME")
         print("")
    customer_name=name_changer(customer_name)
    customer_contact=contact_no()
    name=customer_name+"_"+str(bill_no)
    try:
       mycursor.execute("create table  %s (DATE date,PRODUCT_ID integer ,PRODUCT_NAME VARCHAR(100),PRICE INTEGER,QUANTITY INTEGER,NET_PRICE INTEGER,purchase_price INTEGER)"%(name))
    except:
        pass
    print("TYPE 0 FOR ENDING LIST" )
    print("")
    print("")
    print("ENTER PRODUCT ID AND QUANTITY IN FORM OF PRODUCT ID,QUANTITY")
    print("")   
    i=1
    while True:
        while True:
         print("")
         try:
          l=eval(input("ENTER PRODUCT ID AND QUANTITY"))
          print("")
          break
         except:
           print("PLEASE ENTER VALID PRODUCT ID,IF YOU WANT TO END LIST TYPE ZERO IN NUMERIC")
           print("")
        if type(l)!=int and len(list(l))>2:
            print("THIS CAN'T HAVE MORE THAN 2 VALUES")
            print("")
        elif l!=0 :
          if type(l)==int:    
             l=(l,1)
          elif len(list(l))==1:
              l=list(l)
              l.append(1)              
          else:
             pass
          mycursor.execute("select PRODUCT_ID from cost where PRODUCT_ID=%s;"%(l[0]))
          data=mycursor.fetchall()
          if len(data)==0:
              print("product ID",l[0],"is not entered in the system ")
          else:
                  mycursor.execute("insert into %s(DATE,PRODUCT_ID,QUANTITY) VALUES('%s-%s-%s',%s,%s)"%(name,now.strftime("%y"),now.strftime("%m"),now.strftime("%d"),l[0],l[1]))
                  mycursor.execute("update %s set %s.purchase_price=(select purchase_price from cost where %s.PRODUCT_ID=cost.PRODUCT_ID)"%(name,name,name))
                  mycursor.execute("update %s set %s.price=(select price from cost where %s.PRODUCT_ID=cost.PRODUCT_ID)"%(name,name,name))  
                  mycursor.execute("update %s set %s.PRODUCT_NAME=(select PRODUCT_NAME from cost where %s.PRODUCT_ID=cost.PRODUCT_ID)"%(name,name,name))
                  mycursor.execute("update %s set NET_PRICE=PRICE*QUANTITY"%(name))
                  mydb.commit()
        else:
         break
    mycursor.execute("select * from %s where DATE='%s';"%(name,now.strftime("%y-%m-%d")))
    data=mycursor.fetchall()
    TOTAL_COST=0
    purchase_price=0
    print(" ___________________________________________________________________________________________________________________________________________________________")
    print("|                                                                                                                                                           |")                        
    print("|                           ","            _        __   __  __           __   __      __ ___                                                                 |")
    print("|                           ","           |_  |  | |__| |__ |__|    |\/| |__| |__| |/ |__  |                                                                  |")
    print("|                           ","            _| |__| |    |__ |  \    |  | |  | |  \ |\ |__  |                                                                  |")
    print("|                                                                                                                                                           |")
    print("|                                                                                                                                                           |")
    print("|                                                                                                                    DATE:",now.strftime("%d-%m-%y"),"                        |")
    print("|                                                                                                                                                           |")
    print("|                                                                                                                    TIME:",now.strftime(" %H:%M:%S"),"                       |")
    print(tabulate([["|","NAME",customer_name,"","","|"],["|","BILL NO.",bill_no,"","","|"]], headers=['|           ','                 ','                        ','                         ','                                                          ','|                 '],tablefmt="plain"))
    print("|                                                                                                                                                           |")
    print("|                                                                                                                                                           |")
    t = PrettyTable(['        SR NO.        ','        PRODUCT ID        ','        PRODUCT NAME        ','        PRICE        ','        QUANTITY       ','       NET PRICE '])
    for row in data:
       t.add_row([i,row[1],row[2],row[3],row[4],row[5]])
       TOTAL_COST=TOTAL_COST+row[5]
       purchase_price=purchase_price+(row[4]*row[6])
       i=i+1
    CGST=(TOTAL_COST*2.5)/100
    SGST=(TOTAL_COST*2.5)/100
    TOTAL_COST=round((TOTAL_COST+CGST+SGST),4)
    print(t)
    t = PrettyTable(['                                                                                                                                            ','          '])
    t.add_row(["                                                                                                                       TOTAL (WITHOUT TAX)",round((TOTAL_COST-CGST-SGST),4)])
    t.add_row(["                                                                                                                               SGST (2.5%)",SGST])
    t.add_row(["                                                                                                                               CGST (2.5%)",CGST])
    t.add_row(["                                                                                                             TOTAL COST(INCLUDING ALL TAX)",TOTAL_COST])   
    print(t)    
    t = PrettyTable(['                                                             THANK YOU !   PLEASE VISIT AGAIN                                                            '])
    print(t)
    print("")
    print("")    
    mycursor.close
    mydb.close()
    mydb=mysql.connector.connect(host="localhost",user="root",password="1234",database="admin",)
    mycursor = mydb.cursor()
    mycursor.execute("insert into sale values(%s,%s,%s,%s,%s,%s)",(now.strftime("%y-%m-%d"),bill_no,customer_name,customer_contact,purchase_price,TOTAL_COST))
    mydb.commit()
    mycursor.close()
    mydb.close()
    mydb=mysql.connector.connect(host="localhost",user="root",password="1234",database="customer",)
    mycursor = mydb.cursor()
    mycursor.execute("alter table %s  drop column purchase_price"%(name))
    mydb.commit()
    mycursor.close()
    mydb.close()
 if option==2 :
    print("CHOOSE")
    print(" __________________________________________________________________________________________________________________ ")    
    print("|                                                                                                                  |")
    print("|    ____________________      _____________________      ____________     _______________      ______________     |")
    print("|   |                    |    |                     |    |            |   |               |    |              |    |")
    print("|   | 1)EMPLOYEE         |    | 2)PRODUCT           |    | 3) SALE    |   | 4)EXPENDITURE |    | 5)NET PROFIT |    |")
    print("|   |____________________|    |_____________________|    |____________|   |_______________|    |______________|    |")
    print("|                                                                                                                  |")
    print("|__________________________________________________________________________________________________________________|")
    l1=[1,2,3,4,5]
    option=option_input(l1)
    if option==1:
        print(" __________________________________________________________________________________________________________________________________________________")
        print("|                                                                                                                                                  |")
        print("|   _______________________        ____________________________     _________________      ____________________     ________________________       |")
        print("|  |                       |      |                            |   |                 |    |                    |   |                        |      |")
        print("|  | 1) EMPLOYEE DETAILS   |      |  2)  SEARCH EMPLOYEE       |   | 3) ADD EMPLOYEE |    | 4) REMOVE EMPLOYEE |   | 5) UPDATE INFORMATION  |      |")
        print("|  |_______________________|      |____________________________|   |_________________|    |____________________|   |________________________|      |")
        print("|                                                                                                                                                  |")
        print("|__________________________________________________________________________________________________________________________________________________|")
        l2=[1,2,3,4,5]
        o=option_input(l2)
        mydb=mysql.connector.connect(host="localhost",user="root",password="1234",database="admin",)
        mycursor = mydb.cursor()
        if o==1:
            mycursor.execute("select * from employee ORDER BY SALARY DESC")
            data=mycursor.fetchall()
            i=1
            from prettytable import PrettyTable
            t = PrettyTable([' SR NO.   ','    EMPLOYEE ID   ','       EMPLOYEE NAME        ',' GENDER ','       CONTACT        ','        ADRESSS        ','       SALARY        '])
            for row in data:
                 t.add_row([i,row[0],row[1],row[2],row[3],row[4],row[5]])
                 i=i+1
            print(t)
            print("")
            print("")
        if o==2:
          while True:
           while True:    
            try:
             ID=int(input("ENTER EMPLOYEE ID"))
             break
            except:
              print("PLEASE ENTER VALID ID") 
           mycursor.execute("select employee_id from employee where employee_id=%s;"%(ID))
           data=mycursor.fetchall()
           if len(data)==0:
              print("EMPLOYEE ID  ENTERED BY YOU IS NOT IN THE SYSTEM")
              print("")
           else:
             mycursor.execute("select * from employee  where employee_id=%s;"%(ID))
             from prettytable import PrettyTable
             t = PrettyTable(['    EMPLOYEE ID   ','       EMPLOYEE NAME        ',' GENDER ','       CONTACT        ','        ADRESSS        ','       SALARY        '])
             data=mycursor.fetchall()
             for row in data:
              t.add_row([row[0],row[1],row[2],row[3],row[4],row[5]])
             print(t)
             print("")
             break
        if o==3:       
          mydb=mysql.connector.connect(host="localhost",user="root",password="1234",database="admin",)
          mycursor = mydb.cursor()
          print("")
          print("")
          l=[]
          mycursor.execute("select employee_id from employee")
          data=mycursor.fetchall()
          for row in data:
              l.append(row[0])
          ID=max(l)+1
          ID=int(ID)
          while True:          
           name=input("ENTER EMPLOYEE NAME")
           if all(x.isalpha() or x.isspace() for x in name):
             if len(name)!=0:
              break
             else:
                 print("NAME CAN'T BE EMPTY")
           else:
              print("PLEASE ENTER VALID NAME")
          name=name_changer(name)
          CONTACT=contact_no()
          while True:       
              ADDRESS=input("ENTER EMPLOYEE ADDRESS")
              if all(x.isalnum() or x.isspace()  for x in ADDRESS ) :
               if len(ADDRESS)==0:
                   print("ADRESS CAN'T BE EMPTY")
               else:
                  break
              else:
                  print("ADDRESS CAN'T CONTAIN ANY TYPE OF CHARACTER OTHER THAN ALPHABET AND NUMBER")
          ADDRESS=name_changer(ADDRESS)
          i=1
          while True:
           try:
            SALARY=int(input("ENTER SALARY OF EMPLOYEE"))
            if SALARY>0:
                break
            else:
                print("PLEASE ENTER VALID SALARY(SALARY CAN'T BE NEGATIVE)")
           except:
              print("PLEASE ENTER VALID SALARY")
          while True:
           GENDER=input("ENTER GENDER OF EMPLOYEE")
           if GENDER.upper() in ["MALE","FEMALE","OTHERS"] :
              break
           else:
              print("PLEASE ENTER VALID GENDER")
          mycursor.execute("insert into  employee values(%s,'%s','%s',%s,'%s',%s);"%(ID,name,GENDER,CONTACT,ADDRESS,SALARY))
          mydb.commit()
          print("    ")
          print("    _________________________________")
          print("   |  EMPLOYEE ID OF",name,"IS",ID ,"|")
          print("   |_________________________________|")
        if o==4:
          while True:
           try:
              ID=int(input("ENTER EMPLOYEE ID"))
              break
           except:
              print("PLEASE ENTER VALID ID")
          mycursor.execute("select employee_id from employee where employee_id=%s;"%(ID))
          data=mycursor.fetchall()
          if len(data)==0:
              print("EMPLOYEE ID  ENTERED BY YOU IS ALREADY NOT IN THE SYSTEM")
          else:
             mycursor.execute("delete from employee where employee_id=%s;"%(ID))
             mydb.commit()
          print("")
        if o==5:
          print("         _____________________        ______________________         _________________________      _____________________        ")
          print("        |                     |      |                      |       |                         |    |                     |       ")
          print("        | 1) UPDATE NAME      |      | 2)UPDATE CONTACT     |       | 3)UPDATE ADDRESSS       |    | 4) UPDATE SALARY    |       ")
          print("        |_____________________|      |______________________|       |_________________________|    |_____________________|       ")
          l3=[1,2,3,4]
          o=option_input(l3)
          while True:
           while True:              
            try:
               ID=input("ENTER EMPLOYEE ID")
               mycursor.execute("select employee_id from employee where  employee_id=%s;"%(ID))
               data=mycursor.fetchall()
               break
            except:
               print("PLEASE ENTER VALID ID")
           if len(data) == 0:
              print("THE ID YOU HAVE ENTERED DOES NOT EXIST.PLEASE ENTER VALID ID")
           else:
            if o==1:
             while True:
              EMPLOYEE_NAME=input("ENTER NAME OF EMPLOYEE")                 
              if all(x.isalpha() or x.isspace() for x in EMPLOYEE_NAME ):
                  if  len(EMPLOYEE_NAME)==0:
                      print("NAME CAN'T BE EMPTY")
                  else:
                       break
              else:
                  print("NAME CAN'T CONTAIN ANY TYPE OF CHARACTER OTHER THAN ALPHABET")
             EMPLOYEE_NAME=name_changer(EMPLOYEE_NAME)
             mycursor.execute("update employee set EMPLOYEE_NAME='%s' where employee_id=%s;"%(EMPLOYEE_NAME,ID))
             mydb.commit()
            if o==2:
             EMPLOYEE_CONTACT=contact_no()
             mycursor.execute("update employee set CONTACT_NO=%s where employee_id=%s;"%(EMPLOYEE_CONTACT,ID))
             mydb.commit()
            if o==3:
             while True: 
              EMPLOYEE_ADDRESS=input("enter ADDRESS of employee")
              if all(x.isalnum() or x.isspace()  for x in EMPLOYEE_ADDRESS ) :
               if len(EMPLOYEE_ADDRESS)==0:
                   print("ADRESS CAN'T BE EMPTY")
               else:
                  break
              else:
                  print("ADDRESS CAN'T CONTAIN ANY TYPE OF CHARACTER OTHER THAN ALPHABET AND NUMBER")
             EMPLOYEE_ADDRESS=name_changer(EMPLOYEE_ADDRESS)
             mycursor.execute("update employee set ADDRESS='%s' where employee_id=%s;"%(EMPLOYEE_ADDRESS,ID))
             mydb.commit()
            if o==4:
             i=1
             while True:
              try:
                 EMPLOYEE_SALARY=int(input("ENTER SALARY OF EMPLOYEE"))
                 if EMPLOYEE_SALARY >0:
                     break
                 elif EMPLOYEE_SALARY==0:
                     print("SALARY CAN'T BE ZERO")
                 else:
                     print("SALARY CANT BE NEGATIVE")
              except:
                 print("PLEASE ENTER VALID SALARY")
             mycursor.execute("update employee set SALARY=%s where employee_id=%s;"%(EMPLOYEE_SALARY,ID))
             mydb.commit()
            break  
          print("")
          print("")            
    if option==2:
      mydb=mysql.connector.connect(host="localhost",user="root",password="1234",database="customer",)
      mycursor = mydb.cursor()
      print("       ___________________            _____________________        ______________________      _________________________        ")
      print("      |                   |          |                     |      |                      |    |                         |")
      print("      | 1)PRODUCT DETAILS |          | 2) DELETING PRODUCT |      | 3)ADDING NEW PRODUCT |    | 4) MODIFY PRODUCT PRICE |    ")
      print("      |___________________|          |_____________________|      |______________________|    |_________________________|     ")
      l4=[1,2,3,4]
      o=option_input(l4)
      if o==1:
          mycursor.execute("select * from cost ORDER BY PRODUCT_ID")
          data=mycursor.fetchall()
          t = PrettyTable(["   PRODUCT ID    ","   PRODUCT NAME      ","   PURCHASE PRICE     ","  SELLING PRICE   "])          
          for row in data:
               t.add_row([row[0],row[1],row[2],row[3]])
          print(t)
          print("")
      if o==2:
        while True:
         try:   
          ID=int(input("ENTER PRODUCT ID OF PRODUCT WHICH YOU WANT TO DELETE"))
          break
         except:
             print("PLEASE ENTER VALID ID")
        mycursor.execute("select PRODUCT_ID from cost where PRODUCT_ID=%s;"%(ID))
        data=mycursor.fetchall()
        if len(data)==0:
             print("PRODUCT ID",ID,"IS ALREADY NOT IN THE SYSTEM ")
        else:
            mycursor.execute("delete from cost where PRODUCT_ID=%s;"%(ID))
            mydb.commit()
        print("")
        print("")
      if o==3:
       print("TYPE 0 FOR STOP ADDING ")
       print("")
       l=[]
       mycursor.execute("select PRODUCT_ID from cost")
       data=mycursor.fetchall()
       for row in data:
           l.append(row[0])
       while True:
         while True:
           try:
            ID=int(input("ENTER PRODUCT ID OF PRODUCT WHICH YOU WANT TO ADD"))
            if ID not in l:
             break
            else:
                print("ID ENTERED BY YOU IS ALREADY IN THE SYSTEM")
           except:               
                print("PLEASE ENTER VALID PRODUCT ID")
         if ID==0:
              break
         else:     
          while True:
           name=input("enter product name")
           if all(x.isalnum or x.isspace() for x in name):
            if len(name)==0:
                print("NAME CAN'T BE EMPTY")
            else:
                break
           else:
               print("PLEASE ENTER VALID NAME")
          name=name_changer(name)  
          while True:            
           try:
            purchase_price=int(input("enter purchase price"))
            if purchase_price>0:
                break
            elif purchase_price==0:
                print("PURCHASE PRICE CAN'T BE ZERO")
            else:
                print("PURCHASE PRICE CAN'T BE NEGATIVE")
           except:
              print("PURCHASE PRICE CAN ONLY CONTAIN NUMBER")
          while True:            
           try:
            price=int(input("ENTER SELL PRICE"))
            if price>0 and purchase_price<price:
                break
            elif price==0:
                print(" PRICE CAN'T BE ZERO")
            elif purchase_price>price:
                print("SELLING PRICE CAN'T BE LESS THAN PURCHASE PRICE ")
            else:
                print(" PRICE CAN'T BE NEGATIVE")
           except:
              print(" PRICE CAN ONLY CONTAIN NUMBER")            
          mycursor.execute("insert into cost values(%s,'%s',%s,%s)"%(ID,name,purchase_price,price))
          mydb.commit()           
      if o==4:
         i=1
         l=[]
         mycursor.execute("select PRODUCT_ID from cost")
         data=mycursor.fetchall()
         for row in data:
           l.append(row[0])
         while True:
          while True:
           try:
            ID=int(input("enter product ID"))
            break
           except:
               print("PLEASE ENTER VALID ID")
          if ID in l:
           while True:            
            try:
             purchase_price=int(input("enter purchase price"))
             if purchase_price>0:
                break
             elif purchase_price==0:
                print("PURCHASE PRICE CAN'T BE ZERO")
             else:
                print("PURCHASE PRICE CAN'T BE NEGATIVE")
            except:
              print("PURCHASE PRICE CAN ONLY CONTAIN NUMBER")
           while True:            
            try:
             price=int(input("ENTER SELL PRICE"))
             if price>0 and purchase_price<price:
                break
             elif price==0:
                print(" PRICE CAN'T BE ZERO")
             elif purchase_price>price:
                print("SELLING PRICE CAN'T BE LESS THAN PURCHASE PRICE ")
             else:
                print(" PRICE CAN'T BE NEGATIVE")
            except:
              print(" PRICE CAN ONLY CONTAIN NUMBER")
           mycursor.execute("update cost set price=%s,purchase_price=%s where PRODUCT_ID=%s"%(price,purchase_price,ID))
           mydb.commit()
           print("your changes have been recorded")
           mydb.close()
           mycursor.close()
           break
          else:
              print("")
              print("PROODUCT ID ENTERED BY YOU DOES NOT EXIST")  
    if  option==3:
        print("         _____________________        ______________________         _________________________            ")
        print("        |                     |      |                      |       |                         |        ")
        print("        | 1) TODAYS SALE      |      | 2)MONTHWISE SALE     |       | 3) YEARWISE SALE        |        ")
        print("        |_____________________|      |______________________|       |_________________________|        ")
        print("")
        l=[1,2,3]
        o=option_input(l)
        mydb=mysql.connector.connect(host="localhost",user="root",password="1234",database="admin",)
        mycursor = mydb.cursor()
        i=1
        if o==1:
            mycursor.execute("select * from sale where DATE='%s';"%(now.strftime("%y-%m-%d")))
            data=mycursor.fetchall()
            from prettytable import PrettyTable
            t = PrettyTable(['      SR NO.    ','        DATE        ','          CUSTOMER NAME             ','        CONTACT      ','   TOTAL PURCHASE COST ','        TOTAL COST       '])
            for row in data:
             t.add_row([i,row[0],row[1],row[2],row[3],row[4]])
             i=i+1
            print(t)
            print("")             
        if o==2:
            m=month_input()
            y=year_input()
            mycursor.execute("SELECT * FROM sale WHERE YEAR(Date) = %s AND MONTH(Date) = %s;"%(y,m))
            data=mycursor.fetchall()
            from prettytable import PrettyTable
            t = PrettyTable(['      SR NO.    ','        DATE        ','          CUSTOMER NAME             ','        CONTACT      ','   TOTAL PURCHASE COST ','        TOTAL COST       '])            
            for row in data:
             t.add_row([i,row[0],row[1],row[2],row[3],row[4]])
             i=i+1                          
            print(t)
            print("")
            print("")                                    
        if o==3:
            Y=year_input()
            mycursor.execute("select * from sale where YEAR(Date) = %s;"%(Y))
            data=mycursor.fetchall()
            from prettytable import PrettyTable
            t = PrettyTable(['      SR NO.    ','        DATE        ','          CUSTOMER NAME             ','        CONTACT      ','   TOTAL PURCHASE COST ','        TOTAL COST       '])
            for row in data:
             t.add_row([i,row[0],row[1],row[2],row[3],row[4]])
             i=i+1
            print(t)
            print("")
            print("")                         
    if option ==5:
               print("         _____________________        ______________________         ")
               print("        |                     |      |                      |        ")
               print("        | 1) MONTH WISE PROFIT|      | 2) YEAR WISE PROFIT  |       ")
               print("        |_____________________|      |______________________|        ")           
               mydb=mysql.connector.connect(host="localhost",user="root",password="1234",database="admin",)
               mycursor = mydb.cursor()
               l=[1,2]
               o=option_input(l)
               expenditure=0
               TOTAL_PURCHASE_AMOUNT=0
               total_amount=0  
               if o==1:
                   m=month_input()
                   y=year_input()
                   mycursor.execute("SELECT expenditure_amount FROM expenditure WHERE YEAR(Date) = %s AND MONTH(Date) = %s;"%(y,m))
                   data=mycursor.fetchall()
                   for row in data:
                      expenditure=expenditure+row[0]
                   mycursor.execute("SELECT TOTAL_PURCHASE_AMOUNT,total_amount FROM sale WHERE YEAR(Date) = %s AND MONTH(Date) = %s;"%(y,m))
                   data=mycursor.fetchall()
                   print("NOTE: THIS PROFIT IS WITH RESPECT TO THE PRODUCTS WHICH ARE BEEN SOLD,THIS DOES NOT INCLUDE PURCHASE AMOUNT  OF PRODUCTS WHICH ARE NOW SOLD TILL NOW ")
                   for row in data:
                      TOTAL_PURCHASE_AMOUNT=TOTAL_PURCHASE_AMOUNT+row[0]
                      total_amount=total_amount+row[1]
                   from prettytable import PrettyTable
                   t = PrettyTable(["TOTAL SELL AMOUNT",total_amount])
                   t.add_row(["TOTAL EXPENDITURE(INCLUDING SALARY OF EMPLOYEE)",expenditure])
                   t.add_row(["TOTAL PURCHASE AMOUNT",TOTAL_PURCHASE_AMOUNT])
                   print(t)
                   NET_PROFIT=total_amount-expenditure-TOTAL_PURCHASE_AMOUNT
                   table = []
                   headers = ["NET PROFIT  ",NET_PROFIT]
                   print(tabulate(table, headers, tablefmt="grid"))
               if o ==2:
                   y=year_input()
                   mycursor.execute("SELECT expenditure_amount FROM expenditure WHERE YEAR(Date) = %s ;"%(y))
                   data=mycursor.fetchall()
                   for row in data:
                      expenditure=expenditure+row[0]
                   mycursor.execute("SELECT TOTAL_PURCHASE_AMOUNT,total_amount FROM sale WHERE YEAR(Date) = %s;"%(y))
                   data=mycursor.fetchall()
                   print("NOTE: THIS PROFIT IS WITH RESPECT TO THE PRODUCTS WHICH ARE BEEN SOLD,THIS DOES NOT INCLUDE PURCHASE AMOUNT  OF PRODUCTS WHICH ARE NOW SOLD TILL NOW ")
                   for row in data:
                      TOTAL_PURCHASE_AMOUNT=TOTAL_PURCHASE_AMOUNT+row[0]
                      total_amount=total_amount+row[1]
                   from prettytable import PrettyTable
                   t = PrettyTable(["TOTAL SELL AMOUNT",total_amount])
                   t.add_row(["TOTAL EXPENDITURE(INCLUDING SALARY OF EMPLOYEE)",expenditure])
                   t.add_row(["TOTAL PURCHASE AMOUNT",TOTAL_PURCHASE_AMOUNT])
                   print(t)
                   NET_PROFIT=total_amount-expenditure-TOTAL_PURCHASE_AMOUNT
                   table = []
                   headers = ["NET PROFIT",NET_PROFIT]
                   print(tabulate(table, headers, tablefmt="grid"))
    if option ==4:
               print("         ___________________________________        __________________________________    _____________________   ")
               print("        |                                   |      |                                  |  |                     |")
               print("        | 1) ADD EXPENDITURE(WITHOUT SALARY)|      | 2) ADD SALARY GIVEN TO EMPLOYEE  |  | 3) EXPENDIYURE LIST |   ")
               print("        |___________________________________|      |__________________________________|  |_____________________|     ")         
               mydb=mysql.connector.connect(host="localhost",user="root",password="1234",database="admin",)
               mycursor = mydb.cursor()
               l=[1,2,3]
               o=option_input(l)
               if o==1:
                     while True:
                      expenditure=input("DESCRIBE EXPENDITURE")
                      if len(expenditure)==0:
                          print("PLEASE DECRIBE EXPENDITURE")
                      else:
                          break
                     expenditure=name_changer(expenditure)
                     while True:
                      try:
                       amount=int(input("EXPENDITURE AMOUNT"))
                       if amount >0:
                           break
                       else:
                           print("PLEASE ENTER VALID AMOUNT")
                      except:
                         print("PLEASE ENTER VALID AMOUNT")
                     mycursor.execute("insert into expenditure values(%s,%s,%s)",(now.strftime('%y-%m-%d'),expenditure,amount))
                     mydb.commit()                     
               if o==2:
                     mycursor.execute("select employee_id from employee")
                     data=mycursor.fetchall()
                     LI=[]
                     for row in data:
                         LI.append(row[0])
                     while True:
                      try:
                         ID=int(input("employee ID"))
                         if ID in LI:
                             break
                         else:
                            print("PLEASE ENTER VALID EMPLOYEE ID")
                      except:
                         print("PLEASE ENTER VALID ID")
                     m=month_input()
                     y=year_input()
                     date = datetime.datetime(y, m, 28)
                     mycursor.execute("select EMPLOYEE_NAME,SALARY from employee where employee_id=%s;"%(ID))
                     data=mycursor.fetchall()
                     for row in data:
                      EMPLOYEE_NAME=row[0]
                      SALARY=row[1]
                     description_expenditure=str(ID)+"_"+EMPLOYEE_NAME+"_"+"SALARY"
                     mycursor.execute("insert into expenditure values(%s,%s,%s)",(date.strftime('%y/%m/%d'),description_expenditure,SALARY))
                     mydb.commit()
               if o==3:
                     print("         _______________________        __________________________         _________________________            ")
                     print("        |                       |      |                          |       |                         |        ")
                     print("        | 1) TODAYS EXPENDITURE |      | 2) MONTHWISE EXPENDITURE |       | 3) YEARWISE EXPENDITURE |        ")
                     print("        |_______________________|      |__________________________|       |_________________________|        ")
                     print("")
                     l=[1,2,3]
                     o=option_input(l)
                     mydb=mysql.connector.connect(host="localhost",user="root",password="1234",database="admin",)
                     mycursor = mydb.cursor()
                     from prettytable import PrettyTable
                     i=1
                     if o==1:                       
                         mycursor.execute("select * from expenditure where DATE='%s';"%(now.strftime("%y-%m-%d")))
                         data=mycursor.fetchall()
                         t = PrettyTable(["SR NO.","  DATE  ","DESCRIPTION OF EXPENDITURE","AMOUNT OF EXPENDITURE"])
                         for row in data:
                             t.add_row([i,row[0],row[1],row[2]])
                             i=i+1
                         print(t)    
                     if o==2:
                      m=month_input()
                      y=year_input()
                      mycursor.execute("SELECT * FROM expenditure WHERE YEAR(Date) = %s AND MONTH(Date) = %s;"%(y,m))
                      data=mycursor.fetchall()
                      t = PrettyTable(["SR NO.","  DATE  ","DESCRIPTION OF EXPENDITURE","AMOUNT OF EXPENDITURE"])
                      for row in data:
                       t.add_row([i,row[0],row[1],row[2]])
                       i=i+1
                      print(t)                                   
                     if o==3:
                         y=year_input()
                         mycursor.execute("SELECT * FROM expenditure WHERE YEAR(Date) = %s;"%(y))
                         data=mycursor.fetchall()
                         t = PrettyTable(["SR NO.","  DATE  ","DESCRIPTION OF EXPENDITURE","AMOUNT OF EXPENDITURE"])
                         for row in data:
                             t.add_row([i,row[0],row[1],row[2]])
                             i=i+1
                         print(t)    










