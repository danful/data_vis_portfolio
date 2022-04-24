"""
Define variables which are used across the various scripts
"""

RENAME_DICT = {
    'Water supply; sewerage, waste management and remediation activities' : 'Utilities - water',
    'Wholesale and retail trade; repair of motor vehicles and motorcycles' : 'Wholesale and retail trade',
    'Public administration and defence; compulsory social security' : 'Public administration and defence',
    'Electricity, gas, steam and air conditioning supply' : 'Utilities - electricity and gas',
    'Agriculture, forestry and fishing' : 'Farming',
    'Arts, entertainment and recreation; other service activities' : 'Entertainment and recreation',
    'Arts, entertainment and recreation' : 'Entertainment and recreation'
}

DROP_COLS = [
    'Activities of households as employers; undifferentiated goods and services-producing activities of households for own use',
    'Consumer expenditure'
]

COLOUR_DICT = {
    'Construction' : '#6a3d9a',
    'Utilities - electricity and gas' : '#1f78b4',
    'Manufacturing' : '#fb9a99',
    'spare' : '#33a02c',
    'Farming' : '#b2df8a',
    'Transport and storage' : '#e31a1c',
    'Mining and quarrying' : '#fdbf6f',
    'Utilities - water' : '#ff7f00',
    'Wholesale and retail trade' : '#cab2d6',
    'Other' : '#a6cee3'
}