from field_config_points import *

# [up, down, left, right]
relation = {
    p1: [None, p7, None, p2],
    p2: [None, p8, p1, p3],
    p3: [None, p10, p2, None],
    p4: [None, p11, None, p5],
    p5: [None, p13, p4, p6],
    p6: [None, p14, p5, None],
    p7: [p1, p15, None, p8],
    p8: [p2, p16, p7, p9],
    p9: [None, p17, p8, p10],
    p10: [p3, None, p9, p11],
    p11: [p4, None, p10, p12],
    p12: [None, p20, p11, p13],
    p13: [p5, p21, p12, p14],
    p14: [p6, p22, p13, None],
    p15: [p7, None, None, p16],
    p16: [p8, p28, p15, None],
    p17: [p9, None, None, p18],
    p18: [None, p24, p17, None],
    p19: [None, p26, None, p20],
    p20: [p12, None, p19, None],
    p21: [p13, p34, None, p22],
    p22: [p14, None, p21, None],
    p23: [None, p29, None, p24],
    p24: [p18, None, p23, p25],
    p25: [None, p31, p24, p26],
    p26: [p19, None, p25, p27],
    p27: [None, p33, p26, None],
    p28: [p16, p38, p70, p29],
    p29: [p23, p35, p28, None],
    p30: [None, None, None, p31],
    p31: [p35, None, p30, p32],
    p32: [None, None, p31, None],
    p33: [p27, p36, None, p34],
    p34: [p21, p43, p33, p71],
    p35: [p29, p39, None, p36],
    p36: [p33, p42, p35, None],
    p37: [None, p45, None, p38],
    p38: [p28, p47, p37, p39],
    p39: [p35, None, p38, p40],
    p40: [None, p49, p39, None],
    p41: [None, p50, None, p42],
    p42: [p36, None, p41, p43],
    p43: [p34, p52, p42, p44],
    p44: [None, p53, p43, None],
    p45: [p37, None, None, p46],
    p46: [None, p55, p45, None],
    p47: [p38, p56, None, p48],
    p48: [None, p57, p47, p49],
    p49: [p40, None, p48, p50],
    p50: [p41, None, p49, p51],
    p51: [None, p60, p50, p52],
    p52: [p43, p61, p51, None],
    p53: [p44, None, p68, None],
    p54: [None, p64, None, p55],
    p55: [p46, None, p54, p56],
    p56: [p47, None, p55, None],
    p57: [p48, None, None, p58],
    p58: [None, p65, p57, None],
    p59: [None, p66, None, p60],
    p60: [p51, None, p59, None],
    p61: [p52, None, None, p62],
    p62: [p68, None, p61, p63],
    p63: [None, p67, p62, None],
    p64: [p54, None, None, p65],
    p65: [p58, None, p64, p66],
    p66: [p59, None, p65, p67],
    p67: [p63, None, p66, None],
    p68: [None, p62, None, p53],
    p69: [None, None, p72, p70],
    p70: [None, None, p69, p28],
    p71: [None, None, p34, p72],
    p72: [None, None, p71, p69]
}

# Corners which are the ends of intervals where loot is not set
no_loot_corners = [p69, p70, p71, p72,
                   p23, p24, p25, p26, p27, p29, p30, p31, p32, p33, p35, p36]

# Between these points pacman is initiated
pacman_start_interval = [p49, p50]

# By these rules teleportation is done
teleport = {
    p69: p71,
    p72: p70
}


