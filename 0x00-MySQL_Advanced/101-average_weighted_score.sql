-- A SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students.

DROP PROCEDURE IF EXISTS  ComputeAverageWeightedScoreForUsers;

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users AS usr,
        (SELECT usr.id, SUM(score * weight) / SUM(weight) AS weight_avg
        FROM users AS usr
        JOIN corrections as C ON usr.id=C.user_id
        JOIN projects AS P ON C.project_id=P.id
        GROUP BY usr.id)
    AS weight_AV
    SET usr.average_score = weight_AV.weight_avg
    WHERE usr.id=weight_AV.id;
END //

DELIMITER ;
