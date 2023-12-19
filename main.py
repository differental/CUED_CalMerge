"""
main.py
"""
from datetime import datetime
import math
from icalendar import Calendar, Event
import requests
import pytz
import recurring_ical_events

now = datetime.now(pytz.timezone("Europe/London"))
recommend_year = now.year
if now.month <= 6:
    recommend_year -= 1
YR = int(
    input("Academic Year [" + str(recommend_year) + "]: ").strip() or recommend_year)

ia_or_ib = int(input("\n1. IA\n2. IB\nChoose Year Group: "))

term = int(input("\n1. Michaelmas\n2. Lent\n3. Easter\nChoose Term: "))
TERMID = "mich" if term == 1 else "lent" if term == 2 else "easter"

LAB_GROUP = int(input("Lab Group Number [Skip Lab]: ").strip() or 0)

LAB_URL = '/'.join((
    "http://teach-cals.eng.cam.ac.uk/cued-labs",
    str(YR),
    "ia" if ia_or_ib == 1 else "ib",
    TERMID,
    str(math.ceil(LAB_GROUP/3)*3-2) + "-" + str(math.ceil(LAB_GROUP/3)*3) + ".ics"))

LECTURE_URL = '&'.join((
    "https://td.eng.cam.ac.uk/tod/public/view_ical.php?yearval=" +
    str(YR) + "_" + str((YR+1) % 100),
    "term=" + TERMID[0].upper(),
    "course=" + ("IA" if ia_or_ib == 1 else "IB")))

LECTURE_CLEAN = bool(int(input("""
1. Clean lecture titles and put locations in a seperate line
2. Do Nothing
Choose Mode [1]: """).strip() or 1))

LAB_CLEAN = bool(int(input("""
1. Clean lab titles and "Cambridge, United Kingdom" in lab locations
2. Do Nothing
Choose Mode [1]: """).strip() or 1))

operating_mode = int(input(
    "\n1. Bare Minimum\n2. Essential\n3. All\nChoose Mode [2]: ").strip() or 2)

if LAB_GROUP:
    labr = requests.get(LAB_URL, allow_redirects=True, timeout=10)
    open('lab.ics', 'wb').write(labr.content)
lecturer = requests.get(LECTURE_URL, allow_redirects=True, timeout=10)
open('lecture.ics', 'wb').write(lecturer.content)

if LAB_GROUP:
    with open('lab.ics', 'rb') as labe:
        lab_cal = Calendar.from_ical(labe.read())

with open('lecture.ics', 'rb') as lecturee:
    lecture_cal = Calendar.from_ical(lecturee.read())

cal = Calendar()
cal.add('version', '2.0')
cal.add('prodid', '-//teaching.eng.cam.ac.uk//CUED Calendars//')

allevents = recurring_ical_events.of(
    lecture_cal).between("19700101", "20991231")
if LAB_GROUP:
    allevents += recurring_ical_events.of(
        lab_cal).between("19700101", "20991231")

for event in allevents:
    if ("see rota" in event["SUMMARY"] or "see lab rota" in event["SUMMARY"]):
        continue
    name = event["SUMMARY"].replace("\n", "")
    timestart = event["DTSTART"].dt
    timeend = event["DTEND"].dt
    try:
        location = event["LOCATION"].replace("\n", "")
    except KeyError:
        location = ""

    if LECTURE_CLEAN and name.find('[') + 1:
        if name.find('(Lecture Theatre 1)')+1:
            location = "LT1"
        elif name.find('(Constance Tipper)')+1:
            location = "LT0"
        name = name[0:name.find('[')]

    if LAB_CLEAN and location.find(' - ') + 1:
        location = location[0:location.find(' - ')]

    if (("Industrial Placement" or "1PX") in name) and operating_mode <= 2:
        continue
    if name[0] == ("1" or "2") and name[1] == ("P" or "C") and operating_mode <= 1:
        continue

    newevent = Event()
    newevent.add('summary', name)
    newevent.add('dtstart', timestart)
    newevent.add('dtend', timeend)
    if location:
        newevent['location'] = location
    cal.add_component(newevent)

with open('combined.ics', 'wb') as f:
    f.write(cal.to_ical())
