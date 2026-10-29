
from datetime import date
from decimal import Decimal

from sqlalchemy import (
    URL,
    create_engine,
    String,
    Integer,
    Date,
    Numeric,
    select,
    func
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    Session
)

# --------------------------------------------------
# 1. DATABASE CONNECTION
# --------------------------------------------------

database_url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="Chandu@123",
    host="localhost",
    port=5432,
    database="postgres"
)

engine = create_engine(database_url, echo=False)

# --------------------------------------------------
# 2. DEFINE THE ORM MODEL
# --------------------------------------------------

class Base(DeclarativeBase):
    pass


class RetailSale(Base):
    __tablename__ = "orm_retail_sales"

    order_id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    order_date: Mapped[date] = mapped_column(
        Date, nullable=False
    )
    product: Mapped[str] = mapped_column(
        String(100), nullable=False
    )
    category: Mapped[str] = mapped_column(
        String(50), nullable=False
    )
    quantity: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False
    )
    city: Mapped[str] = mapped_column(
        String(50), nullable=False
    )


try:
    # --------------------------------------------------
    # 3. CREATE TABLE
    # --------------------------------------------------

    Base.metadata.create_all(engine)
    print("1. ORM table created successfully!")

    with Session(engine) as session:

        # --------------------------------------------------
        # 4. CREATE: INSERT A RECORD
        # --------------------------------------------------

        sale = RetailSale(
            order_id=9001,
            order_date=date(2026, 10, 20),
            product="Wireless Mouse",
            category="Accessories",
            quantity=4,
            unit_price=Decimal("750.00"),
            city="Bengaluru"
        )

        # Insert or update this demo record if it already exists
        session.merge(sale)
        session.commit()

        print("2. Sale inserted or refreshed successfully!")

        # --------------------------------------------------
        # 5. READ: FETCH RECORDS
        # --------------------------------------------------

        statement = select(RetailSale).order_by(
            RetailSale.order_id
        )
        sales = session.scalars(statement).all()

        print("\n3. Retail Sales Records:")

        for item in sales:
            print(
                f"Order: {item.order_id}, "
                f"Product: {item.product}, "
                f"Quantity: {item.quantity}, "
                f"City: {item.city}"
            )

        # --------------------------------------------------
        # 6. UPDATE: CHANGE QUANTITY
        # --------------------------------------------------

        existing_sale = session.get(RetailSale, 9001)

        if existing_sale:
            existing_sale.quantity = 5
            session.commit()
            print("\n4. Sale quantity updated to 5!")

        # --------------------------------------------------
        # 7. FILTER: FIND BENGALURU SALES
        # --------------------------------------------------

        statement = select(RetailSale).where(
            RetailSale.city == "Bengaluru"
        )

        bengaluru_sales = session.scalars(statement).all()

        print("\n5. Sales from Bengaluru:")

        for item in bengaluru_sales:
            print(item.order_id, item.product, item.city)

        # --------------------------------------------------
        # 8. COUNT RECORDS
        # --------------------------------------------------

        total = session.scalar(
            select(func.count()).select_from(RetailSale)
        )

        print("\n6. Total ORM records:", total)

        # --------------------------------------------------
        # 9. DELETE DEMO (OPTIONAL)
        # --------------------------------------------------
        # Uncomment these lines only if you want to delete
        # the demonstration record with order_id 9001.
        #
        # demo_sale = session.get(RetailSale, 9001)
        # if demo_sale:
        #     session.delete(demo_sale)
        #     session.commit()
        #     print("Demo record deleted!")

    print("\nSQLAlchemy ORM demo completed successfully!")

except Exception as error:
    print("\nAn error occurred:", error)

finally:
    engine.dispose()
