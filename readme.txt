[Input]

1. Realtime Data (gps_5_2_to_5_4.csv)
2. Trip Data (schAdhCsv_5_2_to_5_4.csv)


[Description]

Add trip information to realtime gps data.

In realtime data (gps_5_2_to_5_4.csv), only keeps records which source is "API". In the filtered data, find the trip information according to vehicle_id and time from trip data (schAdhCsv_5_2_to_5_4.csv). Output realtime data combined with trip data.

* Combine condition:
  - "vehicle_id" from both table matches
  - "time" from realtime data is within a trip from trip data

* Trip
  - A trip is when a vehicle visiting a sequence of stops
  - Duration of trip is found by the minimum and maximum actual datetime of a same trip_id and same vehicle_id


[Output]

Combined table with data from following table and columns

1. Realtime Data
* all columns needed

2. Trip Data
* needed columns:
- trip_id
- block_id
- route_short_name
- direction_id
- headsign