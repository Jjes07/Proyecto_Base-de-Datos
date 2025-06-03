USE nodo;

-- 1. Estudiantes por año y semestre
SELECT e.email AS nombre_estudiante, m.id_matricula
FROM Estudiante e
JOIN Matricula m ON e.id_estudiante = m.id_estudiante
JOIN Curso c ON m.id_curso = c.id_curso
WHERE c.año = 2025 AND c.semestre = 1
ORDER BY e.email;

-- 2. Estudiantes de un curso específico, año y semestre
SELECT e.email AS nombre_estudiante
FROM Estudiante e
JOIN Matricula m ON e.id_estudiante = m.id_estudiante
JOIN Curso c ON m.id_curso = c.id_curso
WHERE c.id_curso = 2 AND c.año = 2025 AND c.semestre = 1;

-- 3. Cursos de un estudiante en un rango de fechas
SELECT c.nombre, c.fecha_inicio, c.fecha_fin
FROM Curso c
JOIN Matricula m ON c.id_curso = m.id_curso
JOIN Estudiante e ON m.id_estudiante = e.id_estudiante
WHERE e.id_estudiante = 1 AND c.fecha_inicio >= '2025-01-01' AND c.fecha_fin <= '2025-12-31';

-- 4. Profesores y sus cursos actuales
SELECT p.id_profesor, p.email, c.nombre
FROM Profesor p
JOIN Curso c ON c.fecha_inicio <= CURRENT_DATE AND c.fecha_fin >= CURRENT_DATE
WHERE c.id_curso IN (
    SELECT id_curso FROM Curso WHERE fecha_inicio <= CURRENT_DATE AND fecha_fin >= CURRENT_DATE
);

-- 5. Cursos ordenados por categoría
SELECT nombre, categoria FROM Curso ORDER BY categoria;

-- 6. Cursos con precio entre 100000 y 500000
SELECT nombre, precio FROM Curso WHERE precio BETWEEN 100000 AND 500000;

-- 7. Usuarios registrados pero no matriculados para un año y semestre
SELECT u.nombre, u.email
FROM Usuario u
WHERE u.id_nodo NOT IN (
    SELECT DISTINCT us.id_nodo
    FROM Usuario us
    JOIN Pago p ON p.referencia_bancaria = us.referencia_bancaria
    JOIN Curso c ON p.id_curso = c.id_curso
    WHERE c.año = 2025 AND c.semestre = 1
);

-- 8. Cursos de una categoría específica
SELECT nombre, categoria FROM Curso WHERE categoria = 'Computación';

-- 9. Tareas del curso con id = 20
SELECT nombre, descripcion, fecha_entrega
FROM Tarea
WHERE id_curso = 20;

-- 10. Materiales publicados por el profesor en curso id = 20
SELECT titulo, descripcion, nombre_archivo
FROM Material
WHERE id_curso = 20;

-- 11. Mensajes de un foro en un curso dado (foro id = 3)
SELECT 
  m.id_mensaje, 
  m.nombre,
  COALESCE(e.email, p.email) AS emisor
FROM mensajeforo m
LEFT JOIN estudiante e ON m.id_estudiante = e.id_estudiante
LEFT JOIN profesor p ON m.id_profesor = p.id_profesor
WHERE m.id_foro = 3;

-- 12. Consulta importante: cantidad de estudiantes por curso
SELECT c.nombre, COUNT(m.id_matricula) AS total_estudiantes
FROM Curso c
JOIN Matricula m ON c.id_curso = m.id_curso
GROUP BY c.nombre
ORDER BY total_estudiantes DESC;

-- Consultas generales
SELECT *
FROM estudiante;
SELECT * 
FROM matricula;
SELECT *
FROM profesor_interesado_curso;
SELECT *
FROM profesor;
SELECT *
FROM curso;
SELECT *
FROM administrador;