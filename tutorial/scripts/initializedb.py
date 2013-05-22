#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    Page,
    Author,
    Book,
    Question,
    Answer,
    Alias,
    Base,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        model = Page('FrontPage', 'This is the front page')
        DBSession.add(model)
        author1 = Author(u'横溝正史', u'よこみぞせいし')
        DBSession.add(author1)
        book1 = Book(1, u'獄門島', 1)
        book2 = Book(1, u'八つ墓村', 0)
        DBSession.add_all([book1, book2])
        question1 = Question('', 0)
        answer1 = Answer(1, u'荒木村長')
        answer2 = Answer(1, u'了然和尚')
        answer3 = Answer(1, u'漢方医幸庵')
        DBSession.add_all([question1])
        DBSession.add_all([answer1, answer2, answer3])
        alias1 = Alias(1, u'村長')
        alias2 = Alias(2, u'和尚')
        alias3 = Alias(3, u'村医者')
        DBSession.add_all([alias1, alias2, alias3])

