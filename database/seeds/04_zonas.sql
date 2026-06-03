USE santa_cruz_segura;

INSERT IGNORE INTO zona_caliente (id_junta, nombre, latitud_centro, longitud_centro, radio_metros, nivel_riesgo) VALUES
  (1, 'Zona Los Mangales Centro',      -17.7834, -63.1821, 300, 'medio'),
  (1, 'Zona Los Mangales Norte',       -17.7790, -63.1850, 250, 'bajo'),
  (2, 'Zona Villa Primero Central',    -17.7654, -63.1934, 300, 'alto'),
  (2, 'Zona Villa Primero Sur',        -17.7700, -63.1960, 200, 'medio'),
  (3, 'Zona Equipetrol Norte',         -17.7701, -63.1756, 350, 'bajo'),
  (3, 'Zona Equipetrol Av. Banzer',    -17.7680, -63.1720, 250, 'medio'),
  (4, 'Zona El Pari Mercado',          -17.7912, -63.1643, 300, 'critico'),
  (4, 'Zona El Pari Residencial',      -17.7950, -63.1680, 200, 'alto'),
  (5, 'Zona Pampa de la Isla Acceso',  -17.7488, -63.1901, 300, 'medio'),
  (5, 'Zona Pampa de la Isla Centro',  -17.7510, -63.1870, 250, 'bajo');
