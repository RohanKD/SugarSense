import pandas as pd
import json
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

def process_health_data(steps_file, heartrate_file, food_file, insulin_file, date_filter, anthropic_api_key):
    steps_df = pd.read_csv(steps_file)
    heartrate_df = pd.read_csv(heartrate_file)
    food_df = pd.read_csv(food_file)
    insulin_df = pd.read_csv(insulin_file)

    steps_df['timestamp'] = pd.to_datetime(steps_df['timestamp'])
    heartrate_df['timestamp'] = pd.to_datetime(heartrate_df['timestamp'])
    food_df['timestamp'] = pd.to_datetime(food_df['timestamp'])
    insulin_df['timestamp'] = pd.to_datetime(insulin_df['timestamp'])

    date = pd.to_datetime(date_filter).date()
    steps_day = steps_df[steps_df['timestamp'].dt.date == date]
    heartrate_day = heartrate_df[heartrate_df['timestamp'].dt.date == date]
    food_day = food_df[food_df['timestamp'].dt.date == date]
    insulin_day = insulin_df[insulin_df['timestamp'].dt.date == date]

    steps_day['hour'] = steps_day['timestamp'].dt.hour
    hourly_steps = steps_day.groupby('hour')['value'].sum().reset_index()

    heartrate_day['hour'] = heartrate_day['timestamp'].dt.hour
    hourly_heartrate = heartrate_day.groupby('hour')['value'].mean().reset_index()

    food_day['hour'] = food_day['timestamp'].dt.hour
    hourly_food = food_day.groupby('hour').agg({
        'calories': 'sum',
        'carbohydrates': 'sum'
    }).reset_index()

    insulin_day['hour'] = insulin_day['timestamp'].dt.hour
    hourly_insulin = insulin_day.groupby('hour')['amount'].sum().reset_index()

    hourly_data = pd.merge(hourly_steps, hourly_heartrate, on='hour', how='outer')
    hourly_data = pd.merge(hourly_data, hourly_food, on='hour', how='outer')
    hourly_data = pd.merge(hourly_data, hourly_insulin, on='hour', how='outer')

    hourly_data.columns = ['hour', 'steps', 'heartrate', 'calories', 'carbohydrates', 'insulin']

    numeric_cols = ['steps', 'heartrate', 'calories', 'carbohydrates', 'insulin']
    hourly_data[numeric_cols] = hourly_data[numeric_cols].fillna(0)

    hourly_data['heartrate'] = hourly_data['heartrate'].round(2)

    hourly_data['hour'] = hourly_data['hour'].astype(int)

    data_json = hourly_data.to_dict(orient='records')
    json_output = json.dumps(data_json, indent=4)

    prompt = f"""
I have collected health data for {date_filter}. Here is my hourly data:

{json_output}

Please analyze how my food intake (calories and carbohydrates), insulin injections, steps, and heart rate interact to impact my blood sugar levels throughout the day. Provide insights and suggestions based on the data.
"""

    client = Anthropic(api_key=anthropic_api_key)

    response = client.completions.create(
        model="claude-v1",
        max_tokens_to_sample=1000,
        prompt=f"{HUMAN_PROMPT}{prompt}{AI_PROMPT}"
    )

    analysis = response.completion.strip()

    return analysis