-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH teacher_assignment_counts AS (
    SELECT teacher_id, COUNT(*) AS total_assignments_graded
    FROM assignments
    WHERE state = 'GRADED'
    GROUP BY teacher_id
),

top_grading_teacher AS (
    SELECT teacher_id
    FROM teacher_assignment_counts
    ORDER BY total_assignments_graded DESC
    LIMIT 1
)

SELECT COUNT(*) AS total_grade_A_assignments
FROM assignments
WHERE teacher_id = (SELECT teacher_id FROM top_grading_teacher)
  AND state = 'GRADED'
  AND grade = 'A';
