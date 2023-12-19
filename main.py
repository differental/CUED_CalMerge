from datetime import datetime
from icalendar import Calendar, Event
import requests
import pytz
import math
import recurring_ical_events

now = datetime.now(pytz.timezone("Europe/London"))
recommend_year = now.year
if (now.month <= 6): recommend_year -= 1
year = int(input("Academic Year [" + str(recommend_year) + "]: ").strip() or recommend_year)

ia_or_ib = int(input("\n1. IA\n2. IB\nChoose Year Group: "))

term = int(input("\n1. Michaelmas\n2. Lent\n3. Easter\nChoose Term: "))
termid = "mich" if term == 1 else "lent" if term == 2 else "easter"

lab_group = int(input("Lab Group Number [Skip Lab]: ").strip() or 0)

lab_url = "http://teach-cals.eng.cam.ac.uk/cued-labs/" + str(year) + ("/ia/" if ia_or_ib == 1 else "/ib/") + termid + "/" + str(math.ceil(lab_group/3)*3-2) + "-" + str(math.ceil(lab_group/3)*3) + ".ics"
lecture_url = "https://td.eng.cam.ac.uk/tod/public/view_ical.php?yearval=" + str(year) + "_" + str((year+1)%100) + "&term=" + termid[0].upper() + "&course=" + ("IA" if ia_or_ib == 1 else "IB")

lecture_clean_choice = int(input("\n1. Clean lecture titles and put locations in a seperate line\n2. Do Nothing\nChoose Mode [1]: ").strip() or 1)
lecture_clean = True if lecture_clean_choice == 1 else False

lab_clean_choice = int(input("\n1. Clean lab titles and \"Cambridge, United Kingdom\" in lab locations\n2. Do Nothing\nChoose Mode [1]: ").strip() or 1)
lab_clean = True if lab_clean_choice == 1 else False

operating_mode = int(input("\n1. Bare Minimum\n2. Essential\n3. All\nChoose Mode [2]: ").strip() or 2)

if lab_group:
    labr = requests.get(lab_url, allow_redirects=True, timeout=10)
    open('lab.ics', 'wb').write(labr.content)
lecturer = requests.get(lecture_url, allow_redirects=True, timeout=10)
open('lecture.ics', 'wb').write(lecturer.content)

if lab_group:
    labe = open('lab.ics', 'rb')
    lab_cal = Calendar.from_ical(labe.read())
    labe.close()

lecturee = open('lecture.ics', 'rb')
lecture_cal = Calendar.from_ical(lecturee.read())
lecturee.close()

cal = Calendar()
cal.add('version', '2.0')
cal.add('prodid', '-//teaching.eng.cam.ac.uk//CUED Calendars//')

allevents = recurring_ical_events.of(lecture_cal).between("19700101", "20991231")
if lab_group:
    allevents += recurring_ical_events.of(lab_cal).between("19700101", "20991231")

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

    if lecture_clean and name.find('[') + 1:
        if name.find('(Lecture Theatre 1)')+1:
            location = "LT1"
        elif name.find('(Constance Tipper)')+1:
            location = "LT0"
        name = name[0:name.find('[')]
        
    if lab_clean and location.find(' - ') + 1:
        location = location[0:location.find(' - ')]
        
    if ("Industrial Placement" in name or "1PX" in name) and operating_mode <= 2:
        continue
    if (name[0] == "1" or name[0] == "2") and (name[1] == "P" or name[1] == "C") and operating_mode <= 1:
        continue
    
    newevent = Event()
    newevent.add('summary', name)
    newevent.add('dtstart', timestart)
    newevent.add('dtend', timeend)
    if location:
        newevent['location'] = location
    cal.add_component(newevent)
    
f = open('combined.ics', 'wb')
f.write(cal.to_ical())
f.close()