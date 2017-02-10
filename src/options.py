from datetime import datetime


def get_first_day():
    today = datetime.today()
    today = today.strftime('%d/%m/%Y')
    today = today[2:]
    first_day_s = "01" + today
    first_day = datetime.strptime(first_day_s, "%d/%m/%Y")
    return first_day


class options():
    command = "print_stats"
    gitlab_server = "http://gitlab.intranet.sky"
    gitlab_token = "QR18DoufKscQAF6HA_BD"
    gitlab_project = "ce-devices-ios/Benji"
    gitlab_max_size = 2000
    gitlab_stats_start_date = get_first_day().strftime("%d/%m/%Y")
    gitlab_stats_end_date = datetime.now().strftime("%d/%m/%Y")

