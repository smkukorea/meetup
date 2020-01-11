from app.models import Event
from datetime import datetime, timedelta

class Schedule:
    def __init__(self, event):
        dates = event.dates.split(",")
        self.days = [datetime.strftime(date, "%a") for date in (datetime.strptime(date, "%m/%d/%Y") for date in dates)]
        self.dates = [datetime.strftime(date, "%m/%d") for date in (datetime.strptime(date, "%m/%d/%Y") for date in dates)]
    
        start_time_parsed = datetime.strptime(event.start, "%I:%M %p")
        end_time_parsed = datetime.strptime(event.end, "%I:%M %p")

        self.times = [datetime.strftime(date, "%I:%M %p") for date in 
                            datetime_range(start_time_parsed, end_time_parsed,
                            timedelta(minutes=15))]

def personal_to_event(user_schedule, event):
    dates = event.dates.split(",")
    times = [datetime.strftime(date, "%I:%M %p") for date in 
                            datetime_range(datetime.strptime(event.start, "%I:%M %p"),
                            datetime.strptime(event.end, "%I:%M %p"),
                            timedelta(minutes=15))]

    user_availability = {}
    short_dates = [datetime.strftime(date, "%m/%d") for date in (datetime.strptime(date, "%m/%d/%Y") for date in dates)]
    days_of_week = [datetime.strftime(date, "%A") for date in (datetime.strptime(date, "%m/%d/%Y") for date in dates)]
    for i in range(len(short_dates)):
        for time in times:
            user_availability[short_dates[i] + " " + time] = user_schedule[days_of_week[i] + " " + time]

    return user_availability


def create_overlap(schedule, user_avail):
    id_list = []
    for time in schedule.times:
        for date in schedule.dates:
            id_list.append(date + " " + time)

    overall_avail = {}
    avail_max = 0
    for id1 in id_list:
        overall_avail[id1] = 0
    for availability in user_avail.values():
        for id1 in id_list:
            if availability[id1]:
                overall_avail[id1] += 1
                if overall_avail[id1] > avail_max:
                    avail_max = overall_avail[id1]

    colors = linear_gradient("#f0f0f0", "#5f7eed", avail_max+1)

    color_dict = {}
    for id1 in id_list:
        color_dict[id1] = colors[overall_avail[id1]]

    return color_dict

def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta

#source for color interpolation functions: https://bsou.io/posts/color-gradients-with-python
def hex_to_RGB(hex):
  ''' "#FFFFFF" -> [255,255,255] '''
  # Pass 16 to the integer function for change of base
  return [int(hex[i:i+2], 16) for i in range(1,6,2)]


def RGB_to_hex(RGB):
  ''' [255,255,255] -> "#FFFFFF" '''
  # Components need to be integers for hex to make sense
  RGB = [int(x) for x in RGB]
  return "#"+"".join(["0{0:x}".format(v) if v < 16 else
            "{0:x}".format(v) for v in RGB])

def linear_gradient(start_hex, finish_hex, n):
  ''' returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    inlcuding the number sign ("#FFFFFF") '''
  # Starting and ending colors in RGB form
  s = hex_to_RGB(start_hex)
  f = hex_to_RGB(finish_hex)
  # Initilize a list of the output colors with the starting color
  RGB_list = [start_hex]
  # Calcuate a color at each evenly spaced value of t from 1 to n
  for t in range(1, n):
    # Interpolate RGB vector for color at the current value of t
    curr_vector = [
      int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
      for j in range(3)
    ]
    # Add it to our list of output colors
    RGB_list.append(RGB_to_hex(curr_vector))

  return RGB_list