-- Script that ranks country origins of bands
-- ordered by number
SELECT origin as origin, SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
