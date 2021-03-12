'''
    Qin Ying Chen
    Coding Exercise: Vending Machine

    Assumptions:
    - machine has 4 items from the start
    - user can buy any amount of any item 
        (as long as there is enough in the machine)
    - the GUI only interacts with the potential buyer
        (no interface is provided for owner/worker of machine 
            to restock or add items)
    - machine accepts only quarters and any bills 
    - machine returns in dollar coins and quarters if change is needed

    The main resources used:
    https://github.com/KeithGalli/GUI/blob/master/WeatherApp.py 
    https://realpython.com/python-gui-tkinter/#displaying-clickable-buttons-with-button-widgets
    https://www.daniweb.com/programming/software-development/threads/398597/tkinter-vending
'''

import Tkinter as tk


''' Item class models vending machine items '''

class Item(object):
    def __init__(self, name, price, qty=0):
        self.Name = name
        self.Price = price
        self.Qty = qty

    def getName(self):
        return self.Name

    def getQty(self):
        return self.Qty
    
    def getPrice(self):
        return self.Price

    def addToQty(self, qty):
        self.Qty += qty

    def reduceQty(self, qty):
        self.Qty -= qty

    def canDispense(self, qty):
        if (self.Qty < qty):    # if not enough in-stock
            return False
        return True

    def __str__(self):
        if (self.Qty == 0):     # if sold out
            return '%s' % (self.Name)
        return '\t%s \n\tCost: $%.2f' % (self.Name, self.Price)

''' Payment class models monetary transactions '''

