import csv
from helpers.flask_essentials import database
from helpers.csv_funcs import get_header
from helpers.csv_funcs import get_file_path
from helpers.csv_funcs import read_csv_to_model
from helpers.schemas import RedshiftSchema

def reset_database():
    database.reflect()
    database.drop_all()
    database.create_all()

def load_mysql(path, name):
    with open(get_file_path(path, name)) as csv_file_ptr:
        reader = csv.reader(csv_file_ptr)
        header_mapper = get_header(reader)
        models = read_csv_to_model(reader, header_mapper)
        database.session.bulk_save_objects(models)
        database.session.commit()

        schema = RedshiftSchema(many=True)
        data = schema.dump(models).data

        return data, header_mapper

def dump_mysql(path, name, header_mapper, data):
    header = list(header_mapper.keys())
    with open(get_file_path(path, name), 'w') as csv_file_ptr:
        writer = csv.writer(csv_file_ptr)
        writer.writerow(header)
        for row in data:
            writer.writerow([getattr(row, column) for column in header ])
