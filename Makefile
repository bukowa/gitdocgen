VERSION=v2.31.0
CLONE_DIR := generate/git
GIT_REPO=https://github.com/git/git

generate:
	if ls ${CLONE_DIR} 1>/dev/null; then true; else git clone ${GIT_REPO} ${CLONE_DIR}; fi
	git -C ${CLONE_DIR} checkout ${VERSION}
	python generate/generate.json.py

.PHONY: generate