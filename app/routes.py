from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index() -> str:
    return render_template("index.html")


@main_bp.get("/bond-market")
def bond_market() -> str:
    return render_template("bond_market.html")


@main_bp.get("/stock-market")
def stock_market() -> str:
    return render_template("stock_market.html")


@main_bp.get("/real-estate-market")
def real_estate_market() -> str:
    return render_template("real_estate_market.html")


@main_bp.get("/global-market")
def global_market() -> str:
    return render_template("global_market.html")
