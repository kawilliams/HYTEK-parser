import pdf_txt_meet
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
    'Women 4x100 Yard Freestyle Relay': 16
    }

PLACES = ['0.5','1','1.5','2','2.5','2.50','3','3.5','4','4.5','5','5.5','6','6.5',
          '7','7.5','8','8.5','9','9.5','10','10.5','11','11.5','12','12.5',
          '13','13.5','14','14.5','15','15.5','16']

def write_to_csv(season, team_name, filename):
    
    with open(filename, 'ab') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)

        for person in season.keys():
            line = [person] +[team_name]+ [0]*23
            #print person
            for i in range(len(season[person])):
                line[i+2] = average_times(season[person][i])
                #print line[i+2]
                           
            writer.writerow(line)
            
    return


def average_times(event_times):
    #print event_times
    sum_times = 0
    if event_times == 0:
        return 0
    else:
        if 0 in event_times:
            event_times.remove(0)
        
        total = len(event_times)                
        for time in event_times:  
            if ('X' in time):
                time = time.strip('X')
            if ('x' in time):
                time = time.strip('x')
            if ':' in time:
                time_sec = int(time[:time.find(':')])*60.0 + float(time[time.find(':')+1:])
            else:
                time_sec = float(time)
            sum_times += time_sec
                        
        average = sum_times/total
        #print "average",average
        return average

def read_in_txt(textfile, team, team_name):
    
    EVENTS = []
    female = False
    f = open(textfile, 'r')
   
    for line in f:
        line = line.strip()
        line = line.split('\n')[0]
        unspaced = " ".join(line.split())
        words = unspaced.split(' ')
        less_space = []
        for word in words:
            if word != '':
                less_space.append(word)
       
        if (('Event' in line) and ('Not' not in line) and 
            ('(' not in line) and ('Rankings' not in line) and
            ('Men') not in line): #delete to add men
            if 'Girls' in line:
                line = line.replace('Girls', 'Women')
            bar = " ".join(line.split()[2:])
            #muffin = bar[:-4]
            #print "muffin", muffin
            
            if bar in EVENT_INDEX.keys(): 
                EVENTS.append(bar)
                index = EVENT_INDEX[bar]
                female = True  
            #print bar
        #print female
        if 'Men' in line:            
            female = False   
        if female:
            time = words[-1].strip('x')           
            time = ' '.join(time.split()) 
            
            if words[0] in PLACES:
                if (words[1][0] == '1') or (words[1][0] == '2') :
                    name = ' '.join(words[2:4])
                else:
                    name = ' '.join(words[1:3])          
                
                if time[0] == 'x':
                    time = time[1:]  
                if ('.' in time) and (time in PLACES):
                    time = words[-2]
                
                if name in team.keys():
                    #print name
                    if "." in time: #int(words[-1]) in range(15):
                        if team[name][index] == 0:
                            team[name][index] = [time]
                        else:
                            team[name][index].append(time)
                            
                            
                    elif int(time) in range(15):
                        if team[name][index] == 0:
                            team[name][index] = [words[-2]]
                        else:
                            team[name][index].append(words[-2])
                        #print team.keys()
                    
                elif len(words) > 5: #(words[1] not in team_name):
                    #print words
                    if (words[4] in team_name) or (words[5] in team_name) or (words[3] in team_name) and (len(words[3]) > 1):
                        #print name, words[3:6], team_name
                        team[name] = [0]*23
                        if "." in words[-1]: #words[-1] in range(15):
                            if team[name][index] == 0:
                                team[name][index] = [words[-1]] #-2 
                            else:
                                team[name][index].append(words[-1]) #-2
                            
                        elif int(words[-1]) in range(15): #"." in words[-1]:
                            if team[name][index] == 0:
                                team[name][index] = [words[-2]] #-1
                            else:                        
                                team[name][index].append(words[-2])#-1
                        #print team.keys()
            
    f.close()
    return team

