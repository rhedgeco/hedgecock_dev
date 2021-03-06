import os
from pathlib import Path
from sanic import Sanic, response

import routing.ice_cream_or_pickle.ice_cream_or_pickle as ice_cream_or_pickle


def add_routes(app: Sanic):
    # create handler for index route
    home_index = Path('./home_index')

    async def index(request):
        return await response.file(str(home_index / 'index.html'))

    async def favicon(request):
        return await response.file(str(home_index / 'favicon.ico'))

    app.static('/static', str(home_index / 'static'))
    app.add_route(index, '/')
    app.add_route(favicon, '/favicon.ico')

    # Ice cream or pickle
    app.add_route(ice_cream_or_pickle.IceCreamOrPickle.as_view(),
                  '/ice_cream_or_pickle')

    # IFTTT testing routes
    @app.route('/test_api/ifttt/v1/status', methods=['GET'])
    def ifttt_status(request):
        headers = request.headers
        channel_key = headers['ifttt-channel-key']

        r = response.text('ONLINE!')
        if channel_key != os.environ.get('IFTTT_SERVICE_KEY'):
            r = response.text('ERROR!')
            r.status = 401

        return r
