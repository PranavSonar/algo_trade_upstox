
def calculate_pivot_points(high, low, close):
    global pp_pp
    pp_pp=(high+low+close) /3
    global pp_r1
    pp_r1= 2*pp_pp - low
    global pp_r2
    pp_r2= pp_pp+(high-low)
    global pp_r3
    pp_r3= high - 2*(pp_pp-low)
    global pp_s1
    pp_s1= 2*pp_pp-high
    global pp_s2
    pp_s2= pp_pp-(high-low)
    global pp_s3
    pp_s3= low - (high-pp_pp)
    print pp_pp
    print pp_r1
    print pp_r2
    print pp_r3
    print pp_s1
    print pp_s2
    print pp_s3

calculate_pivot_points(10476,10412,10471)
