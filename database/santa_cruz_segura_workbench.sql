-- ============================================================
--  Santa Cruz Segura Predictiva — Script MySQL 8
--  Ejecutar en MySQL Workbench: Cmd+Shift+Enter (Mac)
-- ============================================================

CREATE DATABASE IF NOT EXISTS santa_cruz_segura
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE santa_cruz_segura;

-- --------------------------------------------------------
-- 1. junta_vecinal
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS junta_vecinal (
  id_junta          INT AUTO_INCREMENT PRIMARY KEY,
  nombre            VARCHAR(100) NOT NULL,
  distrito          VARCHAR(50)  NOT NULL,
  descripcion       TEXT,
  latitud_centro    DECIMAL(10,8),
  longitud_centro   DECIMAL(11,8),
  activa            BOOLEAN DEFAULT TRUE,
  fecha_registro    DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- --------------------------------------------------------
-- 2. rol
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS rol (
  id_rol       INT AUTO_INCREMENT PRIMARY KEY,
  nombre       VARCHAR(30) NOT NULL UNIQUE,
  descripcion  TEXT
) ENGINE=InnoDB;

-- --------------------------------------------------------
-- 3. usuario
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuario (
  id_usuario     INT AUTO_INCREMENT PRIMARY KEY,
  id_junta       INT          NOT NULL,
  id_rol         INT          NOT NULL,
  nombre         VARCHAR(80)  NOT NULL,
  apellido       VARCHAR(80)  NOT NULL,
  email          VARCHAR(120) NOT NULL UNIQUE,
  telefono       VARCHAR(20),
  password_hash  VARCHAR(255) NOT NULL,
  latitud        DECIMAL(10,8),
  longitud       DECIMAL(11,8),
  activo              BOOLEAN      DEFAULT TRUE,
  email_verificado    TINYINT      NOT NULL DEFAULT 0,
  token_verificacion  VARCHAR(100) NULL,
  session_id          VARCHAR(36)  NULL,
  fecha_registro      DATETIME     DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_usuario_junta FOREIGN KEY (id_junta) REFERENCES junta_vecinal(id_junta),
  CONSTRAINT fk_usuario_rol   FOREIGN KEY (id_rol)   REFERENCES rol(id_rol)
) ENGINE=InnoDB;

-- --------------------------------------------------------
-- 4. tipo_incidente
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS tipo_incidente (
  id_tipo      INT AUTO_INCREMENT PRIMARY KEY,
  nombre       VARCHAR(60) NOT NULL UNIQUE,
  descripcion  TEXT,
  icono        VARCHAR(50)
) ENGINE=InnoDB;

-- --------------------------------------------------------
-- 5. zona_caliente
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS zona_caliente (
  id_zona              INT AUTO_INCREMENT PRIMARY KEY,
  id_junta             INT           NOT NULL,
  nombre               VARCHAR(100)  NOT NULL,
  latitud_centro       DECIMAL(10,8) NOT NULL,
  longitud_centro      DECIMAL(11,8) NOT NULL,
  radio_metros         INT           DEFAULT 200,
  nivel_riesgo         ENUM('bajo','medio','alto','critico') DEFAULT 'bajo',
  total_reportes_30d   INT DEFAULT 0,
  ultima_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_zona_junta FOREIGN KEY (id_junta) REFERENCES junta_vecinal(id_junta)
) ENGINE=InnoDB;

-- --------------------------------------------------------
-- 6. reporte
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS reporte (
  id_reporte      INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario      INT           NOT NULL,
  id_zona         INT           NOT NULL,
  id_tipo         INT           NOT NULL,
  descripcion     TEXT,
  latitud         DECIMAL(10,8) NOT NULL,
  longitud        DECIMAL(11,8) NOT NULL,
  estado          ENUM('pendiente','verificado','resuelto','descartado') DEFAULT 'pendiente',
  anonimo         BOOLEAN DEFAULT FALSE,
  fecha_incidente DATETIME NOT NULL,
  fecha_reporte   DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_reporte_usuario FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
  CONSTRAINT fk_reporte_zona    FOREIGN KEY (id_zona)    REFERENCES zona_caliente(id_zona),
  CONSTRAINT fk_reporte_tipo    FOREIGN KEY (id_tipo)    REFERENCES tipo_incidente(id_tipo)
) ENGINE=InnoDB;

-- --------------------------------------------------------
-- 7. evidencia
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS evidencia (
  id_evidencia   INT AUTO_INCREMENT PRIMARY KEY,
  id_reporte     INT          NOT NULL,
  tipo_archivo   ENUM('imagen','video','audio') NOT NULL,
  ruta_archivo   VARCHAR(255) NOT NULL,
  nombre_original VARCHAR(255),
  fecha_subida   DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_evidencia_reporte FOREIGN KEY (id_reporte) REFERENCES reporte(id_reporte) ON DELETE CASCADE
) ENGINE=InnoDB;

-- --------------------------------------------------------
-- 8. alerta
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS alerta (
  id_alerta    INT AUTO_INCREMENT PRIMARY KEY,
  id_zona      INT          NOT NULL,
  id_junta     INT          NOT NULL,
  id_creador   INT          NOT NULL,
  titulo       VARCHAR(150) NOT NULL,
  descripcion  TEXT,
  tipo         ENUM('preventiva','reactiva','informativa') NOT NULL,
  estado       ENUM('activa','resuelta','expirada') DEFAULT 'activa',
  fecha_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
  fecha_fin    DATETIME,
  CONSTRAINT fk_alerta_zona    FOREIGN KEY (id_zona)    REFERENCES zona_caliente(id_zona),
  CONSTRAINT fk_alerta_junta   FOREIGN KEY (id_junta)   REFERENCES junta_vecinal(id_junta),
  CONSTRAINT fk_alerta_creador FOREIGN KEY (id_creador) REFERENCES usuario(id_usuario)
) ENGINE=InnoDB;

-- --------------------------------------------------------
-- 9. prediccion_ia
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS prediccion_ia (
  id_prediccion   INT AUTO_INCREMENT PRIMARY KEY,
  id_zona         INT           NOT NULL,
  periodo_inicio  DATE          NOT NULL,
  periodo_fin     DATE          NOT NULL,
  nivel_predicho  VARCHAR(20)   NOT NULL,
  probabilidad    DECIMAL(5,4),
  features_json   TEXT,
  fecha_generacion DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_prediccion_zona FOREIGN KEY (id_zona) REFERENCES zona_caliente(id_zona)
) ENGINE=InnoDB;

-- --------------------------------------------------------
-- 10. notificacion
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS notificacion (
  id_notificacion INT AUTO_INCREMENT PRIMARY KEY,
  id_alerta       INT          NOT NULL,
  titulo          VARCHAR(150) NOT NULL,
  mensaje         TEXT         NOT NULL,
  fecha_envio     DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_notificacion_alerta FOREIGN KEY (id_alerta) REFERENCES alerta(id_alerta)
) ENGINE=InnoDB;

-- --------------------------------------------------------
-- 11. usuario_notificacion (tabla puente N:N)
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuario_notificacion (
  id_usuario       INT     NOT NULL,
  id_notificacion  INT     NOT NULL,
  leida            BOOLEAN DEFAULT FALSE,
  fecha_lectura    DATETIME,
  PRIMARY KEY (id_usuario, id_notificacion),
  CONSTRAINT fk_un_usuario       FOREIGN KEY (id_usuario)      REFERENCES usuario(id_usuario),
  CONSTRAINT fk_un_notificacion  FOREIGN KEY (id_notificacion) REFERENCES notificacion(id_notificacion)
) ENGINE=InnoDB;

-- ============================================================
-- TRIGGER: recalcula nivel_riesgo tras cada nuevo reporte
-- ============================================================
DELIMITER $$

CREATE TRIGGER trg_actualizar_zona_riesgo
AFTER INSERT ON reporte
FOR EACH ROW
BEGIN
  DECLARE total INT;

  SELECT COUNT(*) INTO total
  FROM reporte
  WHERE id_zona = NEW.id_zona
    AND fecha_reporte >= DATE_SUB(NOW(), INTERVAL 30 DAY);

  UPDATE zona_caliente
  SET
    total_reportes_30d = total,
    nivel_riesgo = CASE
      WHEN total >= 20 THEN 'critico'
      WHEN total >= 10 THEN 'alto'
      WHEN total >= 5  THEN 'medio'
      ELSE 'bajo'
    END
  WHERE id_zona = NEW.id_zona;
END$$

DELIMITER ;

-- ============================================================
-- VISTA: resumen por barrio para el dashboard
-- ============================================================
CREATE OR REPLACE VIEW v_resumen_barrio AS
SELECT
  j.id_junta,
  j.nombre                                          AS junta,
  j.distrito,
  COUNT(DISTINCT u.id_usuario)                      AS total_vecinos,
  COUNT(DISTINCT r.id_reporte)                      AS total_reportes,
  COUNT(DISTINCT CASE WHEN r.fecha_reporte >= DATE_SUB(NOW(), INTERVAL 30 DAY)
                      THEN r.id_reporte END)         AS reportes_30d,
  COUNT(DISTINCT CASE WHEN a.estado = 'activa'
                      THEN a.id_alerta END)          AS alertas_activas,
  MAX(z.nivel_riesgo)                               AS nivel_riesgo_max
FROM junta_vecinal j
LEFT JOIN usuario          u ON u.id_junta = j.id_junta
LEFT JOIN zona_caliente    z ON z.id_junta = j.id_junta
LEFT JOIN reporte          r ON r.id_zona  = z.id_zona
LEFT JOIN alerta           a ON a.id_junta = j.id_junta
GROUP BY j.id_junta, j.nombre, j.distrito;
