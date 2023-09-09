from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from protein_wiki.auth import login_required
from protein_wiki.db import get_db
import sqlite3

bp = Blueprint("protein", __name__)


@bp.route("/viewall")
def index():
    """Show all the proteins, most recent first."""
    db = get_db()
    proteins = db.execute(
        "SELECT name, info FROM protein"
    ).fetchall()
    return render_template("protein/viewall.html", proteins=proteins)


def get_protein(name):
    """Get a protein and its author by name.

    Checks that the name exists and optionally that the current user is
    the author.

    :param name: name of protein to get
    :param check_author: require the current user to be the author
    :return: the protein with author information
    :raise 404: if a protein with the given name doesn't exist
    :raise 403: if the current user isn't the author
    """
    protein = (
        get_db()
        .execute(
            "SELECT name, info, img_url FROM protein"
            " WHERE name = ?",
            (name,),
        )
        .fetchone()
    )

    if protein is None:
        abort(404, f"Protein name {name} doesn't exist.")

    return protein


@bp.route("/create", methods=("GET", "POST"))
# @login_required
def create():
    """Create a new protein for the current user."""
    if request.method == "POST":
        name = request.form["name"]
        info = request.form["info"]
        img_url = request.form["img_url"]
        error = None

        if not name:
            error = "Name is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO protein (name, info, img_url) VALUES (?, ?, ?, ?)",
                (name, info, img_url),
            )
            db.commit()
            return redirect(url_for("protein.index"))

    return render_template("protein/create.html")


@bp.route("/<name>/update", methods=("GET", "POST"))
# @login_required
def update(name):
    """Update a protein if the current user is the author."""
    protein = get_protein(name)

    if request.method == "POST":
        info = request.form["info"]
        img_url = request.form["img_url"]
        error = None

        if not name:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE protein SET info = ?, img_url = ? WHERE name = ?", (info, img_url, name)
            )
            db.commit()
            return redirect(url_for("protein.index"))

    return render_template("protein/update.html", protein=protein)


@bp.route("/<name>/delete", methods=("POST",))
# @login_required
def delete(name):
    """Delete a protein.

    Ensures that the protein exists and that the logged in user is the
    author of the protein.
    """
    get_protein(name)
    db = get_db()
    db.execute("DELETE FROM protein WHERE name = ?", (name,))
    db.commit()
    return redirect(url_for("protein.index"))

@bp.route('/', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        name = request.form['name']
        # search by protein name
        db = get_db()
        proteins = db.execute(
            "SELECT name, info, img_url FROM protein WHERE name LIKE ?",
            ('%' + name + '%',)
        ).fetchall()
        return render_template("protein/index.html", proteins=proteins, name=name)
    return render_template("protein/index.html", proteins=[])

@bp.route('/<name>')
def wiki(name):
    protein = get_protein(name)
    if protein:
        return render_template('protein/protein.html', protein=protein)
    return "Protein not found", 404