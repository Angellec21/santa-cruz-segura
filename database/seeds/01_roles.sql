USE santa_cruz_segura;

INSERT IGNORE INTO rol (nombre, descripcion) VALUES
  ('vecino',    'Ciudadano del barrio, puede reportar incidentes'),
  ('directivo', 'Directivo de junta, gestiona reportes y emite alertas'),
  ('autoridad', 'Autoridad policial o municipal, acceso de solo lectura amplio'),
  ('admin',     'Administrador del sistema, CRUD completo');
