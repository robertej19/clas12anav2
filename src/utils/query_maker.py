from icecream import ic

def make_query(vars,lims):

    comp_str = ""
    for i,var in enumerate(vars):
        comp = "{} > {} & {} <= {}".format(var,lims[2*i],var,lims[2*i+1])
        comp_str += comp
        if i<len(vars)-1:
            comp_str += " & "

    return comp_str

if __name__ == "__main__":
    vars = ['xB','Q2','t']
    lims = [0.3,0.4,3,4,.45,0.5]
    print(make_query(vars,lims))