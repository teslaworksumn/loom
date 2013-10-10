from flask import Flask, request, url_for, render_template, flash, redirect, abort
from jinja2 import evalcontextfilter, Markup, escape
from flask_mail import Mail, Message
from raven.contrib.flask import Sentry, Client
import config
import re
import strings

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.url_map.strict_slashes = False
app.config.update(config.APP_CONFIG)

app.config.update(config.MAIL_SETTINGS)
mail = Mail(app)

app.config.update(config.SENTRY_SETTINGS)
sentry = Sentry(app)

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n') \
        for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', mixpanel_token=mixpanel_token()), 404

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', form={}, errors={}, mixpanel_token=mixpanel_token())

    form = request.form
    errors = {}

    if not form['email']:
        errors['email'] = strings.ERROR_NO_EMAIL_TO_GET_AHOLD
    
    if not form['report']:
        errors['report'] = strings.ERROR_NO_REPORT

    if not errors:
        subject = strings.SUBJ_REPORT
        msg = Message(subject)
        msg.add_recipient(email_address(config.CONTACT_EMAIL))
        msg.html = render_template('mail/report.html', form=form)
        msg.body = render_template('mail/report.txt', form=form)
        
        mail.send(msg)

        flash(strings.SUCCESS_REPORT_SUBMITTED, 'success')
        return redirect(url_for('index'))

    flash(strings.ERROR_NOT_SUBMITTED, 'danger')
    return render_template('index.html', form=form, errors=errors, mixpanel_token=mixpanel_token())

def mixpanel_token():
    if config.MIXPANEL_SUPPRESS_SEND:
        return None

    return config.MIXPANEL_TOKEN

def redirect_url():
    return request.args.get('next') or request.referrer or url_for('index')

def email_address(email):
    if app.debug or app.testing:
        return config.DEBUG_EMAIL
    
    return email


if __name__ == '__main__':
    app.run()
