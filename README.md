# FinTestTask

FastAPI project to get statistics


## Features

* Get user credits info by API "/user_credits/{user_id}"
* Insert new plans by API "/plans_insert"
* Get plans performance by API "/plans_performance"

## Installation with GitHub

```shell
git clone https://github.com/anatomst/FinTestTask.git
python3 -m venv venv
source venv/bin/activate (on Linux and macOS) or venv\Scripts\activate (on Windows)
pip install -r requirements.txt

"Then you need to create db in mysql and create .env file like .env_sample and fill up all necessary information or you can run mysql server using docker"
docker run -d -p 3306:3306 --name mysql-docker-container -e MYSQL_ROOT_PASSWORD=your_password -e MYSQL_DATABASE=db_name -e MYSQL_USER=your_user_name -e MYSQL_PASSWORD=your_password mysql/mysql-server:latest

"Set up database"
alembic upgrade head
"Or you can make post request to /db/clean"

"Then you need to upload csv files to db using POST request"
On /upload_file/users upload users.csv
On /upload_file/credits upload credits.csv
On /upload_file/dictionary upload dictionary.csv
On /upload_file/plans upload plans.csv
On /upload_file/payments upload payments.csv


"To run app"
uvicorn main:app --reload

```



