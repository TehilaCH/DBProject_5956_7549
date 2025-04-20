CREATE TABLE if not exists Paramedic
(
  paramedic_id INT NOT NULL,
  paramedic_name VARCHAR(30) NOT NULL,
  experience NUMERIC(5),
  PRIMARY KEY (paramedic_id)
);

CREATE TABLE if not exists Medical_event
(
  event_id INT NOT NULL,
  event_location VARCHAR(50) NOT NULL,
  number_of_injured INT NOT NULL,
  event_date DATE NOT NULL,
  PRIMARY KEY (event_id)
);

CREATE TABLE if not exists Medical_equipment
(
  equipment_id INT NOT NULL,
  equipment_name VARCHAR(30) NOT NULL,
  quantity_ INT NOT NULL,
  PRIMARY KEY (equipment_id)
);

CREATE TABLE if not exists Treatment
(
  treatment_id INT NOT NULL,
  treatment_duration INT NOT NULL,
  date DATE NOT NULL,
  treatment_type VARCHAR(30) NOT NULL,
  paramedic_id INT NOT NULL,
  PRIMARY KEY (treatment_id),
  FOREIGN KEY (paramedic_id) REFERENCES Paramedic(paramedic_id)
);

CREATE TABLE if not exists Hospital
(
  hospital_id INT NOT NULL,
  hospital_name VARCHAR(30) NOT NULL,
  address VARCHAR(50) NOT NULL,
  PRIMARY KEY (hospital_id)
);

CREATE TABLE if not exists uses
(
  equipment_id INT NOT NULL,
  treatment_id INT NOT NULL,
  PRIMARY KEY (equipment_id, treatment_id),
  FOREIGN KEY (equipment_id) REFERENCES Medical_equipment(equipment_id),
  FOREIGN KEY (treatment_id) REFERENCES Treatment(treatment_id)
);

CREATE TABLE if not exists Patient
(
  patient_id INT NOT NULL,
  patient_name VARCHAR(30) NOT NULL,
  birthday DATE NOT NULL,
  patient_type INT NOT NULL,
  event_id INT NOT NULL,
  hospital_id INT,
  PRIMARY KEY (patient_id),
  FOREIGN KEY (event_id) REFERENCES Medical_event(event_id),
  FOREIGN KEY (hospital_id) REFERENCES Hospital(hospital_id)
);

CREATE TABLE if not exists receives_treatment
(
  patient_id INT NOT NULL,
  treatment_id INT NOT NULL,
  PRIMARY KEY (patient_id, treatment_id),
  FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
  FOREIGN KEY (treatment_id) REFERENCES Treatment(treatment_id)
);