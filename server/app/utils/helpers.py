from app.models import Product
from app.db.session import engine
from sqlalchemy.orm import Session


def fetch_products_by_ids(product_ids):
    with Session(bind=engine) as session:
        return session.query(Product).where(Product.id.in_(product_ids)).all()