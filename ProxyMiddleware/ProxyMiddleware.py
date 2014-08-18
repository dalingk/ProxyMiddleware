#!/usr/bin/env python
#
#  Kellen Fox
#  https://github.com/Kellel/ProxyMiddleware
#

from bottle import redirect, HTTPError, abort

class ReverseProxied(object):
    """
    Reverse Proxied
    ---------------

    Wrap a wsgi application such that the script name and path info are gleaned from the Nginx Reverse Proxy

    proxy_set_header X-SCRIPT-NAME /path;

    """

    def __init__(self, wrap_app):
        self.wrap_app = wrap_app
        self.wrap_app = self.app = wrap_app

    def __call__ (self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]
        return self.wrap_app(environ, start_response)

class TrailingSlash(object):
    """
    Trailing Slash
    --------------

    Wrap a wsgi bottle  application and attempt to serve the path as is. If this fails then attempt to serve the route with an appended trailing slash

    """

    def __init__(self, wrap_app):
        self.wrap_app = wrap_app
        self.wrap_app = self.app = wrap_app

    def __call__(self, environ, start_response):
        try:
            self.app.router.match(environ)
        except HTTPError:
            PI = environ['PATH_INFO']
            environ['PATH_INFO'] = PI + '/'
            try:
                self.app.router.match(environ)
                start_response('301 Redirect', [('Location', environ['SCRIPT_NAME'] + environ['PATH_INFO']),])
                return []
            except:
                environ['PATH_INFO'] = PI
                pass
        return self.wrap_app(environ, start_response)
