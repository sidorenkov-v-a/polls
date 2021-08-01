def create_poll_data(**kwargs):
    from datetime import datetime, timedelta
    data = {
        'title': 'Test title',
        'description': 'Test description',
        'date_start': datetime.today().strftime('%Y-%m-%d'),
        'date_end': (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    }
    data.update(kwargs)
    return data
