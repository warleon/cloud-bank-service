from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime, date
import os
import time

# Configuración de base de datos con reintentos
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin123@localhost:5432/clientes_db")

def create_db_engine(retries=5, delay=5):
    """Crea la conexión a la base de datos con reintentos"""
    for i in range(retries):
        try:
            engine = create_engine(DATABASE_URL)
            # Intentar conectar
            engine.connect()
            print(f"✅ Conectado a PostgreSQL exitosamente")
            return engine
        except Exception as e:
            print(f"⚠️  Intento {i + 1}/{retries} - PostgreSQL no disponible aún. Reintentando en {delay}s...")
            if i == retries - 1:
                print(f"❌ Error al conectar a PostgreSQL después de {retries} intentos: {e}")
                raise
            time.sleep(delay)

engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelos SQLAlchemy
class ClienteDB(Base):
    __tablename__ = "clientes"
    cliente_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    telefono = Column(String(20))
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    estado = Column(String(20), default="activo")
    documentos = relationship("DocumentoIdentidadDB", back_populates="cliente", cascade="all, delete-orphan")

class DocumentoIdentidadDB(Base):
    __tablename__ = "documentos_identidad"
    documento_id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.cliente_id"))
    tipo_documento = Column(String(20), nullable=False)
    numero_documento = Column(String(20), unique=True, nullable=False)
    fecha_emision = Column(Date)
    fecha_vencimiento = Column(Date)
    cliente = relationship("ClienteDB", back_populates="documentos")

# Schemas Pydantic
class DocumentoIdentidadBase(BaseModel):
    tipo_documento: str
    numero_documento: str
    fecha_emision: Optional[date] = None
    fecha_vencimiento: Optional[date] = None

class DocumentoIdentidadResponse(DocumentoIdentidadBase):
    documento_id: int
    cliente_id: int
    
    class Config:
        from_attributes = True

class ClienteBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str] = None
    estado: Optional[str] = "activo"

class ClienteCreate(ClienteBase):
    documento: DocumentoIdentidadBase

class ClienteResponse(ClienteBase):
    cliente_id: int
    fecha_registro: datetime
    documentos: List[DocumentoIdentidadResponse] = []
    
    class Config:
        from_attributes = True

# FastAPI App
app = FastAPI(title="MS1 - Gestión de Clientes", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints
@app.get("/")
def root():
    return {
        "servicio": "MS1 - Gestión de Clientes",
        "version": "1.0.0",
        "estado": "activo"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/clientes", response_model=ClienteResponse, status_code=201)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """Crear un nuevo cliente con su documento de identidad"""
    # Verificar si el email ya existe
    db_cliente = db.query(ClienteDB).filter(ClienteDB.email == cliente.email).first()
    if db_cliente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # Verificar si el documento ya existe
    db_documento = db.query(DocumentoIdentidadDB).filter(
        DocumentoIdentidadDB.numero_documento == cliente.documento.numero_documento
    ).first()
    if db_documento:
        raise HTTPException(status_code=400, detail="El número de documento ya está registrado")
    
    # Crear cliente
    nuevo_cliente = ClienteDB(
        nombre=cliente.nombre,
        apellido=cliente.apellido,
        email=cliente.email,
        telefono=cliente.telefono,
        estado=cliente.estado
    )
    db.add(nuevo_cliente)
    db.flush()
    
    # Crear documento
    nuevo_documento = DocumentoIdentidadDB(
        cliente_id=nuevo_cliente.cliente_id,
        tipo_documento=cliente.documento.tipo_documento,
        numero_documento=cliente.documento.numero_documento,
        fecha_emision=cliente.documento.fecha_emision,
        fecha_vencimiento=cliente.documento.fecha_vencimiento
    )
    db.add(nuevo_documento)
    db.commit()
    db.refresh(nuevo_cliente)
    
    return nuevo_cliente

@app.get("/clientes", response_model=List[ClienteResponse])
def listar_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todos los clientes"""
    clientes = db.query(ClienteDB).offset(skip).limit(limit).all()
    return clientes

@app.get("/clientes/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Obtener un cliente por ID"""
    cliente = db.query(ClienteDB).filter(ClienteDB.cliente_id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@app.get("/clientes/email/{email}", response_model=ClienteResponse)
def obtener_cliente_por_email(email: str, db: Session = Depends(get_db)):
    """Obtener un cliente por email"""
    cliente = db.query(ClienteDB).filter(ClienteDB.email == email).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@app.get("/clientes/documento/{numero_documento}", response_model=ClienteResponse)
def obtener_cliente_por_documento(numero_documento: str, db: Session = Depends(get_db)):
    """Obtener un cliente por número de documento"""
    documento = db.query(DocumentoIdentidadDB).filter(
        DocumentoIdentidadDB.numero_documento == numero_documento
    ).first()
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return documento.cliente

@app.put("/clientes/{cliente_id}", response_model=ClienteResponse)
def actualizar_cliente(cliente_id: int, cliente: ClienteBase, db: Session = Depends(get_db)):
    """Actualizar información de un cliente"""
    db_cliente = db.query(ClienteDB).filter(ClienteDB.cliente_id == cliente_id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Verificar si el nuevo email ya existe en otro cliente
    if cliente.email != db_cliente.email:
        email_existe = db.query(ClienteDB).filter(
            ClienteDB.email == cliente.email,
            ClienteDB.cliente_id != cliente_id
        ).first()
        if email_existe:
            raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    db_cliente.nombre = cliente.nombre
    db_cliente.apellido = cliente.apellido
    db_cliente.email = cliente.email
    db_cliente.telefono = cliente.telefono
    db_cliente.estado = cliente.estado
    
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@app.delete("/clientes/{cliente_id}")
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Eliminar un cliente"""
    db_cliente = db.query(ClienteDB).filter(ClienteDB.cliente_id == cliente_id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    db.delete(db_cliente)
    db.commit()
    return {"mensaje": "Cliente eliminado exitosamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
