#!/bin/bash
for f in *.html; do python getContactsMin.py $f > ../../data/min/${f%.html}.txt; done
