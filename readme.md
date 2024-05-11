# Netlify DDNS

Dynamic DNS for netlify DNS, syncs your current IPV4 to Netlify DNS records. Easily run with Docker, enjoy.

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/pratyaksh123/netlify-dynamic-dns.git
cd netlify-ddns

# .env file
NETLIFY_AUTH_TOKEN=your_netlify_auth_token_here
NETLIFY_DNS_ZONE_ID=your_netlify_dns_zone_id_here
```

## Env vars
```
NETLIFY_AUTH_TOKEN=your_netlify_auth_token_here
NETLIFY_DNS_ZONE_ID=your_netlify_dns_zone_id_here
```

#### To get dns zone id simply use the get_dns_zones() method in ```main.py```

## Running the Project
#### To build and run the project using Docker, follow these steps:
```
docker build -t  netlify-dns .
docker run -d netlify-dns
```

### Set Up Cron Job for Every 5 Minutes
Add a new line to your crontab to run the Docker container every 5 minutes:

```bash
*/5 * * * * /usr/bin/docker run netlify-dns >> /var/log/your-container.log 2>&1
```

### Clear Logs Every 24 Hours
You can add a cron job to clear the log file every 24 hours at midnight:
```
0 0 * * * /bin/truncate -s 0 /var/log/your-container.log
```