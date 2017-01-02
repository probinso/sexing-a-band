#!/usr/bin/env bash

DST=$(jq '.storage_path' resource.json | tr -d '"')
pushd ${DST}
