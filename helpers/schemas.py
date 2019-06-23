from marshmallow_sqlalchemy import ModelSchema

from helpers.flask_essentials import database
from helpers.models import RedshiftModel


class RedshiftSchema( ModelSchema ):
    class Meta:

        model = RedshiftModel
        strict = True
        sqla_session = database.session
