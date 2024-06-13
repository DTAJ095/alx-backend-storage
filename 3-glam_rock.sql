-- Script that list all bands with Glam rock
-- as their main style, ranked by longevity
SELECT band_name, IFNULL(split, 2020) - IFNULL(fromed, 0) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%';
