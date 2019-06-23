from helpers.flask_essentials import database

class RedshiftModel(database.Model):
    __tablename__ = 'test_msr_source'
    id = database.Column(database.Integer, primary_key=True, autoincrement=True, nullable=False)
    rpt_grp_cd =  database.Column(database.VARCHAR(60), nullable=True)
    lctn_typ_cd = database.Column(database.VARCHAR(10), nullable=True)
    clctn_prd_txt = database.Column(database.VARCHAR(8), nullable=True)
    msr_cd =  database.Column(database.VARCHAR(20), nullable=True)
    clcltn_date =  database.Column(database.VARCHAR(10), nullable=True)
    grp_rate_nmrtr = database.Column(database.VARCHAR(3), nullable=True)
    grp_rate_dnmntr = database.Column(database.VARCHAR(5), nullable=True)
    file_name = database.Column(database.VARCHAR(50), nullable=True)
    creat_ts = database.Column(database.VARCHAR(50), nullable=True)
    creat_user_id = database.Column(database.VARCHAR(30), nullable=True)
    submsn_cmplt_cd = database.Column(database.VARCHAR(10), nullable=True)
