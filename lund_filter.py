


def vec_subtract(vec1,vec2):
    res = tuple(map(lambda i, j: i - j, vec1, vec2)) 
    return res

def vec_add(vec1,vec2):
    res = tuple(map(lambda i, j: i + j, vec1, vec2)) 
    return res

def calc_inv_mass_squared(four_vector):
    fv = four_vector
    inv_mass2 = fv[0]**2-fv[1]**2-fv[2]**2-fv[3]**2
    return inv_mass2

e_mass = 0.000511
Ebeam_4mom = (10.6,0,0,10.6)

filename = "lunds/lunder.txt"


f = open(filename, "r")
for x in range(5,10):
    a = f.readline()
    print(a)
    print(type(a))


"""with open(filename,"r") as f:
        for count,line in enumerate(f):
            #ic(line)
            #print(f[1])
            line_str = str(line)
            #ic(line_str[1])
            #print(line)
            if line_str[1] is not ' ': #LUND format has the number of particles in the second character of a header
                #event_ind += 1
                print(count)
                #values = [event_ind,]
                #events.append([])
                
                #cols = line.split()  
                #for ind, val in enumerate(cols):
                #    values.append(float(val))
                #print(values)
                #events[event_ind].append(values)
            
                #print(events)
                ###Write to header
            else:
                values = []
                #print("particle content")
                cols = line.split()
                #print(cols[3])
                if cols[3]=='11':
                    e_4mom = (float(cols[9]),float(cols[6]),float(cols[7]),float(cols[8]))
                    Q2 = -1*calc_inv_mass_squared(vec_subtract(Ebeam_4mom,e_4mom))
                    if Q2>0.99:
                        print(Q2)
                        print(count)
                        #print(str(f[count+1])[1])


                        #with open("new_file.txt", "w") as new_f:
                        #for line in lines:        
                        #new_f.write(line)
                #for ind, val in enumerate(cols):
                #    values.append(float(val))
                #events[event_ind].append(values)
"""

lund_particle_labels = ["sub_index",
    "lifetime",
    "type_1active",
    "particleID",
    "ind_parent",
    "ind_daughter",
    "mom_x",
    "mom_y",
    "mom_z",
    "E_GeV",
    "Mass_GeV",
    "Vx",
    "Vy",
    "Vz"]