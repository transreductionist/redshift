import copy
from datetime import datetime
from decimal import Decimal
from marshmallow import post_dump
from marshmallow_sqlalchemy import ModelSchema

from helpers.flask_essentials import database
from helpers.models import RedshiftModel

EPOCH = datetime(1970, 1, 1)
INPUT_DATETIME_FORMAT = '%m/%d/%Y'
INPUT_TIMESTAMP_FORMAT = '%m/%d/%Y %M:%S'
OUTPUT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

class RedshiftSchema( ModelSchema ):
    class Meta:

        model = RedshiftModel
        strict = True
        sqla_session = database.session

    @post_dump
    def condition_data( self, data ):
        redshift_header_mapper = self.context
        values = ['' for i in range(0, len(list(redshift_header_mapper.keys())))]
        for field, value in data.items():
            if field == 'id':
                continue
            if field == 'creat_ts':
                if value == '':
                    value = 'NULL'
                else:
                    value = str((datetime.strptime(value, INPUT_TIMESTAMP_FORMAT)- EPOCH).total_seconds())
            elif field == 'clcltn_date':
                if value == '':
                    value = 'NULL'
                else:
                    value = datetime.strptime(value, INPUT_DATETIME_FORMAT)
                    value = value.strftime(OUTPUT_DATETIME_FORMAT)
            elif field == 'grp_rate_nmrtr':
                if value == '':
                    value = 'NULL'
            elif field == 'grp_rate_dnmntr':
                if value == '':
                    value = 'NULL'
                else:
                    value = '{:.1f}'.format(float(value))
            elif value == '':
                    value = 'NULL'
            values[redshift_header_mapper[field]] = value
        values[redshift_header_mapper['finl_sw']] = 'NULL'
        return values
