#!/bin/sh
# deploy do agente de campanhas
gcloud projects add-iam-policy-binding projeto-campanhas \
  --member="serviceAccount:agente@projeto-campanhas.iam.gserviceaccount.com" \
  --role="roles/editor"
gcloud run deploy agente-campanhas --source . --region us-central1 --allow-unauthenticated
