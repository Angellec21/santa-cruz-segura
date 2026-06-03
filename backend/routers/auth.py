from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.schemas.auth import LoginRequest, TokenResponse, RegisterRequest
from backend.schemas.usuario import UsuarioResponse
from backend.services import auth_service
from backend.models.junta_vecinal import JuntaVecinal
from backend.models.tipo_incidente import TipoIncidente
from backend.utils.deps import get_db


class VerificarCodigoRequest(BaseModel):
    email: str
    codigo: str


class ReenviarCodigoRequest(BaseModel):
    email: str

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    token = auth_service.login(data.email, data.password, db)
    return TokenResponse(access_token=token)


@router.post("/register", response_model=UsuarioResponse, status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return auth_service.register(data, db)


@router.get("/verificar/{token}", response_class=HTMLResponse)
def verificar_email(token: str, db: Session = Depends(get_db)):
    ok = auth_service.verificar_email(token, db)
    if ok:
        return HTMLResponse("""
        <html><head><meta charset='UTF-8'/>
        <meta http-equiv='refresh' content='4;url=/index.html'/>
        <style>body{font-family:Inter,sans-serif;background:#060e0a;color:#f1f5f9;display:flex;align-items:center;justify-content:center;height:100vh;margin:0}
        .box{text-align:center;border:1px solid rgba(0,212,122,.25);border-radius:16px;padding:2.5rem 3rem;background:rgba(0,212,122,.05)}
        h2{color:#00d47a}p{color:#94a3b8;font-size:.9rem}</style></head>
        <body><div class='box'>
        <h2>✓ Correo verificado</h2>
        <p>Tu cuenta está activa. Redirigiendo al inicio de sesión…</p>
        </div></body></html>
        """)
    return HTMLResponse("""
    <html><head><meta charset='UTF-8'/><style>body{font-family:Inter,sans-serif;background:#060e0a;color:#f1f5f9;display:flex;align-items:center;justify-content:center;height:100vh;margin:0}
    .box{text-align:center;border:1px solid rgba(248,113,113,.25);border-radius:16px;padding:2.5rem 3rem}
    h2{color:#f87171}p{color:#94a3b8;font-size:.9rem}</style></head>
    <body><div class='box'><h2>Enlace inválido o expirado</h2>
    <p><a href='/index.html' style='color:#00d47a'>Volver al inicio</a></p>
    </div></body></html>
    """, status_code=400)


@router.post("/verificar-codigo")
def verificar_codigo(data: VerificarCodigoRequest, db: Session = Depends(get_db)):
    ok = auth_service.verificar_codigo(data.email, data.codigo, db)
    if not ok:
        raise HTTPException(status_code=400, detail="Código incorrecto. Revisa tu correo.")
    return {"message": "Correo verificado. Ya puedes iniciar sesión."}


@router.post("/reenviar-codigo")
def reenviar_codigo(data: ReenviarCodigoRequest, db: Session = Depends(get_db)):
    auth_service.reenviar_codigo(data.email, db)
    return {"message": "Código reenviado. Revisa tu bandeja de entrada."}


@router.get("/juntas")
def juntas_publicas(db: Session = Depends(get_db)):
    return db.query(JuntaVecinal).filter(JuntaVecinal.activa == True).all()


@router.get("/tipos")
def tipos_publicos(db: Session = Depends(get_db)):
    return db.query(TipoIncidente).all()
