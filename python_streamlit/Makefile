include ../../.env
export

.PHONY: venv install run clean

.venv/bin/activate:
	python3 -m venv .venv
	.venv/bin/pip install pip-tools

requirements.txt: requirements.in
	.venv/bin/pip-compile --no-upgrade requirements.in

install: .venv/bin/activate requirements.txt
	.venv/bin/pip install -r requirements.txt

run: install
	.venv/bin/streamlit run app/start.py --server.port 8080 --server.runOnSave true

clean:
	rm -rf .venv
	rm -f __pycache__
