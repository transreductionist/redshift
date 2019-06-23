import io
from s3_web_storage import WebStorage


def save_bytesio_to_s3(file_data, field_names, file_name):
    output = io.BytesIO()
    if field_names:
        output.write(','.join(field_names).encode())
        output.write('\n'.encode())

    for row in file_data:
        output.write(','.join(map(str, row)).encode())
        output.write('\n'.encode())

    metadata = ('Ventara Redshift', file_name)
    WebStorage.save(file_name, output.getvalue(), metadata)

    output.close()

    return file_name
