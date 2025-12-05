import json
import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for

import matplotlib
matplotlib.use("Agg")  # non-GUI backend for server-safe charts
import matplotlib.pyplot as plt

app = Flask(__name__)

DATA_FILE = "expenses.json"
BUDGET_FILE = "budgets.json"   # NEW: store budgets here


# -----------------------------
# Custom Green Money Palette 🍃💵
# -----------------------------
CHART_COLORS = [
    "#059669",  # Emerald Green
    "#10b981",  # Vibrant Green
    "#34d399",  # Soft Green
    "#6ee7b7",  # Light Mint
    "#a7f3d0",  # Soft Mint
    "#047857",  # Deep Green
    "#064e3b",  # Forest Green
]


# -----------------------------
# Helper functions for expenses
# -----------------------------

def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=4)


def calculate_summary(expenses):
    """Return totals, averages, counts by category."""
    category_totals = {}
    category_counts = {}

    for exp in expenses:
        cat = exp["category"]
        amt = exp["amount"]
        category_totals.setdefault(cat, 0)
        category_counts.setdefault(cat, 0)
        category_totals[cat] += amt
        category_counts[cat] += 1

    summary = {}
    for cat in category_totals:
        total = category_totals[cat]
        count = category_counts[cat]
        avg = total / count if count > 0 else 0
        summary[cat] = {"total": total, "average": avg, "count": count}

    return summary


# -----------------------------
# Helper functions for budgets
# -----------------------------

def load_budgets():
    """Load budgets from JSON. Returns dict: {category: budget_amount}"""
    if not os.path.exists(BUDGET_FILE):
        return {}
    try:
        with open(BUDGET_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}


def save_budgets(budgets):
    """Save budgets dict."""
    with open(BUDGET_FILE, "w") as f:
        json.dump(budgets, f, indent=4)


# -----------------------------
# Static folder (for charts)
# -----------------------------

def ensure_static_folder():
    folder = os.path.join(app.root_path, "static")
    os.makedirs(folder, exist_ok=True)
    return folder


# -----------------------------
# BAR CHART — GREEN FINANCE THEME
# -----------------------------

