from datetime import datetime
from flask import abort, make_response
import re


def email_validator(mail):
    match = re.search(r'[\w.-]+@[\w.-]+.\w+', mail)
    if match:
        return True
    else:
        return False

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

PEOPLE = {
    "fairy.tooth@gmail.com": {
        "email": "fairy.tooth@gmail.com",
        "fname": "Tooth",
        "lname": "Fairy",
        "timestamp": get_timestamp(),
    },
    "ruprecht.knecht@fp.pl": {
        "email": "ruprecht.knecht@fp.pl",
        "fname": "Knecht",
        "lname": "Ruprecht",
        "timestamp": get_timestamp(),
    },
    "bunny.easter@bn.en": {
        "email": "bunny.easter@bn.en",
        "fname": "Easter",
        "lname": "Bunny",
        "timestamp": get_timestamp(),
    }
}

def read_all():
    return list(PEOPLE.values())

def create(person):
    email = person.get("email")
    lname = person.get("lname")
    fname = person.get("fname", "")

    if (email_validator(email)):
        if email not in PEOPLE:
            PEOPLE[email] = {
                "email": email,
                "lname": lname,
                "fname": fname,
                "timestamp": get_timestamp(),
            }
            return PEOPLE[email], 201
        else:
            abort(
                406,
                f"Person with last name {email} already exists",
            )
    else:
        abort(
            400,
            f'Given email is incorrect, email: {email}'
        )

def read_one(email):
    if email in PEOPLE:
        return PEOPLE[email]
    else:
        abort(
            404, f"Person with last name {email} not found"
        )

def update(email, person):
    if email in PEOPLE:
        mail = person.get("email", PEOPLE[email]["email"])
        if (email_validator(mail)):
            PEOPLE[email]["email"] = mail
            PEOPLE[email]["lname"] = person.get("lname", PEOPLE[email]["lname"])
            PEOPLE[email]["fname"] = person.get("fname", PEOPLE[email]["fname"])
            PEOPLE[email]["timestamp"] = get_timestamp()
            return PEOPLE[email]
        else:
            abort(
                400,
                f'Given email is incorrect, email: {mail}'
            )
    else:
            abort(
                404,
                f"Person with email:{email} not found"
            )


def delete(email):
    if email in PEOPLE:
        del PEOPLE[email]
        return make_response(
            f"{email} successfully deleted", 200
        )
    else:
        abort(
            404,
            f"Person with last name {email} not found"
        )