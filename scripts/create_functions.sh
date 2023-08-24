#!/bin/sh -ex

PROJECT_ID=$1
DATASET_ID=$2
REGION=$3
CONNECTION_ID=$4
SERVICE_URL=$5

bq query \
--use_legacy_sql=false \
--location=$REGION \
"CREATE OR REPLACE FUNCTION \`$PROJECT_ID.$DATASET_ID\`.deidentify_string(\
identifier STRING,\
identity STRING,\
value STRING) RETURNS STRING \
REMOTE WITH CONNECTION \`$PROJECT_ID.$REGION.$CONNECTION_ID\` \
OPTIONS (\
endpoint = '$SERVICE_URL',\
user_defined_context = [\
    ('action', 'DEIDENTIFY'),\
    ('tokenType', 'STRING'),\
    ('method','FORMAT_PRESERVING')\
])"

bq query \
--use_legacy_sql=false \
--location=$REGION \
"CREATE OR REPLACE FUNCTION \`$PROJECT_ID.$DATASET_ID\`.reidentify_string(\
identifier STRING,\
identity STRING,\
value STRING) RETURNS STRING \
REMOTE WITH CONNECTION \`$PROJECT_ID.$REGION.$CONNECTION_ID\` \
OPTIONS (\
endpoint = '$SERVICE_URL',\
user_defined_context = [\
    ('action', 'REIDENTIFY'),\
    ('tokenType', 'STRING')
])"

bq query \
--use_legacy_sql=false \
--location=$REGION \
"CREATE OR REPLACE FUNCTION \`$PROJECT_ID.$DATASET_ID\`.deidentify_float(\
identifier STRING,\
identity STRING,\
value FLOAT64) RETURNS FLOAT64 \
REMOTE WITH CONNECTION \`$PROJECT_ID.$REGION.$CONNECTION_ID\` \
OPTIONS (\
endpoint = '$SERVICE_URL',\
user_defined_context = [\
    ('action', 'DEIDENTIFY'),\
    ('tokenType', 'FLOAT'),\
    ('method','FORMAT_PRESERVING')\
])"

bq query \
--use_legacy_sql=false \
--location=$REGION \
"CREATE OR REPLACE FUNCTION \`$PROJECT_ID.$DATASET_ID\`.reidentify_float(\
identifier STRING,\
identity STRING,\
value FLOAT64) RETURNS FLOAT64 \
REMOTE WITH CONNECTION \`$PROJECT_ID.$REGION.$CONNECTION_ID\` \
OPTIONS (\
endpoint = '$SERVICE_URL',\
user_defined_context = [\
    ('action', 'REIDENTIFY'),\
    ('tokenType', 'FLOAT')
])"

bq query \
--use_legacy_sql=false \
--location=$REGION \
"CREATE OR REPLACE FUNCTION \`$PROJECT_ID.$DATASET_ID\`.deidentify_int(\
identifier STRING,\
identity STRING,\
value INT) RETURNS INT \
REMOTE WITH CONNECTION \`$PROJECT_ID.$REGION.$CONNECTION_ID\` \
OPTIONS (\
endpoint = '$SERVICE_URL',\
user_defined_context = [\
    ('action', 'DEIDENTIFY'),\
    ('tokenType', 'INT'),\
    ('method','FORMAT_PRESERVING')\
])"

bq query \
--use_legacy_sql=false \
--location=$REGION \
"CREATE OR REPLACE FUNCTION \`$PROJECT_ID.$DATASET_ID\`.reidentify_int(\
identifier STRING,\
identity STRING,\
value INT) RETURNS INT \
REMOTE WITH CONNECTION \`$PROJECT_ID.$REGION.$CONNECTION_ID\` \
OPTIONS (\
endpoint = '$SERVICE_URL',\
user_defined_context = [\
    ('action', 'REIDENTIFY'),\
    ('tokenType', 'INT')
])"