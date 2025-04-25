import random
import pandas as pd
from sqlalchemy.orm import Session
from app.models import Product
from app.db.session import engine
from app.db.base import Base

df = pd.read_csv("./notebooks/subset_data.csv")

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Insert into DB
with Session(bind=engine) as session:
    for _, row in df.iterrows():
        product = Product(
            id=int(row['article_id']),
            title=row['prod_name'],
            description=row['detail_desc'],
            price=row['price'],
            image_url=row['image_url']
        )
        session.add(product)
    session.commit()

print("✅ Products table seeded.")