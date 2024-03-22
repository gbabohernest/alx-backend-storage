-- A SQL script that creates a stored procedure
-- AddBonus that adds a new correction for a student.

DELIMITER //

CREATE PROCEDURE AddBonus(
    IN user_id INT,
    IN project_name VARCHAR(255),
    IN score FLOAT
)
BEGIN
    DECLARE project_id INT;

    -- Check if project_name already exists in projects table
    SELECT id
    INTO project_id
    FROM projects
    WHERE name = project_name;

    -- If project_name doesn't exist, create a new project
    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;

    -- Add the correction with bonus score for the student
    INSERT INTO corrections (user_id, project_id, score)
    VALUES (user_id, project_id, score);
END //

DELIMITER ;
