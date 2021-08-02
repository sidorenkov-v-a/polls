def create_poll_data(**kwargs):
    from datetime import datetime, timedelta
    data = {
        'title': 'Test title',
        'description': 'Test description',
        'date_start': datetime.today().strftime('%Y-%m-%d'),
        'date_end': (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    }
    data.update(kwargs)
    if isinstance(data['date_start'], datetime):
        data['date_start'] = data['date_start'].strftime('%Y-%m-%d')
    if isinstance(data['date_end'], datetime):
        data['date_end'] = data['date_end'].strftime('%Y-%m-%d')
    return data
