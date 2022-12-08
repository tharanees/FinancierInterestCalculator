#This program is not for direct bank deposit. 
#This is used in instances when the borrower repays the sum by cheque.

#strftime() function, converts datetime object to a string.
#strptime() function, which converts string to a datetime object
from datetime import datetime,timedelta
def validate(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%d/%m/%Y").strftime('%d/%m/%Y'):
            raise ValueError
        return True
    except ValueError:
        return False
dates=[]
array=[]
#Bank Holidays.txt file contains bank holidays (DD/MM/YYYY) separated by tabs
filehandle=open("Bank Holidays.txt","r")
line=filehandle.readline()
filehandle.close()
total_amount=0
weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
customerName = (input("Enter the name of the borrower: ")).upper()
start_date=input("Enter date as DD/MM/YYYY, the finanacier lends money to "+customerName + ": ") #date written on ur chq issued
ans=validate(start_date)
while ans == False:
    print("Wrong date format entered. Please enter the data as DD/MM/YYYY")
    start_date=input("Enter date as DD/MM/YYYY, the finanacier lends money to "+customerName + ": ") 
    ans=validate(start_date)
DD,MM,YYYY=start_date.split("/") # for file name purpose
START_DATE = datetime.strptime(start_date, "%d/%m/%Y")
date_he_gave=input("Enter date as DD/MM/YYYY, when "+customerName+" repaid the loan borrowed by giving cheques to lender: ")#write the data on which borrower came and gave u the payment chqs
ans=validate(date_he_gave)
while ans == False:
    print("Wrong date format entered. Please enter the data as DD/MM/YYYY")
    date_he_gave=input("Enter date as DD/MM/YYYY, when "+customerName+" repaid the loan borrowed by giving cheques to lender: ")
    ans=validate(date_he_gave)
DATE_HE_GAVE=datetime.strptime(date_he_gave, "%d/%m/%Y")
modified_date_he_gave = DATE_HE_GAVE+ timedelta(days=1)
next_date_he_gave=datetime.strftime(modified_date_he_gave, "%d/%m/%Y")
NEXT_DATE_HE_GAVE=datetime.strptime(next_date_he_gave, "%d/%m/%Y")
actual_next_date_he_gave=NEXT_DATE_HE_GAVE
amt_u_gave=float(input("Enter amount the financier lended to "+customerName+ ": "))
previous_balance=float(input("Enter any previous balance due if available: "))
actual_previous_balance=previous_balance
filename=customerName+"-"+DD+"-"+MM+"-"+YYYY+"-"+str("{0:,.2f}".format(amt_u_gave))+".doc"
file=open(filename,"w")
total_interest=0
file.write("{0:<14s}{1:<14s}{2:<10s}{3:>16s}{4:>16s}".format("DATE","CHEQUE NO","DAYS","AMOUNT","INTEREST"))
file.write("\n")
file.write("-"*70)
file.write("\n")
Choice="Y"
while Choice=="Y":
    cheque_no=input("Enter the cheque number of the cheque given by "+customerName+": ")
    cheque_date=input("Enter the date on cheque "+cheque_no +": ")
    ans=validate(cheque_date)
    while ans == False:
        print("Wrong date format entered. Please enter the data as DD/MM/YYYY")
        cheque_date=input("Enter the date on cheque "+cheque_no +": ")
        ans=validate(cheque_date)
    actual_date=cheque_date#storing the date of cheque issued by borrower for later reference
    CHEQUE_DATE = datetime.strptime(cheque_date, "%d/%m/%Y")
    dates.append(actual_date) # for sorting date in ascending order purpose
    cheque_amt=float(input("Enter the amount on cheque "+cheque_no +": "))
    total_amount+=cheque_amt
    working_day=0
    holiday=0
    if CHEQUE_DATE>=START_DATE:
        delta=CHEQUE_DATE-START_DATE
        daycount=delta.days
        #allocating 3 working days for all bank cheques to be cleared.
        while working_day!=3:
            CHEQUE_DATE_DAY = CHEQUE_DATE.weekday()
            thisXMasDayAsString = weekDays[CHEQUE_DATE_DAY]
            DAY="{}".format(thisXMasDayAsString)
            #check if the cheque date is a bank holiday
            position=line.find(cheque_date)
            if DAY=="Saturday" or DAY=="Sunday" or position!=-1:
                #count how many bank holidays come in between.
                holiday+=1
            else:
                working_day+=1
            modified_date = CHEQUE_DATE+ timedelta(days=1)
            next_date=datetime.strftime(modified_date, "%d/%m/%Y")
            cheque_date=next_date
            CHEQUE_DATE=datetime.strptime(cheque_date, "%d/%m/%Y")
        no_of_days=int(daycount+holiday+3)
        #financier charges 2.5% interest per month.
        interest=(no_of_days*0.025*cheque_amt)/30
        array_line=actual_date+"!"+cheque_no+"!"+str(no_of_days)+"!"+"{0:,.2f}".format(cheque_amt)+"!"+"{0:,.2f}".format(interest)
        array.append(array_line)
        total_interest+=interest
    else:
        #if borrower gives the financier any pass dated cheques today, financier can bank them only the next day (if next day is a working day)
        delta=NEXT_DATE_HE_GAVE-START_DATE
        daycount=delta.days
        while working_day!=3:
            #if he gives me some pass dated payment chqs on 10th i m checking if 11th is workind day or not
            NEXT_DATE_HE_GAVE_DAY = NEXT_DATE_HE_GAVE.weekday()
            thisXMasDayAsString = weekDays[NEXT_DATE_HE_GAVE_DAY]
            DAY="{}".format(thisXMasDayAsString)
            position=line.find(next_date_he_gave)
            if DAY=="Saturday" or DAY=="Sunday" or position!=-1:
                holiday+=1
            else:
                working_day+=1
            modified_date = NEXT_DATE_HE_GAVE+ timedelta(days=1)
            next_date=datetime.strftime(modified_date, "%d/%m/%Y")
            next_date_he_gave=next_date
            NEXT_DATE_HE_GAVE=datetime.strptime(next_date_he_gave, "%d/%m/%Y")
        NEXT_DATE_HE_GAVE=actual_next_date_he_gave
        no_of_days=int(daycount+holiday+3)
        interest=(no_of_days*0.025*cheque_amt)/30
        array_line=actual_date+"!"+cheque_no+"!"+str(no_of_days)+"!"+"{0:,.2f}".format(cheque_amt)+"!"+"{0:,.2f}".format(interest)
        array.append(array_line)
        total_interest+=interest
    Choice=(input("Enter Y, if there are more cheques to be entered else enter N and exit: ")).upper()
    while Choice!="Y" and Choice!="N":
        print("Wrong choice entered. Please enter Y or N only")
        Choice=(input("Enter Y, if there are more cheques to be entered else enter N and exit: ")).upper()
subscript=0
index=0
dates.sort(key=lambda date: datetime.strptime(date, "%d/%m/%Y"))
#now dates array is sorted
while index<len(dates):
    if (array[subscript])[:10]!=dates[index]:
        subscript+=1
    else:
        actual_date,cheque_no,no_of_days,cheque_amt,interest=array[subscript].split("!")
        file.write("{0:<14s}{1:<14s}{2:<10.0f}{3:>16s}{4:>16s}".format(actual_date,cheque_no,int(no_of_days),cheque_amt,interest))
        file.write("\n")
        file.write("\n")
        array[subscript]="$$$$$$$$$$$"
        index+=1
        subscript=0
file.write("-"*70)
file.write("{0:<54s}{1:>16s}".format("TOTAL INTEREST:","{0:,.2f}".format(total_interest)))
file.write("\n")
file.write("\n")
file.write("{0:<54s}{1:>16s}".format("AMOUNT GIVEN "+ start_date+":","{0:,.2f}".format(amt_u_gave)))
file.write("\n")
file.write("\n")
if previous_balance>=0:
    file.write("{0:<54s}{1:>16s}".format("ARREARS:","{0:,.2f}".format(previous_balance)))
    file.write("\n")
    file.write("\n")
    file.write("{0:<38s}{1:>16s}{2:>17s}".format("CHEQUE RECEIVED:","{0:,.2f}".format(total_amount),"("+"{0:,.2f}".format(total_amount)+")"))
    file.write("\n")
    file.write("{0:<38s}{1:<33s}".format("","-"*33))
    file.write("\n")  
else:
    if previous_balance<0:
        previous_balance=str(previous_balance)
        previous_balance=float(previous_balance[1:])
        file.write("{0:<38s}{1:>16s}".format("ARREARS:","{0:,.2f}".format(previous_balance)))
        file.write("\n")
        file.write("\n")
        negative_amt=previous_balance+total_amount
        file.write("{0:<38s}{1:>16s}{2:>17s}".format("CHEQUE RECEIVED:","{0:,.2f}".format(total_amount),"("+"{0:,.2f}".format(negative_amt)+")"))
        file.write("\n")
        file.write("{0:<38s}{1:<33s}".format("","-"*33))
        file.write("\n")
actual_balance=total_interest+amt_u_gave+actual_previous_balance-total_amount
if actual_balance>=0:
    file.write("{0:<54s}{1:>16s}".format("BALANCE:","{0:,.2f}".format(actual_balance)))
else:
    actual_balance=str(actual_balance)
    actual_balance=float(actual_balance[1:])
    file.write("{0:<54s}{1:>17s}".format("BALANCE:","("+"{0:,.2f}".format(actual_balance)+")"))
file.write("\n")
file.write("{0:<54s}{1:>17s}".format("","="*17))
file.close()
