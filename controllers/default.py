# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    return dict(message=T('Hello World'))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id[
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs bust be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())


def form_for_artist():
	form = SQLFORM(db.artist)
	if form.accepts(request.vars, session):
	      response.flash = 'form accepted'
	elif form.errors:
	      response.flash = 'form has errors'
	else:
	      response.flash = 'please fill out the form'
	return dict(form=form)
	
def form_for_movie():
	form = SQLFORM(db.movie)
	if form.accepts(request.vars, session):
	      response.flash = 'form accepted'
	elif form.errors:
	      response.flash = 'form has errors'
	else:
	      response.flash = 'please fill out the form'
	return dict(form=form)

def form_for_song():
	form = SQLFORM(db.song)
	if form.accepts(request.vars, session):
	      response.flash = 'form accepted'
	elif form.errors:
	      response.flash = 'form has errors'
	else:
	      response.flash = 'please fill out the form'
	return dict(form=form)
@auth.requires_login()
def form_for_rating():
	form = SQLFORM(db.rating)
	if form.accepts(request.vars, session):
	      response.flash = 'form accepted'
	      k = request.vars.rating
	      n = request.vars.song
	      row = db(db.rating.song==n).select()
	      s=0
	      c=0
	      for i in row:
	        s=s+i.rating
	        c=c+1
	        s=s/c
	      rows = db(db.song.id==n).select()
	      row = rows[0]
	      row.update_record(rating = s)

	elif form.errors:
	      response.flash = 'form has errors'
	else:
	      response.flash = 'please fill out the form'
	return dict(form=form)

def form_for_user():
	form = SQLFORM(db.auth_user)
	if form.accepts(request.vars, session):
	      response.flash = 'form accepted'
	elif form.errors:
	      response.flash = 'form has errors'
	else:# utogenerated create and update forms.
# readable if a field is readable, it will be visible in readonly forms. If a fiel
	      response.flash = 'please fill out the form'
	return dict(form=form)

def query_form():
	form = SQLFORM.factory(
			Field('query_number','integer',requires = IS_INT_IN_RANGE(1,6))
			)
	if form.accepts(request.vars,session):
		redirect(URL('q'+request.vars.query_number))
	return dict(form=form)

def movie_artist_query():
	form = SQLFORM.factory(
			Field('movie_name','string'),
			Field('artist_name','string')
			)
        if form.accepts(request.vars,session):
		 if request.vars.movie_name == '' and request.vars.artist_name == '' :
		                 response.flash = 'please enter one field'
                 else:
			session.movie = request.vars.movie_name
	        	session.artist = request.vars.artist_name
		        redirect(URL('display_link'))
        return dict(form=form)

def display_link():
       if session.movie!='' and session.artist!='': 
	rows = db( ((db.song.movie == db.movie.id) & (db.movie.name==session.movie))&((db.song.singer == db.artist.id)&(db.artist.name==session.artist)) ).select()
       elif session.movie!='':
	 rows =db((db.song.movie==db.movie.id) & (db.movie.name == session.movie) ).select()
       else:
	  rows = db((db.song.singer == db.artist.id) & (db.artist.name == session.artist)).select()
       return dict(r = rows)
	  
def display_details():
	idno = request.vars.idno
	rows = db(db.song.id == idno).select()
	return dict(r=rows[0])

def q1():
	row = db((db.song.singer == db.artist.id) & (db.artist.id == 3)).select(db.song.name)
	return dict(r=row)

def q2():
	row = db((db.song.singer==db.artist.id) & (db.artist.name == "Balu")).select(db.song.name)
	return dict(r=row)

def q3():
	row = db(((db.song.singer == db.artist.id) & (db.artist.name == "Balu")) & ((db.song.movie == db.movie.id) & (db.movie.name=="Shankarabharanam"))).select(db.song.name)
	return dict(r=row)

def q4():
	row = db(((db.song.singer == db.artist.id) & (db.artist.name == "Balu")) & ((db.song.movie==db.movie.id) & (db.movie.release_date<datetime.date(2000,1,1)))).select(db.song.name,db.song.actor)
	return dict(r=row)

def q5():
	row=db((db.song.rating>=4) & (db.song.singer==db.artist.id)).select(db.song.name,db.artist.name)
	return dict(r=row)

def reset_state():
	db.artist.truncate()
	db.song.truncate()
	db.movie.truncate()
	db.rating.truncate()
        return dict(r="All Tables Successfully Cleared :D")
	
