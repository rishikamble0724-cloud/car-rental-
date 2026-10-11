# ============================================================
#  CAR RENTAL SYSTEM  -  BACKEND (Python + Flask + SQLite)
#  Vercel version: runs as a serverless function at /api/*
#  Note: Vercel's filesystem is read-only except /tmp, so the
#  SQLite database lives in /tmp (data resets between deploys).
# ============================================================

import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_FILE = "/tmp/rental.db"   # /tmp is the only writable folder on Vercel


def get_db():
    con = sqlite3.connect(DB_FILE)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    con = get_db()
    con.execute("""CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        brand TEXT,
        price INTEGER)""")
    con.execute("""CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer TEXT,
        car_id INTEGER,
        days INTEGER,
        amount INTEGER)""")
    if con.execute("SELECT COUNT(*) FROM cars").fetchone()[0] == 0:
        con.executemany("INSERT INTO cars (name, brand, price) VALUES (?, ?, ?)", [
            ("Swift ZXi", "Maruti", 1750),
            ("City VX", "Honda", 2800),
            ("XUV700 AX7", "Mahindra", 4900),
            ("Fortuner", "Toyota", 6500),
            ("Model 3", "Tesla", 9200),
        ])
    con.commit()
    con.close()


init_db()


@app.route("/api", methods=["GET"])
@app.route("/api/", methods=["GET"])
def home():
    return jsonify({"message": "Car Rental Backend is running"})


@app.route("/api/cars", methods=["GET"])
def list_cars():
    con = get_db()
    rows = con.execute("SELECT id, brand, name, price FROM cars ORDER BY id").fetchall()
    con.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/bookings", methods=["GET"])
def list_bookings():
    con = get_db()
    rows = con.execute("""SELECT b.id, b.customer,
                                 c.brand || ' ' || c.name AS car,
                                 b.days, b.amount
                          FROM bookings b
                          JOIN cars c ON c.id = b.car_id
                          ORDER BY b.id DESC""").fetchall()
    con.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/bookings", methods=["POST"])
def create_booking():
    data = request.get_json(force=True)
    customer = str(data.get("customer", "")).strip()
    car_id = int(data.get("car_id", 0))
    days = int(data.get("days", 0))

    if not customer or days <= 0:
        return jsonify({"error": "Enter customer name and valid days"}), 400

    con = get_db()
    car = con.execute("SELECT * FROM cars WHERE id = ?", (car_id,)).fetchone()
    if car is None:
        con.close()
        return jsonify({"error": "Car ID not found"}), 404

    amount = car["price"] * days
    con.execute("INSERT INTO bookings (customer, car_id, days, amount) VALUES (?, ?, ?, ?)",
                (customer, car_id, days, amount))
    con.commit()
    con.close()
    return jsonify({"message": "Booking created", "amount": amount})
