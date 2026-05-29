from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.schemas.auth import LoginRequest, TokenResponse, RegisterRequest
from backend.schemas.usuario import UsuarioResponse
from backend.services import auth_service
from backend.models.junta_vecinal import JuntaVecinal
from backend.models.tipo_incidente import TipoIncidente
from backend.utils.deps import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    token = auth_service.login(data.email, data.password, db)
    return TokenResponse(access_token=token)


@router.post("/register", response_model=UsuarioResponse, status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return auth_service.register(data, db)


@router.get("/juntas")
def juntas_publicas(db: Session = Depends(get_db)):
    return db.query(JuntaVecinal).filter(JuntaVecinal.activa == True).all()


@router.get("/tipos")
def tipos_publicos(db: Session = Depends(get_db)):
    return db.query(TipoIncidente).all()
