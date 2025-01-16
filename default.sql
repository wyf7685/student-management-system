INSERT INTO college (college_id, name)
SELECT 1, '信息学院'
WHERE NOT EXISTS (
    SELECT 1 FROM college WHERE college_id = 1
);

