import json
from app.models import Message
from app.db.session import engine
from sqlalchemy.orm import Session

def load_chat_history():
    history = []
    with Session(bind=engine) as session:
        messages = session.query(Message).order_by(Message.timestamp).all()
        for message in messages:
            history.append({"role": "user", "content": message.query})
            try:
                product_ids = json.loads(message.response)
            except json.JSONDecodeError:
                product_ids = []
            history.append({
                "role": "assistant",
                "content": f"Here's my recommendations:",
                "product_ids": product_ids
            })
    return history

def save_chat_message(query, product_ids):
    from app.models import Message  # Local import to avoid circular import
    with Session(bind=engine) as session:
        new_msg = Message(query=query, response=json.dumps(product_ids))
        session.add(new_msg)
        session.commit()
