test:
	docker-compose -f docker-compose.dev.yaml exec api pytest

run:
	docker compose -f docker-compose.dev.yaml up -d

down:
	docker-compose -f docker-compose.dev.yaml down

build:
	docker-compose -f docker-compose.dev.yaml build

ps:
	docker-compose -f docker-compose.dev.yaml ps

logs:
	docker-compose -f docker-compose.dev.yaml logs -f api

restart:
	docker-compose -f docker-compose.dev.yaml restart api

checkreq:
	pip install --upgrade pur
	pur --no-ssl-verify --dry-run-changed -r requirements-dev.txt

installreq:
	pip install --upgrade uv
	uv pip install --no-ssl-verify -r requirements-dev.txt
