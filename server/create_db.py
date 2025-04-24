from app.db.base import Base
from app.db.session import engine
from app.models import Product, Message

def create_tables():
    print("🔧 Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully.")

if __name__ == "__main__":
    create_tables()
