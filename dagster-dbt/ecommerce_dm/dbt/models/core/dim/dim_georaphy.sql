{{ config(
      materialized = 'table',
      unique_key = 'geographykey'
) }}

SELECT
      id AS geography_key,
      cityname AS city_name,
      countryname AS country_name,
      regionname AS region_name
FROM
      {{ ref('geography') }}