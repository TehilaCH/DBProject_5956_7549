# Medical Corps
## Phase 1: Design and Build the Database

### **Introduction**  
The **Medical Corps Database** is designed to efficiently manage information related to paramedics, patients, treatments, medical equipment, hospitals, and medical events.  
This system ensures **structured organization** and tracking of essential details such as patient care, medical procedures, evacuation logistics, and resource management.  

---

### **Purpose of the Database**  
This database serves as a **structured and reliable solution** for the Medical Corps to:  

- **Manage paramedic assignments** by recording their experience and linking them to performed treatments.  
- **Store patient records**, including personal details, medical conditions, and treatment history.  
- **Document medical treatments**, tracking procedure types, durations, and associated personnel.  
- **Monitor medical equipment usage**, ensuring the availability of essential supplies.  
- **Track hospital evacuations**, recording patient transfers and methods of transport.  
- **Log medical events**, documenting incidents, casualty counts, and locations.  

---

### **Potential Use Cases**  
- **Medical Corps Administrators** can oversee paramedic assignments, track patient treatments, and manage medical resources.  
- **Paramedics** can document treatments performed and access relevant medical equipment records.  
- **Hospital Staff** can monitor incoming evacuations, ensuring proper patient admission and care.  
- **Commanders and Emergency Coordinators** can analyze event data to **improve medical response and evacuation efficiency**.  

---

This **structured database** helps streamline **military medical operations**, improving **organization, efficiency, and responsiveness** in both **routine and emergency scenarios**. 

##**ERD (Entity-Relationship Diagram)**

![image](https://github.com/user-attachments/assets/da5a72ef-cd2a-4089-9fd3-fe25ce63078e)



##**DSD (Data Structure Diagram)**


![image](https://github.com/user-attachments/assets/359cba96-4835-4f30-896a-a2dfd793bc3c)

###  SQL Scripts  
Provide the following SQL scripts:  

- **Create Tables Script** - The SQL script for creating tables in the database is available in the repository:  
📜 **[Medical_Corps_createTables.sql](phase1/createTables.sql)**

- **Insert Data Script** - The SQL script for inserting data into the database tables is available in the repository:  
📜 **[Medical_Corps_insertTables.sql](phase1/insertTables.sql)**

- **Drop Tables Script** - The SQL script for dropping all tables is available in the repository:  
📜 **[Medical_Corps_dropTables.sql](phase1/dropTables.sql)**

- **Select All Data Script** - The SQL script for selecting all data from the tables is available in the repository:
📜 **[Medical_Corps_selectAllTables.sql](phase1/selectAllTables.sql)**



- **Create Tables Script** - The SQL script for creating tables in the database is available in the repository:  
📜 **[Medical_Corps_createTables.sql](phase1/createTables.sql)**

- **Insert Data Script** - The SQL script for inserting data into the database tables is available in the repository:  
📜 **[Medical_Corps_insertTables.sql](phase1/insertTables.sql)**

- **Drop Tables Script** - The SQL script for dropping all tables is available in the repository:  
📜 **[Medical_Corps_dropTables.sql](phase1/dropTables.sql)**

- **Select All Data Script** - The SQL script for selecting all data from the tables is available in the repository:  
📜 **[Medical_Corps_selectAllTables.sql](phase1/selectAllTables.sql)**



 ###  Data  
 ####  First tool: using [mockaro](https://www.mockaroo.com/) to create csv file
 #####  Entering a data to paramedic table

 ![image](https://github.com/user-attachments/assets/1cea1c80-8e39-45df-86e8-96b7897a5833)

 

📜 **[ParamedicData.csv](https://github.com/TehilaCH/Databases/blob/main/phase1/mockaroo/ParamedicData.csv)**


 
 ![image](https://github.com/user-attachments/assets/f38cc4dd-e10a-4acf-8a9c-21d0cf4be148)

 ![image](https://github.com/user-attachments/assets/12000609-88d4-444c-87f4-8821e94e7b69)

![image](https://github.com/user-attachments/assets/a0c8323c-c322-4e51-9205-e364c3239460)



####  Second tool: using [generatedata](https://generatedata.com/generator). to create csv file 
#####  Entering a data to Medical_equipment table
 ![image](https://github.com/user-attachments/assets/67218d4a-d127-474a-8181-3e36840aa8c2)

 ![image](https://github.com/user-attachments/assets/e2dd38e7-591a-45bc-87b9-b66314f9eaff)
 ![image](https://github.com/user-attachments/assets/3f7ec108-b2ca-461a-af45-ed63cada98d6)


 📜 **[EquipmentData.csv](https://github.com/TehilaCH/Databases/blob/main/phase1/generatedata/EquipmentData.csv)**
 

 ####  Third tool: using python to create csv file


### Backup 
-   backups files are kept with the date and hour of the backup:  

