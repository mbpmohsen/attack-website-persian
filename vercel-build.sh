#!/bin/sh
set -eu

cd attack-style
npm run build-copy

cd ..
python3 update-attack.py \
  --modules \
    clean \
    datasources \
    groups \
    matrices \
    mitigations \
    software \
    tactics \
    techniques \
    campaigns \
    assets \
    datacomponents \
    detectionstrategies \
    analytics \
    website_build \
    random_page \
    redirections \
    subdirectory \
    search \
  --extras \
    resources \
    versions \
    blog \
    benefactors \
    contribute \
  --attack-brand \
  --no-test-exitstatus

cd attack-search
npm run build
npm run copy
