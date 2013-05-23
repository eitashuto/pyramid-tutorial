#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from docutils.core import publish_parts

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.view import (
    view_config,
    forbidden_view_config,
    )

from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
    )

from .models import (
    DBSession,
    Page,
    Author,
    Book,
    Question,
    Answer,
    Alias,
    )

from .security import USERS

import json
from .database_util import AlchemyEncoder
   
# regular expression used to find WikiWords
wikiwords = re.compile(r"\b([A-Z]\w+[A-Z]+\w+)")

@view_config(route_name='view_wiki',
             permission='view')
def view_wiki(request):
    return HTTPFound(location = request.route_url('books',))

@view_config(route_name='view_page', renderer='templates/view.pt',
             permission='view')
def view_page(request):
    pagename = request.matchdict['pagename']
    page = DBSession.query(Page).filter_by(name=pagename).first()
    if page is None:
        return HTTPNotFound('No such page')

    def check(match):
        word = match.group(1)
        exists = DBSession.query(Page).filter_by(name=word).all()
        if exists:
            view_url = request.route_url('view_page', pagename=word)
            return '<a href="%s">%s</a>' % (view_url, word)
        else:
            add_url = request.route_url('add_page', pagename=word)
            return '<a href="%s">%s</a>' % (add_url, word)

    content = publish_parts(page.data, writer_name='html')['html_body']
    content = wikiwords.sub(check, content)
    edit_url = request.route_url('edit_page', pagename=pagename)
    return dict(page=page, content=content, edit_url=edit_url,
                logged_in=authenticated_userid(request))

@view_config(route_name='add_page', renderer='templates/edit.pt',
             permission='edit')
def add_page(request):
    pagename = request.matchdict['pagename']
    if 'form.submitted' in request.params:
        body = request.params['body']
        page = Page(pagename, body)
        DBSession.add(page)
        return HTTPFound(location = request.route_url('view_page',
                                                      pagename=pagename))
    save_url = request.route_url('add_page', pagename=pagename)
    page = Page('', '')
    return dict(page=page, save_url=save_url,
                logged_in=authenticated_userid(request))

@view_config(route_name='edit_page', renderer='templates/edit.pt',
             permission='edit')
def edit_page(request):
    pagename = request.matchdict['pagename']
    page = DBSession.query(Page).filter_by(name=pagename).one()
    if 'form.submitted' in request.params:
        page.data = request.params['body']
        DBSession.add(page)
        return HTTPFound(location = request.route_url('view_page',
                                                      pagename=pagename))
    return dict(
        page=page,
        save_url = request.route_url('edit_page', pagename=pagename),
        logged_in=authenticated_userid(request),
        )

@view_config(route_name='login', renderer='templates/login.pt')
@forbidden_view_config(renderer='templates/login.pt')
def login(request):
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        if USERS.get(login) == password:
            headers = remember(request, login)
            return HTTPFound(location = came_from,
                             headers = headers)
        message = 'Failed login'

    return dict(
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        login = login,
        password = password,
        )

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.route_url('view_wiki'),
                     headers = headers)

@view_config(route_name='books', renderer='templates/books.pt')
def books(request):
    return dict(book_titles = ["悪魔", "Bulls1", "Miami Heat"])

@view_config(route_name='books_info', renderer='json')
def books_info(request):
    #for r in request.params: print r
    hint = request.params['val_book_hint']
    if len(hint) == 0:
        return json.dumps({})

    book_list = []
    #authors = DBSession.query(Author).filter_by(name=hint).all()
    authors = DBSession.query(Author).filter(Author.name.like("%" + hint + "%")).all()
    for author in authors:
        books = DBSession.query(Book).filter_by(author_id=author.id).all()
        for book in books:
            book_list.append({"title": book.title, "id": book.id, "question_id": book.question_id,"author": author.name})
            
    
    #books = DBSession.query(Book).filter_by(title=hint).all()
    books = DBSession.query(Book).filter(Book.title.like("%" + hint + "%")).all()
    for book in books:
        author = DBSession.query(Author).filter_by(id=book.author_id).first()
        book_list.append({"title": book.title, "id": book.id, "question_id": book.question_id,"author": author.name})
            
    result = json.dumps(book_list)
    return result

@view_config(route_name='question', renderer='json')
def question(request):
    return {}
  
@view_config(route_name='check_answer', renderer='json')
def check_answer(request):
    question_id = request.params['question_id']
    input_answer = request.params['input_answer']

    # multiple delimiters do not work correctly for Japanese word
    input_answers = input_answer.split(u" ")
    input_answers = reduce(lambda a,b: a+b, map(lambda x: x.split(u"　"), input_answers), [])
    input_answers = reduce(lambda a,b: a+b, map(lambda x: x.split(u","), input_answers), [])
    
    correct = 0
    all_answers = DBSession.query(Answer).filter_by(question_id=question_id).all()
    print all_answers
    for input_answer in input_answers: 
        print input_answer
        for answer in all_answers:
            print answer.text
            if score_answer(answer, input_answer):
                correct += 1
                break
    
    result = {}
    result["result"] = correct == len(input_answers)
    result["correct"] = correct

    if result["result"]:
        print "NEXT"
        question = DBSession.query(Question).filter_by(id=question_id).first()
        result["next"] = DBSession.query(Question).filter_by(id=next).first().id if (question.next != 0) else 0
    
    return result

def score_answer(answer, input):
    if answer.text == input:
        return True
    
    all_aliases = DBSession.query(Alias).filter_by(answer_id=answer.id).all()
    for alias in all_aliases: 
        if input == alias.text:
            return True
    
    return False
    

        
