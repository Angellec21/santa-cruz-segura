SET SQL_SAFE_UPDATES = 0;

-- Promover lecaroquispe@gmail.com a admin
UPDATE usuario
SET id_rol = 4
WHERE email = 'lecaroquispe@gmail.com';

-- Insertar usuarios de prueba (contraseña: Admin123)
INSERT IGNORE INTO usuario (id_junta, id_rol, nombre, apellido, email, password_hash, activo) VALUES
  (2, 2, 'Maria',  'Directiva', 'directivo@scs.bo', '$2b$12$VJCJr5Bz4.Lr7kFl1YtNi.nkRey2xThG5UA.J8xTBrrPpAbXAw.9y', TRUE),
  (3, 3, 'Carlos', 'Policia',   'policia@scs.bo',   '$2b$12$VJCJr5Bz4.Lr7kFl1YtNi.nkRey2xThG5UA.J8xTBrrPpAbXAw.9y', TRUE),
  (1, 1, 'Juan',   'Vecino',    'vecino@scs.bo',    '$2b$12$VJCJr5Bz4.Lr7kFl1YtNi.nkRey2xThG5UA.J8xTBrrPpAbXAw.9y', TRUE);
