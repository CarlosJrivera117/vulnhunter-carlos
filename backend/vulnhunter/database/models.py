"""Relational persistence model for the VulnHunter MVP."""

from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import relationship

from vulnhunter.database.connection import Base


class User(Base):
    __tablename__ = "users"

        # Identificador único de cada usuario (número que crece solo: 1, 2, 3...).
    id = Column(Integer, primary_key=True, index=True)

    # --- Datos de acceso ---
    # Correo: debe ser único (no se puede repetir) y obligatorio.
    email = Column(String(150), unique=True, nullable=False)
    # Contraseña cifrada con bcrypt (NUNCA se guarda en texto plano).
    hashed_password = Column(String(255), nullable=False)

    # --- Datos personales (los que se piden en el registro) ---
    # Nombre y apellido del usuario. Obligatorios.
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    # RUT chileno con formato 12.345.678-9. Único para que no se repita.
    rut = Column(String(20), unique=True, nullable=True)
    # Número de contacto (teléfono). Opcional.
    telefono = Column(String(30), nullable=True)
    # Fecha de nacimiento. Opcional.
    fecha_nacimiento = Column(String(20), nullable=True)

    # --- Rol: define qué panel ve el usuario ---
    # "user" = cliente (ve solo sus escaneos).
    # "admin" = administrador (ve el movimiento de toda la plataforma).
    role = Column(String(20), nullable=False, default="user", server_default="user")

    # --- Estado y fecha de creación ---
    # is_active: permite "desactivar" una cuenta sin borrarla.
    is_active = Column(Boolean, nullable=False, default=True, server_default=text("true"))
    # created_at: guarda automáticamente cuándo se creó la cuenta.
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=text("CURRENT_TIMESTAMP"),
    )


    websites = relationship(
        "Website",
        back_populates="owner",
        cascade="all, delete-orphan",
    )
    requested_scans = relationship(
        "Scan",
        back_populates="requested_by",
        foreign_keys="Scan.requested_by_user_id",
    )


class Website(Base):
    # Tabla "websites": guarda los sitios web que un usuario registra para analizar.
    __tablename__ = "websites"

    __table_args__ = (
        # Un mismo usuario no puede registrar dos veces la misma URL.
        UniqueConstraint("user_id", "url", name="uq_websites_user_url"),
        # El estado de verificación solo puede ser uno de estos cuatro valores.
        CheckConstraint(
            "verification_status IN ('pending', 'verified', 'failed', 'expired')",
            name="ck_websites_verification_status",
        ),
        # Índice para buscar rápido los sitios de un usuario.
        Index("ix_websites_user_id", "user_id"),
    )

    # Identificador único del sitio.
    id = Column(Integer, primary_key=True, index=True)
    # Dirección del sitio web a analizar.
    url = Column(String(500), nullable=False)
    # A qué usuario pertenece este sitio. Si se borra el usuario, se borran sus sitios (CASCADE).
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # Fecha en que se registró el sitio (se llena sola).
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    # --- Verificación de propiedad del sitio ---
    # Estado: si el usuario demostró o no que el sitio es suyo.
    verification_status = Column(
        String(20), nullable=False, default="pending", server_default="pending"
    )
    # Método usado para verificar (por archivo, por DNS, etc.).
    verification_method = Column(String(50), nullable=True)
    # Token de verificación cifrado.
    verification_token_hash = Column(String(255), nullable=True)
    # Fecha en que se verificó el sitio.
    verified_at = Column(DateTime(timezone=True), nullable=True)
    # Permite desactivar un sitio sin borrarlo.
    is_active = Column(Boolean, nullable=False, default=True, server_default=text("true"))

    # --- Relaciones con otras tablas ---
    # "owner": el usuario dueño de este sitio.
    owner = relationship("User", back_populates="websites")
    # "scans": todos los escaneos hechos a este sitio. Si se borra el sitio, se borran sus escaneos.
    scans = relationship("Scan", back_populates="website", cascade="all, delete-orphan")



