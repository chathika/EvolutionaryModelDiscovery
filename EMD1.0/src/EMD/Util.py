import re
def netLogoEMDLineToArray(netlogoEMDLine):
    netlogoEMDLine = netlogoEMDLine.lower()
    if "@emd" in netlogoEMDLine:
        return re.sub("[\s;]","",netlogoEMDLine).split("@")
    else:
        print("Not and EMD annotated line!")