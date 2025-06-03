CREATE DATABASE IF NOT EXISTS nodo;
USE nodo;

-- Usuario
CREATE TABLE IF NOT EXISTS usuario (
	id_nodo INT AUTO_INCREMENT PRIMARY KEY,
	documento VARCHAR(30) NOT NULL UNIQUE,
	nombre VARCHAR(50) NOT NULL,
	email VARCHAR(50) NOT NULL UNIQUE,
	genero VARCHAR(15),
	referencia_bancaria VARCHAR(50) NOT NULL UNIQUE
);

-- Administrador
CREATE TABLE IF NOT EXISTS administrador (
	id_admin INT AUTO_INCREMENT PRIMARY KEY,
	nombre VARCHAR(50) NOT NULL,
	email VARCHAR(50) NOT NULL UNIQUE,
	contraseña VARCHAR(50) NOT NULL
);

-- Profesor
CREATE TABLE IF NOT EXISTS profesor (
	id_profesor INT AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(50) NOT NULL UNIQUE,
	telefono VARCHAR(20) NOT NULL,
	area_principal VARCHAR(50) NOT NULL,
	area_alternativa VARCHAR(50),
	contraseña VARCHAR(50) NOT NULL
);

-- Estudiante
CREATE TABLE IF NOT EXISTS estudiante (
	id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(50) NOT NULL UNIQUE,
	contraseña VARCHAR(50) NOT NULL
);

-- Curso
CREATE TABLE IF NOT EXISTS curso (
	id_curso INT AUTO_INCREMENT PRIMARY KEY,
    id_profesor INT NOT NULL,
	nombre VARCHAR(100) NOT NULL,
	categoria VARCHAR(50),
	url TEXT NOT NULL,
	fecha_inicio DATE NOT NULL,
	fecha_fin DATE NOT NULL,
	año INT NOT NULL,
	semestre INT NOT NULL,
	precio FLOAT NOT NULL,
    FOREIGN KEY (id_profesor) REFERENCES profesor(id_profesor) 
		ON UPDATE CASCADE ON DELETE CASCADE
);

