IGNORED_NAMED_ENTITY = [
   "AGPL",
   "Cube License"
]


copyright_statement_markers = (
    '©',
    '(c)',
    # C sign in Restructured Text:
    '|copy|',
    '&#169',
    '&#xa9',
    '169',
    'xa9',
    'u00a9',
    '00a9',
    '\251',
    # have copyright but also (c)opyright and ©opyright
    'opyr',
    # have copyright but also (c)opyleft
    'opyl',
    'copr',
    'right',
    'reserv',
    'auth',
    'filecontributor',
    'devel',
    '<s>',
    '</s>',
    '<s/>',
    'by ',  # note the trailing space
    # common for emails
    '@',
)