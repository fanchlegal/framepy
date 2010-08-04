from kalapy import web

@web.route('/fox')
def fox():
    return 'FOo eXtended'

@web.route('/foox')
def foox():
    return 'FOO eXtended'
