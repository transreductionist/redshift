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
        header, header_mapper = get_header(reader)
        models = read_csv_to_model(reader, header_mapper)
        database.session.bulk_save_objects(models)
        database.session.commit()
        return map_models_to_redshift_data(models, header_mapper)

def dump_mysql(path, name, header_mapper, data):
    header = list(header_mapper.keys())
    with open(get_file_path(path, name), 'w') as csv_file_ptr:
        writer = csv.writer(csv_file_ptr)
        writer.writerow(header)
        for row in data:
            writer.writerow([getattr(row, column) for column in header ])

def add_new_redshift_fields(header_mapper):
    for field, value in header_mapper.items():
        if value >= 9:
            header_mapper[field] += 1
    header_mapper['finl_sw'] = 9
    header = [sorted_item[0] for sorted_item in sorted(header_mapper.items(), key=lambda kv: (kv[1], kv[0]))]
    return header, header_mapper

def map_models_to_redshift_data(models, header_mapper):
    schema = RedshiftSchema()
    redshift_header, redshift_header_mapper = add_new_redshift_fields(header_mapper)
    schema.context = redshift_header_mapper
    data = []
    for model in models:
        data.append(schema.dump(model).data)
    return data, redshift_header
