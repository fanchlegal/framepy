from kalapy import web
from kalapy import db
from kalapy.db import Q
from kalapy.web import request

@web.route('/Spacial:Help')
def help():
    return web.redirect('http://docutils.sourceforge.net/docs/user/rst/quickstart.html')

@web.route('/search')
def search():
    q = request.args.get('q', '')
    revisions = None
    if q.strip():
        Revision = db.get_model('wiki:revision')
        query = Revision.all().filter(Q('text =', '%'+q+'%')|Q('note =', '%'+q+'%'))
        revisions = query.fetchall()
    return web.render_template('search.html', revisions=revisions)
