USE santa_cruz_segura;

INSERT IGNORE INTO tipo_incidente (nombre, descripcion, icono) VALUES
  ('Robo a domicilio',  'Ingreso forzado a vivienda',         'home-alert'),
  ('Robo a transeúnte', 'Asalto en vía pública',              'run-fast'),
  ('Hurto',             'Sustracción sin violencia',           'bag-personal'),
  ('Violencia',         'Agresión física o verbal',            'fist'),
  ('Persona sospechosa','Comportamiento sospechoso en la zona','eye'),
  ('Vandalismo',        'Daño a bienes públicos o privados',   'spray'),
  ('Otro',              'Incidente no categorizado',           'alert-circle');
