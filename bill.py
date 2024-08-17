import tkinter as tk
import pymysql
from tkinter import messagebox

class BillApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Super Market")
        scrn_width = self.root.winfo_screenwidth()
        scrn_height = self.root.winfo_screenheight()

        self.root.geometry(f"{scrn_width}x{scrn_height}+0+0")

        mainTitle = tk.Label(self.root, text="Super Market Billing System", bg="light gray", fg="red", bd=5, relief="groove", font=("Arial", 40, "bold"))
        mainTitle.pack(side="top", fill="x")

        self.item_name = tk.StringVar()
        self.item_price = tk.IntVar()
        self.item_quant = tk.IntVar()
        self.total = tk.IntVar()
        self.total.set(0)

        self.inputFrame = tk.Frame(self.root, bg="light gray", bd=5, relief="groove")
        self.inputFrame.place(x=20, y=90, width=400, height=700)

        item = tk.Label(self.inputFrame, text="Item Name:", bg="light gray", font=("Arial", 15, "bold"))
        item.grid(row=0, column=0, padx=10, pady=30)
        self.itemIn = tk.Entry(self.inputFrame, width=15, bd=2, font=("Arial", 15))
        self.itemIn.grid(pady=30, row=0, column=1)

        quant = tk.Label(self.inputFrame, text="Item Quantity:", bg="light gray", font=("Arial", 15, "bold"))
        quant.grid(row=1, column=0, padx=10, pady=30)
        self.quantIn = tk.Entry(self.inputFrame, width=15, bd=2, font=("Arial", 15))
        self.quantIn.grid(pady=30, row=1, column=1)

        purchaseBtn = tk.Button(self.inputFrame, command=self.purchase, text="Purchase", width=8, bd=2, relief="raised", bg="sky blue", font=("Arial", 15, "bold"))
        purchaseBtn.grid(row=2, column=0, padx=40, pady=70)

        printBillBtn = tk.Button(self.inputFrame, command=self.print_bill, text="Print Bill", width=8, bd=2, relief="raised", bg="sky blue", font=("Arial", 15, "bold"))
        printBillBtn.grid(row=2, column=1, padx=30, pady=70)

        addBtn = tk.Button(self.inputFrame, command=self.add_fun, text="Add Item", width=15, bg="sky blue", bd=2, relief="raised", font=("Arial", 15, "bold"))
        addBtn.grid(row=3, column=0, padx=40, columnspan=2, pady=30)

        self.detailFrame = tk.Frame(self.root, bg="light gray", bd=5, relief="groove")
        self.detailFrame.place(x=450, y=90, width=1050, height=700)

        self.list = tk.Listbox(self.detailFrame, bg="cyan", font=("Arial", 15), bd=3, relief="sunken", width=1050, height=600)
        self.list.grid(row=0, column=0, padx=10, pady=10)

    def add_fun(self):
        self.addFrame = tk.Frame(self.root, bg="light gray", bd=5, relief="groove")
        self.addFrame.place(x=460, y=90, width=400, height=550)

        itemName = tk.Label(self.addFrame, text="Item Name:", bg="light gray", font=("Arial", 15, "bold"))
        itemName.grid(row=0, column=0, padx=10, pady=30)
        self.itemNameIn = tk.Entry(self.addFrame, textvariable=self.item_name, width=15, bd=2, font=("Arial", 15))
        self.itemNameIn.grid(pady=30, row=0, column=1)

        itemQuant = tk.Label(self.addFrame, text="Item Quantity:", bg="light gray", font=("Arial", 15, "bold"))
        itemQuant.grid(row=1, column=0, padx=10, pady=30)
        self.itemQuantIn = tk.Entry(self.addFrame, textvariable=self.item_quant, width=15, bd=2, font=("Arial", 15))
        self.itemQuantIn.grid(pady=30, row=1, column=1)

        itemPrice = tk.Label(self.addFrame, text="Item Price:", bg="light gray", font=("Arial", 15, "bold"))
        itemPrice.grid(row=2, column=0, padx=10, pady=30)
        self.itemPriceIn = tk.Entry(self.addFrame, textvariable=self.item_price, width=15, bd=2, font=("Arial", 15))
        self.itemPriceIn.grid(pady=30, row=2, column=1)

        okBtn = tk.Button(self.addFrame, command=self.insert_fun, text="OK", width=8, bg="sky blue", bd=2, relief="raised", font=("Arial", 15, "bold"))
        okBtn.grid(row=3, column=0, padx=40, pady=30)

        closeBtn = tk.Button(self.addFrame, command=self.close, text="Close", width=8, bg="sky blue", bd=2, relief="raised", font=("Arial", 15, "bold"))
        closeBtn.grid(row=3, column=1, padx=40, pady=30)

    def insert_fun(self):
        try:
            con = pymysql.connect(host="localhost", user="root", passwd="Dhavle@2427", database="billdb")
            cur = con.cursor()
            cur.execute("INSERT INTO item (item_name, item_price, item_quantity) VALUES (%s, %s, %s)",
                        (self.item_name.get(), self.item_price.get(), self.item_quant.get()))
            con.commit()
            tk.messagebox.showinfo("Success", "Item Added Successfully!")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            con.close()
            self.clear()

    def clear(self):
        self.item_name.set("")
        self.item_price.set(0)
        self.item_quant.set(0)
        self.itemIn.delete(0, tk.END)
        self.quantIn.delete(0, tk.END)

    def close(self):
        self.addFrame.destroy()

    def purchase(self):
        item = self.itemIn.get()
        quant = int(self.quantIn.get())

        try:
            con = pymysql.connect(host="localhost", user="root", passwd="Dhavle@2427", database="billdb")
            cur = con.cursor()
            cur.execute("select item_price, item_quantity from item where item_name=%s", item)
            data = cur.fetchone()

            if data:
                if data[1] >= quant:
                    amount = data[0] * quant
                    self.total.set(self.total.get() + amount)
                    singleItem = f"Price of {quant} {item} is: {amount}"
                    self.list.insert(tk.END, singleItem)
                    self.clear_inputFrame()
                    update = data[1] - quant
                    cur.execute("update item set item_quantity=%s where item_name=%s", (update, item))
                    con.commit()
                else:
                    tk.messagebox.showerror("Error", "Item Quantity does not meet the requirement!")
                    self.clear_inputFrame()
            else:
                tk.messagebox.showerror("Error", "Invalid Item Name!")
                self.clear_inputFrame()
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            con.close()

    def clear_inputFrame(self):
        self.itemIn.delete(0, tk.END)
        self.quantIn.delete(0, tk.END)

    def print_bill(self):
        line = "------------------------------------"
        self.list.insert(tk.END, line)
        print_bill = f"Total Bill-------------: {self.total.get()}"
        self.list.insert(tk.END, print_bill)

root = tk.Tk()
app = BillApp(root)
root.mainloop()
