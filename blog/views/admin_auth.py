from flask import Blueprint, render_template, redirect, session, get_flashed_messages, flash, request
from ..config.database import get_connection
from werkzeug.security import generate_password_hash, check_password_hash


admin = Blueprint("admin", __name__)
db = get_connection()

@admin.get("/")
def login_page():
    return render_template("admin/login.html")


@admin.get("/register")
@admin.get("/sign-up")
def register_page():
    conn, cursor = db
    query = "SELECT * FROM admin"
    cursor.execute(query)
    conn.commit()
    admin = cursor.fetchall()
    if admin:
        # flash("Failed to register admin", "danger")
        return redirect("/owner/")
    

    return render_template("/admin/register.html")

@admin.post("/create")
def handle_register_admin():
    form = request.form

    # GET THE FORM FIELDS
    name = form.get("name")
    email = form.get("email")
    password = form.get("password")
    hashed_password = generate_password_hash(password)

    if not db:
        flash("Error connecting to db", "danger")
        return redirect("/owner/register")
    
    conn, cursor = db
    query = "INSERT INTO admin (name, email, password) VALUES (%s, %s, %s)"
    cursor.execute(query, [name, email, hashed_password])
    conn.commit()

    if not cursor.rowcount:
        flash("Failed to register admin", "danger")
        return redirect("/owner/register")
    
    flash("Registration succesful", "success")
    return redirect("/owner/")

@admin.post("/login")
def handle_login_admin():
    form = request.form

    # GET THE INPUTS
    email = form.get("email")
    password = form.get("password")

    if not db:
        flash("Error connecting to db", "danger")
        return redirect("/owner/")
    conn, cursor = db

    # GET THE ADMIN
    query = "SELECT * FROM admin WHERE email = %s"
    cursor.execute(query, [email])

    admin = cursor.fetchone()
    # admin = cursor.fetchall()

    if not admin:
        flash("Admin does not exist", "danger")
        return redirect("/owner/")
    
    # VERIFY PASSWORD
    if not check_password_hash(admin.get("password"), password):
        flash("Incorect Credentials", "danger")
        return redirect("/owner")
    
    # CREATE ADMIN LOGIN SESSION
    session["ADMIN_LOGIN"] = admin.get("email")
    session["ADMIN_NAME"] = admin.get("name")

    flash("Login successful", "success")
    return redirect("/owner/dashboard")

# HANDLE ADMIN LOGOUT
@admin.get("/logout")
def logout_admin():
    session.pop("ADMIN_LOGIN", None)
    flash("Logout Successful", "success")
    return redirect("/owner/")

# VIEW DASHBOARD PAGE
@admin.get("/dashboard")
def dashboard_page():
    # if not session["ADMIN_LOGIN"]:
    #     return redirect("/owner/")
    # user = session["ADMIN_LOGIN"]
    return render_template("/admin/dashboard.html")