VERSION=v2.31.0
CLONE_DIR := generate/git
GIT_REPO=https://github.com/git/git

VERSION_HTML=3692c01e1b89453b05f8049443583bfa935f300c
CLONE_DIR_HTML=generate/githtml
GIT_REPO_HTML=https://github.com/git/htmldocs

generate:
	if ls ${CLONE_DIR} 1>/dev/null; then true; else git clone ${GIT_REPO} ${CLONE_DIR}; fi
	git -C ${CLONE_DIR} checkout ${VERSION}
	python generate/generate.json.py

generate-html:
	if ls ${CLONE_DIR_HTML} 1>/dev/null; then true; else git clone ${GIT_REPO_HTML} ${CLONE_DIR_HTML}; fi
	git -C ${CLONE_DIR_HTML} checkout ${VERSION_HTML}


.PHONY: generate generate-html