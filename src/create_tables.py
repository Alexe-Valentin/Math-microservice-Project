import sys
import logging

from src.app import create_app
from src.database import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import inspect

# Configure simple logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def main():
    app = create_app()
    try:
        with app.app_context():
            logger.info("Creating all tables…")
            db.create_all()

            # Use SQLAlchemy Inspector to list tables
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            logger.info(f"Tables now in database: {', '.join(tables)}")

        logger.info("✅ Done.")
    except SQLAlchemyError:
        logger.exception("Database error occurred")
        sys.exit(1)


if __name__ == "__main__":
    main()
