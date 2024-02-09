from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, relationship, Session, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Float, Table, ForeignKey, DateTime, Date, Boolean

# -------------------------------------------------------------------------------------------------------------------
Base = declarative_base()

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    def as_dict(self):
        role_dict = {column.name: getattr(self, column.name) for column in self.__table__.columns}

        return role_dict


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    def as_dict(self):
        company_dict = {column.name: getattr(self, column.name) for column in self.__table__.columns}

        return company_dict


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))
    is_active = Column(Boolean, default=True)

    role = relationship("Role", back_populates="users")
    company = relationship("Company", back_populates="users")

    def as_dict(self):
        user_dict = {column.name: getattr(self, column.name) for column in self.__table__.columns if column.name not in ['role_id', 'company_id']}
        user_dict['role'] = self.role.name if self.role else None
        user_dict['company'] = self.company.name if self.company else None

        return user_dict


# Para establecer la relación inversa entre usuarios y roles
Role.users = relationship("User", back_populates="role")

# Para establecer la relación inversa entre usuarios y empresas
Company.users = relationship("User", back_populates="company")


product_category_association = Table(
    'product_category_association',
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    product_code = Column(String, index=True, unique=True)
    brand = Column(String)
    detailed_description = Column(String)
    purchase_price = Column(Float)
    sale_price = Column(Float)
    units_in_stock = Column(Integer)
    warehouse_location = Column(String)
    manufacturing_date = Column(String)
    expiration_date = Column(String)
    suppliers = Column(String)  # Assuming you store suppliers as a string (comma-separated, for example)
    min_inventory_level = Column(Integer)
    image = Column(String)
    additional_notes = Column(String)
    tax_info = Column(String)
    units_sold = Column(Integer)
    movement_history = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    company_id = Column(Integer, ForeignKey("companies.id"))

    categories = relationship('Category', secondary=product_category_association, back_populates='products')
    orders = relationship('OrderItem', back_populates='product')  # Agregado

    def as_dict(self):
        product_dict = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        product_dict["categories"] = [category.name for category in self.categories]
        product_dict["created_at"] = str(product_dict["created_at"])
        product_dict["updated_at"] = str(product_dict["updated_at"])
        return product_dict


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    products = relationship('Product', secondary=product_category_association, back_populates='categories')

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="pending")  # Puedes definir más estados según tus necesidades
    company_id = Column(Integer, ForeignKey("companies.id"))
    items = relationship('OrderItem', back_populates='order')

    def as_dict(self):
        order_dict = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        order_dict["order_date"] = str(order_dict["order_date"])
        order_dict["items"] = [{"product_id": item.product.id,
                                "product_name": item.product.name,
                                "quantity": item.quantity,
                                "unit_price": item.product.sale_price,
                                "total_price": item.total_price,
                                } for item in self.items]
        return order_dict


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    unit_price = Column(Float)
    total_price = Column(Float)

    order = relationship('Order', back_populates='items')
    product = relationship('Product', back_populates='orders')



# -------------------------------------------------------------------------------------------------------------------
# Configuracion de la base de datos
DATABASE_URL = "sqlite:///app/./inventarix.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Creacion de la sesion de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Funcion para obtener la sesion de la base de datos en las rutas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# -------------------------------------------------------------------------------------------------------------------