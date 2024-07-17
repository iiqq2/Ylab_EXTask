DC = docker compose
ENV = --env-file .env
APP_FILE = docker_compose/app.yaml
DB_FILE = docker_compose/db.yaml
REDIS_FILE = docker_compose/redis.yaml
PROJECT_NAME = ylab

.PHONY: app
app:
	${DC} -p ${PROJECT_NAME} -f ${APP_FILE} ${ENV} up -d

.PHONY: app-logs
app-logs:
	${DC} -p ${PROJECT_NAME} -f ${APP_FILE} ${ENV} logs -f

.PHONY: app-down
app-down:
	${DC} -p ${PROJECT_NAME} -f ${APP_FILE} ${ENV} down

.PHONY: db
db:
	${DC} -p ${PROJECT_NAME} -f ${DB_FILE} ${ENV} up -d

.PHONY: db-logs
db-logs:
	${DC} -p ${PROJECT_NAME} -f ${DB_FILE} ${ENV} logs -f

.PHONY: db-down
db-down:
	${DC} -p ${PROJECT_NAME} -f ${DB_FILE} ${ENV} down

.PHONY: redis
redis:
	${DC} -p ${PROJECT_NAME} -f ${REDIS_FILE} ${ENV} up -d

.PHONY: redis-logs
redis-logs:
	${DC} -p ${PROJECT_NAME} -f ${REDIS_FILE} ${ENV} logs -f

.PHONY: redis-down
redis-down:
	${DC} -p ${PROJECT_NAME} -f ${REDIS_FILE} ${ENV} down

.PHONY: migrate
migrate:
	${DC} -p ${PROJECT_NAME} -f ${APP_FILE} ${ENV} exec app sh -c "alembic upgrade head"

.PHONY: gunicorn
gunicorn:
	${DC} -p ${PROJECT_NAME} -f ${APP_FILE} ${ENV} exec app sh -c "gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000"

.PHONY: all-up
all-up: app db redis

.PHONY: all-down
all-down:
	${DC} -p ${PROJECT_NAME} -f ${APP_FILE} -f ${DB_FILE} -f ${REDIS_FILE} ${ENV} down
