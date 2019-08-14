#!/usr/bin/env bash
# Change this to your working directory.
cd /home/theo/PycharmProjects/thems_facts/getter_service || exit
gcloud app deploy ./fact_getter_app.yaml --quiet
