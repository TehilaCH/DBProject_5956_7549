-- =============================
-- פונקציה: עדכון ניסיון לפרמדיקים לפי כמות טיפולים
-- מחזירה Ref Cursor עם רשימת הפרמדיקים לאחר העדכון
-- =============================

CREATE OR REPLACE FUNCTION update_paramedic_experience()
RETURNS REFCURSOR AS $$

DECLARE
    -- יצירת Cursor שמחזיר את כל מזהי הפרמדיקים מטבלת paramedic
    paramedic_cursor CURSOR FOR
        SELECT soldier_id FROM paramedic;

    -- משתנה לשמירת מזהה הפרמדיק הנוכחי בלולאה
    v_paramedic_id INT;

    -- משתנה לשמירת מספר הטיפולים של הפרמדיק הנוכחי
    v_treat_count INT;

    -- משתנה לשמירת Ref Cursor שיוחזר בסוף הפונקציה
    v_refcursor REFCURSOR;

BEGIN
    -- פותחים את ה-Cursor כדי להתחיל קריאה על הפרמדיקים
    OPEN paramedic_cursor;

    -- לולאה אינסופית שתקרא כל פרמדיק אחד אחרי השני
    LOOP
        -- שולפים מזהה פרמדיק מה-Cursor לתוך המשתנה v_paramedic_id
        FETCH paramedic_cursor INTO v_paramedic_id;

        -- אם לא נמצא עוד פרמדיק, יוצאים מהלולאה
        EXIT WHEN NOT FOUND;

        -- סופרים את מספר הטיפולים שבוצעו על ידי הפרמדיק הנוכחי
        SELECT COUNT(*) INTO v_treat_count
        FROM treatment
        WHERE paramedic_id = v_paramedic_id;

        -- אם מספר הטיפולים גבוה מ-20, מעדכנים ניסיון ב-5 נקודות
        IF v_treat_count > 20 THEN
            UPDATE soldier
            SET experience = experience + 5
            WHERE soldier_id = v_paramedic_id AND role_type = 'paramedic';

        -- אם מספר הטיפולים בין 10 ל-20, מעדכנים ניסיון ב-2 נקודות
        ELSIF v_treat_count BETWEEN 10 AND 20 THEN
            UPDATE soldier
            SET experience = experience + 2
            WHERE soldier_id = v_paramedic_id AND role_type = 'paramedic';

        -- אחרת, מעדכנים ניסיון בנקודה אחת בלבד
        ELSE
            UPDATE soldier
            SET experience = experience + 1
            WHERE soldier_id = v_paramedic_id AND role_type = 'paramedic';
        END IF;
    END LOOP;

    -- סוגרים את ה-Cursor לאחר סיום העיבוד
    CLOSE paramedic_cursor;

    -- פותחים Ref Cursor חדש עם רשימת הפרמדיקים והניסיון המעודכן
    OPEN v_refcursor FOR
        SELECT soldier_id, soldier_name, experience
        FROM soldier
        WHERE role_type = 'paramedic';

    -- מחזירים את ה-Ref Cursor לקריאה חיצונית (לדוגמה תוכנית ראשית)
    RETURN v_refcursor;

EXCEPTION
    -- במקרה של כל שגיאה במהלך הפונקציה, מציגים הודעת שגיאה
    WHEN OTHERS THEN
        RAISE NOTICE 'Error in update_paramedic_experience: %', SQLERRM;
        RETURN NULL; -- מחזירים NULL במקרה של שגיאה
END;
$$ LANGUAGE plpgsql;


-- =============================
-- פרוצדורה: עדכון ניסיון לפרמדיקים שטיפלו באירועים עם יותר מ-10 פצועים
-- =============================

CREATE OR REPLACE PROCEDURE update_experience_by_event()
LANGUAGE plpgsql
AS $$
BEGIN
    -- מבצעים UPDATE על טבלת soldier, מעדכנים ניסיון +3 לכל פרמדיק שטיפל באירוע עם >10 פצועים
    UPDATE soldier
    SET experience = experience + 3
    WHERE soldier_id IN (
        -- בוחרים את כל הפרמדיקים שטיפלו באירועים עם מספר פצועים מעל 10
        SELECT DISTINCT t.paramedic_id
        FROM treatment t
        JOIN patient p ON t.treatment_id = p.treatment_id
        JOIN medical_event me ON p.event_id = me.event_id
        WHERE me.number_of_injured > 10
    ) AND role_type = 'paramedic';

EXCEPTION
    -- במידה ויש שגיאה, מציגים הודעה מתאימה
    WHEN OTHERS THEN
        RAISE NOTICE 'Error in update_experience_by_event: %', SQLERRM;
END;
$$;


-- =============================
-- מחיקת טריגר קודם אם קיים
-- =============================

DROP TRIGGER IF EXISTS trg_after_insert_treatment ON treatment;


-- =============================
-- פונקציית טריגר: עדכון ניסיון לפרמדיק בטיפול חירום ארוך
-- =============================

CREATE OR REPLACE FUNCTION trg_update_paramedic_experience()
RETURNS TRIGGER AS $$
BEGIN
    -- נבדוק האם סוג הטיפול הוא 'EMERGENCY' וזמן הטיפול מעל 20
    IF NEW.treatment_type = 'EMERGENCY' AND NEW.treatment_duration > 20 THEN
        UPDATE soldier
        SET experience = experience + 1
        WHERE soldier_id = NEW.paramedic_id
          AND role_type = 'paramedic';
    END IF;

    RETURN NEW; -- חשוב להחזיר את השורה כדי שההכנסה תושלם
END;
$$ LANGUAGE plpgsql;


-- =============================
-- יצירת הטריגר החדש על טבלת treatment לאחר הכנסת שורה
-- =============================

CREATE TRIGGER trg_after_insert_treatment
AFTER INSERT ON treatment
FOR EACH ROW
EXECUTE FUNCTION trg_update_paramedic_experience();

-- =============================
-- תוכנית ראשית: קריאה לפונקציה ולעדכון ניסיון, הצגת פרמדיקים, וקריאה לפרוצדורה נוספת
-- =============================

DO $$
DECLARE
    cur REFCURSOR; -- משתנה לשמירת ה-Ref Cursor שהפונקציה תחזיר
    rec RECORD;    -- משתנה לשמירת שורה בזמן הלולאה להצגת הנתונים
BEGIN
    -- קריאה לפונקציה לעדכון ניסיון שמחזירה Ref Cursor
    cur := update_paramedic_experience();

    -- לולאה לקריאת כל רשומה מתוך ה-Ref Cursor
    LOOP
        FETCH cur INTO rec;      -- שולפים רשומה מה-Cursor לתוך המשתנה rec
        EXIT WHEN NOT FOUND;    -- אם לא נשארו עוד רשומות, יוצאים מהלולאה

        -- מציגים הודעה עם פרטי הפרמדיק: מזהה, שם וניסיון מעודכן
        RAISE NOTICE 'Paramedic ID: %, Name: %, Experience: %',
            rec.soldier_id, rec.soldier_name, rec.experience;
    END LOOP;

    -- סוגרים את ה-Cursor לאחר סיום הקריאה
    CLOSE cur;

    -- קריאה לפרוצדורה לעדכון ניסיון נוסף על פי אירועים עם יותר מ-10 פצועים
    CALL update_experience_by_event();

END
$$;
