from flask import Flask,render_template,request,flash,redirect,url_for
import sqlite3 as sql
import json


app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    mydict = create_dict()
    con = sql.connect("database.db")
    con.row_factory=sql.Row
    cur =con.cursor()
    cur.execute("select * from cart")
    data =cur.fetchall()
    print(data)
    for row in data:
        mydict.add(row[0],({"name":row[1],"price":row[2],"quantity":row[3],"total":row[4]}))

    to_json = json.dumps(mydict, indent=2, sort_keys=True)
    print(to_json)

    with open("showCart.txt", "w") as my_file:
        my_file.write(to_json)        
     

    return render_template("index.html",datas=data)

@app.route("/add_item",methods=['POST','GET'])
def add_item():
    if request.method=="POST":   
        name=request.form.get("name")
        price=request.form.get("price")
        quantity=request.form.get("quantity")
        total = float(price) * int(quantity)
        con=sql.connect("database.db")
        cur=con.cursor()
        cur.execute("insert into cart(name,price,quantity,total) values (?,?,?,?)",(name,price,quantity,total))
        con.commit()
        flash("item Added","SUCCESS")
        return redirect(url_for("index"))
    return render_template("add_item.html")

@app.route("/edit_item/<string:pid>",methods=['POST','GET'])
def edit_item(pid):
    
    if request.method=='POST':
        name=request.form.get("name")
        price=request.form.get("price")
        quantity=request.form.get("quantity")
        total=request.form.get("total")
        total = float(price) * int(quantity)  

        con =sql.connect("database.db")
        cur=con.cursor()
        cur.execute("update cart set name=?,price=?,quantity=?,total=? where pid=?",(name,price,quantity,total,pid))
        con.commit()
        flash('User Updated','success')
        return redirect(url_for("index"))
    con=sql.connect("database.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from cart where pid=?",(pid,))
    data=cur.fetchone()
    print(data)


    return render_template("edit_item.html",datas=data)

@app.route("/delete_item/<string:pid>",methods=['GET'])
def delete_item(pid):
    con=sql.connect("database.db")
    cur=con.cursor()
    cur.execute("delete from cart where pid=?",(pid,))
    con.commit()
    flash('User Deleted','warning')
    return redirect(url_for("index"))

class create_dict(dict): 
  
    def __init__(self): 
        self = dict() 
          
    def add(self, key, value): 
        self[key] = value

if __name__ =="__main__":
    app.secret_key='admin123'
    app.run(debug=True)