class Scan(Base):
    # Tabla "scans": guarda cada análisis que se le hace a un sitio web.
    __tablename__ = "scans"

    __table_args__ = (
        # El estado del escaneo solo puede ser uno de estos valores.
        CheckConstraint(
            "status IN ('pending', 'running', 'completed', 'partial', 'failed')",
            name="ck_scans_status",
        ),
        # El progreso debe ir entre 0 y 100 (es un porcentaje).
        CheckConstraint(
            "progress_percentage BETWEEN 0 AND 100",
            name="ck_scans_progress_percentage",
        ),
        # El total de vulnerabilidades nunca puede ser negativo.
        CheckConstraint(
            "total_vulnerabilities >= 0",
            name="ck_scans_total_vulnerabilities",
        ),
        # El puntaje de riesgo, si existe, va entre 0 y 100.
        CheckConstraint(
            "risk_score IS NULL OR risk_score BETWEEN 0 AND 100",
            name="ck_scans_risk_score",
        ),
        # El nivel de riesgo solo puede ser uno de estos valores.
        CheckConstraint(
            "risk_level IS NULL OR risk_level IN ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO')",
            name="ck_scans_risk_level",
        ),
        # Índices para acelerar las búsquedas más comunes.
        Index("ix_scans_website_id", "website_id"),
        Index("ix_scans_requested_by_user_id", "requested_by_user_id"),
        Index("ix_scans_status_started_at", "status", "started_at"),
    )

    # Identificador interno del escaneo (número).
    id = Column(Integer, primary_key=True, index=True)
    # Identificador público del escaneo (texto único, ej: un UUID).
    scan_id = Column(String(100), unique=True, nullable=False)
    # URL que se analizó.
    url = Column(String(500), nullable=False)
    # A qué sitio registrado pertenece. Si se borra el sitio, se borran sus escaneos (CASCADE).
    website_id = Column(Integer, ForeignKey("websites.id", ondelete="CASCADE"), nullable=True)
    # Qué usuario pidió el escaneo. Si se borra el usuario, el escaneo queda sin dueño (SET NULL).
    requested_by_user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    # Descripción opcional del escaneo.
    description = Column(String(500), nullable=True)
    # Qué tipos de escaneo se pidieron (SSL, XSS, etc.), guardados como texto.
    scan_types = Column(Text, nullable=False)
    # Estado actual del escaneo (pendiente, corriendo, completado...).
    status = Column(String(50), nullable=False, default="pending", server_default="pending")
    # Fecha y hora en que empezó el escaneo (se llena sola).
    started_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=text("CURRENT_TIMESTAMP"),
    )
    # Fecha y hora en que terminó el escaneo.
    completed_at = Column(DateTime(timezone=True), nullable=True)
    # Porcentaje de avance del escaneo (0 a 100).
    progress_percentage = Column(Integer, nullable=False, default=0, server_default="0")
    # Qué escáner se está ejecutando en este momento.
    current_scanner = Column(String(100), nullable=True)
    # Cantidad total de vulnerabilidades encontradas.
    total_vulnerabilities = Column(Integer, nullable=False, default=0, server_default="0")
    # Puntaje de riesgo calculado (0 a 100).
    risk_score = Column(Integer, nullable=True)
    # Nivel de riesgo en palabras (CRITICAL, HIGH, MEDIUM, LOW, INFO).
    risk_level = Column(String(50), nullable=True)
    # Errores ocurridos durante el escaneo, guardados como texto (JSON).
    errors = Column(Text, nullable=False, default="{}", server_default="{}")

    # --- Relaciones con otras tablas ---
    # "website": el sitio al que pertenece este escaneo.
    website = relationship("Website", back_populates="scans")
    # "requested_by": el usuario que solicitó este escaneo.
    requested_by = relationship(
        "User",
        back_populates="requested_scans",
        foreign_keys=[requested_by_user_id],
    )
    # "findings": los hallazgos (vulnerabilidades) encontrados en este escaneo.
    findings = relationship(
        "Finding",
        back_populates="scan",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

class Finding(Base):
    # Tabla "findings": guarda cada vulnerabilidad encontrada en un escaneo.
    __tablename__ = "findings"

    __table_args__ = (
        # La severidad solo puede ser uno de estos valores.
        CheckConstraint(
            "severity IN ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO')",
            name="ck_findings_severity",
        ),
        # El nivel de confianza solo puede ser uno de estos tres.
        CheckConstraint(
            "confidence IN ('high', 'medium', 'low')",
            name="ck_findings_confidence",
        ),
        # Índices para buscar rápido por escaneo y por severidad.
        Index("ix_findings_scan_id", "scan_id"),
        Index("ix_findings_severity", "severity"),
    )

    # Identificador único del hallazgo.
    id = Column(Integer, primary_key=True, index=True)
    # A qué escaneo pertenece. Si se borra el escaneo, se borran sus hallazgos (CASCADE).
    scan_id = Column(Integer, ForeignKey("scans.id", ondelete="CASCADE"), nullable=False)
    # Tipo de vulnerabilidad (ej: "XSS", "SQL Injection").
    type = Column(String(100), nullable=False)
    # Gravedad del hallazgo (CRITICAL, HIGH, MEDIUM, LOW, INFO).
    severity = Column(String(50), nullable=False)
    # Dónde se encontró la vulnerabilidad (URL, parámetro, etc.).
    location = Column(String(500), nullable=True)
    # Qué escáner detectó este hallazgo.
    scanner = Column(String(100), nullable=True)
    # Descripción detallada de la vulnerabilidad.
    description = Column(Text, nullable=True)
    # Recomendación de cómo solucionarla.
    recommendation = Column(Text, nullable=True)
    # Evidencia que demuestra el hallazgo.
    evidence = Column(Text, nullable=True)
    # Nivel de confianza en que el hallazgo es real (high, medium, low).
    confidence = Column(String(50), nullable=False, default="low", server_default="low")
    # Fecha en que se registró el hallazgo (se llena sola).
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    # --- Relación con la tabla de escaneos ---
    # "scan": el escaneo al que pertenece este hallazgo.
    scan = relationship("Scan", back_populates="findings")

