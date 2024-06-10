compose-run:
	make compose-stop
	echo "Starting containers with compose..."
	docker-compose up -d --build

compose-stop:
	echo "Stopping containers..."
	docker-compose down --remove-orphans 

compose-logs:
	docker-compose logs -f

black:
	poetry run black .

isort:
	poetry run isort --profile black . 

run:
	poetry run streamlit run 0_💬_Chat_with_assistant.py

format:
	make isort
	make black

test:
	pytest tests/
	
start:
	- make compose-stop
	- make compose-run
	
clean-start:
	- make mongo-clean
	- make start

# Start with --debug flag True

run-debug:
	- export DEBUG=True
	- make start
	make compose-logs


mongo-clean:
	echo "Cleaning mongo..."
	rm -rf ./data/*
