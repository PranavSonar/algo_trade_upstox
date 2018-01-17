from math import ceil


def calculate_pivot_points(high, low, close):
    global pp_pp
    pp_pp=ceil((high+low+close) /3)
    global pp_r1
    pp_r1= ceil(2*pp_pp - low)
    global pp_r2
    pp_r2= ceil(pp_pp+(high-low))
    global pp_r3
    pp_r3= ceil(high + 2*(high-low))
    global pp_s1
    pp_s1= ceil(2*pp_pp-high)
    global pp_s2
    pp_s2= ceil(pp_pp-(high-low))
    global pp_s3
    pp_s3= ceil(pp_pp - 2*(high-low))
    pivots = {}
    pivots['pp_pp'] = pp_pp
    pivots['pp_r1'] = pp_r1
    pivots['pp_r2'] = pp_r2
    pivots['pp_r3'] = pp_r3
    pivots['pp_s1'] = pp_s1
    pivots['pp_s2'] = pp_s2
    pivots['pp_s3'] = pp_s3
    return pivots

