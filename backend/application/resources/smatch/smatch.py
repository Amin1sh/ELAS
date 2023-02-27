from flask import Blueprint
from orm_interface.base import Session

smatch = Blueprint("smatch", __name__)
session = Session()

@smatch.route("/home")
@smatch.route("/")
def smatch_home():
    return "Smatch home"
