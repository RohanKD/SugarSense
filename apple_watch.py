import pandas as pd
import json

def process_health_data(steps_file, heartrate_file, date_filter):
    steps_df = pd.read_csv(steps_file)
    heartrate_df = pd.read_csv(heartrate_file)

    steps_df['timestamp'] = pd.to_datetime(steps_df['timestamp'])
    heartrate_df['timestamp'] = pd.to_datetime(heartrate_df['timestamp'])

    date = pd.to_datetime(date_filter).date()
    steps_day = steps_df[steps_df['timestamp'].dt.date == date]
    heartrate_day = heartrate_df[heartrate_df['timestamp'].dt.date == date]

    steps_day['hour'] = steps_day['timestamp'].dt.hour
    hourly_steps = steps_day.groupby('hour')['value'].sum().reset_index()

    heartrate_day['hour'] = heartrate_day['timestamp'].dt.hour
    hourly_heartrate = heartrate_day.groupby('hour')['value'].mean().reset_index()

    hourly_data = pd.merge(hourly_steps, hourly_heartrate, on='hour', how='outer')
    hourly_data.columns = ['hour', 'steps', 'heartrate']
    hourly_data['steps'] = hourly_data['steps'].fillna(0).astype(int)
    hourly_data['heartrate'] = hourly_data['heartrate'].fillna(0).round(2)

    data_json = hourly_data.to_dict(orient='records')
    json_output = json.dumps(data_json, indent=4)
    print(json_output)
    return json_output


