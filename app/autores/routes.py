from flask import Blueprint, request, jsonify

autor = Blueprint('autor', __name__)

@autor.route("/author")
def author():
    r  = Author.query.order_by(Author.name).all()
    return r

@autor.route("/create/<nameAuthor>")
def authorCreate(nameAuthor):
    newAuthor = Author(name)
    db.session.add(newAuthor)
    db.session.commit()
    return "Autor adicionado!"

@autor.route("/upgrade/<nameAuthor>")
def authorUpgarde(nameAuthor):
    author = Author.query.filter_by(name=nameAuthor).first()
    author.name = nameAuthor
    db.session.add(author)
    db.session.commint()
    return "Autor Atualizado"

@autor.route("/delete/<nameAuthor>")
def authorDelete(nameAuthor):
    db.session.delete(nameAuthor)
    db.session.commit()
    return "Autor removido"
