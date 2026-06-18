.PHONY: init fetch build graph validate demo clean

VAULT ?= vault
GRAPH_OUT ?= docs/graph

init:
	python3 scripts/init_vault.py --vault $(VAULT)

fetch:
	python3 scripts/fetch_github_repos.py --repos data/repos.json --vault $(VAULT)

build:
	python3 scripts/build_wiki_from_repos.py --vault $(VAULT)

graph:
	python3 scripts/graphify_wiki.py --vault $(VAULT) --out $(GRAPH_OUT)

validate:
	python3 scripts/validate_workshop.py --vault $(VAULT) --graph $(GRAPH_OUT)/graph.dot

demo: init fetch build graph validate

clean:
	rm -rf $(GRAPH_OUT) vault/raw/github/*.json vault/raw/github/*.md scripts/__pycache__