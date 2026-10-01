#!/bin/sh
# deploy do agente de campanhas: conta de serviço própria, papel mínimo, acesso só autenticado
gcloud projects add-iam-policy-binding projeto-campanhas \
  --member="serviceAccount:agente@projeto-campanhas.iam.gserviceaccount.com" \
  --role="roles/run.invoker"
gcloud run deploy agente-campanhas --source . --region us-central1 --no-allow-unauthenticated
