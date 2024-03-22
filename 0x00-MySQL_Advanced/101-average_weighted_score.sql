-- A SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students.

DROP PROCEDURE IF EXISTS  ComputeAverageWeightedScoreForUsers;

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    -- Declare variables for calculations
    DECLARE total_score FLOAT;
    DECLARE total_weight FLOAT;
    DECLARE avg_weighted_score FLOAT;

    -- Calculate total_score and total_weight
    SELECT SUM(C.score * P.weight), SUM(P.weight)
    INTO total_score, total_weight
    FROM corrections C
    JOIN projects P ON C.project_id = P.id;

    -- Calculate average weighted score
    IF total_weight > 0 THEN
        SET avg_weighted_score = total_score / total_weight;
    ELSE
        SET avg_weighted_score = 0;
    END IF;

    -- Update the average_score for all users
    UPDATE users
    SET average_score = avg_weighted_score;
END //

DELIMITER ;
