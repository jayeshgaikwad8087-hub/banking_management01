import os
from datetime import datetime
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()
from dotenv import load_dotenv
load_dotenv()
app=Flask(__name__)
app.secret_key=os.getenv("SECRET_KEY","change-me")
client=MongoClient(os.getenv("MONGO_URI","mongodb://localhost:27017/"),serverSelectionTimeoutMS=5000)
db=client[os.getenv("DB_NAME","bank_management")]

@app.context_processor
def globals():
    return {"app_name":"Bank Management System","developer":"Jayesh Gaikwad"}

@app.route("/")
def dashboard():
    return render_template("dashboard.html",stats={
        "customers":db.customers.count_documents({}),
        "accounts":db.accounts.count_documents({}),
        "transactions":db.transactions.count_documents({}),
        "loans":db.loans.count_documents({})
    })

@app.route("/customers")
def customers():
    return render_template("customers.html",customers=list(db.customers.find().sort("created_at",-1)))
@app.route("/customers/add",methods=["GET","POST"])
def add_customer():
    if request.method=="POST":
        db.customers.insert_one({k:request.form.get(k,"") for k in ["name","email","phone","address"]}|{"created_at":datetime.utcnow()})
        flash("Customer added.","success"); return redirect(url_for("customers"))
    return render_template("form.html",title="Add Customer",fields=["name","email","phone","address"],action="add_customer")
@app.route("/customers/delete/<id>")
def delete_customer(id):
    try: db.customers.delete_one({"_id":ObjectId(id)})
    except: pass
    return redirect(url_for("customers"))

@app.route("/accounts")
def accounts(): return render_template("accounts.html",accounts=list(db.accounts.find().sort("created_at",-1)))
@app.route("/accounts/add",methods=["GET","POST"])
def add_account():
    if request.method=="POST":
        db.accounts.insert_one({"account_no":request.form["account_no"],"customer":request.form["customer"],"type":request.form["type"],"balance":float(request.form.get("balance",0) or 0),"status":request.form["status"],"created_at":datetime.utcnow()})
        flash("Account created.","success"); return redirect(url_for("accounts"))
    return render_template("form.html",title="Open Account",fields=["account_no","customer","type","balance","status"],action="add_account")

@app.route("/transactions",methods=["GET","POST"])
def transactions():
    if request.method=="POST":
        db.transactions.insert_one({"account_no":request.form["account_no"],"type":request.form["type"],"amount":float(request.form["amount"]),"description":request.form.get("description",""),"created_at":datetime.utcnow()})
        flash("Transaction recorded.","success"); return redirect(url_for("transactions"))
    return render_template("transactions.html",transactions=list(db.transactions.find().sort("created_at",-1).limit(100)))

@app.route("/loans")
def loans(): return render_template("loans.html",loans=list(db.loans.find().sort("created_at",-1)))
@app.route("/loans/add",methods=["GET","POST"])
def add_loan():
    if request.method=="POST":
        db.loans.insert_one({"customer":request.form["customer"],"amount":float(request.form["amount"]),"type":request.form["type"],"status":request.form["status"],"created_at":datetime.utcnow()})
        flash("Loan saved.","success"); return redirect(url_for("loans"))
    return render_template("form.html",title="New Loan",fields=["customer","amount","type","status"],action="add_loan")

@app.route("/employees")
def employees(): return render_template("module.html",title="Employees")
@app.route("/cards")
def cards(): return render_template("module.html",title="Cards")
@app.route("/reports")
def reports(): return render_template("module.html",title="Reports")
@app.route("/settings")
def settings(): return render_template("module.html",title="Settings")

pages=["profile","notifications","audit","branches","atm","beneficiaries","payments","transfers","deposits","recurring","interest","kyc","documents","support","complaints","feedback","security","roles","backup","logs","analytics","monthly","annual","cashflow","reconciliation","statements","cheques","benefit","insurance","investments","forex","upi","netbanking","mobilebanking","offers","products","pricing","faq","about","contact","help","terms","privacy","developer"]
for route in pages:
    title=route.replace("-"," ").title()
    def make_view(t):
        def view(): return render_template("module.html",title=t)
        return view
    app.add_url_rule("/"+route,endpoint="p_"+route,view_func=make_view(title))

@app.route("/api/stats")
def api_stats(): return jsonify({c:db[c].count_documents({}) for c in ["customers","accounts","transactions","loans"]})
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.getenv("PORT",5000)),debug=True)
