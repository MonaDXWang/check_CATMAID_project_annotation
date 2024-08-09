import re

# Function to clean neuron names
def clean_name(name):
    # Remove anything after the first dot
    name = re.split(r'\.', name)[0]
    # Remove anything after the first dot
    name = re.split(r'\_', name)[0]
    # Remove square brackets
    name = re.sub(r'[\[\]\!\?]', '', name)
    return name.strip()

def nclass(n):
    if n in (
        'AVG', 'DVC', 'PVR', 'PVT', 'RIH', 'RIR', 'DVA', 'AQR', 'AVM', 'PQR',
        'PVM', 'DVB', 'PDA', 'PDB', 'ALA', 'AVL', 'RID', 'RIS',
        'I3', 'I4', 'I5', 'I5', 'M1', 'M4', 'M5', 'MI'
    ):
        return n
    if n in (
        'PVNL', 'PVNR','PVNL_or_R_1','PVNL_or_R_2','PVNL_or_R_3','PVNLorR'
    ):
        return 'PVN'
    if n in (
        'RICL', 'RICR', 'RICRa', 'RICRp'
    ):
        return 'RIC'
    if len(n) == 4 and n[-1] in 'LR' and n[:3] in (
        'ADA', 'ADE', 'ADF', 'ADL', 'AFD', 'AIA', 'AIB', 'AIM', 'AIN', 'AIY',
        'AIZ', 'ALM', 'ALN', 'ASE', 'ASG', 'ASH', 'ASI', 'ASJ', 'ASK', 'AUA',
        'AVA', 'AVB', 'AVD', 'AVE', 'AVF', 'AVH', 'AVJ', 'AVK', 'AWA', 'AWB',
        'AWC', 'BAG', 'BDU', 'CAN', 'FLP', 'GLR', 'HSN', 'IL1', 'IL2', 'LUA',
        'OLL', 'PDE', 'PHA', 'PHB', 'PHC', 'PLM', 'PLN', 'PVC', 'PVD', 
        'PVP', 'PVQ', 'PVW', 'RIA', 'RIB', 'RIF', 'RIG', 'RIM', 'RIP',
        'RIV', 'RMD', 'RMF', 'RMG', 'RMH', 'SDQ', 'URB', 'URX'
    ):
        return n[:3]
    if len(n) == 5 and n[-2:] in ('DL', 'DR', 'VL', 'VR') and n[:3] in (
        'CEP', 'GLR', 'IL1', 'IL2', 'OLQ', 'RMD', 'SAA', 'SIA', 'SIB', 'SMB',
        'SMD', 'URA', 'URY'
    ):
        return n[:3]
    if len(n) == 8 and re.match('BWM-[DV][LR]0[0-8]', n):
        return 'BWM' + n[-2:]
    if n in (
        'RMED', 'RMEL', 'RMER', 'RMEV', 'SABD', 'SABVL', 'SABVR',
    ):
        return n[:3]
    if n in (
        'CEPshDL', 'CEPshDR', 'CEPshVL', 'CEPshVR'
    ):
        return n[:5]
    if n[:2] in ('AS', 'VB', 'VA', 'VD') and n[2:] in map(str, range(12)):
        return n[:2] + 'n'
    if n in ('VA12', 'VD12', 'VD13'):
        return n[:2] + 'n'
    if re.match('^(DA[1-9])|(DB[1-7])|(DD[1-6])|(VC[1-6])$', n):
        return n[:2] + 'n'

    return n


def npair(n):
    if n in (
        'AVG', 'DVC', 'PVR', 'PVT', 'RIH', 'RIR', 'DVA', 'AQR', 'AVM',
        'PQR', 'IL1', 'IL2', 'RMD', 'RME', 'SAB',
        'PVM', 'DVB', 'PDA', 'PDB', 'ALA', 'AVL', 'RID', 'RIS',
        'I3', 'I4', 'I5', 'I5', 'M1', 'M4', 'M5', 'MI',
        'SABD', 'excgl'
    ):
        return n
    cls = nclass(n)
    if cls in (
        'ADA', 'AIA', 'AIB', 'AIN', 'AIY', 'AIZ', 'BDU', 'LUA', 'PVN', 'PVP',
        'PVW', 'RIA', 'RIB', 'RIF', 'RIG', 'RIM', 'RIP', 'AVA', 'AVD', 'AVE',
        'AVB', 'PVC', 'ADL', 'AFD', 'ASE', 'ASG', 'ASH', 'ASI', 'ASJ', 'ASK',
        'AUA', 'AWA', 'AWB', 'AWC', 'BAG', 'FLP', 'OLL', 'URB', 'RMG', 'PDE',
        'ALM', 'ALN', 'PHA', 'PHB', 'PHC', 'PLM', 'PLN', 'PVD', 'SDQ', 'RIV',
        'RMF', 'RMH', 'AIM', 'AVF', 'AVH', 'AVJ', 'AVK', 'PVQ', 'RIC', 'ADE',
        'ADF', 'HSN', 'URX',
        'I1', 'I2', 'M2', 'M3', 'MC', 'NSM',
        'CAN'
    ):
        return cls
    if cls in (
        'ASn', 'DAn', 'DBn', 'DDn', 'VAn', 'VBn', 'VCn', 'VDn'
    ):
        return n
    if cls in (
        'SAA', 'URY', 'SMB', 'SMD', 'URA', 'SIB', 'SIA', 'CEP', 'OLQ',
        'CEPsh'
    ):
        return n[:-1]
    if n[:-1] in (
        'SABV', 'IL1D', 'IL1V', 'IL2D', 'IL2V', 'RMDD', 'RMDV', 'GLRD',
        'GLRV',
    ):
        return n[:-1]
    if n in (
        'IL1L', 'IL1R', 'IL2L', 'IL2R', 'RMDL', 'RMDR', 'GLRL', 'GLRR',
        'RMEL', 'RMER'
    ):
        return n[:3] + 'L/R'
    if n in ('RMED', 'RMEV'):
        return 'RMED/V'

    if len(n) == 8 and re.match('BWM-[DV][LR]0[0-8]', n):
        return 'BWM' + n[-2:] + n[4]

    print(n, 'is not a valid cell?')

    return n