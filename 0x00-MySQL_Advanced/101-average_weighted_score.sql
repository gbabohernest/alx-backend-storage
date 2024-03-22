-- A SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students.

DROP PROCEDURE IF EXISTS  ComputeAverageWeightedScoreForUsers;

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id_val INT;
    DECLARE done INT DEFAULT FALSE;
    DECLARE cur_users CURSOR FOR
        SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur_users;

    read_loop: LOOP
        FETCH cur_users INTO user_id_val;
        IF done THEN
            LEAVE read_loop;
        END IF;

        DECLARE total_score FLOAT;
        DECLARE total_weight INT;
        DECLARE average_score FLOAT;

        -- Calculate total_score and total_weight for each user
        SELECT SUM(c.score * p.weight), SUM(p.weight)
        INTO total_score, total_weight
        FROM corrections c
        INNER JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id_val;

        -- Calculate average_score
        IF total_weight > 0 THEN
            SET average_score = total_score / total_weight;
        ELSE
            SET average_score = 0;
        END IF;

        -- Update average_score in the users table for each user
        UPDATE users
        SET average_score = average_score
        WHERE id = user_id_val;
    END LOOP;

    CLOSE cur_users;
END //

DELIMITER ;
