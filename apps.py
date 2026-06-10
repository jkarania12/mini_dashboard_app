from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

orders = [
    {
        "id": 1,
        "customer_name": "Jay",
        "location": "Westlands",
        "status": "Pending",
        "amount": 2500
    },
    {
        "id": 2,
        "customer_name": "Amit",
        "location": "Parklands",
        "status": "Delivered",
        "amount": 4200
    }
]


@app.route("/")
def index():
    status_filter = request.args.get("status")

    if status_filter:
        filtered_orders = [
            order for order in orders
            if order["status"].lower() == status_filter.lower()
        ]
    else:
        filtered_orders = orders

    total_orders = len(filtered_orders)
    pending_orders = len([o for o in filtered_orders if o["status"] == "Pending"])
    delivered_orders = len([o for o in filtered_orders if o["status"] == "Delivered"])
    total_value = sum(o["amount"] for o in filtered_orders)

    return render_template(
        "index.html",
        orders=filtered_orders,
        total_orders=total_orders,
        pending_orders=pending_orders,
        delivered_orders=delivered_orders,
        total_value=total_value,
        selected_status=status_filter
    )


@app.route("/add", methods=["GET", "POST"])
def add_order():
    if request.method == "POST":
        new_order = {
            "id": len(orders) + 1,
            "customer_name": request.form["customer_name"],
            "location": request.form["location"],
            "status": request.form["status"],
            "amount": float(request.form["amount"])
        }

        orders.append(new_order)
        return redirect(url_for("index"))

    return render_template("add_order.html")


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)