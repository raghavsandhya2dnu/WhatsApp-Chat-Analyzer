import re
import pandas as pd

def preprocess(data):
    print("Preprocess started")

    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s(?:1[0-2]|0?[1-9]):[0-5][0-9][\s\u202f\u00a0]?(?:AM|PM|am|pm)\s-\s'
    messages = re.split(pattern, data)[1:]
    date = re.findall(pattern, data)
    print(f"Found {len(messages)} messages and {len(date)} dates")

    dates = [d.replace('\u202f', ' ').replace('\u00a0', ' ') for d in date]
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    try:
        df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ')
    except Exception as e:
        print("Date parsing error:", e)
        return None

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages_list = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:  # user exists
            users.append(entry[1])
            messages_list.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages_list.append(entry[0])

    df['user'] = users
    df['message'] = messages_list

    df.drop(columns=['user_message'], inplace=True)
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df

