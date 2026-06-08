from flask import Blueprint, render_template

from app.models.dashboard_model import get_dashboard_metrics
from app.utils.decorators import login_required

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    metrics = get_dashboard_metrics()
    return render_template("dashboard/index.html", metrics=metrics)

