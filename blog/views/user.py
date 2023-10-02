from flask import Blueprint, render_template, redirect, session, get_flashed_messages, flash, request


user = Blueprint("user", __name__)

@user.get("/home/")
@user.get("/")
def home_page():
    return render_template("users/index.html")

@user.get("/gallery")
def gallery_page():
    return render_template("users/gallery.html")

@user.get("/reservations")
def reservation_page():
    return render_template("users/make-reservations.html")

@user.get("/contact")
def contact_page():
    return render_template("users/contact-us.html")

@user.get("/about")
def about_page():
    return render_template("users/about-us.html")

@user.get("/room-standard")
def roomstandard_page():
    return render_template("users/roomstandard.html")

@user.get("/FAQ")
def FAQ_page():
    return render_template("users/FAQ.html")
