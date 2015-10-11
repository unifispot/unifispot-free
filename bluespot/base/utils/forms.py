

def print_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
	for error in errors:
	    print "Error in the %s field - %s" % (getattr(form, field).label.text,error)

def get_errors(form):
    """ Return form errors as string """
    form_errors = ""
    for field, errors in form.errors.items():
        for error in errors:
            form_errors = form_errors+ "Error in the %s field - %s </br>" % (getattr(form, field).label.text,error)
    return form_errors
