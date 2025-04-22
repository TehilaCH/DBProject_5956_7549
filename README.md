# Medical Corps

### Database Design and Development by:
- Hodaya Ben Shabat
- Tehila Chananayev

### Organization:
- Israel Defense Forces (IDF), Medical Corps – Health Division

## 📑 Table of Contents

- [Medical Corps](#medical-corps)
- [Submitted by](#submitted-by)
- [Organization](#organization)
- [Phase 1: Design and Build the Database](#phase-1-design-and-build-the-database)
- [Introduction](#introduction)
- [Purpose of the Database](#purpose-of-the-database)
- [Potential Use Cases](#potential-use-cases)
- [ERD (Entity-Relationship Diagram)](#erd-entity-relationship-diagram)
- [DSD (Data-Structure Diagram)](#dsd-data-structure-diagram)
- [SQL Scripts](#sql-scripts)
- [Data](#data)
  - [First Tool: Mockaroo](#first-tool-using-mockaro-to-create-csv-file)
  - [Second Tool: Generatedata](#second-tool-using-generatedata-to-create-csv-file)
  - [Third Tool: Python](#third-tool-using-python-to-create-csv-file)
- [Backup and Restore](#backup)

  
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

## **ERD (Entity-Relationship Diagram)**

![image](https://github.com/user-attachments/assets/da5a72ef-cd2a-4089-9fd3-fe25ce63078e)



## **DSD (Data Structure Diagram)**


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
 

 ####  Third tool: using python to create sql file


### Backup 
-   backups files are kept with the date and hour of the backup:
  
- **Backup Screenshot:**  
  ![image](https://github.com/user-attachments/assets/14eff330-cc7d-4833-9e47-c557c95efe34)

   ![image](https://github.com/user-attachments/assets/74c6f76a-583a-4459-8551-6b97ab412a53)
  
- **Restore Screenshot:**  


# דוח פרויקט - שלב ב'

## 1.הצגת כל האירועים שהתרחשו בשנת 2024

**תיאור:**  
שאילתה זו מציגה את כל האירועים הרפואיים שהתרחשו במהלך שנת 2024, באמצעות סינון לפי תאריך.

**שאילתא:**
![image](https://github.com/user-attachments/assets/8cd3eb33-b8bd-4450-b8b7-60d08b59dd2a)

## 2. כמות השימושים בציוד רפואי לפי חודש בשנת 2023

**תיאור:**  
שאילתה זו מציגה את כמות השימושים בציוד רפואי בכל חודש במהלך שנת 2023, על מנת להבין את דפוסי השימוש לאורך השנה.

**שאילתא:**

![image](https://github.com/user-attachments/assets/6bde7d13-e655-4f3a-9259-f7e7b8043e21)

## 3. מספר הטיפולים שביצע כל פרמדיק לפי חודש ושנה

**תיאור:**  
הטבלה מציגה את מספר הטיפולים שכל פרמדיק ביצע, מקובץ לפי חודש ושנה.

**שאילתא:**


![image](https://github.com/user-attachments/assets/9ec45cb0-ec07-4b21-954b-7010abd2f264)


## 4. חולים שקיבלו יותר משני טיפולים

**תיאור:**  
שאילתה זו מציגה חולים אשר קיבלו יותר מ-2 טיפולים שונים, לצורך איתור מקרים רפואיים מורכבים יותר.

**שאילתא:**

![image](https://github.com/user-attachments/assets/5a43dd09-1409-493b-8190-5d0d1584eef8)
  השאילתה מציגה חובשים שביצעו טיפולים באירועים עם יותר מ-10 פצועים 


  ## 5. פרמדיקים שביצעו טיפולים באירועים עם יותר מ-10 פצועים

**תיאור:**  
מטרת שאילתה זו היא לאתר פרמדיקים שפעלו באירועים רבי-נפגעים (מעל 10 פצועים).

**שאילתא:**

![image](https://github.com/user-attachments/assets/3c044109-284b-45b7-a849-2c8444073280)

  ## 6. ציוד רפואי שנעשה בו שימוש ביותר מ-5 טיפולים שונים

**תיאור:**  הטבלה מציגה ציוד רפואי אשר שימש ביותר מ-5 טיפולים שונים, כדי לאתר ציוד בשימוש תדיר.

**שאילתא:**
 ![image](https://github.com/user-attachments/assets/a96c6021-fc14-4c41-8c9b-5e524c177f12)
שאילתה שמציגה חולים שטופלו בטיפולים שבוצעו על ידי חובשים עם ניסיון מעל 10

  ## 7. חולים שטופלו בטיפולים שבוצעו על ידי פרמדיקים עם ניסיון מעל 10 שנים

**תיאור:**  הטבלה מציגה את החולים שטופלו על ידי פרמדיקים מנוסים (ניסיון מעל 10 שנים), כדי לבחון את הקשר בין ניסיון לטיפול.

**שאילתא:**

![image](https://github.com/user-attachments/assets/2fc1de94-2e71-4e10-b7cc-4c6c4f48f7a8)
 ## 8. ממוצע מספר החולים בכל שנה

**תיאור:**  שאילתה זו מחשבת את ממוצע מספר החולים שהשתתפו באירועים רפואיים בכל שנה, לצורך מעקב מגמות רב-שנתיות.

**שאילתא:**

![image](https://github.com/user-attachments/assets/181f248d-4749-4225-a6eb-a19083199c9d)

**שלושה שאילתות לעדכון:**
 ## 1. עדכון ניסיון פרמדיקים שפעלו באירועים רבי-נפגעים
 **תיאור:** שאילתה זו מעדכנת את הניסיון של פרמדיקים שפעלו באירועים שבהם היו יותר מ-10 פצועים. מטרת השאילתה היא להוסיף שנה אחת לניסיון של כל פרמדיק שהשתתף בטיפול באירועים משמעותיים כאלה, מתוך הנחה כי השתתפות באירועים מורכבים תורמת לניסיון המקצועי.
 **שאילתא:**
 
  **נתונים לפני עדכון:**
 
![image](https://github.com/user-attachments/assets/6529fcac-6fba-4c2f-920b-3a404a44c825)
 
  **הרצה שאילתת עדכון:**
  
![image](https://github.com/user-attachments/assets/a655e247-f1c9-41c1-bc8b-a6855aed05c9)
 **נתונים אחרי עדכון:**
 
 
![image](https://github.com/user-attachments/assets/dd61e92d-d82f-4548-ac17-702ba19b7f06)

 ## 2.עדכון כמות הציוד הרפואי עבור ציוד שנעשה בו שימוש ביותר מ-2 טיפולים
 **תיאור:**נעדכן את כמות הציוד הרפואי שנעשה בו שימוש ביותר מ-2 טיפולים, על מנת להבטיח שהציוד יישאר זמין ונגיש במקרים חוזרים.
 
**נתונים לפני עדכון:**

 
![image](https://github.com/user-attachments/assets/a83a428f-75cd-4626-9302-7575b82020f6)
**הרצה שאילתת עדכון:**



![image](https://github.com/user-attachments/assets/61837f05-611c-4d26-8232-a5eee54d4d44)

 **נתונים אחרי עדכון:**
 
 
![image](https://github.com/user-attachments/assets/441f4c35-da79-4733-a078-61f12b9df9c7)


 ## 3.עדכון סוג פצוע עבור חולה שעבר יותר מ-3 טיפולים
 **תיאור:**נעדכן את סוג הפצוע מ-1 (קל) ל-2 (בינוני), עבור חולה שעבר יותר מ-3 טיפולים שונים.
  **נתונים לפני עדכון:**
  
  
  ![image](https://github.com/user-attachments/assets/e15617fc-db0a-48b6-b736-5404accd622b)

 **הרצה שאילתת עדכון:**
 
 
 ![image](https://github.com/user-attachments/assets/6a516537-3429-46d3-8095-aca04001dba8)

  **נתונים אחרי עדכון:**
  
  
  ![image](https://github.com/user-attachments/assets/d0f4f767-6f78-4ec3-a33b-de30de4b887a)

**שלושה שאילתות למחיקה:**
 ## 1.מחיקת ציוד רפואי שלא נעשה בו שימוש באף טיפול
 **תיאור:**השאילתה מוחקת פריטי ציוד רפואי שלא נעשה בהם שימוש באף טיפול, כלומר כאלה שלא מופיעים בטבלת השימוש בציוד.
 **שאילתא:**
  **נתונים לפני מחיקה:**
  

 ![image](https://github.com/user-attachments/assets/961fa830-a792-4a70-8b63-54a20a468689)
 **הרצה שאילתת מחיקה:**


 
 ![image](https://github.com/user-attachments/assets/d443d234-3e1f-4a04-9a13-190cfb293c9a)

 **נתונים אחרי מחיקה:**
 
 
![image](https://github.com/user-attachments/assets/0d1b8ae4-7872-4ad0-82fe-7ec2b33231e2)

 ## 2.מוחקת מטופלים שמעולם לא עברו טיפול
 **תיאור:**השאילתה מוחקת את כל הפצועים שלא מופיעים בטבלת הטיפולים, כלומר כאלה שלא עברו אף טיפול.
**שאילתא:**
 
 **נתונים לפני מחיקה:**
  
  

![image](https://github.com/user-attachments/assets/6940a5b7-b7e0-4bfa-88ed-c5900e018062)
 
 **הרצה שאילתת מחיקה:**
 
  


![image](https://github.com/user-attachments/assets/f987af76-80fa-408e-8ee2-c4f87da5a9c7)
 **נתונים אחרי מחיקה:**
 
   

![image](https://github.com/user-attachments/assets/31338719-d608-4868-8096-f3b28c204ad0)


 ## 3.מחיקת בתי חולים שלא נקלטו אליהם פצועים
 **תיאור:** השאילתה מסירה מהמערכת בתי חולים שלא נקלט אליהם אף פצוע בטבלת הפצועים.
**שאילתא:**
 
**נתונים לפני מחיקה:**

    
 ![image](https://github.com/user-attachments/assets/eb1db62d-c09b-481b-b70e-e745e7b59a7f)

**הרצה שאילתת מחיקה:**
 

![image](https://github.com/user-attachments/assets/318c8892-dbd9-48e0-bf77-8a6f799109e2)

 **נתונים אחרי מחיקה:**
 
 
 ![image](https://github.com/user-attachments/assets/826fcb2b-35ec-48fd-a901-62240298432f)

 
