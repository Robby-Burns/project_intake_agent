import os
import json
from typing import List, Dict, Optional
from app.interfaces.database_adapter import DatabaseAdapter
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# SQLAlchemy Setup
Base = declarative_base()

class ConversationTurn(Base):
    __tablename__ = 'conversation_turns'
    id = Column(Integer, primary_key=True)
    session_id = Column(String(255), index=True)
    user_input = Column(Text)
    bot_response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class SessionMetadata(Base):
    __tablename__ = 'session_metadata'
    session_id = Column(String(255), primary_key=True)
    metadata_json = Column(Text) # Store as JSON string for flexibility
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PostgresAdapter(DatabaseAdapter):
    """
    PostgreSQL Adapter for state persistence.
    Reference: workflow/08_AGNOSTIC_FACTORIES.md
    """
    
    def __init__(self, connection_string: Optional[str] = None):
        self.connection_string = connection_string or os.getenv("DATABASE_URL")
        if not self.connection_string:
             # Fallback to SQLite for local development if not set (though Docker defines it)
             self.connection_string = "sqlite:///local_state.db"
             
        self.engine = create_engine(self.connection_string)
        Base.metadata.create_all(self.engine) # Auto-migrate for MVP
        self.Session = sessionmaker(bind=self.engine)

    def save_conversation_turn(self, session_id: str, user_input: str, bot_response: str) -> None:
        session = self.Session()
        try:
            turn = ConversationTurn(
                session_id=session_id,
                user_input=user_input,
                bot_response=bot_response
            )
            session.add(turn)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_conversation_history(self, session_id: str) -> List[Dict[str, str]]:
        session = self.Session()
        try:
            turns = session.query(ConversationTurn).filter_by(session_id=session_id).order_by(ConversationTurn.timestamp).all()
            return [{"user": t.user_input, "bot": t.bot_response} for t in turns]
        finally:
            session.close()

    def save_metadata(self, session_id: str, metadata: Dict[str, str]) -> None:
        session = self.Session()
        try:
            # Check if exists
            existing = session.query(SessionMetadata).filter_by(session_id=session_id).first()
            if existing:
                existing.metadata_json = json.dumps(metadata)
            else:
                new_meta = SessionMetadata(
                    session_id=session_id,
                    metadata_json=json.dumps(metadata)
                )
                session.add(new_meta)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_metadata(self, session_id: str) -> Optional[Dict[str, str]]:
        session = self.Session()
        try:
            record = session.query(SessionMetadata).filter_by(session_id=session_id).first()
            if record:
                return json.loads(record.metadata_json)
            return None
        finally:
            session.close()
