from app.configuracao.db import db
from app.livros.models import Booker

class Author(db.Model):
    __tablename__ = "author"

    id = db.Column(db.Integer, primaru_key=True)
    name = db.Column(db.String)
    booker_id = db.Column(db.Integer, db.Foreignkey('booker.id'))

    #Relacionameto de tabela
    booker = db.relationship('Booker',foreign_keys=booker_id)

    #Construtor campos obrigatorios
    #Author("João","blablablablalbalbalbalbalbalba")
    def __init__(self,name):
        self.name = name

    #Representacao quando realizar pesquisa 
    def __repr__(self):
        return "<Author %r>" %self.name
