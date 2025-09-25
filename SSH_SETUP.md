# SSH Deployment Setup Guide

## 📋 **Setup Steps for Remote Kubernetes Deployment**

### 1. **Add SSH Public Key to Ubuntu Machine**

Copy this public key to your Ubuntu machine (`zebra@el114d1u22-593`):

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDn4UfuD8eRgQox+EDENAobth0+FGK+GetmwGADCK5gXfwsA5bbOcGWyxzOsXEt720917XB2ZWLRcQF7GzQmjQl7+FCg4oww+PL/2t6Prq2jt5s6l97eqP0bjznrUpNwqPWhEtWfi7UqiDKLyf//F+KGskEEYncUnm0yoeUJ8bDRWRiOToWc8wzRDH0TJsBTFAGMh8Pc3Vg27nhr+sllQCzp2y7kg2EIH9nTfZCZ7IzWQIIfdLRo8R08ZQ2qcXfzwnhZFdD0xGB/0IjtKvWMCMLZWper0JTzEyIcHlyyQPP9a6F4zUDlaLkqDRGJIiYST9blK2IxoyQ2RHzpc/J27jT1ircCDV0/X6EyoqIYBrbEyM1IBhcNuoVekmb/O5BWnoezlXD0mAHRRZatyJ5Upf0uVh7GMc7STLWG/Chtlv6YJuhjht/LjMjhhD2Tgrm45zkrLWR0LpxEHG27Hbduz2G970WbQsFV6ifLmAYtdf1FUbEF54tf6njq+Zqfd3RHWcMFPLLEKK5/CXVSEY5JBDEa2PqM0Sw1lvRrjuMmSDY8doJZl4Gbu+ngAczZ4oFqJOF4BqxlbCbTACb+VW0mor0On22/6fJT6D5LqG75qgzmDIZtcpssFpH4bQAlUc+AbFRWl1brQLRbNIov9bPkKH40Jox7AtmRdzol2Bk4mqgNQ== zgn\sb9122@ZBR-3CK20ShGEXD
```

**On your Ubuntu machine, run:**
```bash
# Add the public key to authorized_keys
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDn4UfuD8eRgQox+EDENAobth0+FGK+GetmwGADCK5gXfwsA5bbOcGWyxzOsXEt720917XB2ZWLRcQF7GzQmjQl7+FCg4oww+PL/2t6Prq2jt5s6l97eqP0bjznrUpNwqPWhEtWfi7UqiDKLyf//F+KGskEEYncUnm0yoeUJ8bDRWRiOToWc8wzRDH0TJsBTFAGMh8Pc3Vg27nhr+sllQCzp2y7kg2EIH9nTfZCZ7IzWQIIfdLRo8R08ZQ2qcXfzwnhZFdD0xGB/0IjtKvWMCMLZWper0JTzEyIcHlyyQPP9a6F4zUDlaLkqDRGJIiYST9blK2IxoyQ2RHzpc/J27jT1ircCDV0/X6EyoqIYBrbEyM1IBhcNuoVekmb/O5BWnoezlXD0mAHRRZatyJ5Upf0uVh7GMc7STLWG/Chtlv6YJuhjht/LjMjhhD2Tgrm45zkrLWR0LpxEHG27Hbduz2G970WbQsFV6ifLmAYtdf1FUbEF54tf6njq+Zqfd3RHWcMFPLLEKK5/CXVSEY5JBDEa2PqM0Sw1lvRrjuMmSDY8doJZl4Gbu+ngAczZ4oFqJOF4BqxlbCbTACb+VW0mor0On22/6fJT6D5LqG75qgzmDIZtcpssFpH4bQAlUc+AbFRWl1brQLRbNIov9bPkKH40Jox7AtmRdzol2Bk4mqgNQ== zgn\sb9122@ZBR-3CK20ShGEXD" >> ~/.ssh/authorized_keys

# Set correct permissions
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh

# Create deployment directory
mkdir -p ~/zbot-deploy
```

### 2. **Add GitHub Secrets**

Add these secrets to your GitHub repository:

#### **SSH_PRIVATE_KEY**
```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAACFwAAAAdzc2gtcn
NhAAAAAwEAAQAAAgEA5+FH7g/HkYEKMfhAxDQKG7YdPhRivhnrZsBgAwiuYF38LAOW2znB
[... rest of the private key ...]
-----END OPENSSH PRIVATE KEY-----
```

#### **SSH_USER**
```
zebra
```

#### **REMOTE_HOST**
```
[YOUR_UBUNTU_MACHINE_IP]
```

### 3. **Get Your Ubuntu Machine IP**

On your Ubuntu machine, run:
```bash
# Get local IP
ip addr show | grep "inet " | grep -v 127.0.0.1

# Or get external IP if accessible from internet
curl ifconfig.me
```

### 4. **Test SSH Connection**

From Windows PowerShell, test the connection:
```powershell
ssh -i $env:USERPROFILE\.ssh\github_actions_key zebra@[YOUR_UBUNTU_IP]
```

### 5. **Required GitHub Secrets Summary**

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `DOCKER_HUB_USERNAME` | `sagarbandagar` | Your Docker Hub username |
| `DOCKER_HUB_TOKEN` | `dckr_pat_...` | Your Docker Hub access token |
| `SSH_PRIVATE_KEY` | `-----BEGIN OPENSSH...` | Private key for SSH access |
| `SSH_USER` | `zebra` | Username on Ubuntu machine |
| `REMOTE_HOST` | `[IP_ADDRESS]` | IP address of Ubuntu machine |

### 6. **Deploy Flow**

1. **Push code** → Triggers GitHub Actions
2. **Build & Push** → Docker images to Docker Hub
3. **SSH Deploy** → Connect to Ubuntu machine
4. **Update K8s** → Deploy new images to Minikube
5. **Verify** → Check pod status

✅ **Once setup is complete, every push to main will automatically deploy to your Kubernetes cluster!**