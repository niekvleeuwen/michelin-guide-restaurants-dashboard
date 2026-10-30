# Server Setup

Debian/Ubuntu VPS. Run steps marked *local* on your own machine, the rest on the server.

## 1. SSH keys and disabling password auth

**Local:** create a key (skip if you already have one) and copy it to the server.

```bash
ssh-keygen -t ed25519
ssh-copy-id user@your-server-ip
```

**Test the key login in a new terminal before continuing:**

```bash
ssh user@your-server-ip
```

**Server:** disable password authentication.

```bash
sudo nano /etc/ssh/sshd_config
```

Set:

```
PasswordAuthentication no
PubkeyAuthentication yes
PermitRootLogin prohibit-password
```

Also check `/etc/ssh/sshd_config.d/*.conf`, since files there can override the main config (e.g. `50-cloud-init.conf` often sets `PasswordAuthentication yes`, and the first value found wins).

```bash
sudo sshd -t && sudo systemctl restart ssh
```

Verify the effective values:

```bash
sudo sshd -T | grep -E 'passwordauthentication|pubkeyauthentication|permitrootlogin'
```

Keep your current session open and confirm a new login still works.

## 2. Firewall

Allow SSH **before** enabling the firewall, or you will lock yourself out.

```bash
sudo apt-get install -y ufw
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 443/udp
sudo ufw enable
sudo ufw status verbose
```

Also open the same ports in your VPS provider's panel, if it has a separate firewall.

## 3. Unprivileged (rootless) Docker user

Install Docker first from the [official repo](https://docs.docker.com/engine/install/ubuntu/), then:

```bash
sudo adduser dockeruser
sudo apt-get update
sudo apt-get install -y uidmap dbus-user-session slirp4netns systemd-container docker-ce-rootless-extras

# Disable the system-wide (rootful) daemon
sudo systemctl disable --now docker.service docker.socket
sudo rm -f /var/run/docker.sock

# Check subuid/subgid entries exist (should print two lines)
grep dockeruser /etc/subuid /etc/subgid
# If empty:
# sudo usermod --add-subuids 100000-165535 --add-subgids 100000-165535 dockeruser

# Keep the user's services running without a login
sudo loginctl enable-linger dockeruser

# Allow binding ports 80/443 (needed for web servers like Caddy)
# Note: this applies system-wide to all users, not just dockeruser
echo 'net.ipv4.ip_unprivileged_port_start=80' | sudo tee /etc/sysctl.d/99-rootless.conf
sudo sysctl --system
```

Open a proper session as the user (don't use `su` or `sudo -u`):

```bash
sudo machinectl shell dockeruser@
```

Then, as `dockeruser`:

```bash
dockerd-rootless-setuptool.sh install
systemctl --user enable --now docker

echo 'export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock' >> ~/.bashrc
source ~/.bashrc

docker run --rm hello-world
```

The setup tool also creates a `rootless` Docker context. `DOCKER_HOST` takes precedence over any context, so the CLI always talks to the rootless daemon. If `docker` isn't found or points at the wrong binary, follow the `PATH` hint printed by `dockerd-rootless-setuptool.sh`.

## 4. Deploy the app

As `dockeruser`:

```bash
git clone --depth 1 https://github.com/niekvleeuwen/michelin-guide-restaurants-dashboard.git
cd michelin-guide-restaurants-dashboard
cp .env.dist .env
chmod 600 .env     # keep secrets private
nano .env          # fill in your values
docker compose up -d
docker compose ps
```

## 5. Updates

**Server OS:** enable automatic security updates (as your sudo user).

```bash
sudo apt-get install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

**App:** as `dockeruser`, from the project directory.

```bash
git pull
docker compose up -d --build
docker image prune -f
```

## Troubleshooting

| Problem                                                        | Fix                                                                                                           |
|----------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| `XDG_RUNTIME_DIR needs to be set` / `Failed to connect to bus` | Not in a real session. Use `machinectl shell dockeruser@` and make sure linger is enabled.                    |
| `cannot expose privileged port 80`                             | Apply the sysctl setting in step 3.                                                                           |
| `failed to lock .../dockerd-rootless/lock`                     | The daemon is already running, or `.bashrc` contains pasted script content. Keep only the `DOCKER_HOST` export line. |
| Let's Encrypt fails                                            | Open ports 80/443 in `ufw` (step 2) and the VPS panel.                                                        |
