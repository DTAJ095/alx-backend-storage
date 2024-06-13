-- Script that creates a stored procedure ComputeAverageScoreForUser
-- that computes the average score of a student
DELIMITER $$
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE avg_score INT;
    SET avg_Score = (SELECT AVG(score) FROM corrections AS C WHERE C.user_id = user_id);
    UPDATE users SET average_score = avg_score WHERE id=user_id;
END
$$
DELIMITER;
