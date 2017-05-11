import pandas as pd
import numpy as np

def grouped_trips(filepath):
    df = pd.read_csv(filepath)
    
    # merge date & time
    df['actual_datetime'] = df['actual_date'] + ' ' + df['actual_time']
    df['actual_datetime'] = pd.to_datetime(df['actual_datetime'], format='%m-%d-%y %H:%M:%S')

    # grouping
    df = df.groupby(['vehicle_id', 'actual_date', 'trip_id', 'block_id', 'route_short_name', 'headsign', 'direction_id'])
    df = df.agg({
            'actual_datetime': {
                '_min': np.min,
                '_max': np.max
            }
        })
    
    df.reset_index(inplace=True)
    df.columns = list(map(''.join, df.columns.values))
    
    return df

def merge_realtime(realtime_csv, trip_csv, output_filepath):
    # input: realtime data
    cols = ['vehicle_id', 'time', 'lat', 'lon', 'heading', 'speed', 'assignment_id', 'assignment_type',
            'source', 'time_processed', 'sched_adh_msec', 'sched_adh']
    df_realtime = pd.read_csv(realtime_csv, usecols=cols)
    df_realtime = df_realtime[ df_realtime['source'] == 'API' ]    
    df_realtime['time'] = pd.to_datetime(df_realtime['time'], format='%Y-%m-%d %H:%M:%S.%f')
    
    # input: trip data
    df_trip = grouped_trips(trip_csv)
    
    # merge valid trips
    cols = ['vehicle_id', 'time']
    merged = df_realtime[cols].merge(df_trip, how='inner', on='vehicle_id')
    merged = merged[ (merged['time'] >= merged['actual_datetime_min']) & (merged['time'] <= merged['actual_datetime_max']) ]

    # merge results
    result = df_realtime.merge(merged, how='left')
    result = result.sort_values(['vehicle_id', 'trip_id', 'time'])

    # output
    # reorder columns
    cols = ['vehicle_id', 'trip_id', 'time', 'block_id', 'route_short_name', 
            'headsign', 'direction_id', 'lat', 'lon', 'heading', 
            'speed', 'sched_adh', 'sched_adh_msec', 'time_processed', 'assignment_id', 
            'assignment_type', 'source']
    
    result.to_csv(output_filepath + '.csv', columns=cols, index=False)


    result.dropna(subset=['trip_id']).to_csv(output_filepath + '_cleaned' + '.csv', columns=cols, index=False)



def main():
    realtime_csv = 'gps_report_5_5.csv'
    trip_csv = 'schAdhCsv_5_5.csv'
    output_filepath = 'output'
    
    # grouped_trips(trip_csv)
    merge_realtime(realtime_csv, trip_csv, output_filepath)

if __name__ == "__main__":
    main()
