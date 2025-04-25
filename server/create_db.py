import argparse
from app.db.base import Base
from app.db.session import engine
from app.models import Product, Message

def create_tables(drop_existing=False):
    if drop_existing:
        print("⚠️  Dropping existing tables...")
        Base.metadata.drop_all(bind=engine)
        print("🗑️  Tables dropped.")

    print("🔧 Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create database tables for ShopLens.")
    parser.add_argument("-n", "--new", action="store_true", help="Drop all tables before creating new ones")
    args = parser.parse_args()

    create_tables(drop_existing=args.new)

