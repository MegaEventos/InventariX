from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


# ========================
#      ROLES
# ========================
class RoleCreate(BaseModel):
    name: str


class RoleUpdate(BaseModel):
    name: Optional[str]


# ========================
#      COMPANIES
# ========================
class CompanyCreate(BaseModel):
    name: str


class CompanyUpdate(BaseModel):
    name: Optional[str]


# ========================
#      USERS
# ========================
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role_id: int
    company_id: int


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role_id: Optional[int] = None
    company_id: Optional[int] = None


# ========================
#      CATEGORIES
# ========================
class CategoryCreate(BaseModel):
    name: str


# ========================
#      PRODUCTS
# ========================
class ProductCreate(BaseModel):
    name: str = Field(default='product_name', max_length=150)
    description: str = Field(max_length=150)
    product_code: str
    category_ids: List[int]
    brand: str
    detailed_description: Optional[str] = None
    purchase_price: float
    sale_price: float
    units_in_stock: int
    warehouse_location: Optional[str] = None
    manufacturing_date: Optional[str] = None
    expiration_date: Optional[str] = None
    # suppliers: List[str]
    min_inventory_level: int
    additional_notes: Optional[str] = None
    tax_info: Optional[str] = None
    units_sold: int
    movement_history: str


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(max_length=150)
    description: Optional[str] = Field(max_length=150)
    product_code: Optional[str] = None
    category_ids: Optional[List[int]] = None
    brand: Optional[str] = None
    detailed_description: Optional[str] = None
    purchase_price: Optional[float] = None
    sale_price: Optional[float] = None
    units_in_stock: Optional[int] = None
    warehouse_location: Optional[str] = None
    manufacturing_date: Optional[str] = None
    expiration_date: Optional[str] = None
    # suppliers: Optional[] List[str] = None
    min_inventory_level: Optional[int] = None
    additional_notes: Optional[str] = None
    tax_info: Optional[str] = None
    units_sold: Optional[int] = None
    movement_history: Optional[str] = None


# ========================
#      ORDERS
# ========================
class OrderCreate(BaseModel):
    customer_name: str
    product_ids: List[int]
    quantities: List[int]