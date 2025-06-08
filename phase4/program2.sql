-- =============================================
-- פונקציה: get_patients_in_hospital_by_treatments
-- הצגת חיילים (פצועים) בבית חולים לפי סינון מספר טיפולים
-- קולטת: מזהה בית חולים ומספר מינימלי של טיפולים
-- מחזירה: REFCURSOR עם רשימת פצועים שעומדים בקריטריונים
-- =============================================
CREATE OR REPLACE FUNCTION get_patients_in_hospital_by_treatments(
    hospital_id_param INT,         -- מזהה בית החולים אותו נרצה לבדוק
    min_treatments INT             -- מינימום מספר טיפולים שנדרש לפצוע
)
RETURNS REFCURSOR AS $$
DECLARE
    patient_cursor REFCURSOR;      -- משתנה לשמירת ה־Ref Cursor שיוחזר
    patient_rec RECORD;            -- משתנה זמני לבדיקה אם קיימות תוצאות
BEGIN
    -- פתיחת הקורסור עם אפשרות גלילה אחורה (SCROLL)
    OPEN patient_cursor SCROLL FOR
        SELECT p.soldier_id, s.soldier_name, s.experience, p.hospital_id
        FROM patient p
        JOIN soldier s ON p.soldier_id = s.soldier_id
        WHERE p.role_type = 'patient'
          AND p.hospital_id = hospital_id_param     -- סינון לפי בית חולים
          AND (
              SELECT COUNT(*)                       -- ספירת טיפולים לפי soldier_id
              FROM receives_treatment rt
              WHERE rt.soldier_id = p.soldier_id 
                AND rt.role_type = 'patient'
          ) >= min_treatments;                     -- סינון לפי מספר טיפולים

    -- בדיקה אם הקורסור מחזיר לפחות תוצאה אחת
    FETCH NEXT FROM patient_cursor INTO patient_rec;

    IF NOT FOUND THEN
        -- אם לא נמצאה תוצאה - סוגרים קורסור וזורקים חריגה
        CLOSE patient_cursor;
        RAISE EXCEPTION 'לא נמצאו פצועים בבית חולים % עם לפחות % טיפולים',
                        hospital_id_param, min_treatments;
    END IF;

    -- מחזירים את הקורסור להתחלה כדי שהקריאה תחזיר את כל הרשומות
    MOVE BACKWARD ALL IN patient_cursor;

    RETURN patient_cursor;                -- מחזירים את הקורסור למי שקרא לפונקציה
END;
$$ LANGUAGE plpgsql;


-- =============================================
-- פרוצדורה: promote_commander_if_qualified
-- קידום דרגת מפקדים לפי סך המבצעים שהם הובילו או ניסיון
-- מקבלת סף ניסיון ומבצעים, ומקדמת את המפקדים העומדים בתנאי
-- =============================================
CREATE OR REPLACE PROCEDURE promote_commander_if_qualified(
    exp_threshold INT DEFAULT 5,     -- סף ניסיון ברירת מחדל לקידום
    ops_threshold INT DEFAULT 3      -- סף מבצעים ברירת מחדל לקידום
)
LANGUAGE plpgsql
AS $$
DECLARE
    rec RECORD;           -- שורה נבחרת המייצגת מפקד
    ops_count INT;        -- מספר מבצעים שהמפקד הוביל
    new_rank TEXT;        -- הדרגה החדשה לאחר קידום
