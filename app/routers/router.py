from typing import List
from ..dependencies import *
from ..models.model import *
from ..models.scheme import *
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status, File, UploadFile, APIRouter

router = APIRouter()


# ========================
#      HOME
# ========================
    
# ---> Home
@router.get("/", tags=['Home'])
async def home():
    return JSONResponse(content="Welcome to InventariX", status_code=200)


# ========================
#      AUTHORIZATION
# ========================

# ---> JWT Authorization
@router.post(f"{URI}/token/", tags=['Authorization'])
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not Hasher.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    token_data = {"sub": user.username}
    access_token = JWT_Authentication.create_token(token_data)

    return JSONResponse(content={"access_token": access_token, "token_type": "bearer", "user": user.as_dict()}, status_code=200)
    

# ---> Function to obtain the data of the current user
async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    payload = JWT_Authentication.decode_token(token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
    

# ---> The user obtains his own information
@router.post(f"{URI}/my-profile/", response_model=dict, tags=["Profile"])
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user.as_dict()


# ========================
#      ROLES
# ========================
    
# ---> Create role
@router.post(f"{URI}/role/", response_model=dict, tags=["Roles"])
async def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    db_role = Role(name=role.name)

    db.add(db_role)
    db.commit()
    db.refresh(db_role)

    return JSONResponse(content=db_role.as_dict(), status_code=200)


# ---> Read roles
@router.get(f"{URI}/role/", response_model=List[RoleCreate], tags=["Roles"])
async def get_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()

    result = [role.as_dict() for role in roles]
    
    return JSONResponse(content=result, status_code=200)


# ---> Search role for id number
@router.get(f"{URI}/role/{{role_id}}", response_model=dict, tags=["Roles"])
async def get_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()

    if role:
        return JSONResponse(content={"role": role.as_dict()}, status_code=200)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")


# ---> Update role
@router.put(f"{URI}/role/{{role_id}}", response_model=dict, tags=["Roles"])
async def update_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    db_role = db.query(Role).filter(Role.id == role_id).first()

    if not db_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    if role.name:
        db_role.name = role.name

    db.commit()
    db.refresh(db_role)

    return JSONResponse(content=db_role.as_dict(), status_code=200)


# ---> Delete role
@router.delete(f"{URI}/role/{{role_id}}", response_model=dict, tags=["Roles"])
async def delete_role(role_id: int, db: Session = Depends(get_db)):
    db_role = db.query(Role).filter(Role.id == role_id).first()

    if db_role:
        db.delete(db_role)
        db.commit()

        return JSONResponse(content={"message": f"Role {db_role.name} deleted successfully"}, status_code=200)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    

# ========================
#      COMPANIES
# ========================
    
# ---> Create company
@router.post(f"{URI}/companies/", response_model=dict, tags=["Companies"])
async def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = Company(name=company.name)

    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    return JSONResponse(content=db_company.as_dict(), status_code=200)


# ---> Read companies
@router.get(f"{URI}/companies/", response_model=List[CompanyCreate], tags=["Companies"])
async def get_companies(db: Session = Depends(get_db)):
    companies = db.query(Company).all()

    result = [company.as_dict() for company in companies]
    
    return JSONResponse(content=result, status_code=200)


# ---> Search company for id number
@router.get(f"{URI}/companies/{{company_id}}", response_model=dict, tags=["Companies"])
async def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()

    if company:
        return JSONResponse(content={"company": company.as_dict()}, status_code=200)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")


# ---> Update company
@router.put(f"{URI}/companies/{{company_id}}", response_model=dict, tags=["Companies"])
async def update_company(company_id: int, company: CompanyUpdate, db: Session = Depends(get_db)):
    db_company = db.query(Company).filter(Company.id == company_id).first()

    if not db_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    if company.name:
        db_company.name = company.name

    db.commit()
    db.refresh(db_company)

    return JSONResponse(content=db_company.as_dict(), status_code=200)


# ---> Delete company
@router.delete(f"{URI}/companies/{{company_id}}", response_model=dict, tags=["Companies"])
async def delete_company(company_id: int, db: Session = Depends(get_db)):
    db_company = db.query(Company).filter(Company.id == company_id).first()

    if db_company:
        db.delete(db_company)
        db.commit()

        return JSONResponse(content={"message": f"Company {db_company.name} deleted successfully"}, status_code=200)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")


# ========================
#      USERS
# ========================
    
# ---> Create user
@router.post(f"{URI}/users/", tags=['Users'])
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Verificamos si el correo electrónico ya está en uso
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    company = db.query(Company).filter(Company.id == user.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # Encriptamos la contraseña antes de guardarla en la base de datos
    hashed_password = Hasher.hash_password(user.password)

    # Creamos el nuevo usuario en la base de datos
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        role_id=user.role_id,
        company_id=user.company_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return JSONResponse(content=db_user.as_dict(), status_code=200)


# ---> Read users
@router.get(f"{URI}/users/", response_model=List[UserCreate], tags=["Users"])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    result = [user.as_dict() for user in users]
    
    return JSONResponse(content=result, status_code=200)


# ---> Search user for id number
@router.get(f"{URI}/users/{{user_id}}", tags=['Users'])
async def get_user(user_id: int, db: Session = Depends(get_db)):
    # payload = JWT_Authentication.decode_token(token)
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return JSONResponse(content={"user": user.as_dict()}, status_code=200)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


# ---> Update user
@router.put(f"{URI}/users/{{user_id}}", tags=['Users'])
async def update_user(user_id: int, item: UserUpdate, db: Session = Depends(get_db)):
    # payload = JWT_Authentication.decode_token(token)
    user = db.query(User).filter(User.id == user_id).first()

    if user:
        # Actualiza solo los campos proporcionados en la solicitud
        for field, value in item.dict().items():
            if value is not None:
                setattr(user, field, value)

        db.commit()
        db.refresh(user)

        result = {"message": f"User {user.username} updated successfully", "user": user.as_dict()}
        return JSONResponse(content=result, status_code=200)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")


# ---> Delete user
@router.delete(f"{URI}/users/{{user_id}}", tags=['Users'])
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    # payload = JWT_Authentication.decode_token(token)
    user = db.query(User).filter(User.id == user_id).first()

    if user:
        db.delete(user)
        db.commit()

        return JSONResponse(content={"message": f"User {user.username} deleted successfully"})
    else:
        raise HTTPException(status_code=404, detail="User not found")


# ========================
#      CATEGORIES
# ========================
    
# ---> Create category
@router.post(f"{URI}/categories/", response_model=dict, tags=['Categories'])
async def create_category(category: CategoryCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> dict:
    payload = JWT_Authentication.decode_token(token)

    # Verificar si la categoria ya existe
    existing_category = db.query(Category).filter(Category.name == category.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category already exists")

    new_category = Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return JSONResponse(content={"message": "Category created successfully", "category": new_category.as_dict()})


# ---> Read categories
@router.get(f"{URI}/categories/", tags=['Categories'], response_model=List[CategoryCreate]) # RESPONSE MODEL TEST = I NEED MORE INFORMATION FOR THIS
async def get_category(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> List[CategoryCreate]: # RESPONSE MODEL TEST = I NEED MORE INFORMATION FOR THIS
    payload = JWT_Authentication.decode_token(token)
    categories = db.query(Category).all()
    return JSONResponse(content={"categories": [category.as_dict() for category in categories]})


# ========================
#      PRODUCTS
# ========================

# ---> Create product
@router.post(f"{URI}/products/", response_model=dict, tags=['Products'])
async def create_product(item: ProductCreate = Depends(), product_image: UploadFile = File(...), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = JWT_Authentication.decode_token(token)

    user = db.query(User).filter(User.username == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_product = Product(
        name = item.name,
        description = item.description,
        product_code = item.product_code,
        brand = item.brand,
        detailed_description = item.detailed_description,
        purchase_price = item.purchase_price,
        sale_price = item.sale_price,
        units_in_stock = item.units_in_stock,
        warehouse_location = item.warehouse_location,
        manufacturing_date = item.manufacturing_date,
        expiration_date = item.expiration_date,
        min_inventory_level = item.min_inventory_level,
        additional_notes = item.additional_notes,
        tax_info = item.tax_info,
        units_sold = item.units_sold,
        movement_history = item.movement_history,
        company_id = user.company_id
    )

    for category_id in item.category_ids:
        category = db.query(Category).filter(Category.id == category_id).first()
        if category:
            new_product.categories.append(category)
        else:
            raise HTTPException(status_code=404, detail=f"Category with ID {category_id} not found")

    if product_image:
        image_path = f"app/uploaded_images/{product_image.filename}"
        with open(image_path, "wb") as f:
            f.write(product_image.file.read())
        new_product.image = image_path

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    result = {"message": "Product created successfully", "product": new_product.as_dict()}

    return JSONResponse(content=result, status_code=200)


# ---> Read products
@router.get(f"{URI}/products/", tags=['Products'], response_model=List[ProductCreate]) # RESPONSE MODEL TEST = I NEED MORE INFORMATION FOR THIS
async def get_products(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> List[ProductCreate]: # RESPONSE MODEL TEST = I NEED MORE INFORMATION FOR THIS
    payload = JWT_Authentication.decode_token(token)
    user = db.query(User).filter(User.username == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    products = db.query(Product).filter(Product.company_id == user.company_id).all()

    result = {"products": [product.as_dict() for product in products]}

    return JSONResponse(content=result, status_code=200)


# ---> Search product for id number
@router.get(f"{URI}/products/{{product_id}}", tags=['Products'])
async def get_product(product_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = JWT_Authentication.decode_token(token)
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        return JSONResponse(content={"product": product.as_dict()})
    else:
        raise HTTPException(status_code=404, detail="Product not found")


# ---> Update product
@router.put(f"{URI}/products/{{product_id}}", tags=['Products'])
async def update_product(product_id: int, item: ProductUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = JWT_Authentication.decode_token(token)
    product = db.query(Product).filter(Product.id == product_id).first()

    if product:
        # Actualiza solo los campos proporcionados en la solicitud
        for field, value in item.dict().items():
            if value is not None:
                setattr(product, field, value)

        db.commit()
        db.refresh(product)

        result = {"message": f"Product {product_id} updated successfully", "product": product.as_dict()}
        return JSONResponse(content=result, status_code=200)
    else:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")


# ---> Delete product
@router.delete(f"{URI}/products/{{product_id}}", tags=['Products'])
async def delete_product(product_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = JWT_Authentication.decode_token(token)
    product = db.query(Product).filter(Product.id == product_id).first()

    if product:
        db.delete(product)
        db.commit()

        return JSONResponse(content={"message": "Product deleted successfully"})
    else:
        raise HTTPException(status_code=404, detail="Product not found")


# ========================
#      ORDERS
# ========================
# ---> Create order
@router.post(f"{URI}/orders/", response_model=dict, tags=['Orders'])
async def create_order(order_data: OrderCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = JWT_Authentication.decode_token(token)
    new_order = Order(customer_name=order_data.customer_name)
    
    for product_id, quantity in zip(order_data.product_ids, order_data.quantities):
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            # Verifica que haya suficientes unidades en stock antes de crear la orden
            if product.units_in_stock >= quantity:
                # Crea el item de la orden
                order_item = OrderItem(
                    quantity=quantity,
                    unit_price=product.sale_price,
                    total_price=product.sale_price * quantity
                )
                order_item.product = product
                new_order.items.append(order_item)

                # Actualiza la cantidad en stock del producto
                product.units_in_stock -= quantity
                # Actualiza la cantidad de productos vendidos
                product.units_sold += quantity
            else:
                raise HTTPException(status_code=400, detail=f"Not enough units in stock for product {product_id}")
        else:
            raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    result = {"message": "Order created successfully", "order": new_order.as_dict()}
    return JSONResponse(content=result, status_code=200)


# ---> Read orders
@router.get(f"{URI}/orders/", response_model=List[dict], tags=['Orders'])
async def get_orders(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = JWT_Authentication.decode_token(token)
    orders = db.query(Order).all()

    result = [order.as_dict() for order in orders]
    return JSONResponse(content=result, status_code=200)