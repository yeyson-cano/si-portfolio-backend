.PHONY: db-init db-migrate

db-init:
	docker-compose exec backend \
		conda run -n si-backend python -m app.models.init_db

db-migrate:
	docker-compose exec backend \
		conda run -n si-backend alembic upgrade head
