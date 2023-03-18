from datetime import datetime 
import pendulum
from airflow import DAG
from airflow.decorators import dag, task
from airflow.models import Variable
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


# Variables are stored in the Metadata DB
# Instead of hardcoding the tablenames, you can take it from
# Variable.get("training_table") and Variable.get("prediction_table")
# created with the 1st Exercise
TRAINING_TABLE = 'training' #Variable.get("training_table")
PREDICTION_TABLE = 'prediction' #Variable.get("prediction_table")

# default_args = {
#     "owner": "airflow",
#     "depends_on_past": False,
#     "start_date": datetime(now.year, now.month, now.day),
#     "email": ["pioneer22022001@gmail.com"],
#     "email_on_failure": True,
#     "email_on_retry": False,
#     "retries": 1,
#     "retry_delay": datetime.timedelta(minutes=1)
# }

@dag(
    dag_id="save_data_to_db",
    schedule_interval="0 0 * * *",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
)
def create_ml_table():
    create_houseinfo_table = PostgresOperator(
        task_id="create_house_data_table",
        postgres_conn_id="postgres_db",
        sql="""
            CREATE TABLE IF NOT EXISTS housedata (
                "loai_phong" TEXT,
                "ngay_dang" DATE,
                "gia_phong" TEXT,
                "dien_tich" TEXT,
                "suc_chua" TEXT,
                "dien" TEXT,
                "nuoc" TEXT,
                "may_lanh" TEXT,
                "wc_rieng" TEXT,
                "cho_de_xe" TEXT,
                "wifi" TEXT,
                "tu_do" TEXT,
                "khong_chung_chu" TEXT,
                "tu_lanh" TEXT,
                "may_giat" TEXT,
                "bao_ve" boolean,
                "giuong_ngu" boolean,
                "nau_an" boolean,
                "tivi" boolean,
                "thu_cung" boolean,
                "tu_quan_ao" boolean,
                "cua_so" boolean,
                "may_nuoc_nong" boolean,
                "gac_lung" boolean,
                "quan" text,
                "nam" boolean,
                "nu" boolean
            );""",
    )

    create_houseinfo_temp_table = PostgresOperator(
        task_id="create_houseinfo_temp_table",
        postgres_conn_id="postgres_db",
        sql="""
            DROP TABLE IF EXISTS houseinfo_temp;
            CREATE TABLE houseinfo_temp (
                "loai_phong" TEXT,
                "ngay_dang" DATE,
                "gia_phong" TEXT,
                "dien_tich" TEXT,
                "suc_chua" TEXT,
                "dien" TEXT,
                "nuoc" TEXT,
                "may_lanh" TEXT,
                "wc_rieng" TEXT,
                "cho_de_xe" TEXT,
                "wifi" TEXT,
                "tu_do" TEXT,
                "khong_chung_chu" TEXT,
                "tu_lanh" TEXT,
                "may_giat" TEXT,
                "bao_ve" boolean,
                "giuong_ngu" boolean,
                "nau_an" boolean,
                "tivi" boolean,
                "thu_cung" boolean,
                "tu_quan_ao" boolean,
                "cua_so" boolean,
                "may_nuoc_nong" boolean,
                "gac_lung" boolean,
                "quan" text,
                "nam" boolean,
                "nu" boolean
            );""",
    )
    @task
    def get_data():
        # NOTE: configure this as appropriate for your airflow environment
        data_path = "/opt/spark/resources/data/cleaned_house_price_data.csv"
        postgres_hook = PostgresHook(postgres_conn_id="postgres_db")
        conn = postgres_hook.get_conn()
        cur = conn.cursor()
        with open(data_path, "r") as file:
            cur.copy_expert(
                "COPY houseinfo_temp(loai_phong,ngay_dang,gia_phong,dien_tich,suc_chua,dien,nuoc,may_lanh,wc_rieng,cho_de_xe,wifi,tu_do,khong_chung_chu,tu_lanh,may_giat,bao_ve,giuong_ngu,nau_an,tivi,thu_cung,tu_quan_ao,cua_so,may_nuoc_nong,gac_lung,quan,nam,nu) FROM STDIN WITH CSV HEADER DELIMITER AS ',' QUOTE '\"'",
                file,
            )
        conn.commit()
    @task    
    def merge_data():
        query = """
            INSERT INTO housedata
            SELECT *
            FROM (
                SELECT *
                FROM houseinfo_temp
            ) t
            ON CONFLICT("ngay_dang","gia_phong","dien_tich","quan","loai_phong") DO NOTHING
            ;
        """
#ON CONFLICT DO NOTHING;
        try:
            postgres_hook = PostgresHook(postgres_conn_id="postgres_db")
            conn = postgres_hook.get_conn()
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
            return 0
        except Exception as e:
            return 1
    [create_houseinfo_table, create_houseinfo_temp_table] >> get_data() >> merge_data()

dag = create_ml_table()
