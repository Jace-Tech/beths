from flask import Flask, render_template
from .config.variables import SECRET_KEY

def create_app():
    app = Flask(__name__)

    #CONFIGS
    app.config["SECRET_KEY"] = SECRET_KEY



    #BLUEPRINTS
    from .views.admin_auth import admin
    app.register_blueprint(admin, url_prefix="/owner")

    from .views.user import user
    app.register_blueprint(user)

    
    # ERROR ROUTES 

    # 404 - ERROR
    @app.errorhandler(404)
    def error_404(error):
        return render_template("error-404.html")

    # 500 - ERROR
    # @app.errorhandler(Exception)
    # def error_500(error):
    #     print("500 Error", error)
    #     return render_template("error-500.html")




    return app