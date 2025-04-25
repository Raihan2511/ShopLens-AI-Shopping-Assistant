from app.models import Product
from app.db.session import engine
from sqlalchemy.orm import Session


def fetch_products_by_ids(product_ids):
    with Session(bind=engine) as session:
        return session.query(Product).where(Product.id.in_(product_ids)).all()

def extract_product_ids(res):
    import re
    match = re.search(r"\[([^\]]+)\]", res)
    if match:
        ids_str = match.group(1)
        product_ids = [int(x.strip()) for x in ids_str.split(",") if x.strip().isdigit()]
        text = res[:match.start()].strip()
        return product_ids, text
    else:
        return [], res