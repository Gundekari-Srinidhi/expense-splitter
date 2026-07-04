from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "expense_splitter_secret_key"

groups = []

import os

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor(dictionary=True)
print("Database Connected Successfully")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE email=%s
            """,
            (email,)
        )

        user = cursor.fetchone()

        if user is None:
            return render_template(
                "login.html",
                error="Email does not exist."
            )

        if user["password"] != password:
            return render_template(
                "login.html",
                error="Incorrect password."
            )

        session["user_id"] = user["id"]
        session["user_name"] = user["name"]

        return redirect("/dashboard")

    return render_template("login.html")

@app.route("/")
def home():
    return redirect("/login")

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        if user:
            return render_template(
                "sign-up.html",
                error="Email already exists."
            )

        cursor.execute(
            """
            INSERT INTO users(name, email, password)
            VALUES(%s,%s,%s)
            """,
            (name, email, password)
        )

        db.commit()

        return redirect("/login")

    return render_template("sign-up.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    # Groups
    cursor.execute(
        """
        SELECT *
        FROM group_s
        WHERE created_by=%s
        """,
        (session["user_id"],)
    )
    groups = cursor.fetchall()

    # Member count for each group
    for group in groups:

        cursor.execute(
            "SELECT COUNT(*) AS total FROM group_members WHERE group_id=%s",
            (group["id"],)
        )

        group["member_count"] = cursor.fetchone()["total"]

    # Total Groups
    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM group_s
        WHERE created_by = %s
        """,
        (session["user_id"],)
    )

    result = cursor.fetchone()
    total_groups = result["total"]

   

    # Total Expenses
    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM expenses
        WHERE group_id IN (
            SELECT id
            FROM group_s
            WHERE created_by = %s
        )
        """,
        (session["user_id"],)
    )

    total_expenses = cursor.fetchone()["total"]
    # Total Amount
    cursor.execute(
        """
        SELECT IFNULL(SUM(amount), 0) AS total
        FROM expenses
        WHERE group_id IN (
            SELECT id
            FROM group_s
            WHERE created_by = %s
        )
        """,
        (session["user_id"],)
    )

    total_amount = cursor.fetchone()["total"]

    return render_template(
        "dashboard.html",
        groups=groups,
        total_groups=total_groups,
        total_expenses=total_expenses,
        total_amount=total_amount,
        user_name=session["user_name"]
    )

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

@app.route("/group/<int:id>")
def group(id):

    cursor.execute(
        "SELECT * FROM group_s WHERE id=%s",
        (id,)
    )

    group = cursor.fetchone()

    if group is None:
        return redirect("/dashboard")

    # Load members
    cursor.execute(
        """
        SELECT member_email
        FROM group_members
        WHERE group_id=%s
        """,
        (id,)
    )

    members = cursor.fetchall()

    cursor.execute(
        """
        SELECT name
        FROM users
        WHERE id=%s
        """,
        (session["user_id"],)
    )

    logged_user = cursor.fetchone()["name"]

    group["members"] = []

    for member in members:

        if member["member_email"] == logged_user:
            group["members"].append("You")
        else:
            group["members"].append(member["member_email"])
            

    cursor.execute(
        """
        SELECT
            id,
            expense_name,
            amount,
            paid_by
        FROM expenses
        WHERE group_id=%s
        """,
        (id,)
    )

    expenses = cursor.fetchall()

    group["expenses"] = []

    for expense in expenses:

       group["expenses"].append({

            "id": expense["id"],

            "name": expense["expense_name"],

            "amount": expense["amount"],

            "paidBy": expense["paid_by"]

        })

    return render_template(
        "group.html",
        group=group,
        id=id
    )
@app.route("/create-group", methods=["GET", "POST"])
def create_group():
    cursor.execute(
        """
        SELECT name
        FROM users
        WHERE id=%s
        """,
        (session["user_id"],)
    )

    user = cursor.fetchone()

    logged_user = user["name"]

    if request.method == "POST":

        if request.form["groupName"].strip() == "":
            return "Group name cannot be empty"
        
        if request.form["groupDescription"].strip() == "":
            return "Description cannot be empty."

        if request.form["members"].strip() == "":
            return "Add at least one member"

        members = request.form["members"].split(",")

        members = [member.strip() for member in members if member.strip()]

        if logged_user not in members:
            members.insert(0, logged_user)

        group = {
            "name": request.form["groupName"],
            "description": request.form["groupDescription"],
            "members": members,
            "expenses": []
        }

        sql = """
        INSERT INTO group_s(name, description, created_by)
        VALUES(%s, %s, %s)
        """

        values = (
            request.form["groupName"],
            request.form["groupDescription"],
            session["user_id"]
        )

        cursor.execute(sql, values)

        group_id = cursor.lastrowid

        for member in members:

            sql = """
            INSERT INTO group_members(group_id, member_email)
            VALUES(%s, %s)
            """

            values = (
                group_id,
                member.strip()
            )

            cursor.execute(sql, values)

        db.commit()

        return redirect("/dashboard")

    return render_template("create-group.html")


@app.route("/add-expense/<int:id>", methods=["GET", "POST"])
def add_expense(id):

    cursor.execute(
        "SELECT * FROM group_s WHERE id=%s",
        (id,)
    )

    group = cursor.fetchone()

    if group is None:
        return redirect("/dashboard")

    cursor.execute(
        """
        SELECT member_email
        FROM group_members
        WHERE group_id=%s
        """,
        (id,)
    )

    members = cursor.fetchall()

    group["members"] = []

    for member in members:
        group["members"].append(member["member_email"])

    if request.method == "POST":

        sql = """
        INSERT INTO expenses
        (group_id, expense_name, amount, paid_by)
        VALUES(%s,%s,%s,%s)
        """

        values = (
            id,
            request.form["expenseName"],
            request.form["expenseAmount"],
            request.form["paidBy"]
        )

        cursor.execute(sql, values)
        
        expense_id = cursor.lastrowid
        split_members = request.form.getlist("splitAmong")
        for member in split_members:

            cursor.execute(
                """
                INSERT INTO expense_split
                (expense_id, member_email)
                VALUES(%s,%s)
                """,
                (
                    expense_id,
                    member
                )
            )
        
            db.commit()
        if len(split_members) == 0:
            return "Please select at least one member to split the expense."

        return redirect(f"/group/{id}")

    return render_template(
        "add-expense.html",
        group=group,
        id=id
    )

@app.route("/settle/<int:id>", methods=["POST"])
def settle(id):

    cursor.execute(
        "DELETE FROM expenses WHERE group_id=%s",
        (id,)
    )

    db.commit()

    return redirect(f"/group/{id}")

@app.route("/settlement/<int:id>")
def settlement(id):

    # ----------------------------
    # Get Group
    # ----------------------------
    cursor.execute(
        "SELECT * FROM group_s WHERE id=%s",
        (id,)
    )

    group = cursor.fetchone()

    if group is None:
        return redirect("/dashboard")

    # ----------------------------
    # Get Members
    # ----------------------------
    cursor.execute("""
        SELECT member_email
        FROM group_members
        WHERE group_id=%s
    """, (id,))

    members = cursor.fetchall()

    group["members"] = []

    for member in members:
        group["members"].append(member["member_email"])

    # ----------------------------
    # Get Expenses
    # ----------------------------
    cursor.execute("""
        SELECT
            id,
            expense_name,
            amount,
            paid_by
        FROM expenses
        WHERE group_id=%s
        """, (id,))

    expenses = cursor.fetchall()

    group["expenses"] = []

    for expense in expenses:
        group["expenses"].append({
            "id": expense["id"],
            "name": expense["expense_name"],
            "amount": float(expense["amount"]),
            "paidBy": expense["paid_by"]
        })
    # ----------------------------
    # Total Expense
    # ----------------------------
    total = 0

    for expense in group["expenses"]:
        total += expense["amount"]

    
    # ----------------------------
    # Balance Dictionary
    # ----------------------------
    balance = {}

    for member in group["members"]:
        balance[member] = 0

    # ----------------------------
    # Calculate Balances
    # ----------------------------
    for expense in group["expenses"]:

        cursor.execute("""
            SELECT member_email
            FROM expense_split
            WHERE expense_id=%s
        """, (expense["id"],))

        split_members = cursor.fetchall()

        if len(split_members) == 0:
            continue

        expense_share = expense["amount"] / len(split_members)

        # Everyone owes their share
        for member in split_members:
            balance[member["member_email"]] -= expense_share

        # Payer gets full amount back
        if expense["paidBy"] in balance:
            balance[expense["paidBy"]] += expense["amount"]

   

    # ----------------------------
    # Creditors & Debtors
    # ----------------------------
    creditors = []
    debtors = []

    for person, amount in balance.items():

        if amount > 0:
            creditors.append([person, amount])

        elif amount < 0:
            debtors.append([person, -amount])

    # ----------------------------
    # Settlement
    # ----------------------------
    settlements = []

    while creditors and debtors:

        creditor = creditors[0]
        debtor = debtors[0]

        pay = min(creditor[1], debtor[1])

        settlements.append({
            "from": debtor[0],
            "to": creditor[0],
            "amount": round(pay, 2)
        })

        creditor[1] -= pay
        debtor[1] -= pay

        if creditor[1] <= 0.01:
            creditors.pop(0)

        if debtor[1] <= 0.01:
            debtors.pop(0)

    return render_template(
        "settlement.html",
        group=group,
        total=total,
        settlements=settlements,
        id=id
    )

@app.route("/edit-group/<int:id>", methods=["GET", "POST"])
def edit_group(id):

    cursor.execute(
        "SELECT * FROM group_s WHERE id=%s",
        (id,)
    )

    group = cursor.fetchone()

    if group is None:
        return redirect("/dashboard")

    cursor.execute(
        """
        SELECT member_email
        FROM group_members
        WHERE group_id=%s
        """,
        (id,)
    )

    members = cursor.fetchall()

    group["members"] = []

    for member in members:
        group["members"].append(member["member_email"])

    if request.method == "POST":

        # Update group details
        cursor.execute(
            """
            UPDATE group_s
            SET name=%s,
                description=%s
            WHERE id=%s
            """,
            (
                request.form["groupName"],
                request.form["groupDescription"],
                id
            )
        )

        # Delete old members
        cursor.execute(
            "DELETE FROM group_members WHERE group_id=%s",
            (id,)
        )

        # Insert updated members
        members = request.form["members"].split(",")

        for member in members:

            cursor.execute(
                """
                INSERT INTO group_members(group_id, member_email)
                VALUES(%s,%s)
                """,
                (
                    id,
                    member.strip()
                )
            )

        db.commit()

        return redirect(f"/group/{id}")

    return render_template(
        "edit-group.html",
        group=group,
        id=id
    )

@app.route("/delete-expense/<int:group_id>/<int:expense_id>", methods=["POST"])
def delete_expense(group_id, expense_id):

    cursor.execute(
        "DELETE FROM expenses WHERE id=%s",
        (expense_id,)
    )

    db.commit()

    return redirect(f"/group/{group_id}")

@app.route("/delete-group/<int:id>", methods=["POST"])
def delete_group(id):

    cursor.execute(
        "DELETE FROM group_members WHERE group_id=%s",
        (id,)
    )

    cursor.execute(
        "DELETE FROM expenses WHERE group_id=%s",
        (id,)
    )

    cursor.execute(
        "DELETE FROM group_s WHERE id=%s",
        (id,)
    )

    db.commit()

    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)


