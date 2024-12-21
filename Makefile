SRC_DIR := app
TEST_DIR := tests


run:
	fastapi dev $(SRC_DIR)/main.py

lint:
	isort $(SRC_DIR)/ --check
	isort $(TEST_DIR)/ --check
	black $(SRC_DIR)/ --check
	black $(TEST_DIR)/ --check
	pylint $(SRC_DIR)/
	pylint $(TEST_DIR)/

format:
	isort $(SRC_DIR)/
	isort $(TEST_DIR)/
	black $(SRC_DIR)/
	black $(TEST_DIR)/

post_test:
	coverage html

test:
	pytest -s --cov=$(SRC_DIR) -vv
	make post_test