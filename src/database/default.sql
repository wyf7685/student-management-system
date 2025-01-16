INSERT INTO college (college_id, name)
SELECT 1, '信息学院'
WHERE NOT EXISTS (
    SELECT 1 FROM college WHERE college_id = 1
);

INSERT INTO major (major_id, name, college_id)
SELECT 11, '计算机科学与技术', 1
WHERE NOT EXISTS (
    SELECT 1 FROM major WHERE major_id = 11
);

INSERT INTO class (class_id, name, major_id, year)
SELECT 111, '计算机科学与技术2301', 11, 2023
WHERE NOT EXISTS (
    SELECT 1 FROM class WHERE class_id = 111
);

INSERT INTO student (
    student_id, name, gender, birth, phone, email,
    college_id, major_id, class_id, enrollment_date
)
SELECT 
    1111, '张三', 'M', '2005-01-01 00:00:00', '13800138000', 'zhangsan@example.com',
    1, 11, 111, '2023-09-01'
WHERE NOT EXISTS (
    SELECT 1 FROM student WHERE student_id = 1111
);

INSERT INTO teacher (
    teacher_id, name, gender, birth, phone, email
)
SELECT 
    1001, '李四', 'M', '1980-01-01 00:00:00', '13900139000', 'lisi@example.com'
WHERE NOT EXISTS (
    SELECT 1 FROM teacher WHERE teacher_id = 1001
);

INSERT INTO system_account (
    role, password, salt, student_id, teacher_id, admin_id
)
SELECT 
    'Student', 
    '697d423a3558f0ab2e71cea50014029628ee62cd154e1e81d5cd960932cce9b6',
    'default',
    1111,
    NULL,
    NULL
WHERE NOT EXISTS (
    SELECT 1 FROM system_account 
    WHERE role = 'Student' AND student_id = 1111
);

INSERT INTO system_account (
    role, password, salt, student_id, teacher_id, admin_id
)
SELECT 
    'Teacher', 
    '697d423a3558f0ab2e71cea50014029628ee62cd154e1e81d5cd960932cce9b6',
    'default',
    NULL,
    1001,
    NULL
WHERE NOT EXISTS (
    SELECT 1 FROM system_account 
    WHERE role = 'Teacher' AND teacher_id = 1001
);

INSERT INTO system_account (
    role, password, salt, student_id, teacher_id, admin_id
)
SELECT 
    'Admin', 
    '697d423a3558f0ab2e71cea50014029628ee62cd154e1e81d5cd960932cce9b6',
    'default',
    NULL,
    NULL,
    'admin'
WHERE NOT EXISTS (
    SELECT 1 FROM system_account 
    WHERE role = 'Admin' AND admin_id = 'admin'
);
-- 插入奖项信息
INSERT INTO award (award_id, student_id, award_name, award_date)
SELECT 1, 1111, '全国大学生程序设计竞赛一等奖', '2023-10-01'
WHERE NOT EXISTS (
    SELECT 1 FROM award WHERE award_id = 1
);

INSERT INTO award (award_id, student_id, award_name, award_date)
SELECT 2, 1111, '优秀毕业生', '2023-06-30'
WHERE NOT EXISTS (
    SELECT 1 FROM award WHERE award_id = 2
);

INSERT INTO award (award_id, student_id, award_name, award_date)
SELECT 3, 1111, '学术论文发表奖', '2023-05-15'
WHERE NOT EXISTS (
    SELECT 1 FROM award WHERE award_id = 3
);
-- 插入课程信息
INSERT INTO course (course_id, name, credits)
SELECT 101, '计算机组成原理', 3
WHERE NOT EXISTS (
    SELECT 1 FROM course WHERE course_id = 101
);

INSERT INTO course (course_id, name, credits)
SELECT 102, '数据结构', 3
WHERE NOT EXISTS (
    SELECT 1 FROM course WHERE course_id = 102
);

INSERT INTO course (course_id, name, credits)
SELECT 103, '操作系统', 3
WHERE NOT EXISTS (
    SELECT 1 FROM course WHERE course_id = 103
);

INSERT INTO course (course_id, name, credits)
SELECT 104, '数据库系统', 3
WHERE NOT EXISTS (
    SELECT 1 FROM course WHERE course_id = 104
);

INSERT INTO course (course_id, name, credits)
SELECT 105, '计算机网络', 3
WHERE NOT EXISTS (
    SELECT 1 FROM course WHERE course_id = 105
);
-- 插入考试信息
INSERT INTO exam (course_id, time, duration, name, description, location)
SELECT 101, '2023-11-01 09:00:00', 120, '计算机组成原理', '期末考试', '教学楼A101'
WHERE NOT EXISTS (
    SELECT 1 FROM exam WHERE course_id = 101 AND time = '2023-11-01 09:00:00'
);

INSERT INTO exam (course_id, time, duration, name, description, location)
SELECT 102, '2023-11-02 10:00:00', 150, '数据结构', '期末考试', '教学楼B202'
WHERE NOT EXISTS (
    SELECT 1 FROM exam WHERE course_id = 102 AND time = '2023-11-02 10:00:00'
);

INSERT INTO exam (course_id, time, duration, name, description, location)
SELECT 103, '2023-11-03 11:00:00', 120, '操作系统', '期末考试', '教学楼C303'
WHERE NOT EXISTS (
    SELECT 1 FROM exam WHERE course_id = 103 AND time = '2023-11-03 11:00:00'
);

INSERT INTO exam (course_id, time, duration, name, description, location)
SELECT 104, '2023-11-04 12:00:00', 150, '数据库系统', '期末考试', '教学楼D404'
WHERE NOT EXISTS (
    SELECT 1 FROM exam WHERE course_id = 104 AND time = '2023-11-04 12:00:00'
);

INSERT INTO exam (course_id, time, duration, name, description, location)
SELECT 105, '2023-11-05 13:00:00', 120, '计算机网络', '期末考试', '教学楼E505'
WHERE NOT EXISTS (
    SELECT 1 FROM exam WHERE course_id = 105 AND time = '2023-11-05 13:00:00'
);