def generate_category_bar_chart(summary):
    if not summary:
        return None

    categories = list(summary.keys())
    totals = [summary[c]["total"] for c in categories]
    colors = CHART_COLORS[:len(categories)]

    plt.figure(figsize=(7, 4.5))
    plt.bar(categories, totals, color=colors, edgecolor="#064e3b")

    plt.title("Total Spending by Category", fontsize=14, pad=10)
    plt.xlabel("Category")
    plt.ylabel("Total Spent")
    plt.xticks(rotation=30, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()

    static = ensure_static_folder()
    path = os.path.join(static, "category_spending_bar.png")
    plt.savefig(path, dpi=120)
    plt.close()

    return "category_spending_bar.png"


# -----------------------------
# PIE CHART — GREEN FINANCE THEME
# -----------------------------

def generate_category_pie_chart(summary):
    if not summary:
        return None

    categories = list(summary.keys())
    totals = [summary[c]["total"] for c in categories]
    colors = CHART_COLORS[:len(categories)]

    plt.figure(figsize=(5.2, 5.2))
    wedges, texts, autotexts = plt.pie(
        totals,
        labels=categories,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors,
        textprops={"color": "#064e3b", "fontsize": 11},
        pctdistance=0.8
    )

    plt.setp(autotexts, color="white", fontsize=11, weight="bold")
    plt.title("Category Share of Total Spending", fontsize=14, pad=12)
    plt.tight_layout()

    static = ensure_static_folder()
    path = os.path.join(static, "category_spending_pie.png")
    plt.savefig(path, dpi=120)
    plt.close()

    return "category_spending_pie.png"


# -----------------------------
# ROUTES
# -----------------------------

@app.route("/")
def index():
    all_expenses = load_expenses()
    budgets = load_budgets()

    # Filters from query string
    selected_category = request.args.get("category", "").strip()
    year_filter = request.args.get("year", "").strip()
    month_filter = request.args.get("month", "").strip()

    display_expenses = []

    for file_idx, exp in enumerate(all_expenses):
        try:
            date_obj = datetime.strptime(exp["date"], "%Y-%m-%d")
        except Exception:
            continue

        # Year filter
        if year_filter:
            try:
                if date_obj.year != int(year_filter):
                    continue
            except ValueError:
                pass

        # Month filter
        if month_filter:
            try:
                if date_obj.month != int(month_filter):
                    continue
            except ValueError:
                pass

        # Category filter
        if selected_category:
            if exp["category"].lower() != selected_category.lower():
                continue

        copy_exp = exp.copy()
        copy_exp["file_index"] = file_idx
        copy_exp["date_obj"] = date_obj
        display_expenses.append(copy_exp)

    # Sort by date (newest first)
    display_expenses.sort(key=lambda e: e["date_obj"], reverse=True)

    # Summary & charts (based on filtered expenses)
    summary = calculate_summary(display_expenses)
    bar_chart = generate_category_bar_chart(summary) if summary else None
    pie_chart = generate_category_pie_chart(summary) if summary else None

    # -----------------------------
    # Build budget view for dashboard
    # -----------------------------
    budget_view = {}
    for cat, budget_amount in budgets.items():
        spent = summary.get(cat, {}).get("total", 0.0)
        remaining = budget_amount - spent
        percent_used = (spent / budget_amount * 100) if budget_amount > 0 else None

        budget_view[cat] = {
            "budget": budget_amount,
            "spent": spent,
            "remaining": remaining,
            "percent_used": percent_used,
        }

    return render_template(
        "index.html",
        expenses=display_expenses,
        summary=summary,
        selected_category=selected_category,
        year_filter=year_filter,
        month_filter=month_filter,
        bar_chart_filename=bar_chart,
        pie_chart_filename=pie_chart,
        budget_view=budget_view,   # NEW
    )


@app.route("/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        date_input = request.form.get("date", "").strip()
        category = request.form.get("category", "").strip()
        amount_input = request.form.get("amount", "").strip()
        note = request.form.get("note", "").strip()

        # Default date = today
        if date_input == "":
            date_str = datetime.today().strftime("%Y-%m-%d")
        else:
            try:
                datetime.strptime(date_input, "%Y-%m-%d")
                date_str = date_input
            except ValueError:
                return render_template("add_expense.html", error="Invalid date format. Use YYYY-MM-DD.")

        if not category:
            return render_template("add_expense.html", error="Category cannot be empty.")

        try:
            amount = float(amount_input)
        except ValueError:
            return render_template("add_expense.html", error="Amount must be a number.")

        new_expense = {
            "date": date_str,
            "category": category,
            "amount": amount,
            "note": note,
        }

        data = load_expenses()
        data.append(new_expense)
        save_expenses(data)

        return redirect(url_for("index"))

    return render_template("add_expense.html")


@app.route("/delete/<int:expense_index>", methods=["POST"])
def delete_expense(expense_index):
    expenses = load_expenses()
    if 0 <= expense_index < len(expenses):
        expenses.pop(expense_index)
        save_expenses(expenses)
    return redirect(url_for("index"))


# -----------------------------
# BUDGET MANAGEMENT
# -----------------------------

@app.route("/budgets", methods=["GET", "POST"])
def manage_budgets():
    budgets = load_budgets()
    error = None

    if request.method == "POST":
        category = request.form.get("category", "").strip()
        amount_input = request.form.get("amount", "").strip()

        if not category:
            error = "Category cannot be empty."
        else:
            try:
                amount = float(amount_input)
                if amount < 0:
                    error = "Budget cannot be negative."
                else:
                    budgets[category] = amount
                    save_budgets(budgets)
                    return redirect(url_for("manage_budgets"))
            except ValueError:
                error = "Budget amount must be a number."

    return render_template("budgets.html", budgets=budgets, error=error)


@app.route("/budgets/delete/<category>", methods=["POST"])
def delete_budget(category):
    budgets = load_budgets()
    if category in budgets:
        budgets.pop(category)
        save_budgets(budgets)
    return redirect(url_for("manage_budgets"))


if __name__ == "__main__":
    app.run(debug=True)