-- Matricula
CREATE TABLE IF NOT EXISTS matricula (
	id_matricula INT AUTO_INCREMENT PRIMARY KEY,
	id_estudiante INT NOT NULL,
	id_admin INT NOT NULL,
	id_curso INT NOT NULL,
	fecha_matricula DATE NOT NULL,
	estado VARCHAR(20) NOT NULL,
	contraseña_ingreso VARCHAR(50) NOT NULL,
	FOREIGN KEY (id_estudiante) REFERENCES estudiante(id_estudiante) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (id_admin) REFERENCES administrador(id_admin) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (id_curso) REFERENCES curso(id_curso) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Pago
CREATE TABLE IF NOT EXISTS pago (
	id_pago INT AUTO_INCREMENT PRIMARY KEY,
	id_curso INT NOT NULL,
	fecha_pago DATE NOT NULL,
	referencia_bancaria VARCHAR(50) NOT NULL,
	FOREIGN KEY (referencia_bancaria) REFERENCES usuario(referencia_bancaria) ON UPDATE CASCADE ON DELETE RESTRICT,
	FOREIGN KEY (id_curso) REFERENCES curso(id_curso) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Material
CREATE TABLE IF NOT EXISTS material (
	id_material INT AUTO_INCREMENT PRIMARY KEY,
	id_curso INT NOT NULL,
	id_profesor INT NOT NULL,
	titulo VARCHAR(100) NOT NULL,
	descripcion TEXT,
	nombre_archivo VARCHAR(255) NOT NULL,
	FOREIGN KEY (id_curso) REFERENCES curso(id_curso) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (id_profesor) REFERENCES profesor(id_profesor) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Tarea
CREATE TABLE IF NOT EXISTS tarea (
	id_tarea INT AUTO_INCREMENT PRIMARY KEY,
	id_curso INT NOT NULL,
	id_profesor INT NOT NULL,
	nombre VARCHAR(100) NOT NULL,
	descripcion TEXT,
	fecha_creacion DATE NOT NULL,
	fecha_entrega DATE NOT NULL,
	puntaje FLOAT NOT NULL,
	archivo_profesor VARCHAR(255) NOT NULL,
	FOREIGN KEY (id_curso) REFERENCES curso(id_curso) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (id_profesor) REFERENCES profesor(id_profesor) ON UPDATE CASCADE ON DELETE CASCADE
);

-- RespuestaTarea
CREATE TABLE IF NOT EXISTS respuestatarea (
	id_respuesta INT AUTO_INCREMENT PRIMARY KEY,
	id_tarea INT NOT NULL,
	id_estudiante INT NOT NULL,
	archivo_entrega VARCHAR(255) NOT NULL,
	fecha_envio DATE NOT NULL,
	FOREIGN KEY (id_tarea) REFERENCES tarea(id_tarea) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (id_estudiante) REFERENCES estudiante(id_estudiante) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Foro
CREATE TABLE IF NOT EXISTS foro (
	id_foro INT AUTO_INCREMENT PRIMARY KEY,
	id_curso INT NOT NULL,
	id_profesor INT NOT NULL,
	nombre VARCHAR(100) NOT NULL,
	descripcion TEXT,
	fecha_creacion DATE NOT NULL,
	fecha_terminacion DATE NOT NULL,
	FOREIGN KEY (id_curso) REFERENCES curso(id_curso) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (id_profesor) REFERENCES profesor(id_profesor) ON UPDATE CASCADE ON DELETE CASCADE
);

-- MensajeForo
CREATE TABLE IF NOT EXISTS mensajeforo (
  id_mensaje INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  descripcion TEXT,
  id_foro INT NOT NULL,
  id_estudiante INT,
  id_profesor INT,
  id_mensaje_respuesta INT,

  FOREIGN KEY (id_foro) REFERENCES foro(id_foro) ON DELETE CASCADE,
  FOREIGN KEY (id_estudiante) REFERENCES estudiante(id_estudiante) ON DELETE CASCADE,
  FOREIGN KEY (id_profesor) REFERENCES profesor(id_profesor) ON DELETE CASCADE,
  FOREIGN KEY (id_mensaje_respuesta) REFERENCES mensajeforo(id_mensaje) ON DELETE CASCADE,

  CHECK (
    (id_estudiante IS NOT NULL AND id_profesor IS NULL)
    OR (id_profesor IS NOT NULL AND id_estudiante IS NULL)
  )
);


-- ProfesorInteresadoCurso
CREATE TABLE IF NOT EXISTS profesor_interesado_curso (
	id_profesor INT NOT NULL,
	id_curso INT NOT NULL,
	PRIMARY KEY (id_profesor, id_curso),
	FOREIGN KEY (id_profesor) REFERENCES profesor(id_profesor) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (id_curso) REFERENCES curso(id_curso) ON UPDATE CASCADE ON DELETE CASCADE
);

-- DescargaMaterial
CREATE TABLE IF NOT EXISTS descarga_material (
	id_descarga INT PRIMARY KEY auto_increment NOT NULL,
	id_estudiante INT NOT NULL,
	id_material INT NOT NULL,
	FOREIGN KEY (id_estudiante) REFERENCES estudiante(id_estudiante) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (id_material) REFERENCES material(id_material) ON UPDATE CASCADE ON DELETE CASCADE
);
    
-- Crear el usuario 
CREATE USER IF NOT EXISTS 'admin_nodo'@'localhost' IDENTIFIED BY '1234';

-- permisos a la bd
GRANT ALL PRIVILEGES ON nodo.* TO 'admin_nodo'@'localhost';

-- Aplicar los cambios de privilegios
FLUSH PRIVILEGES;