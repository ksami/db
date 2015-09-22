#!/bin/bash
for f in *.html; do echo $f; python getContactsMin.py $f > ../../data/min/${f%.html}.txt; done
