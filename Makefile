# Database Config
export POSTGRES_USER=postgres
export POSTGRES_DB=Hirestream
export POSTGRES_PASSWORD=postgres
export POSTGRES_SERVER=192.168.1.5
export POSTGRES_PORT=5432
 
# Project Config
export PROJECT_TITLE=Hirestream
export PROJECT_VERSION=0.1
export SECRET_KEY=bf84f20c1c76dd4775122859caf00a9e2e0c91ae36679040506182448f80e7c0
export ALGORITHM=HS256

runserver:
	echo "Starting Uvicorn"
	uvicorn main:app --reload