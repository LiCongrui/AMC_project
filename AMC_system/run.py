# -*- coding: utf-8 -*-

from optparse import OptionParser

from AMC import create_app

optparser = OptionParser()
optparser.add_option('-p', '--port', dest='port', help='Server Http Port Number', default=9001, type='int')
(options, args) = optparser.parse_args()

app = create_app()
app.run(debug=True)
