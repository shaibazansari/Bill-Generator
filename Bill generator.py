import datetime
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

d_date = datetime.datetime.now()
# create root window
root=Tk()
root.title("Bill Management system")
# get screen resolution
rw=root.winfo_screenwidth()
rh=root.winfo_screenheight()
# root.geometry("1200x800")
root.geometry(("%dx%d" % (rw,rh)))
#=================MainTreeView======================
billsTV = ttk.Treeview(root,height=15)

#-----------------Assigning list---------------------
itemnamelist=[]
ratelist=[]
quantitylist=[]
costlist=[]
#----------------ENTRY VARIABLES----------------------
addItemNameVar=StringVar()
addItemRateVar=StringVar()
addItemQuantityVar=StringVar()
addItemCostVar=StringVar()
addItemNoVar=StringVar()
addFileNameVar=StringVar()
deleteItemNameVar=StringVar()

def quantityFieldListener(a,b,c):
    global addItemQuantityVar
    global addItemCostVar
    global addItemRateVar
    rate=addItemRateVar.get()
    quantity = addItemQuantityVar.get()
    if quantity != "":
        try:
            quantity=int(quantity)
            rate=int(rate)
            cost = quantity*rate
            addItemQuantityVar.set(quantity)
            addItemCostVar.set("%.2f"%cost)
        except ValueError:
            quantity=quantity[:-1]
            addItemQuantityVar.set(quantity)
    else:
        quantity=""
        addItemQuantityVar.set(quantity)

def costFieldListener(a,b,c):
    global addItemQuantityVar
    global addItemCostVar
    global addItemRateVar
    rate=addItemRateVar.get()
    cost = addItemCostVar.get()
    if cost !="":
        try:
            cost = float(cost)
            rate=float(rate)
            quantity=cost/rate
            quantity_int=int(quantity)
            addItemQuantityVar.set(quantity_int)
            addItemCostVar.set("%.2f"%cost)
        except ValueError:
            cost=cost[:-1]
            addItemCostVar.set(cost)
    else:
        cost=""
        addItemCostVar.set(cost)

#---------------------Tracing the Entries-------------------
addItemQuantityVar.trace('w',quantityFieldListener)
addItemCostVar.trace('w',costFieldListener)

def remove_all_widgets():
    global root
    for widget in root.winfo_children():
        widget.place_forget()   

def addupdateitem():
    str1=addItemNameVar.get()
    str2=addItemRateVar.get()
    str3=addItemQuantityVar.get()
    str4=addItemCostVar.get()
    str5=addItemNoVar.get()
    new=int(str5)
    if str1.isalnum():
        if str2.isdigit() and str3.isdigit():
            itemnamelist[new-1]=str1
            ratelist[new-1]=str2
            quantitylist[new-1]=str3
            costlist[new-1]=str4
            showitem()
        else:
            messagebox.showinfo("Note","Rate & Quantity value should be numeric")
            root.deiconify()

def delete_selected():
    selected_item= billsTV.selection()[0]
    values = list(billsTV.item(selected_item)['values'])
    str1=selected_item[len(selected_item)-1]
    c=0
    for i in itemnamelist:
        c=c+1
        if i==values[0]:
            n=c
    print(n)
    billsTV.delete(selected_item)
    showitem()
    del itemnamelist[n-1]
    del ratelist[n-1]
    del quantitylist[n-1]
    del costlist[n-1]
    showitem()

def placeitem():
    n=len(itemnamelist)
    billsTV.insert("",'end',text=n,values=(itemnamelist[n-1],ratelist[n-1],quantitylist[n-1],costlist[n-1]))

def showitem():
    n=len(itemnamelist)
    for i in billsTV.get_children():
        billsTV.delete(i)
    for i in range(0,n):
        billsTV.insert("",'end',text=i+1,values=(itemnamelist[i],ratelist[i],quantitylist[i],costlist[i]))

