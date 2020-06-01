from .database import engine
from sqlalchemy import text
from datetime import datetime
from dateutil.relativedelta import relativedelta

def filter_latest_date():
    """
    retrieves registry lates date on a station
    """
    conn = engine.connect()
    last_date_statement = text("SELECT date FROM measurement ORDER BY date desc LIMIT 1")
    last_date = conn.execute(last_date_statement).first()[0]

    return last_date

def filter_twelve_months(last_date):
    """
    convertor of dates, that returns date (string) of 
    12 motnhs before latest date found in the registries 
    """
    date_time_obj = datetime.strptime(last_date, '%Y-%m-%d')
    date_minus_12_months = date_time_obj - relativedelta(months=+12)
    delta_date_str = date_minus_12_months.strftime('%Y-%m-%d')

    return delta_date_str

def precipitation_summary():
    """
    retrieves lastest registry date on databse to gather
    last 12 months of registries and then returns a dictionary sorted
    by Stations and it's registries dates
    """
    conn = engine.connect()

    last_date = filter_latest_date()

    delta_date_str = filter_twelve_months(last_date)

    last_12_motnhs_stmt = text("SELECT s.name, m.date, m.prcp FROM measurement as m JOIN station as s ON s.station == m.station WHERE date >= :months_12 ORDER BY date desc")
    last_12_months = conn.execute(last_12_motnhs_stmt, months_12=delta_date_str).fetchall()

    station_names = { pair[0]: {} for pair in last_12_months}

    for pair in last_12_months:
        station_names[pair[0]][pair[1]] = pair[2]

    return station_names

def stations_summary():
    """
    GET's amount of stations, sorts stations by activity
    and tells more active station as well
    """
    conn = engine.connect()

    stations_summary_dict = {}

    number_stations_statement = text("SELECT count(name) FROM station")
    number_stations = conn.execute(number_stations_statement).first()[0]

    stations_summary_dict["Number of stations"] = number_stations

    activity_stations_statement = text("select s.name, count(m.id) from station as s join measurement as m on s.station == m.station group by s.name order by 2 desc")
    activity_stations = conn.execute(activity_stations_statement).fetchall()
    activity_stations_d = { pair[0]: pair[1] for pair in activity_stations}

    stations_summary_dict["Stations activity (descending)"] = activity_stations_d

    stations_summary_dict["Most active station"] = activity_stations[0][0]

    return stations_summary_dict

def tobservation_summary():
    """
    GETS's last 12 months of temperature observations sorted by most active stations
    """
    conn = engine.connect()

    last_date = filter_latest_date()

    delta_date_str = filter_twelve_months(last_date)

    last_12_motnhs_tobs_act_stmt = text("SELECT s.name, count(m.tobs) FROM measurement as m JOIN station as s ON s.station == m.station WHERE date >= :months_12 GROUP BY s.name ORDER BY 2 desc")
    last_12_months_tobs_act = conn.execute(last_12_motnhs_tobs_act_stmt, months_12=delta_date_str).fetchall()


    last_12_motnhs_tobs_stmt = text("SELECT s.name, m.date, m.tobs FROM measurement as m JOIN station as s ON s.station == m.station WHERE date >= :months_12 ORDER BY 2 desc")
    last_12_months_tobs = conn.execute(last_12_motnhs_tobs_stmt, months_12=delta_date_str).fetchall()

    station_names = { pair[0]: {"Amount of temperature observations": pair[1], "Observations": {}} for pair in last_12_months_tobs_act}

    for pair in last_12_months_tobs:
        station_names[pair[0]]["Observations"][pair[1]] = pair[2]


    return station_names

def temp_stats(temp_dic):
    temp_summary = {key: {"min": 0, "max": 0, "avrg": 0} for key in temp_dic.keys()}
    for key, value in temp_dic.items():
        t_num_list = value["temps"].values()
        temp_summary[key]["min"] = min(t_num_list)
        temp_summary[key]["max"] = max(t_num_list)
        temp_summary[key]["avrg"] = round(sum(t_num_list) / len(t_num_list), 2)
    return temp_summary


def start_date(start=None, end=None):
    conn = engine.connect()

    last_date = filter_latest_date()

    delta_date_str = filter_twelve_months(last_date)
    
    start_tobs_statement = text("SELECT s.name, m.date, m.tobs FROM measurement as m JOIN station as s ON s.station == m.station WHERE date >= :st AND date <= :lt ORDER BY 2 desc")
    if end:
        try:
            star_tobs = conn.execute(start_tobs_statement, st=start, lt=end).fetchall()
        except Exception:
            star_tobs = conn.execute(start_tobs_statement, st=delta_date_str, lt=last_date).fetchall()
    else:
        try:
            star_tobs = conn.execute(start_tobs_statement, st=start, lt=last_date).fetchall()
        except Exception:
            star_tobs = conn.execute(start_tobs_statement, st=delta_date_str, lt=last_date).fetchall()

    temps = { trio[0]: {"temps": {}} for trio in star_tobs}
    
    for trio in star_tobs:
        temps[trio[0]]["temps"][trio[1]] = trio[2]

    temp_summary = temp_stats(temps)

    return temp_summary