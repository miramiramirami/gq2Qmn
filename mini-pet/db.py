from sqlalchemy.orm import declarative_base, Mapped, mapped_column, sessionmaker
from sqlalchemy import create_engine, select

Base = declarative_base()

engine = create_engine(
    "sqlite:///db.sqlite3",
    connect_args={"check_same_thread": False}, 
    echo=True
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class ChatReqs(Base):
    __tablename__ = 'chat_reqs'

    id: Mapped[int] = mapped_column(primary_key=True)
    ip_address: Mapped[str] = mapped_column(index=True)
    prompt: Mapped[str]
    response: Mapped[str]


def get_user_reqs(ip_address: str) -> list[ChatReqs]:
    with SessionLocal() as session:
        res = session.execute(select(ChatReqs).filter(ChatReqs.ip_address == ip_address))
        return res.scalars().all()
    

def add_req_data(ip_address: str, prompt: str, response: str) -> None:
    with SessionLocal() as session:
        new_req = ChatReqs(
            ip_address=ip_address,
            prompt=prompt,
            response=response
        )

        session.add(new_req)
        session.commit()
    
