SECRET_KEY = 'YOUR_SECRET_KEY'
MIXPANEL_TOKEN = 'YOUR_MIXPANEL_TOKEN'
MIXPANEL_SUPPRESS_SEND = True

CONTACT_EMAIL = 'operator@exceed.umn.edu'
DEBUG_EMAIL = 'webmaster@exceed.umn.edu'

APP_CONFIG = {
  'DEBUG': False,
  'TESTING': False
}

MAIL_SETTINGS = {
  'MAIL_SERVER': 'smtp.mailgun.org',
  'MAIL_PORT': '25',
  'MAIL_USE_TLS': False,
  'MAIL_USERNAME': 'postmaster@exceed.umn.edu',
  'MAIL_PASSWORD': 'your-mailer-password',
  'MAIL_DEFAULT_SENDER': 'loom@exceed.umn.edu',
  'MAIL_SUPPRESS_SEND': True
}

SENTRY_SETTINGS = {
  'SENTRY_DSN': 'http://1234:5678@your-sentry-dsn.umn.edu/773'
}
