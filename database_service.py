import harperdb

url = "https://your-clouddatabaseurl.harperdbcloud.com"
username = "YOUR_USER"
password = "YOUR_PASSWORD"

db = harperdb.HarperDB(
    url=url,
    username=username,
    password=password
)

SHEMA = "yoga_repo"
TABLE = "yogas"
TABLE_TODAY = "yoga_today"


def insert_yoga(yoga_data):
    return db.insert(SHEMA, TABLE, [yoga_data])


def delete_yoga(yoga_id):
    return db.delete(SHEMA, TABLE, [yoga_id])


def get_all_yoga():
    return db.sql(f"select video_id,channel,title,duration from {SHEMA}.{TABLE}")


def get_yoga_today():
    return db.sql(f"select * from {SHEMA}.{TABLE_TODAY} where id = 0")


def update_yoga_today(yoga_data, insert=False):
    yoga_data['id'] = 0
    if insert:
        return db.insert(SHEMA, TABLE_TODAY, [yoga_data])
    return db.update(SHEMA, TABLE_TODAY, [yoga_data])

