from init_db import db, ma
from . import User
from marshmallow import Schema
from flask_marshmallow import Marshmallow
from flask import Flask, jsonify


class WishListItem(db.Model):
    __tablename__ = 'wish_list_items'
    id = db.Column(db.Integer, primary_key=True)
    authors = db.Column(db.String(256))
    title = db.Column(db.String(256))
    likes = db.Column(db.Integer)
    pub_date = db.Column(db.Date)

    def __repr__(self):
        return '<Wish List Item {}>'.format(self.title)


class WishListItemSchema(ma.ModelSchema):
    class Meta:
        model = WishListItem


class Like(db.Model):
    __tablename__ = 'wish_list_likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    wish_item_id = db.Column(db.Integer, db.ForeignKey('wish_list_items.id'), nullable=False)

    def __repr__(self):
        return '<Wish List Item {}>'.format(self.like)


class LikeSchema(ma.ModelSchema):
    class Meta:
        model = Like



