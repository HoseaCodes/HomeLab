# Bronco / DR Mobile Detailing Deployment

**Recorded:** November 20, 2026

**Status:** Migration planning and source transfer started. The current public site was observed responding from Vercel. HomeLab Docker deployment is pending build/start and public routing verification.

## Application

Bronco is a Next.js 14 marketing and lead-capture application for DR Mobile Detailing in Pearland, Texas. It includes a contact form that sends quote requests through Gmail SMTP.

## Deployment facts

- Development source: `/home/dominique/projects/bronco` on `dev01`.
- Deployment source: `/home/dominique/deployments/bronco` on `apps-01`.
- Existing public host: Vercel.
- Existing public URL: `https://www.drmobiledetailing.com/`.
- HomeLab host: `apps-01`, IP `192.168.0.47`.
- Planned Docker host port: `192.168.0.47:3002`.
- Container application port: `3000`.
- Restart policy: `unless-stopped`.
- Runtime secrets: `EMAIL_USER`, `EMAIL_PASS`, and `EMAIL_TO`.
- Production env file: deployment directory `.env`, intended permissions `600`.
- Health endpoint: `/api/health`.

## Verified state

- The public Vercel hostname responded with HTTP `200` during verification.
- Bronco contains a Next.js contact-form API route using Gmail SMTP.
- Docker Engine and Docker Compose are installed and running on `apps-01`.
- `apps-01` uses host port `3000` for Family Rotation and `3001` for SneakerAPI.
- Host port `3002` was selected for the Bronco migration to avoid those existing services.
- A source transfer to `/home/dominique/deployments/bronco` was attempted from `dev01`.

## Pending verification

- Confirm the deployment source transfer contains `Dockerfile`, `docker-compose.yml`, and application source.
- Confirm the production `.env` exists only on `apps-01` and contains restricted permissions.
- Build and start the Docker container.
- Confirm `/api/health` returns HTTP `200` on port `3002`.
- Confirm the contact form sends email without exposing credentials.
- Configure or verify Cloudflare Tunnel routing for the public HomeLab hostname.
- Decide whether Vercel remains active or is retired after HomeLab verification.
- Confirm monitoring, rollback, and backup/recovery procedures.

## Operations runbook

### Transfer source

Routine source transfers exclude `.git`, `node_modules`, `.next`, `.vercel`, and env files:

```bash
cd ~/projects/bronco

tar --exclude=.git --exclude=node_modules --exclude=.next \
    --exclude=.vercel --exclude=.env --exclude='.env.*' \
    -czf - -C ~/projects/bronco . \
  | ssh dominique@192.168.0.47 \
    "mkdir -p ~/deployments/bronco && tar -xzf - -C ~/deployments/bronco"
```

### Production environment

Create the production env file on `apps-01`:

```bash
cd ~/deployments/bronco
touch .env
chmod 600 .env
nano .env
```

The env file should contain runtime values for:

- `EMAIL_USER`
- `EMAIL_PASS`
- `EMAIL_TO`
- `NODE_ENV=production`
- `PORT=3000`

Do not commit or document actual secret values.

### Build and start

```bash
cd ~/deployments/bronco
sudo docker compose up -d --build
sudo docker compose ps
```

### Health check

```bash
curl -i http://192.168.0.47:3002/api/health
sudo docker compose logs --tail 100 bronco
```

A successful health response must be confirmed before public routing is considered complete.

### Recreate after configuration changes

Changing `.env` does not update a running container. Recreate the container after env changes:

```bash
cd ~/deployments/bronco
sudo docker compose up -d --force-recreate bronco
```

### Troubleshooting

Check container status and port publication:

```bash
sudo docker ps --filter name=bronco
sudo ss -ltnp | grep -E ':3000|:3001|:3002'
```

Check app logs:

```bash
sudo docker compose logs --tail 100 bronco
```

For contact-form failures, verify SMTP credentials, network access to Gmail SMTP, recipient configuration, and application logs.

## Security and recovery boundaries

- The Gmail app password exposed in development must be considered compromised and rotated before production use.
- Runtime SMTP credentials must remain outside source control and public documentation.
- Deleting and recreating the container does not require persistent application data for this simple marketing site.
- Decommissioning Vercel should happen only after the HomeLab deployment and contact form are independently verified.
- Database and backup requirements do not apply unless application features are added that persist user data.
