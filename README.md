# TODO #
Make type a parameter in request, don't store it as a field. Multiple values can be tokenized to the same token, i.e. id and age could be the same number but one is string and one is int. Also reduces storage cost.

Don't store pk as a field, it is already the document id. Save cost.

Implement a cache for dao get requests? I.e. pk -> token.

Remove the field-attribute, will it ever be used? Same logic as encryption, i.e. each value is deterministically encrypted to the same token.

Move method to parameter rather than context? Requires fewer remote functions.

# Local development #

Run locally in developer mode
```sh
gcloud auth application-default login    
gcloud beta code dev --dockerfile=./Dockerfile --application-default-credential
```

Access swagger on local server: [http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)

Run local server
```sh
uvicorn tokenvaultapi.main:api --reload
```

Lint
```sh
sh ./scripts/lint.sh
```

Format
```sh
sh ./scripts/format.sh
```

Test
```sh
pytest
or
python3 -m pytest
```

# Deploy service from source #

Input to CLI calls
```sh
PROJECT_ID=<YOR_GCP_PROJECT_ID>
DATASET_ID=remote_functions
REGION=europe-west1
CONNECTION_ID=tokenvault
```

Deploy from source
```sh
gcloud run deploy tokenvault --source .
```

Proxy requests to deployed service, use `http://localhost:8080/docs` for swagger GUI
```sh
gcloud beta run services proxy tokenvault --project $PROJECT_ID
SERVICE_URL=$(gcloud run services describe tokenvault --format='value(status.url)' --region=europe-west1)
```

Create Remote functionconnection and show service account to give access to tokenvault service
```sh
bq mk --connection --location=$REGION --project_id=$PROJECT_ID --connection_type=CLOUD_RESOURCE $CONNECTION_ID
bq show --connection $PROJECT_ID.$REGION.$CONNECTION_ID
```

Give service account permission to invoke cloud run service
```sh
gcloud run services add-iam-policy-binding tokenvault \
  --member='serviceAccount:CALLING_SERVICE_IDENTITY' \
  --role='roles/run.invoker'
```

```sh
bq --location=$REGION mk \
    --dataset \
    --description="DESCRIPTION" \
    $PROJECT_ID:$DATASET_ID
```

# Create Remote Functions #

```sh
sh ./scripts/create_functions.sh $PROJECT_ID $DATASET_ID $REGION $CONNECTION_ID $SERVICE_URL
```