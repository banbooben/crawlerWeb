import click
from flask.cli import with_appcontext


# from configs.sysconf import PROJECT_PATH
# from . import app

def init_command(app):
    # user_cli = AppGroup('user')
    #
    # @user_cli.command('create')
    # @click.argument('name')
    @app.cli.command("create_all", help="create tables if not exists")
    @with_appcontext
    def create_all():
        from application.initialization.extensions_process.flask_sqlalchemy_process import db
        db.create_all()

    @app.cli.command("drop_all", help="drop all tables, very! dangerous!")
    @with_appcontext
    def drop_all():
        res = click.prompt("drop table is very dangerous continue?.. y to continue", confirmation_prompt=True)
        if res.upper() != "Y":
            click.echo("abort!")
            return
        from application.initialization.extensions_process.flask_sqlalchemy_process import db
        click.echo("by you command!")
        db.drop_all()
        return
