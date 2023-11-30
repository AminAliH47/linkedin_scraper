from time import time

LINKEDIN_AUTHENTICATION_COOKIES = [
    {'name': 'lang', 'value': 'v=2&lang=en-us', 'domain': '.linkedin.com', 'path': '/', 'expires': -1,
     'httpOnly': False, 'secure': True, 'sameSite': 'None'},
    {'name': 'AMCV_14215E3D5995C57C0A495C55%40AdobeOrg',
     'value': '-637568504%7CMCIDTS%7C19692%7CvVersion%7C5.1.1', 'domain': '.linkedin.com', 'path': '/',
     'expires': 1716925538, 'httpOnly': False, 'secure': False, 'sameSite': 'None'},
    {'name': 'li_rm',
     'value':
     'AQEGC1VEnJ3aKAAAAYwhw-ZHcWHlG1Smy8hw1HvCSV6ZiONzUoL6m6zM7iPiJ7a9_y2sqjNSDUcXnGyP06SZzOd46I-6yv1jeCSFkpIMO12C-Ym_F4UBYbiH',
     'domain': '.www.linkedin.com', 'path': '/',
     'expires': 1732909539, 'httpOnly': True,
     'secure': True,
     'sameSite': 'None'},
    {'name': 'li_at',
     'value':
     'AQEDATSvI-sB0g-7AAABjCHD9XYAAAGMRdB5dk0AP-3BnTPyX5KK-0rcqwrSBXZaI08sFByO6TCehIhabnYm_JnERhmlmEa7LgH0w3yJZtXRi875TRDzVbs89L7DRKZk51EiJ9_ADn8U1PIWUDnuO-c9',
     'domain': '.www.linkedin.com', 'path': '/',
     'expires': 1732909539, 'httpOnly': True,
     'secure': True, 'sameSite': 'None'},
    {'name': 'liap', 'value': 'true', 'domain': '.linkedin.com',
     'path': '/', 'expires': 1709149539,
     'httpOnly': False, 'secure': True, 'sameSite': 'None'},
    {'name': 'JSESSIONID', 'value': '"ajax:0782053775527920009"',
     'domain': '.www.linkedin.com', 'path': '/',
     'expires': 1709149539, 'httpOnly': False, 'secure': True,
     'sameSite': 'None'},
    {'name': 'bcookie', 'value': '"v=2&2ea2e7f0-d15b-4a98-8132-9658e6f6849c"',
     'domain': '.linkedin.com',
     'path': '/', 'expires': 1732909539, 'httpOnly': False,
     'secure': True, 'sameSite': 'None'},
    {'name': 'bscookie',
     'value': '"v=1&2023113019453520bfbe87-9af8-4c05-8a78-8fb43baae038AQHHqeVTx4KRYr37X7mTYb7vQgO5av1u"',
     'domain': '.www.linkedin.com', 'path': '/',
     'expires': 1732909539, 'httpOnly': True, 'secure': True,
     'sameSite': 'None'},
    {'name': 'lidc',
     'value':
     '"b=VB27:s=V:r=V:a=V:p=V:g=5428:u=147:x=1:i=1701373540:t=1701375200:v=2:sig=AQFT0oDXq8s1OM30AvkUAkgpL4c0FK8f"',
     'domain': '.linkedin.com', 'path': '/', 'expires': time() + 1000,
     'httpOnly': False, 'secure': True,
     'sameSite': 'None'}
]