def printbill():
    top=Toplevel()
    top.title("Save Bill")
    top.geometry("350x200+600+350")
    def createfile():
        amount=0
        costint=[]
        filename=addFileNameVar.get()
        fob=open(filename+'.txt','w+')
        fob.write('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
        filedatetime=d_date.strftime("  %d-%m-%Y\t\t\t\t\t  Bill Generator\t\t\t\t\t  %I:%M:%S %p")
        fob.write(filedatetime)
        fob.write('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n')
        fob.write('\t\t\tItemname\t\t'+'Rate\t\t'+'Quantity\t'+'Amount\n')
        for i in range(0,len(itemnamelist)):
            fob.write('\n\t\t\t{0}\t\t\t  {1}\t\t   {2}\t\t   {3}'.format(itemnamelist[i],ratelist[i],quantitylist[i],costlist[i]))
        for i in range(0,len(costlist)):
            new=float(costlist[i])
            costint.append(new)
            amount=amount+costint[i]
        fob.write('\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        fob.write('\n\t\t\tTotal amount:\t\t\t\t\t\t   {0} Rs'.format(amount))
        fob.write('\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        fob.close()
        messagebox.showinfo("Note",f"Your bill file is successfully saved in {filename}.txt format")
        top.deiconify()
        top.mainloop()
        try:
            top.destroy()
        except:
            pass
    L1=Label(top,text="Enter File name and press Enter",font=('Arial',14),fg="red")
    filename=Entry(top,textvariable=addFileNameVar, bd=5)
    button=Button(top,text="Enter",width=15,height=2,cursor="hand2",command=createfile)
    L1.pack()
    filename.pack()
    button.pack()

def updateitem():

    remove_all_widgets()
    showitem()
    
    titlelabel=Label(root,text="Billing System ",font=('Arial',40),bg="gray85")
    titlelabel.place(x=600,y=50)

    itemNOLabel= Label(root, text="Item NO",font=('Arial',14),bg="gray85")
    itemNOLabel.place(x=150, y=150)

    itemNOEntry= Entry(root,textvariable=addItemNoVar,width=10,bd=5)
    itemNOEntry.place(x=150, y=200)

    itemNameLabel= Label(root, text="Item Name",font=('Arial',14),bg="gray85")
    itemNameLabel.place(x=300, y=150)

    itemNameEntry= Entry(root,textvariable=addItemNameVar, width=25,bd=5)
    itemNameEntry.place(x=450, y=150)

    itemRateLabel= Label(root, text="Rate",font=('Arial',14),bg="gray85")
    itemRateLabel.place(x=775, y=150)
    
    itemRateEntry= Entry(root,textvariable=addItemRateVar,width=25,bd=5)
    itemRateEntry.place(x=875, y=150)

    itemQuantityLabel= Label(root, text="Quantity",font=('Arial',14),bg="gray85")
    itemQuantityLabel.place(x=300, y=200)
    
    itemQuantityEntry= Entry(root,textvariable=addItemQuantityVar,width=25,bd=5)
    itemQuantityEntry.place(x=450, y=200)

    itemCostLabel= Label(root, text="Cost",font=('Arial',14),bg="gray85")
    itemCostLabel.place(x=775, y=200)
    
    itemCostEntry= Entry(root,textvariable=addItemCostVar,width=25,bd=5)
    itemCostEntry.place(x=875, y=200)


    def clearEntry():
        itemNOEntry.delete(0,END)
        itemNameEntry.delete(0,END)
        itemQuantityEntry.delete(0,END)
        itemCostEntry.delete(0,END)
        itemRateEntry.delete(0,END)
    clearEntry()

    backbutton=Button(root,text="<< Back",width=15,bd=1,height=2,bg="lightyellow4",cursor="hand2",command=mainwindow)
    backbutton.place(x=300,y=260)

    clearentrybutton=Button(root,text="Clear Entry",bd=1,width=15,height=2,bg="lightyellow4",cursor="hand2",command=clearEntry)
    clearentrybutton.place(x=600,y=260)

    updateitembutton=Button(root,text="Update Item",bd=1,width=15,height=2,cursor="hand2",bg="lightyellow4",command=addupdateitem)
    updateitembutton.place(x=925,y=260)

    billLabel=Label(root, text="Bill Preview", font="Arial 25",fg="gray25",bg="gray85")
    billLabel.place(x=600,y=340)

    billsTV.place(x=150,y=400)

    scrollBar = ttk.Scrollbar(root, orient="vertical",command=billsTV.yview)
    scrollBar.place(x=1150,y=400,height=330)

    billsTV.configure(yscrollcommand=scrollBar.set)
    
    billsTV["columns"]=("1","2","3","4")
    #billsTV['show']='headings'      //removes th 0th column
    
    billsTV.heading('#0',text="NO.")
    billsTV.heading('#1',text="ITEM NAME")
    billsTV.heading('#2',text="RATE")
    billsTV.heading('#3',text="QUANTITY")
    billsTV.heading('#4',text="COST")


    cancelbutton=Button(root,text="Close",width=15,height=2,bg="lightyellow4",bd=1,cursor="hand2",command=root.destroy)
    cancelbutton.place(x=160,y=750)
    
def mainwindow():

    def clearEntry():
        itemNameEntry.delete(0,END)
        itemQuantityEntry.delete(0,END)
        itemCostEntry.delete(0,END)
        itemRateEntry.delete(0,END)

    
    remove_all_widgets()
    showitem()
    
    titlelabel=Label(root,text="Billing System ",font=('Arial',40),bg="gray85")
    titlelabel.place(x=550,y=50)

    itemNameLabel= Label(root, text="Item Name",font=('Arial',14),bg="gray85")
    itemNameLabel.place(x=300, y=150)

    itemNameEntry= Entry(root,textvariable=addItemNameVar, width=25,bd=5)
    itemNameEntry.place(x=450, y=150)

    itemRateLabel= Label(root, text="Rate",font=('Arial',14),bg="gray85")
    itemRateLabel.place(x=775, y=150)
    
    itemRateEntry= Entry(root,textvariable=addItemRateVar,width=25,bd=5)
    itemRateEntry.place(x=875, y=150)
    
    itemQuantityLabel= Label(root, text="Quantity",font=('Arial',14),bg="gray85")
    itemQuantityLabel.place(x=300, y=200)
    
    itemQuantityEntry= Entry(root,textvariable=addItemQuantityVar,width=25,bd=5)
    itemQuantityEntry.place(x=450, y=200)
    
    itemCostLabel= Label(root, text="Cost",font=('Arial',14),bg="gray85")
    itemCostLabel.place(x=775, y=200)

    itemCostEntry= Entry(root,textvariable=addItemCostVar,width=25,bd=5)
    itemCostEntry.place(x=875, y=200)

    clearEntry()
    billLabel=Label(root, text="Bill Preview", font="Arial 25",fg="gray25",bg="gray85")
    billLabel.place(x=600,y=340)

    billsTV.place(x=150,y=400)

    scrollBar = ttk.Scrollbar(root, orient="vertical",command=billsTV.yview)
    scrollBar.place(x=1150,y=400,height=330)

    billsTV.configure(yscrollcommand=scrollBar.set)
    
    billsTV["columns"]=("1","2","3","4")
    #billsTV['show']='headings'      //removes th 0th column
    
    billsTV.heading('#0',text="NO.")
    billsTV.heading('#1',text="ITEM NAME")
    billsTV.heading('#2',text="RATE")
    billsTV.heading('#3',text="QUANTITY")
    billsTV.heading('#4',text="COST")
    
    def additem():
        str1=addItemNameVar.get()
        str2=addItemRateVar.get()
        str3=addItemQuantityVar.get()
        str4=addItemCostVar.get()
        if str1.isalnum():
            if str2.isdigit() and str3.isdigit():
                itemnamelist.append(str1)
                ratelist.append(str2)
                quantitylist.append(str3)
                costlist.append(str4)
                placeitem()
                clearEntry()
            else:
                messagebox.showinfo("Note","Rate & Quantity value should be numeric")
                root.deiconify()
    
    cancelbutton=Button(root,text="Close",width=15,height=2,bg="lightyellow4",bd=1,cursor="hand2",command=root.destroy)
    cancelbutton.place(x=160,y=750)

    printbillbutton=Button(root,text="Print",bd=1,width=15,bg="lightyellow4",cursor="hand2",height=2,command=printbill)
    printbillbutton.place(x=1030,y=750)

    updateitembutton=Button(root,text="Update",width=15,bg="lightyellow4",bd=1,cursor="hand2",height=2,command=updateitem)
    updateitembutton.place(x=300,y=260)

    deletebutton=Button(root,text="Delete Selected",bg="lightyellow4",bd=1,width=19,height=2,cursor="hand2", command=delete_selected)
    deletebutton.place(x=600,y=260)
        
    additembutton=Button(root,text="Add",bg="lightyellow4",bd=1,width=15,height=2,cursor="hand2",command=additem)
    additembutton.place(x=925,y=260)

def mainlogin():
    titlelabel=Label(root,text="Billing System ",font=('Arial',40),bg="gray85")
    titlelabel.place(x=600,y=50)

    startbutton=Button(root,text="START",width=20,bg="lightyellow4",cursor="hand2",height=2,command=mainwindow)
    startbutton.place(x=650,y=250)

    Exitbutton=Button(root,text="EXIT",bg="lightyellow4",cursor="hand2",width=20,height=2,command=root.destroy)
    Exitbutton.place(x=650,y=350)
    root.configure(bg="gray85")

mainlogin()
# the root window handles the mouse click event
root.mainloop()
