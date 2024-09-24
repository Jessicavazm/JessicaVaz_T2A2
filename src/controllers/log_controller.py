from flask import Blueprint
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from psycopg2 import errorcodes

from init import db
from models.log import Log, log_schema, logs_schema
from utils import auth_as_admin_decorator

# Create marathon blueprint
log_bp = Blueprint("log", __name__,url_prefix="/log")

@log_bp.route("/")
def get_all_logs():
    # Create and execute stmt, order by date
    # Convert marathon to list to use IF statement 
    stmt = db.select(Log).order_by(Log.entry_created)
    logs = list(db.session.scalars(stmt))
    if logs:
        # Serialise data using logs_schema
        return logs_schema.dump(logs), 200
    # Else returns error message
    else:
        return {"Error": "No logs to display."}, 400
    


# Create route for 'GET' a specific log
@log_bp.route("/<int:log_id>")
def get_a_log(log_id):
    # Use stmt and filter_by to select a specific log
    stmt = db.select(Log).filter_by(id=log_id)
    log = db.session.scalar(stmt)
    # If log returns it, Else returns error msg
    if log:
        return log_schema.dump(log)
    else:
        return {"error": f"Log with {log_id} has not been found."}, 404
    

# Delete log route, JWT required, @auth_as_admin allows admins to delete logs
@log_bp.route("/<int:log_id>", methods=["DELETE"])
@jwt_required()
@auth_as_admin_decorator
def delete_log(log_id):
    # Find log in DB using stmt
    stmt = db.select(Log).filter_by(id=log_id)
    log = db.session.scalar(stmt)
    
    # If log exists, delete log and commit changes to DB
    if log:
        try:
            db.session.delete(log)
            db.session.commit()
            return {"message": f"Log with id {log_id} has been successfully deleted."}, 200
        except SQLAlchemyError as e:
            return {"message": "Error occurred while deleting log.", "details": str(e)}, 500
    # Else return error msg
    else:
        return {"message": f"Log with id {log_id} was not found."}, 404