def main():
    """
    filename = 'dataA102016.csv'
    with open(filename, 'ab') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)

        line = ['Swimmer','School','50 Free','100 Free','200 Free','500 Free','1000 Free','1650 Free','100 Back','200 Back','100 Breast','200 Breast','100 Fly','200 Fly','100 IM','200 IM','400 IM']
        writer.writerow(line)
    
    #---------------------------------------------------
    #Davidson
    #--------
    team_name = "Davidson College-NC"
    dav_team = {}
    dav_path = "Atlantic10_Season2016/Atlantic10_Season2016/WDavidsonResults/"
    #HY-TEK files
    txt_file1 = dav_path + "2016%20Georgetown%20Results.txt"
    team_meet1 = read_in_txt(txt_file1, dav_team, team_name)
    #print team_meet1
    
    txt_file2 = dav_path + '15-16SWIM_ODU_Marshall_HTML.txt'
    team_meet2 = read_in_txt(txt_file2, team_meet1, team_name)
    #print team_meet2
   
    txt_file3 = dav_path + 'DavidsonUNCW%20Results.txt'
    team_meet3 = read_in_txt(txt_file3, team_meet2, team_name)
    #print team_meet3
    
    csv_file = dav_path + 'Davidson_Richmond.txt' 
    team_meet4 = pdf_txt_meet.read_in_csvtxt(csv_file, team_meet3, team_name)
    #print team_meet4    
    write_to_csv(team_meet4, team_name, filename)
    
    #---------------------------------------------------
    #Richmond
    #--------
    team_name = "University of Richmond-VA"
    rich_team={}
    rich_path = "Atlantic10_Season2016/Atlantic10_Season2016/WRichmondResults/"
    #HY-TEK files
    txt_file1 = rich_path + "Rich_Duquesne.txt"
    team_meet1 = read_in_txt(txt_file1, rich_team, team_name)
    txt_file2 = rich_path + "Rich_GeorgeMason.txt"
    team_meet2 = read_in_txt(txt_file2, team_meet1, team_name)
    txt_file3 = rich_path + "Rich_QueensVTech.txt"
    team_meet3 = read_in_txt(txt_file3, team_meet2, team_name)    
    #PDF to txt files
    csv_file4 = rich_path + 'Rich_GeorgeWashington.txt' 
    team_meet4 = pdf_txt_meet.read_in_csvtxt(csv_file4, team_meet3, team_name)
    csv_file5 = rich_path + 'Rich_JMU.txt' 
    team_meet5 = pdf_txt_meet.read_in_csvtxt(csv_file5, team_meet4, team_name)
    csv_file6 = rich_path + 'Rich_VU.txt' 
    team_meet6 = pdf_txt_meet.read_in_csvtxt(csv_file6, team_meet5, team_name)

    write_to_csv(team_meet6, team_name, filename)
    
    #---------------------------------------------------
    #George Washington
    #-----------------
    team_name = "George Washington University-PV"
    short = "George Washington"
    gw_team={}
    gw_path = "Atlantic10_Season2016/Atlantic10_Season2016/WGeorgeWashingtonResults/"
    #HY-TEK files
    txt_file1 = gw_path + "GW_GeorgeMason.txt"
    team_meet1 = read_in_txt(txt_file1, gw_team, team_name)
    csv_file2 = gw_path + "GW_Georgetown.txt"
    team_meet2 = read_in_txt(csv_file2, team_meet1, team_name)
    csv_file3 = gw_path + "GW_Howard.txt"
    team_meet3 = read_in_txt(csv_file3, team_meet2, team_name)    
    #PDF to txt files
    csv_file4 = gw_path + "GW_Richmond.txt"
    team_meet4 = pdf_txt_meet.read_in_csvtxt(csv_file4, team_meet3, team_name)
    csv_file5 = gw_path + "GW_Towson.txt" 
    team_meet5 = pdf_txt_meet.read_in_csvtxt(csv_file5, team_meet4, team_name)
    csv_file6 = gw_path + "GW_W&M.txt"
    team_meet6 = pdf_txt_meet.read_in_csvtxt(csv_file6, team_meet5, team_name)

    write_to_csv(team_meet6, team_name, filename)  
   
    
    #---------------------------------------------------
    #Duquesne
    #-----------------
    team_name = "Duquesne University-AM"
    short = "Duquesne"
    duq_team={}
    duq_path = "Atlantic10_Season2016/Atlantic10_Season2016/WDuquesneResults/"
    
    #HY-TEK files    
    txt_file1 = duq_path + "Davidson_Richmond.txt"
    team_meet1 = pdf_txt_meet.read_in_csvtxt(txt_file1, duq_team, team_name)
    csv_file2 = duq_path + "Duq_LaSalleStLouisStBon.txt"
    team_meet2 = read_in_txt(csv_file2, team_meet1, team_name)
    csv_file3 = duq_path + "Duq_OhioXavier.txt"
    team_meet3 = read_in_txt(csv_file3, team_meet2, team_name) 
    csv_file4 = duq_path + "Duq_Richmond.txt"
    team_meet4 = pdf_txt_meet.read_in_csvtxt(csv_file4, team_meet3, team_name)    
    csv_file5 = duq_path + "Duq_StMarys.txt"
    team_meet5 = read_in_txt(csv_file5, team_meet4, team_name) 
    csv_file6 = duq_path + "Duq_Youngstown.txt"
    team_meet6 = read_in_txt(csv_file6, team_meet5, team_name)    
    #PDF to txt files
    csv_file7 = duq_path + "Duq_Oakland.txt"
    team_meet7 = pdf_txt_meet.read_in_csvtxt(csv_file7, team_meet6, team_name)    
    csv_file8 = duq_path + "Duq_StFrancis.txt" 
    team_meet8 = pdf_txt_meet.read_in_csvtxt(csv_file8, team_meet7, team_name)
    csv_file9 = duq_path + "Duq_Toledo.txt"
    team_meet9 = pdf_txt_meet.read_in_csvtxt(csv_file9, team_meet8, team_name)
    
    write_to_csv(team_meet9, team_name, filename)      
    
  
    #---------------------------------------------------
    #Fordham BUGGY
    #-----------------
    team_name = "Fordham-MR"
    short = "Fordham"
    ford_team={}
    ford_path = "Atlantic10_Season2016/Atlantic10_Season2016/WFordhamResults/"    
    #HY-TEK files    
    txt_file1 = ford_path + "Fordham_ArmyWP.txt"
    team_meet1 = read_in_txt(txt_file1, ford_team, team_name)
    #print team_meet1
    csv_file2 = ford_path + "Fordham_BostonU.txt"
    team_meet2 = read_in_txt(csv_file2, team_meet1, team_name)
    #print team_meet2
    csv_file3 = ford_path + "Fordham_FairfieldMonmouth.txt"
    team_meet3 = read_in_txt(csv_file3, team_meet2, team_name) 
    #print team_meet3
    csv_file4 = ford_path + "Fordham_IonaLaSalle.txt"
    team_meet4 = read_in_txt(csv_file4, team_meet3, team_name)    
    #print team_meet4
    csv_file5 = ford_path + "Fordham_LIUPost.txt"
    team_meet5 = read_in_txt(csv_file5, team_meet4, team_name) 
    #print team_meet5
    csv_file6 = ford_path + "Fordham_Manhattan.txt"
    team_meet6 = read_in_txt(csv_file6, team_meet5, team_name)    
    #print team_meet6
    csv_file7 = ford_path + "Fordham_Marist.txt"
    team_meet7 = read_in_txt(csv_file7, team_meet6, team_name)
    #print team_meet7
    csv_file8 = ford_path + "Fordham_StFrancis.txt" 
    team_meet8 = read_in_txt(csv_file8, team_meet7, team_name)
    #print team_meet8

    write_to_csv(team_meet8, team_name, filename)      
    
    
    #---------------------------------------------------
    #LaSalle
    #-----------------
    team_name = "La Salle-MA"
    short = "La Salle"
    ls_team={}
    ls_path = "Atlantic10_Season2016/Atlantic10_Season2016/WLaSalleResults/"
    
    #HY-TEK files    
    txt_file1 = ls_path + "LaSalle_FordhamIona.txt"
    team_meet1 = read_in_txt(txt_file1, ls_team, team_name)
    #print team_meet1
    txt_file2 = ls_path + "LaSalle_Villanova.txt"
    team_meet2 = read_in_txt(txt_file2, team_meet1, team_name)
    #print team_meet2
    #PDF to txt files
    #csv_file3 = ls_path + "LaSalle_Delaware.txt"
    #team_meet3 = pdf_txt_meet.read_in_csvtxt(csv_file3, team_meet2, team_name)    
    #print team_meet3
    csv_file4 = ls_path + "LaSalle_Drexel.txt"
    team_meet4 = pdf_txt_meet.read_in_csvtxt(csv_file4, team_meet2, team_name) #KATY team_meet3 
    #print team_meet4
    csv_file5 = ls_path + "LaSalle_Duq&StB&StL.txt"
    team_meet5 = pdf_txt_meet.read_in_csvtxt(csv_file5, team_meet4, team_name)    
    #print team_meet5
    csv_file6 = ls_path + "LaSalle_GeorgeMason.txt"
    team_meet6 = pdf_txt_meet.read_in_csvtxt(csv_file6, team_meet5, team_name)    
    #print team_meet6   
    csv_file7 = ls_path + "LaSalle_Penn.txt"
    team_meet7 = pdf_txt_meet.read_in_csvtxt(csv_file7, team_meet6, team_name)    
    #print team_meet7     
    
    write_to_csv(team_meet7, team_name, filename)       
    
    #---------------------------------------------------
    #Rhode Island - BUGGY missing people
    #-----------------
    team_name = "Rhode Island-NE"
    short = "Rhode Island-NE"
    ri_team={}
    ri_path = "Atlantic10_Season2016/Atlantic10_Season2016/WRhodeIslandResults/"
    
    #HY-TEK files    
    txt_file1 = ri_path + "RI_Maine.txt"
    team_meet1 = read_in_txt(txt_file1, ri_team, team_name)
    write_to_csv(team_meet1, team_name, filename)   
    
    
    #---------------------------------------------------
    #StBonaventure
    #-----------------
    team_name = "St. Bonaventure-NI"
    short = "St. Bonaventure-NI"
    sb_team={}
    sb_path = "Atlantic10_Season2016/Atlantic10_Season2016/WStBonaventureResults/"
    
    #HY-TEK files    
    txt_file1 = sb_path + "StB_Buffalo.txt"
    team_meet1 = read_in_txt(txt_file1, sb_team, team_name)
    #print team_meet1
    txt_file2 = sb_path + "StB_Canisius.txt"
    team_meet2 = read_in_txt(txt_file2, team_meet1, team_name)
    #print team_meet2
    txt_file3 = sb_path + "StB_Colgate.txt"
    team_meet3 = read_in_txt(txt_file3, team_meet2, team_name)
    #print team_meet3
    txt_file4 = sb_path + "StB_Canisius.txt"
    team_meet4 = read_in_txt(txt_file4, team_meet3, team_name)
    #print team_meet4    
    write_to_csv(team_meet4, team_name, filename)  
    
    #---------------------------------------------------
    #StLouis
    #-----------------
    team_name = "SLU-OZ"
    short = "SLU-OZ"
    sl_team={}
    sl_path = "Atlantic10_Season2016/Atlantic10_Season2016/WStLouisResults/"
    
    #HY-TEK files    
    txt_file1 = sl_path + "StLouis_DSU&Lindenwood&Maryville.txt"
    team_meet1 = read_in_txt(txt_file1, sl_team, team_name)
    #print len(team_meet1.keys()  )
    txt_file2 = sl_path + "StLouis_DuqLaSalleStBon.txt"
    team_meet2 = read_in_txt(txt_file2, team_meet1, team_name)
    #print len(team_meet2)   
    txt_file3 = sl_path + "StLouis_Truman.txt"
    team_meet3 = read_in_txt(txt_file3, team_meet2, team_name)    
    #print len(team_meet3)
    txt_file4 = sl_path + "StLouis_WashU.txt"
    team_meet4 = read_in_txt(txt_file4, team_meet3, team_name)        
    #print len(team_meet4)
    #PDF to txt files
    csv_file5 = sl_path + "StLouis_ALR&HS.txt"
    team_meet5 = pdf_txt_meet.read_in_csvtxt(csv_file5, team_meet4, team_name)    
    #print team_meet5    
    csv_file6 = sl_path + "StLouis_UMSL&LindenwoodB&Maryville.txt"
    team_meet6 = pdf_txt_meet.read_in_csvtxt(csv_file6, team_meet5, team_name)    
    #print team_meet6
    csv_file7 = sl_path + "StLouis_WestIll.txt"
    team_meet7 = pdf_txt_meet.read_in_csvtxt(csv_file7, team_meet6, team_name)    
    #print team_meet7 
    write_to_csv(team_meet7, team_name, filename) 
    
    #---------------------------------------------------
    #UMass
    #-----------------
    team_name = "Massachusetts-NE"
    short = "Massachusetts"
    um_team={}
    um_path = "Atlantic10_Season2016/Atlantic10_Season2016/WUMassResults/"
    
    #HY-TEK files    
    txt_file1 = um_path + "UMass_Brown.txt"
    team_meet1 = read_in_txt(txt_file1, um_team, team_name)
    #print len(team_meet1.keys()  )
    txt_file2 = um_path + "UMass_Bryant.txt"
    team_meet2 = read_in_txt(txt_file2, team_meet1, team_name)
    #print len(team_meet2)       
    write_to_csv(team_meet2, team_name, filename) 
    """
    # NEW SEASON: 2015
    filename = 'dataA102015.csv'
    with open(filename, 'ab') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)

        line = ['Swimmer','School','50 Free','100 Free','200 Free','500 Free','1000 Free','1650 Free','100 Back','200 Back','100 Breast','200 Breast','100 Fly','200 Fly','100 IM','200 IM','400 IM']
        writer.writerow(line)
    
    #---------------------------------------------------
    #Davidson 2015
    #--------
    team_name = "Davidson College-NC"
    dav_team = {}
    dav_path = "Atlantic10_Season2015/WDavidsonResults/"
    #HY-TEK files
    txt_file1 = dav_path + "Dav_Queens.txt"
    team_meet1 = read_in_txt(txt_file1, dav_team, team_name)
    #print team_meet1
    
    txt_file2 = dav_path + 'Dav_Rich.txt'
    team_meet2 = read_in_txt(txt_file2, team_meet1, team_name)
    #print team_meet2
   
    txt_file3 = dav_path + 'Dav_W&M.txt'
    team_meet3 = read_in_txt(txt_file3, team_meet2, team_name)
    #print team_meet3
    
    csv_file = dav_path + 'Dav_GeorgetownGW.txt' 
    team_meet4 = pdf_txt_meet.read_in_csvtxt(csv_file, team_meet3, team_name)
    #print team_meet4    
    write_to_csv(team_meet4, team_name, filename)
    
    #---------------------------------------------------
    #Richmond
    #--------
    team_name = "University of Richmond-VA"
    rich_team={}
    rich_path = "Atlantic10_Season2015/WRichmondResults/"
    #HY-TEK files
    txt_file1 = rich_path + "Rich_GeorgeMason.txt"
    team_meet1 = read_in_txt(txt_file1, rich_team, team_name)
    txt_file2 = rich_path + "Rich_JMU.txt"
    team_meet2 = read_in_txt(txt_file2, team_meet1, team_name)
    txt_file3 = rich_path + "Rich_Liberty.txt"
    team_meet3 = read_in_txt(txt_file3, team_meet2, team_name)    
    txt_file4 = rich_path + "Rich_Villanova.txt"
    team_meet4 = read_in_txt(txt_file4, team_meet3, team_name) 
    write_to_csv(team_meet4, team_name, filename)
    
    #---------------------------------------------------
    #George Washington
    #-----------------
    team_name = "George Washington University-PV"
    short = "George Washington"
    gw_team={}
    gw_path = "Atlantic10_Season2015/WGWResults/"
    #HY-TEK files
    csv_file1 = gw_path + "GW_BucknellBU.txt"
    team_meet1 = pdf_txt_meet.read_in_csvtxt(csv_file1, gw_team, team_name) 
    csv_file2 = gw_path + "GW_Drexel.txt"
    team_meet2 = pdf_txt_meet.read_in_csvtxt(csv_file2, team_meet1, team_name)
    csv_file3 = gw_path + "GW_GMU.txt" 
    team_meet3 = pdf_txt_meet.read_in_csvtxt(csv_file3, team_meet2, team_name)
    csv_file4 = gw_path + "GW_Howard (1).txt"
    team_meet4 = pdf_txt_meet.read_in_csvtxt(csv_file4, team_meet3, team_name)

    write_to_csv(team_meet4, team_name, filename)  
   
    
    #---------------------------------------------------
    #Duquesne
    #-----------------
    team_name = "Duquesne University-AM"
    short = "Duquesne"
    duq_team={}
    duq_path = "Atlantic10_Season2015/WDuquesneResults/"
    
    #HY-TEK files    
    txt_file1 = duq_path + "Duq_LaSalleStBona.txt"
    team_meet1 = read_in_txt(txt_file1, duq_team, team_name)
    csv_file2 = duq_path + "Duq_Marshall.txt"
    team_meet2 = read_in_txt(csv_file2, team_meet1, team_name)
    csv_file3 = duq_path + "Duq_StFrancis.txt"
    team_meet3 = read_in_txt(csv_file3, team_meet2, team_name) 
    #csv_file4 = duq_path + "Duq_StMarys.txt"
    #team_meet4 = pdf_txt_meet.read_in_csvtxt(csv_file4, team_meet3, team_name)    
    
    write_to_csv(team_meet3, team_name, filename)      
    
  
    #---------------------------------------------------
    #Fordham
    #-----------------
    team_name = "Fordham-MR"
    short = "Fordham"
    ford_team={}
    ford_path = "Atlantic10_Season2015/WFordhamResults/"    
    #HY-TEK files    
    txt_file1 = ford_path + "Ford_Iona.txt"
    team_meet1 = read_in_txt(txt_file1, ford_team, team_name)
    #print team_meet1
    csv_file2 = ford_path + "Ford_Marist.txt"
    team_meet2 = read_in_txt(csv_file2, team_meet1, team_name)
    #print team_meet2
    csv_file3 = ford_path + "Ford_UConn.txt"
    team_meet3 = read_in_txt(csv_file3, team_meet2, team_name) 
    #print team_meet3
    csv_file4 = ford_path + "Ford_UMass.txt"
    team_meet4 = read_in_txt(csv_file4, team_meet3, team_name)    
   
    write_to_csv(team_meet4, team_name, filename)      
    
    
    #---------------------------------------------------
    #LaSalle
    #-----------------
    team_name = "La Salle-MA"
    short = "La Salle"
    ls_team={}
    ls_path = "Atlantic10_Season2015/WLaSalleResults/"
    
    #HY-TEK files    
    txt_file1 = ls_path + "LS_Duq_Bona.txt"
    team_meet1 = read_in_txt(txt_file1, ls_team, team_name)
    #print team_meet1
    txt_file2 = ls_path + "LS_FordRich.txt"
    team_meet2 = read_in_txt(txt_file2, team_meet1, team_name)
    txt_file3 = ls_path + "LS_GM.txt"
    team_meet3 = read_in_txt(txt_file3, team_meet2, team_name) 
    txt_file4 = ls_path + "LS_Penn.txt"
    team_meet4 = read_in_txt(txt_file4, team_meet3, team_name)    
    
    write_to_csv(team_meet4, team_name, filename)       
    
    #---------------------------------------------------
    #Rhode Island
    #-----------------
    team_name = "Rhode Island-NE"
    short = "Rhode Island-NE"
    ri_team={}
    ri_path = "Atlantic10_Season2015/WRhodeIslandResults/"
    
    #HY-TEK files    
    txt_file1 = ri_path + "RI_Providence.txt"
    team_meet1 = read_in_txt(txt_file1, ri_team, team_name)
       
    csv_file2 = ri_path + "RI_Maine.txt"
    team_meet2 = pdf_txt_meet.read_in_csvtxt(csv_file2, team_meet1, team_name)    
    csv_file3 = ri_path + "RI_Vermont.txt"
    team_meet3 = pdf_txt_meet.read_in_csvtxt(csv_file3, team_meet2, team_name)    
    csv_file4 = ri_path + "RI_Wagner.txt"
    team_meet4 = pdf_txt_meet.read_in_csvtxt(csv_file4, team_meet3, team_name)    
    write_to_csv(team_meet4, team_name, filename)
    
    #---------------------------------------------------
    #StBonaventure
    #-----------------
    team_name = "St. Bonaventure-NI"
    short = "St. Bonaventure-NI"
    sb_team={}
    sb_path = "Atlantic10_Season2015/WStBonaResults/"
    
    #HY-TEK files    
    txt_file1 = sb_path + "Duq_LaSalleStBona.txt"
    team_meet1 = read_in_txt(txt_file1, sb_team, team_name)
    #print team_meet1
    txt_file2 = sb_path + "SB_Binghamton.txt"
    team_meet2 = read_in_txt(txt_file2, team_meet1, team_name)
    #print team_meet2
    txt_file3 = sb_path + "SB_Colgate.txt"
    team_meet3 = read_in_txt(txt_file3, team_meet2, team_name)
    #print team_meet3
    txt_file4 = sb_path + "SB_Niagara.txt"
    team_meet4 = read_in_txt(txt_file4, team_meet3, team_name)
    #print team_meet4    
    write_to_csv(team_meet4, team_name, filename)  
    
    #---------------------------------------------------
    #StLouis
    #-----------------
    team_name = "SLU-OZ"
    short = "SLU-OZ"
    sl_team={}
    sl_path = "Atlantic10_Season2015/WStLouisResults/"
    
    #HY-TEK files    
    txt_file1 = sl_path + "SL_Bona&Duq&LS.txt"
    team_meet1 = read_in_txt(txt_file1, sl_team, team_name)
    #print len(team_meet1.keys()  )
    txt_file2 = sl_path + "SL_Evansville.txt"
    team_meet2 = read_in_txt(txt_file2, team_meet1, team_name)
    #print len(team_meet2)   
    txt_file3 = sl_path + "SL_Truman.txt"
    team_meet3 = read_in_txt(txt_file3, team_meet2, team_name)    
    #print len(team_meet3)
    #PDF to txt files
    csv_file4 = sl_path + "SL_Ark&HSU.txt"
    team_meet4 = pdf_txt_meet.read_in_csvtxt(csv_file4, team_meet3, team_name)    
    
    write_to_csv(team_meet4, team_name, filename) 
    
    #---------------------------------------------------
    #UMass
    #-----------------
    team_name = "Massachusetts-NE"
    short = "Massachusetts"
    um_team={}
    um_path = "Atlantic10_Season2015/WUMassResults/"
    
    #HY-TEK files    
    txt_file1 = um_path + "UMass_Brown.txt"
    team_meet1 = read_in_txt(txt_file1, um_team, team_name)
    #print len(team_meet1.keys()  )
    txt_file2 = um_path + "UMass_Bryant.txt"
    team_meet2 = read_in_txt(txt_file2, team_meet1, team_name)
    #print len(team_meet2)    
    txt_file3 = um_path + "UMass_BU.txt"
    team_meet3 = read_in_txt(txt_file3, team_meet2, team_name)
    #print len(team_meet2) 
    write_to_csv(team_meet3, team_name, filename) 
    return

if __name__ == "__main__":
    main()