BEGIN
    -- לולאה על כל המפקדים בטבלה commander עם דרגה
    FOR rec IN
        SELECT s.soldier_id, s.soldier_name, s.experience, c.rank
        FROM soldier s
        JOIN commander c ON s.soldier_id = c.soldier_id AND c.role_type = 'commander'
        WHERE s.role_type = 'commander'
    LOOP
        -- שלב 1: חישוב מספר המבצעים שהמפקד הוביל
        SELECT COUNT(*) INTO ops_count
        FROM operation
        WHERE ID = rec.soldier_id AND role_type = 'commander';

        -- שלב 2: בדיקה האם עומד בתנאי לקידום
        IF rec.experience >= exp_threshold OR ops_count >= ops_threshold THEN
            -- שלב 3: קביעת דרגה חדשה לפי דרגה קיימת
            CASE rec.rank
                WHEN 'Private' THEN new_rank := 'Corporal';    
                WHEN 'Corporal' THEN new_rank := 'Sergeant';
                WHEN 'Sergeant' THEN new_rank := 'Lieutenant';
                WHEN 'Lieutenant' THEN new_rank := 'Captain';
                WHEN 'Captain' THEN new_rank := 'Major';
                WHEN 'Major' THEN new_rank := 'General';
                WHEN 'General' THEN new_rank := 'General'; -- אין דרגה גבוהה יותר
                ELSE new_rank := rec.rank; -- מקרה דרגה לא צפויה
            END CASE;

            -- שלב 4: עדכון הדרגה בטבלת commander
            UPDATE commander
            SET rank = new_rank
            WHERE soldier_id = rec.soldier_id;

            -- הודעה על קידום
			
            RAISE NOTICE 'Commander ID % (%): has been promoted to rank %', rec.soldier_id, rec.soldier_name, new_rank;  
        END IF;
    END LOOP;
EXCEPTION
    WHEN OTHERS THEN
        -- טיפול בשגיאות והצגת הודעה במקרה של כשל
        RAISE NOTICE 'Error in procedure: %', SQLERRM;
END;
$$;


-- =============================================
-- טריגר: trg_promote_commander_after_update
-- מטרת הטריגר: לבצע קידום דרגה למפקדים באופן אוטומטי
-- מתי הוא מופעל: לאחר כל עדכון (AFTER UPDATE) על הטבלה soldier
-- איך הוא עובד: קורא לפונקציה trg_promote_commander, שמפעילה את הפרוצדורה promote_commander_if_qualified
-- הערה חשובה: הטריגר מופעל אוטומטית ואין צורך לקרוא לו מפונקציה ראשית
-- =============================================

-- פונקציית טריגר - מבצעת את הקריאה לפרוצדורה שמקדמת מפקדים

-- מחיקת הטריגר הקודם אם קיים
DROP TRIGGER IF EXISTS trg_promote_commander_after_update ON soldier;

CREATE OR REPLACE FUNCTION trg_promote_commander()
RETURNS TRIGGER AS
$$
BEGIN

    -- קריאה לפרוצדורה שמבצעת קידום דרגה לפי ניסיון או מספר מבצעים
    CALL promote_commander_if_qualified();

    -- טריגר AFTER לא משפיע על השורה שעודכנה ולכן מחזיר NULL
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- יצירת הטריגר עצמו שמופעל אחרי כל UPDATE בטבלת soldier
CREATE TRIGGER trg_promote_commander_after_update
AFTER UPDATE ON soldier
FOR EACH STATEMENT        -- מופעל פעם אחת לכל משפט UPDATE (לא לכל שורה)
EXECUTE FUNCTION trg_promote_commander();



-- =============================================
-- תוכנית ראשית (DO block)
-- דוגמה להרצת הפונקציה להצגת פצועים בבית חולים עם סינון לפי טיפולים
-- וגם קריאה לפורצדורה לקידום מפקדים
-- =============================================
DO $$
DECLARE
    cur REFCURSOR;       -- משתנה שיאחסן את הקורסור מהפונקציה
    rec RECORD;          -- משתנה לאחסון שורות בעת איטרציה על הקורסור
BEGIN
    -- קריאה לפונקציה לקבלת פצועים בבית חולים 2 עם לפחות 2 טיפולים
    cur := get_patients_in_hospital_by_treatments(2, 2);

    -- לולאה לקריאת התוצאות מהקורסור והצגתן
    LOOP
        FETCH cur INTO rec;
        EXIT WHEN NOT FOUND;

        -- הצגת פרטי הפצועים עם RAISE NOTICE
        RAISE NOTICE 'ID: %, Name: %, Exp: %, Hospital: %',
            rec.soldier_id, rec.soldier_name, rec.experience, rec.hospital_id;
    END LOOP;

    -- סגירת הקורסור לאחר קריאת כל התוצאות
    CLOSE cur;
     
    -- קריאה לפורצדורה לקידום מפקדים עם פרמטרים ברירת מחדל
    CALL promote_commander_if_qualified();

END;
$$;
