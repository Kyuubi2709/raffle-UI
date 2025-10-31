# raffle-UI
A Raffle UI to draw the winners of the FluxCloud &amp; K.A.T Halloween giveaway


Yes! I put together a tiny Flask web UI you can run in Docker. It lets you upload your participants CSV (and optional exclude CSV), set the number of prizes, and optionally enter a seed for a reproducible draw. It enforces your rules (tickets = total months; one prize max per FluxID; remove tickets of winners before next draws).

Download the ready-to-run project

raffle_frontend_docker.zip

Inside you’ll find:

app.py (Flask app)

raffle_core.py (raffle logic)

templates/ (simple UI)

static/style.css

requirements.txt

Dockerfile

README.md (quickstart)

Quickstart (Docker)
unzip raffle_frontend_docker.zip
cd raffle_frontend
docker build -t raffle-ui .
docker run --rm -p 8080:8080 raffle-ui
# open http://localhost:8080

Notes

Participants CSV must contain flux_id and either months or term (1m, 3m, 6 months, 1y, etc.). Multiple rows per flux_id are summed.

Optional exclude CSV has a single flux_id column.

Add a Seed to make the draw deterministic and verifiable; leave blank to use cryptographically strong randomness.
