import csv

EVENT_INDEX = {
    'Women 50 Yard Freestyle' : 0,
    'Women 100 Yard Freestyle' : 1,
    'Women 200 Yard Freestyle' : 2,
    'Women 500 Yard Freestyle' : 3,
    'Women 1000 Yard Freestyle' : 4,
    'Women 1650 Yard Freestyle' : 5,
    'Women 100 Yard Backstroke' : 6,
    'Women 200 Yard Backstroke' : 7,
    'Women 100 Yard Breaststroke' : 8,
    'Women 200 Yard Breaststroke' : 9,
    'Women 100 Yard Butterfly' : 10,
    'Women 200 Yard Butterfly' : 11,
    'Women 100 Yard IM': 12,
    'Women 200 Yard IM' : 13,
    'Women 400 Yard IM' : 14,
    'Women 200 Yard Freestyle Relay' : 15,
    'Women 400 Yard Freestyle Relay' : 16,
    'Women 800 Yard Freestyle Relay' : 17,
    'Women 200 Yard Medley Relay' : 18,
    'Women 400 Yard Medley Relay' : 19,
    'Women 4x50 Yard Medley Relay': 18,
    'Women 4x50 Yard Freestyle Relay': 15,
    'Women 4x100 Yard Medley Relay': 19,
    'Women 4x100 Yard Freestyle Relay': 16,
    "50's of stroke": 20
    }

PLACES = ['0.5','1','1.5','2','2.5','2.50','3','3.5','4','4.5','5','5.5','6','6.5',
          '7','7.5','8','8.5','9','9.5','10','10.5','11','11.5','12','12.5',
          '13','13.5','14','14.5','15','15.5','16']


def read_in_csvtxt(textfile, team, team_name):
    EVENTS = []
    female = False
    f = open(textfile, 'rb')
    
    for line in f:
        
        if ("Men" in line):
            female = False
        if ("Diving" in line):
            not_diving = False
            
        if ("Event" in line) and ("(" not in line) and ("Diving" not in line) and ("Men" not in line) and ("Scores" not in line) and ("Rankings" not in line) and ("Boys" not in line):
            event = line.strip()
            if "Girls" in event:
                event = event.replace("Girls", "Women")
            if ("50 Yard Backstroke" in event) or ("50 Yard Breaststroke" in event) or ("50 Yard Butterfly" in event):
                event_index = 20 #50's strokes
            else:
                event_index = EVENT_INDEX[" ".join(event.split(' ')[3:])]
            #print " ".join(event.split(' ')[3:]), event_index
            female = True
            not_diving = True
        if (team_name in line) and female and not_diving and ("50 Yard Backstroke" not in event) and ("50 Yard Breaststroke" not in event) and ("50 Yard Butterfly" not in event):
            #print event_index
            line = line.split()
            #print line
            person = ' '.join(line[1:3])
            line[-1] = line[-1].strip('x')
            line[-1] = ' '.join(line[-1].split())
            
                             
            if (line[-1] in PLACES): 
                time = line[-2]

            else:
                time = line[-1]
            
            if 'x' in time:
                time = time.strip('x')
            if 'DQ' in time:
                time = 0
            if person in team.keys():
                if team[person][event_index] == 0:
                    team[person][event_index] = [time]
                else:
                    team[person][event_index].append(time)
            else:
                #print "add", person
                team[person] = [0]*23
                
                team[person][event_index] = [time]    
            
    f.close() 
    return team

"""
def main():
    
    #Davidson
    #--------
    team_name = "Davidson College-NC"#"Georgetown University-AM"#
    dav_team = {}
    
    #HY-TEK files
    csv_file = 'Davidson_Richmond.txt' #'GW_Georgetown.txt'# 
    team_meet4 = read_in_csvtxt(csv_file, dav_team, team_name)
    print team_meet4

    #---------------------------------------------------
    return

if __name__ == "__main__":
    main()
"""