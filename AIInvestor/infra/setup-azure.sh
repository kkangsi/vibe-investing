#!/usr/bin/env bash
# AI Investor — one-time Azure account setup.
#
# Run this on YOUR local machine (not in CI). Outputs go directly to
# GitHub Secrets — copy/paste them in the printed order. Nothing is
# logged to a file.
#
# Prerequisites:
#   brew install azure-cli gh
#   az login
#   gh auth login

set -euo pipefail

ENV_NAME="${1:-prod}"   # prod | dev
RG="rg-aiinvestor-${ENV_NAME}"
LOCATION="koreacentral"
SP_NAME="github-aiinvestor-${ENV_NAME}-deploy"

echo "▶ Step 1/5 — Subscription"
SUBSCRIPTION_ID=$(az account show --query id -o tsv)
TENANT_ID=$(az account show --query tenantId -o tsv)
echo "   subscription: $SUBSCRIPTION_ID"
echo "   tenant:       $TENANT_ID"

echo ""
echo "▶ Step 2/5 — Resource group ($RG @ $LOCATION)"
az group create --name "$RG" --location "$LOCATION" --output none
echo "   ✓ created (or already exists)"

echo ""
echo "▶ Step 3/5 — Service principal scoped to $RG"
SP_JSON=$(az ad sp create-for-rbac \
  --name "$SP_NAME" \
  --role contributor \
  --scopes "/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RG}" \
  --sdk-auth)
CLIENT_ID=$(echo "$SP_JSON" | jq -r .clientId)
echo "   ✓ SP created — clientId: $CLIENT_ID"

echo ""
echo "▶ Step 4/5 — Grant the SP 'User Access Administrator' on the RG"
echo "   (needed so Bicep can create role assignments)"
az role assignment create \
  --assignee "$CLIENT_ID" \
  --role "User Access Administrator" \
  --scope "/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RG}" \
  --output none
echo "   ✓ role assigned"

echo ""
echo "▶ Step 5/5 — Push secrets into GitHub repo"
echo "   (interactive — gh CLI will prompt for confirmation)"

REPO=$(git config --get remote.origin.url | sed -E 's#.*github.com[:/](.+)\.git#\1#')
echo "   target repo: $REPO"

# AZURE_CREDENTIALS — full SP JSON
echo "$SP_JSON" | gh secret set AZURE_CREDENTIALS --repo "$REPO"

# AZURE_DEPLOYER_CLIENT_ID — used by the workflow to look up the SP's object ID
echo -n "$CLIENT_ID" | gh secret set AZURE_DEPLOYER_CLIENT_ID --repo "$REPO"

echo ""
echo "▶ Remaining secrets to set manually (these are application secrets, not Azure):"
echo "   gh secret set TELEGRAM_BOT_TOKEN       --repo $REPO   # from BotFather"
echo "   gh secret set DEEPSEEK_API_KEY         --repo $REPO   # from platform.deepseek.com"
echo "   gh secret set TELEGRAM_WEBHOOK_SECRET  --repo $REPO   # any random 32-hex string"
echo "   gh secret set USER_ID_SALT             --repo $REPO   # any random string"
echo ""
echo "Generate suggested random values:"
echo "   TELEGRAM_WEBHOOK_SECRET=$(openssl rand -hex 16)"
echo "   USER_ID_SALT=$(openssl rand -hex 24)"
echo ""
echo "✅ Done. Push to main (or trigger 'deploy-aiinvestor' workflow) to deploy."
