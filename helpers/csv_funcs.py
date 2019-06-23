import csv
from helpers.models import RedshiftModel

def get_header(csv_reader):
    headers = next(csv_reader, None)
    model_mapper = {}
    for idx, field in enumerate(headers):
        model_mapper[field] = idx
    return model_mapper

def get_file_path(path, name):
    return '{}{}'.format(path, name)

def read_csv_to_model(csv_reader, model_mapper):
    source_models = []
    for row in csv_reader:
        model = RedshiftModel(
            rpt_grp_cd=row[model_mapper['rpt_grp_cd']],
            lctn_typ_cd=row[model_mapper['lctn_typ_cd']],
            clctn_prd_txt=row[model_mapper['clctn_prd_txt']],
            msr_cd=row[model_mapper['msr_cd']],
            clcltn_date=row[model_mapper['clcltn_date']],
            grp_rate_nmrtr=row[model_mapper['grp_rate_nmrtr']],
            grp_rate_dnmntr=row[model_mapper['grp_rate_dnmntr']],
            file_name=row[model_mapper['file_name']],
            creat_ts=row[model_mapper['creat_ts']],
            creat_user_id=row[model_mapper['creat_user_id']],
            submsn_cmplt_cd=row[model_mapper['submsn_cmplt_cd']]
        )
        source_models.append(model)
    return source_models
