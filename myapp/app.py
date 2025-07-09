from datetime import datetime
import uuid

from flask import Flask, render_template, request
from sqlalchemy import func

from models import SessionLocal
from viz.database import Step


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    session = SessionLocal()

    # Get filters from URL query string
    id_filter = request.args.get("id")
    path_filter = request.args.get("path")
    ctime_filter = request.args.get("ctime")
    mtime_filter = request.args.get("mtime")
    sort_by = request.args.get("sort_by", "ctime")
    order = request.args.get("order", "asc")

    # query = session.query(Step.id, Step.path, Step.ctime, Step.mtime)
    query = session.query(
        Step.id.label("id"),
        Step.path.label("path"),
        Step.ctime.label("ctime"),
        Step.mtime.label("mtime"),
    )

    # Filtering
    if id_filter:
        query = query.filter(Step.id == uuid.UUID(id_filter))
    if path_filter:
        query = query.filter(Step.path == path_filter)
    if ctime_filter:
        query = query.filter(
            func.strftime("%Y-%m-%d %H:%M:%S", Step.ctime) == ctime_filter
        )
    if mtime_filter:
        query = query.filter(
            func.strftime("%Y-%m-%d %H:%M:%S", Step.mtime) == mtime_filter
        )

    filters = [
        {"name": "id", "placeholder": "Filter by ID"},
        {"name": "path", "placeholder": "Filter by Path"},
        {"name": "ctime", "placeholder": "Filter by Created Time"},
        {"name": "mtime", "placeholder": "Filter by Modified Time"},
    ]

    filter_values = {
        "id": id_filter,
        "path": path_filter,
        "ctime": ctime_filter,
        "mtime": mtime_filter,
    }
    
    # Sorting
    sort_column = getattr(Step, sort_by, Step.ctime)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Abstraction
    columns = [
        {'name': 'id', 'label': 'ID'},
        {'name': 'path', 'label': 'Path'},
        {'name': 'ctime', 'label': 'Created At'},
        {'name': 'mtime', 'label': 'Modified At'}
    ]

    entries = query.all()
    session.close()

    return render_template(
        "index.jinja.html",
        entries=entries,
        filters=filters,
        filter_values=filter_values,
        sort_by=sort_by,
        order=order,
        columns=columns,
        request=request,
    )


@app.template_filter("datetimefmt")
def datetimefmt(value, fmt="%Y-%m-%d %H:%M:%S"):
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.strftime(fmt)
    if isinstance(value, str):
        return value
    return value  # fallback in case it's not a datetime
