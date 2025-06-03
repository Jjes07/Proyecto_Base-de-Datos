USE nodo;

-- Usuario
INSERT INTO usuario (documento, nombre, email, genero, referencia_bancaria) VALUES
('123456789', 'Ana Torres', 'ana@example.com', 'F', 'REF001'),
('987654321', 'Luis Pérez', 'luis@example.com', 'M', 'REF002'),
('456789123', 'Carlos Ríos', 'carlos@example.com', 'M', 'REF003'),
('321654987', 'Laura Gómez', 'laura@example.com', 'F', 'REF004'),
('654987321', 'Jorge Díaz', 'jorge@example.com', 'M', 'REF005');

-- Administrador
INSERT INTO administrador (nombre, email, contraseña) VALUES
('Lucía Herrera', 'lucia.admin@lms.com', 'admin123'),
('José Ramírez', 'jose.admin@lms.com', 'admin456'),
('Sofía Peña', 'sofia.admin@lms.com', 'admin789'),
('Marcos Vidal', 'marcos.admin@lms.com', 'admin321'),
('Elena Rojas', 'elena.admin@lms.com', 'admin654');

-- Profesor
INSERT INTO profesor (email, telefono, area_principal, area_alternativa, contraseña) VALUES
('profe1@lms.com', '3011111111', 'Matemáticas', 'Física', 'clave1'),
('profe2@lms.com', '3022222222', 'Finanzas', 'Estadística', 'clave2'),
('profe3@lms.com', '3033333333', 'Música', 'Arte', 'clave3'),
('profe4@lms.com', '3044444444', 'Sistemas', 'Redes', 'clave4'),
('profe5@lms.com', '3055555555', 'Mecánica', 'Ingeniería', 'clave5');

-- Estudiante
INSERT INTO estudiante (email, contraseña) VALUES
('est1@lms.com', 'est123'),
('est2@lms.com', 'est234'),
('est3@lms.com', 'est345'),
('est4@lms.com', 'est456'),
('est5@lms.com', 'est567');

-- Curso
INSERT INTO curso (id_profesor, nombre, categoria, url, fecha_inicio, fecha_fin, año, semestre, precio) VALUES
(1, 'Álgebra Lineal', 'Matemáticas', 'http://curso1.com', '2025-01-15', '2025-05-15', 2025, 1, 250000),
(2, 'Contabilidad Básica', 'Finanzas', 'http://curso2.com', '2025-01-20', '2025-05-20', 2025, 1, 300000),
(3, 'Introducción a la Música', 'Música', 'http://curso3.com', '2025-01-10', '2025-05-10', 2025, 1, 200000),
(4, 'Programación I', 'Sistemas', 'http://curso4.com', '2025-02-01', '2025-06-01', 2025, 1, 350000),
(5, 'Termodinámica', 'Mecánica', 'http://curso5.com', '2025-03-01', '2025-07-01', 2025, 1, 280000);

-- Matricula
INSERT INTO matricula (id_estudiante, id_admin, id_curso, fecha_matricula, estado, contraseña_ingreso) VALUES
(1, 1, 1, '2025-01-05', 'activa', 'm123'),
(2, 2, 2, '2025-01-07', 'activa', 'm234'),
(3, 3, 3, '2025-01-10', 'activa', 'm345'),
(4, 4, 4, '2025-01-12', 'activa', 'm456'),
(5, 5, 5, '2025-01-15', 'activa', 'm567');

-- Pago
INSERT INTO pago (id_curso, fecha_pago, referencia_bancaria) VALUES
(1, '2025-01-04', 'REF001'),
(2, '2025-01-06', 'REF002'),
(3, '2025-01-08', 'REF003'),
(4, '2025-01-11', 'REF004'),
(5, '2025-01-13', 'REF005');

-- Material
INSERT INTO material (id_curso, id_profesor, titulo, descripcion, nombre_archivo) VALUES
(1, 1, 'Vectores y Matrices', 'PDF del curso de álgebra', 'algebra1.pdf'),
(2, 2, 'Balance contable', 'Guía de ejercicios', 'finanzas1.pdf'),
(3, 3, 'Partituras básicas', 'Material para lectura musical', 'musica1.pdf'),
(4, 4, 'Sintaxis en Python', 'Primeros pasos en programación', 'programa1.pdf'),
(5, 5, 'Procesos térmicos', 'Notas sobre calor y energía', 'termo1.pdf');

-- Tarea
INSERT INTO tarea (id_curso, id_profesor, nombre, descripcion, fecha_creacion, fecha_entrega, puntaje, archivo_profesor) VALUES
(1, 1, 'Tarea 1', 'Ejercicios de vectores', '2025-01-16', '2025-01-30', 5.0, 'vectores.pdf'),
(2, 2, 'Tarea 1', 'Libro diario', '2025-01-21', '2025-02-04', 4.0, 'diario.pdf'),
(3, 3, 'Tarea 1', 'Escala mayor', '2025-01-11', '2025-01-25', 5.0, 'escala.pdf'),
(4, 4, 'Tarea 1', 'Variables y tipos', '2025-02-02', '2025-02-16', 4.5, 'python.pdf'),
(5, 5, 'Tarea 1', 'Ejercicios de entropía', '2025-03-02', '2025-03-16', 5.0, 'entropia.pdf');

-- Foro
INSERT INTO foro (nombre, descripcion, fecha_creacion, fecha_terminacion, id_curso, id_profesor) VALUES
('Presentación', 'Foro para presentarse', '2025-01-15', '2025-05-15', 1, 1),
('Dudas Contables', 'Espacio para preguntas', '2025-01-20', '2025-05-20', 2, 2),
('Apreciación musical', 'Debates sobre obras musicales', '2025-01-10', '2025-05-10', 3, 3),
('Código limpio', 'Buenas prácticas en programación', '2025-02-01', '2025-06-01', 4, 4),
('Conceptos térmicos', 'Preguntas sobre calor y entropía', '2025-03-01', '2025-07-01', 5, 5);

-- MensajeForo
INSERT INTO mensajeforo (nombre, descripcion, id_foro, id_estudiante, id_mensaje_respuesta) VALUES
('Hola a todos', 'Un gusto empezar el curso', 1, 1, NULL),
('Pregunta 1', '¿Qué es el debe y el haber?', 2, 2, NULL),
('Re: Pregunta 1', 'Es una forma de balancear cuentas.', 2, 3, 2),
('Duda de clase', '¿Qué es una escala menor?', 3, 4, NULL),
('Comentario', 'Buen aporte!', 3, 5, 4);

-- RespuestaTarea
INSERT INTO respuestatarea (archivo_entrega, fecha_envio, id_tarea, id_estudiante) VALUES
('res1.pdf', '2025-01-25', 1, 1),
('res2.pdf', '2025-01-30', 2, 2),
('res3.pdf', '2025-01-28', 3, 3),
('res4.pdf', '2025-02-10', 4, 4),
('res5.pdf', '2025-03-10', 5, 5);

-- DescargaMaterial
INSERT INTO descarga_material (id_estudiante, id_material) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);

-- ProfesorInteresadoCurso
INSERT INTO profesor_interesado_curso (id_profesor, id_curso) VALUES
(1, 2),
(2, 3),
(3, 4),
(4, 5),
(5, 1);