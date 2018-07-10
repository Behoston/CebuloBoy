from sanic import Sanic
from sanic_jinja2 import SanicJinja2

import models

app = Sanic()

jinja = SanicJinja2(app)
app.static('/static', './static')


#
# Specify the package name, if templates/ dir is inside module
# jinja = SanicJinja2(app, pkg_name='sanicapp')
# or use customized templates path
# jinja = SanicJinja2(app, pkg_name='sanicapp', pkg_path='other/templates')
# or setup later
# jinja = SanicJinja2()
# jinja.init_app(app)


@app.route('/')
@jinja.template('index.html')
async def index(request):
    shops = models.Shop.select()
    return {
        'shops': shops,
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337, debug=True)
