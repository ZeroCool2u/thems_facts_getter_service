#!/usr/bin/env bash
cd /home/theo/PycharmProjects/thems_facts/getter_service/ || exit
dev_appserver.py --application=facts-sender fact_getter_app.yaml
