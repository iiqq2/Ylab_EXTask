DC = docker compose
ENV = --env-file .env
APP_FILE = docker_compose/app.yaml
DB_FILE = docker_compose/db.yaml
REDIS_FILE = docker_compose/redis.yaml
ZOOKEEPER_FILE = docker_compose/zookeeper.yaml
KAFKA_FILE = docker_compose/kafka.yaml
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

.PHONY: zookeeper
zookeeper:
	${DC} -p ${PROJECT_NAME} -f ${ZOOKEEPER_FILE} ${ENV} up -d

.PHONY: zookeeper-logs
zookeeper-logs:
	${DC} -p ${PROJECT_NAME} -f ${ZOOKEEPER_FILE} ${ENV} logs -f

.PHONY: zookeeper-down
zookeeper-down:
	${DC} -p ${PROJECT_NAME} -f ${ZOOKEEPER_FILE} ${ENV} down

.PHONY: kafka
kafka:
	${DC} -p ${PROJECT_NAME} -f ${KAFKA_FILE} ${ENV} up -d

.PHONY: kafka-logs
kafka-logs:
	${DC} -p ${PROJECT_NAME} -f ${KAFKA_FILE} ${ENV} logs -f

.PHONY: kafka-down
kafka-down:
	${DC} -p ${PROJECT_NAME} -f ${KAFKA_FILE} ${ENV} down

