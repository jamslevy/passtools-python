import flask
import os, sys
from datetime import datetime
try:
    import simplejson as json
except ImportError:
    import json

import passtools


app = flask.Flask(__name__)

API_KEY = '3384f7e5-e195-4c2f-94ac-5a1c7ae37b33'

"""
	Template Views 
"""

@app.route('/')
def templates():
	context = { 'page': 'templates' }
	pt_service = passtools.Service(API_KEY)
	context['templates'] = pt_service.list_templates()
	return flask.render_template('templates.html', **context)

@app.route('/template/<int:template_id>')
def template(template_id):
	context = { 'page': 'template' }
	pt_service = passtools.Service(API_KEY)
	context['template'] = pt_service.get_template(template_id)
	return flask.render_template('template.html', **context)

@app.route('/template/<int:template_id>/delete')
def delete_template(template_id):
	pt_service = passtools.Service(API_KEY)
	pt_service.delete_template(template_id)
	return flask.redirect('/')


"""
	Pass Views 
"""

@app.route('/passes')
def passes():
	context = { 'page': 'passes' }
	pt_service = passtools.Service(API_KEY)
	context['passes']  = pt_service.list_passes()
	context['api_key'] = pt_service.api_client.api_key
	return flask.render_template('passes.html', **context)

@app.route('/pass/<int:pass_id>')
def pt_pass(pass_id):
	context = { 'page': 'pass' }
	pt_service = passtools.Service(API_KEY)
	context['pt_pass'] = pt_service.get_pass(pass_id)
	return flask.render_template('pass.html', **context)

@app.route('/template/<int:template_id>/pass')
def create_pass(template_id):
	pt_service = passtools.Service(API_KEY)
	pass_template = pt_service.get_template(template_id) # TODO: this shouldn't be necessary
	new_pass  = pt_service.create_pass(template_id, template_fields_model=pass_template.fields_model)
	return flask.redirect('/pass/%s' % new_pass.pass_id)	

@app.route('/pass/<int:pass_id>/update')
def update_pass(pass_id):
	pt_service = passtools.Service(API_KEY)
	update_fields = json.loads(flask.request.args.get('fields'))
	pt_service.update_pass(pass_id, update_fields)
	pt_service.push_pass(pass_id)
	return flask.redirect('/pass/%s' % pass_id)	

@app.route('/pass/<int:pass_id>/delete')
def delete_pass(pass_id):
	pt_service = passtools.Service(API_KEY)
	pt_service.delete_pass(pass_id)
	return flask.redirect('/')	


"""
	Custom Template Filters
"""

@app.template_filter()
def timesince(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

    now = datetime.utcnow()
    diff = now - dt
    
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        
        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)

    return default

@app.template_filter()
def pretty_dict(d, indent=4):
	return json.dumps(d, sort_keys=True, indent=indent).replace('\n','<br/>').replace(' ','&nbsp;')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