class Payment(object):
    def __init__(self, amtDue, itemNum, qty):
        self.ReceivedAmt = 0
        self.AmountDue = amtDue
        self.Change = 0
        self.Processing = True
        self.ItemNum = itemNum
        self.QtyDue = qty

    def getItemNum(self):
        return self.ItemNum

    def getQty(self):
        return self.QtyDue

    def isProcessing(self):
        return self.Processing

    def promptForPayment(self):
        MESSAGE.set("Payment Due: $%.2f" % (self.AmountDue))

    def completedPayment(self):
        self.AmountDue = 0
        self.Processing = False  

    ''' cancels this payment transaction
        and returns amount buyer has paid
        for (in change), if any '''
    def cancel(self):
        changeStr = None

        if (self.ReceivedAmt > 0):
            self.Change = self.ReceivedAmt
            changeStr = self.giveChange()

        self.AmountDue = 0
        self.Processing = False

        return changeStr

    ''' calculates the change to return to buyer
        and returns a string to display on GUI '''
    def giveChange(self):   # assumes machine only has quarters & dollar coins
        self.Change *= 100  # convert from dollar to cents
        changeStr = "YOUR CHANGE:"

        if(self.Change//100 > 0):
            changeStr += " %d dollar coin(s)" % (self.Change/100)
            self.Change = self.Change%100

        if (self.Change//25 > 0):
            changeStr += " and %d quarter coin(s)" % (self.Change/25)
            self.Change = self.Change%25

        return changeStr 

    ''' processes the money received from buyer
        and returns a string to display change 
        if any '''
    def processPay(self, money):
        changeStr = None

        # invalid payment
        if (money < 0):
            return changeStr
        
        self.ReceivedAmt += money

        # received enough money to pay
        if (money >= self.AmountDue):
            # only give change if received more than amount due
            if (money > self.AmountDue):
                self.Change = money - self.AmountDue
                changeStr = self.giveChange()

            self.completedPayment()
            return changeStr

        # not enough money to pay
        self.AmountDue -= money
        self.promptForPayment()
        return changeStr

''' VendingMachine class models vending machines '''

class VendingMachine(object):
    def __init__(self):
        self.Items = []
        self.Profit = 0
    
    def getProfit():
        return self.Profit

    def addItem(self, name, price, qty=0):
        # check if item already exists
        for item in self.Items:
            if (item.getName == name):
                return False
        
        # item does not exit so add it to machine
        self.Items.append(Item(name, price, qty))
        return True

    def restockItem(self, selectionNum, addToQty):
        if (addToQty < 0):  # canot restock with negative quantity
            return False

        selectionNum -= 1    # adjust the selected val to get valid index

        # if invalid index
        if (selectionNum < 0 or  selectionNum > len(Items)-1):  
            return False

        # valid index so restock the item
        self.Items[selectionNum].addToQty(addToQty)
        return True

    def getItemPrice(self, selectionNum):
        return self.Items[selectionNum-1].getPrice()

    def dispenseItem(self, selectionNum, qty):
        self.Profit += qty*self.Items[selectionNum-1].getPrice()
        self.Items[selectionNum-1].reduceQty(qty)

        MESSAGE.set("Purchase of %d %s is completed! \nThank you!" 
                                % (qty, self.Items[selectionNum-1].getName()))

    ''' determines whether or not a purchase of selected item with
        quantity can be made and returns corresponding bool value
        to represent result 
        (displays message on GUI if purchase cannot be made) '''
    def processPurchase(self, selectionNum, qty):
        if (qty <= 0):
            MESSAGE.set("UNSUCCESSFUL PURCHASE: \nquantity must be > 0")
            return False

        selectionNum -= 1    # adjust the selected val to get valid index

        # if not a valid index
        if (selectionNum < 0 or selectionNum > len(self.Items)-1):     
            MESSAGE.set("UNSUCCESSFUL PURCHASE: \nnot a valid selection")
            return False
        # if no more of the item left
        if (self.Items[selectionNum].getQty() == 0):    
            MESSAGE.set("UNSUCCESSFUL PURCHASE: \nthere is no more " 
                        + self.Items[selectionNum].getName())
            return False
        # if there is enough supply, process purchase
        if (self.Items[selectionNum].canDispense(qty)):
            return True

        # insufficient supply
        MESSAGE.set("UNSUCCESSFUL PURCHASE: \nthere are only %d of %s left" 
                        % (self.Items[selectionNum].getQty(), self.Items[selectionNum].getName()))
        return False
        
    def __str__(self):
        displayStr = "\nVending Machine Items\n"

        for i in range(0, len(self.Items)):
            if (self.Items[i].getQty() > 0):   # if there is more in the machine
                displayStr += "\n%d. %s" % (i+1, self.Items[i]) 
            else:    # if sold out
                displayStr += "\n%d. \t%s\n\tSorry, it's sold out..." % (i+1, self.Items[i])
        
        displayStr += "\n\nEnter the number for your selection and quantity in"
        displayStr += "\nthe boxes below and confirm your selection with the"
        displayStr += "\ncorresponding button to move on to payment"

        return displayStr + "\n"
    

''' initialize some vending machine items '''

VM = VendingMachine()
VM.addItem("Green Tea KitKat", 1.5, 10)
VM.addItem("Matcha Pocky", 2, 10)
VM.addItem("Instant Matcha Latte", 1, 10)
VM.addItem("Green Tea Oreo", 5, 10)

''' global payment request '''

global PAYMENT_REQUEST
PAYMENT_REQUEST = Payment(-1, -1, -1)
PAYMENT_REQUEST.cancel()

''' func to handle processing of selected item with quantity
    (called when Confirm Selection button is pressed) '''

def processSelection(selectedNum, quantity):
    global PAYMENT_REQUEST

    # if there isn't already a payment transaction taking place
    if (not PAYMENT_REQUEST.isProcessing()):
        try:
            selectedNum = int(selectedNum)
            quantity = int(quantity)

            # if purchase of selected item can be made
            if (VM.processPurchase(selectedNum, quantity) == True):
                amtDue = VM.getItemPrice(selectedNum)*quantity
                PAYMENT_REQUEST = Payment(amtDue, selectedNum, quantity)
                PAYMENT_REQUEST.promptForPayment()
        except:
            MESSAGE.set("INVALID VALUE(S) ENTERED")

    else:
        MESSAGE.set("Unfinished transaction...\n" + MESSAGE.get())

    initialState(root) 

''' func to handle payments
    (called when Confirm Payment button is pressed) '''

def processPayment(moneyEntered):
    try:
        moneyEntered = float(moneyEntered)
        changeStr = PAYMENT_REQUEST.processPay(moneyEntered)

        # if payment is complete
        if (not PAYMENT_REQUEST.isProcessing()):
            VM.dispenseItem(PAYMENT_REQUEST.getItemNum(), PAYMENT_REQUEST.getQty())
            if (changeStr != None):
                MESSAGE.set(MESSAGE.get() + "\n" + changeStr)
    except:
        MESSAGE.set("INVALID VALUE(S) ENTERED\n" + MESSAGE.get())

    initialState(root)

''' func to reset vending machine to its initial/wait state
    (called when Clear Selection button is pressed) '''

def reset():
    MESSAGE.set("Waiting for action...")
    initialState(root)

''' func to cancel current transaction and payment
    (called when Cancel button is pressed) '''

def processCancel():
    changeStr = PAYMENT_REQUEST.cancel()
    if (changeStr != None):    
        MESSAGE.set("CANCELED...\n" + changeStr)
    else:   
        MESSAGE.set("Transaction is canceled!\nWaiting for action...")
    initialState(root)

''' func to display and set initial/wait state of machine '''

def initialState(root):
    # display product selections

    displayLabel = tk.Label(itemsFrame, width=70, text=str(VM), justify='left') 
    displayLabel.grid(row=1, column=1)

    # get entries (selection & quantity)

    selectLabel = tk.Label(optFrame, text="Make a selection:\n(1, 2, 3 or 4)", bg='#8BA870')
    selectLabel.place(x=60, y=20)
    item = tk.Entry(optFrame, width=10)
    item.place(x=70, y=60)

    qtyLabel = tk.Label(optFrame, text="How many?\n(must be > 0)", bg='#8BA870')
    qtyLabel.place(x=190, y=20)
    qty = tk.Entry(optFrame, width=10)
    qty.place(x=190, y=60)

    processLabel = tk.Label(optFrame, textvariable=MESSAGE, bd=10)
    processLabel.place(x=500, y=150)

    # buttons (confirm & cancel)

    confirmSelect = tk.Button(optFrame, text="Confirm Selection", 
                    command=lambda: processSelection(item.get(), qty.get()))
    confirmSelect.place(x=70, y=120)

    clrSelect = tk.Button(optFrame, text="Clear Selection", command=reset)
    clrSelect.place(x=70, y=150)

    payLabel = tk.Label(optFrame, text="Enter payment amount:\n(Quarters, ex: 0.25/Bills, ex: 1)", 
                            bg='#8BA870')
    payLabel.place(x=300, y=20)
    pay = tk.Entry(optFrame, width=10)
    pay.place(x=350, y=60)

    confirmPay = tk.Button(optFrame, text="Confirm Payment", 
                            command=lambda: processPayment(pay.get()))
    confirmPay.place(x=330, y=120)
    cancel = tk.Button(optFrame, text="Cancel", command=processCancel)
    cancel.place(x=330, y=150)

    # only enable payment entry & buttons if payment is expected
    if (not PAYMENT_REQUEST.isProcessing()):
        pay.config(state='disabled')
        confirmPay.config(state='disabled')
        cancel.config(state='disabled')
    else:
        pay.config(state='normal')
        confirmPay.config(state='normal')
        cancel.config(state='normal')

    root.mainloop()


''' set up GUI '''

root = tk.Tk()
root.title("Vending Machine")
root.geometry("800x600")

welcomeLabel = tk.Label(root, text="Welcome to Matcha Snacks!", 
                            font="Verdana 15 bold", pady=10)
welcomeLabel.pack()

# frames

itemsFrame = tk.Frame(root, width=600, height=200, bg='#A6D785', bd=10)
itemsFrame.pack(side=tk.TOP)

optFrame = tk.Frame(root, width=600, height=250, bg='#8BA870', bd=10)
optFrame.pack(fill=tk.X, side=tk.BOTTOM, expand=True)

MESSAGE = tk.StringVar()
MESSAGE.set("Waiting for action...")

''' start the GUI/machine '''

initialState(root)
