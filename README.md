<p align="center">
  <img src="https://img.shields.io/badge/MediCore-Pro-00b4d8?style=for-the-badge&labelColor=030614&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzIiIGhlaWdodD0iMzIiIHZpZXdCb3g9IjAgMCAzMiAzMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB4PSIyIiB5PSIxMiIgd2lkdGg9IjI4IiBoZWlnaHQ9IjgiIHJ4PSIyIiBmaWxsPSIjMDBiNGQ4Ii8+PHJlY3QgeD0iMTIiIHk9IjIiIHdpZHRoPSI4IiBoZWlnaHQ9IjI4IiByeD0iMiIgZmlsbD0iIzAwYjRkOCIvPjwvc3ZnPg==" alt="MediCore Pro"/>
</p>

<h1 align="center">MediCore Pro</h1>

<p align="center">
  <strong>The Future of Hospital Management</strong><br>
  A futuristic, enterprise-grade Hospital Management SaaS platform with a stunning 3D landing page and production-ready Django backend.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Django-5.1-092E20?style=flat-square&logo=django" alt="Django"/>
  <img src="https://img.shields.io/badge/DRF-3.15-ff1709?style=flat-square&logo=django" alt="DRF"/>
  <img src="https://img.shields.io/badge/PostgreSQL-16-336791?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/Redis-7-DC382D?style=flat-square&logo=redis&logoColor=white" alt="Redis"/>
  <img src="https://img.shields.io/badge/Celery-5.4-37814A?style=flat-square&logo=celery" alt="Celery"/>
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="License"/>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-project-structure">Structure</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-api-endpoints">API</a> •
  <a href="#-deployment">Deployment</a> •
  <a href="#-security">Security</a>
</p>

---

## 🖼️ Preview

<table>
  <tr>
    <td width="50%">
      <strong>🌑 Dark Futuristic Landing Page</strong><br><br>
      ✦ 3D floating DNA helix animation<br>
      ✦ Heartbeat SVG line animation<br>
      ✦ Glassmorphism cards with neon glow<br>
      ✦ Animated stat counters<br>
      ✦ Particle background system<br>
      ✦ Pricing toggle (Monthly/Annual)
    </td>
    <td width="50%">
      <strong>⚙️ Enterprise Django Backend</strong><br><br>
      ✦ Multi-tenant architecture<br>
      ✦ JWT + MFA authentication<br>
      ✦ Role-based access control<br>
      ✦ Stripe & Razorpay payments<br>
      ✦ Real-time WebSocket notifications<br>
      ✦ Encrypted medical records
    </td>
  </tr>
</table>

---

## ✨ Features

### 🎨 Frontend — Futuristic Landing Page
- **Dark Navy/Black Theme** with neon blue (`#00b4d8`) and cyan (`#00ffcc`) accents
- **3D Medical Elements** — Rotating DNA helix, heartbeat line, floating pill capsules
- **40+ Animated Particles** floating in the background
- **Glassmorphism Design** — Frosted glass cards with blur and glow effects
- **Animated Counters** — 500+ Hospitals, 10K+ Doctors, 1M+ Patients, 99.9% Uptime
- **4 Feature Cards** — Patient Management, Doctor Scheduling, Billing System, Analytics Dashboard
- **3-Tier Pricing** — Basic ($49), Pro ($149), Enterprise (Custom) with monthly/annual toggle
- **Scroll Animations** — Intersection Observer-based reveal effects
- **Fully Responsive** — Desktop, tablet, and mobile layouts
- **Google Fonts** — Inter + Outfit for modern typography

### 🏗️ Backend — Production-Ready Django API
| Module | Description |
|--------|-------------|
| **🏥 Multi-Tenant** | Each hospital gets an isolated PostgreSQL schema via `django-tenants` |
| **👤 Authentication** | JWT access/refresh tokens with rotation & blacklisting |
| **🔐 MFA** | TOTP-based two-factor auth with QR code provisioning |
| **👥 RBAC** | 4 roles — Admin, Doctor, Staff, Patient — with granular permissions |
| **🧑‍⚕️ Patient Management** | Full CRUD with search, filter, EHR records, prescriptions |
| **📅 Appointments** | Smart scheduling with conflict detection, cancel/check-in actions |
| **💳 Billing** | Invoicing, Stripe hosted checkout (PCI-safe), webhook processing |
| **💰 Subscriptions** | Plan management with trial, upgrade, downgrade, cancel, renewal flows |
| **🔔 Real-Time** | Django Channels WebSocket for instant notifications |
| **📊 Analytics** | Pre-computed daily dashboard metrics via Celery tasks |
| **📝 Audit Logs** | Immutable trail of all sensitive operations with IP tracking |
| **🔒 Encryption** | AES (Fernet) encryption for diagnosis, notes, insurance data |
| **📁 File Storage** | AWS S3 with private ACL, extension whitelist, 10MB limit |

---

## 🛠️ Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | HTML5, CSS3 (Vanilla), JavaScript (ES6+) |
| **Backend** | Python 3.12, Django 5.1, Django REST Framework 3.15 |
| **Database** | PostgreSQL 16 (multi-tenant schemas) |
| **Cache** | Redis 7 |
| **Task Queue** | Celery 5.4 + Celery Beat |
| **WebSocket** | Django Channels + channels-redis |
| **Auth** | SimpleJWT + PyOTP (MFA) |
| **Payments** | Stripe + Razorpay |
| **Storage** | AWS S3 (django-storages) |
| **Monitoring** | Sentry SDK, django-health-check |
| **API Docs** | drf-spectacular (OpenAPI 3.0 / Swagger) |
| **Server** | Gunicorn + Nginx |
| **Container** | Docker + Docker Compose |

---

## 📁 Project Structure

```
medicore-pro/
│
├── frontend/                          # 🎨 Landing Page
│   ├── index.html                     # Main page with all sections
│   ├── css/styles.css                 # Design system, 3D animations, glassmorphism
│   └── js/main.js                     # Particles, DNA helix, counters, scroll FX
│
├── backend/                           # ⚙️ Django Backend
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env.example                   # Environment variable template
│   │
│   ├── medicore/                      # Project configuration
│   │   ├── __init__.py                # Celery app loader
│   │   ├── celery.py                  # Task queue + beat schedule
│   │   ├── asgi.py                    # ASGI (HTTP + WebSocket)
│   │   ├── wsgi.py                    # WSGI entry point
│   │   ├── urls.py                    # Root URL router
│   │   └── settings/
│   │       ├── base.py                # Shared config (DB, JWT, REST, S3, Stripe)
│   │       ├── development.py         # Debug mode, console email, CORS open
│   │       └── production.py          # HSTS, Sentry, secure cookies
│   │
│   └── apps/
│       ├── core/                      # Shared utilities
│       │   ├── exceptions.py          # RBAC permissions, AES encryption, error handler
│       │   └── tasks.py               # Celery background jobs
│       ├── hospitals/                 # Tenant model (Hospital, Department, Domain)
│       ├── users/                     # Custom User, JWT auth, MFA, profile
│       ├── patients/                  # Patient, MedicalRecord, Prescription
│       ├── doctors/                   # Doctor, DoctorSchedule, DoctorLeave
│       ├── appointments/              # Appointment CRUD with conflict detection
│       ├── billing/                   # Invoice, Payment, Stripe/Razorpay webhooks
│       ├── subscriptions/             # Plan, Subscription, lifecycle events
│       ├── notifications/             # WebSocket consumer + JWT middleware
│       ├── analytics/                 # DailyAnalytics pre-computed snapshots
│       └── audit/                     # AuditLog model + auto-logging middleware
│
└── docker/                            # 🐳 Infrastructure
    ├── Dockerfile                     # Python 3.12 slim, non-root user
    ├── docker-compose.yml             # PostgreSQL, Redis, Django, Celery, Nginx
    └── nginx/nginx.conf               # Reverse proxy, security headers, WebSocket
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- PostgreSQL 16+
- Redis 7+
- Docker & Docker Compose (optional)

### Option 1: Local Development

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/medicore-pro.git
cd medicore-pro/backend

# Virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Environment variables
cp .env.example .env
# Edit .env — set DB_NAME, DB_USER, DB_PASSWORD, REDIS_URL

# Database setup
python manage.py migrate
python manage.py createsuperuser

# Run the server
python manage.py runserver

# In another terminal — start Celery worker
celery -A medicore worker -l info

# In another terminal — start Celery beat
celery -A medicore beat -l info
```

### View the Landing Page

```bash
# Serve the frontend locally
cd frontend
npx serve .
# Opens at http://localhost:3000
```

---

## 📡 API Endpoints

### 🔑 Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/register/` | User registration |
| `POST` | `/api/v1/auth/login/` | Get JWT token pair |
| `POST` | `/api/v1/auth/token/refresh/` | Refresh access token |
| `GET/PUT` | `/api/v1/auth/profile/` | View/update profile |
| `GET` | `/api/v1/auth/mfa/setup/` | Get TOTP secret + QR |
| `POST` | `/api/v1/auth/mfa/setup/` | Verify OTP & enable MFA |
| `POST` | `/api/v1/auth/password/change/` | Change password |

### 🧑‍⚕️ Core Resources
| Method | Endpoint | Description |
|--------|----------|-------------|
| `CRUD` | `/api/v1/patients/` | Patient management |
| `CRUD` | `/api/v1/patients/records/` | Medical records (EHR) |
| `CRUD` | `/api/v1/patients/prescriptions/` | Prescriptions |
| `CRUD` | `/api/v1/appointments/` | Appointment booking |
| `POST` | `/api/v1/appointments/{id}/cancel/` | Cancel appointment |
| `POST` | `/api/v1/appointments/{id}/check_in/` | Patient check-in |

### 💳 Billing & Subscriptions
| Method | Endpoint | Description |
|--------|----------|-------------|
| `CRUD` | `/api/v1/billing/invoices/` | Invoice management |
| `GET` | `/api/v1/billing/payments/` | Payment history |
| `POST` | `/api/v1/billing/checkout/` | Create Stripe checkout |
| `GET` | `/api/v1/subscriptions/plans/` | List plans (public) |
| `GET` | `/api/v1/subscriptions/current/` | Current subscription |
| `POST` | `/api/v1/subscriptions/change-plan/` | Upgrade/downgrade |
| `POST` | `/api/v1/subscriptions/cancel/` | Cancel subscription |

### 🔔 Real-Time & Docs
| Protocol | Endpoint | Description |
|----------|----------|-------------|
| `WS` | `/ws/notifications/` | WebSocket notifications |
| `POST` | `/webhooks/stripe/` | Stripe webhook |
| `POST` | `/webhooks/razorpay/` | Razorpay webhook |
| `GET` | `/api/docs/` | Swagger UI |
| `GET` | `/health/` | Health check |

---

## 🔐 Security

| Feature | Implementation |
|---------|---------------|
| **Authentication** | JWT (30min access + 7d refresh) with token blacklisting |
| **MFA** | TOTP via PyOTP with QR provisioning + backup codes |
| **Password** | PBKDF2 hashing, 10-char min, common password detection |
| **Encryption** | AES-128-CBC (Fernet) for diagnosis, notes, insurance numbers |
| **Tenant Isolation** | Separate PostgreSQL schemas per hospital |
| **RBAC** | 4 roles: Admin, Doctor, Staff, Patient |
| **Rate Limiting** | 30 req/min (anonymous), 120 req/min (authenticated) |
| **Transport** | HSTS preload, HTTPS redirect, secure cookies |
| **Headers** | CSP, X-Frame-Options DENY, X-Content-Type-Options nosniff |
| **Payment** | PCI-safe hosted checkout — zero card data stored |
| **Audit Trail** | Immutable logs with user, action, IP, user-agent, changes |
| **File Upload** | 10MB limit, extension whitelist (.pdf, .jpg, .png, .dcm) |
| **CSRF/XSS** | Django middleware + CSP headers |
| **Account Lock** | Auto-lock after failed login attempts |

---

## 🗄️ Database Schema

```
┌─────────────┐     ┌──────────┐     ┌────────────────┐
│  Hospital    │────▶│   User   │────▶│    Doctor       │
│  (Tenant)    │     │  (RBAC)  │     │  (Profile)      │
└──────┬───────┘     └────┬─────┘     └───────┬─────────┘
       │                  │                    │
       ▼                  ▼                    ▼
┌─────────────┐     ┌──────────┐     ┌────────────────┐
│ Department  │     │ Patient  │────▶│  Appointment    │
│             │     │          │     │  (Scheduling)   │
└─────────────┘     └────┬─────┘     └────────────────┘
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
        ┌──────────┐ ┌────────┐ ┌──────────┐
        │ Medical  │ │Invoice │ │Prescrip- │
        │ Record   │ │        │ │tion      │
        └──────────┘ └───┬────┘ └──────────┘
                         ▼
                    ┌──────────┐
                    │ Payment  │
                    └──────────┘

┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Subscription │  │ Notification │  │  Audit Log   │
│ + Plan       │  │ (WebSocket)  │  │ (Immutable)  │
└──────────────┘  └──────────────┘  └──────────────┘
```

**12 Core Models:** Hospital, User, Doctor, Patient, Appointment, MedicalRecord, Prescription, Invoice, Payment, Subscription, Notification, AuditLog

---

## ☁️ Deployment

### Frontend → Netlify (Free)
1. Push repo to GitHub
2. Go to [netlify.com](https://netlify.com) → Import project
3. Set **Base directory**: `frontend`
4. Set **Publish directory**: `frontend`
5. Deploy ✅

### Backend → Render (Free Tier)
1. Go to [render.com](https://render.com) → New Web Service
2. Connect GitHub repo → Set root to `backend`
3. **Build**: `pip install -r requirements.txt`
4. **Start**: `gunicorn medicore.wsgi:application`
5. Add PostgreSQL database + environment variables
6. Deploy ✅

### Backend → Docker (Self-Hosted)
```bash
cd docker
docker-compose up --build -d
```

---

## ⚙️ Background Jobs

| Task | Schedule | Description |
|------|----------|-------------|
| `send_appointment_reminders` | Every 15 min | Notify patients of upcoming appointments |
| `check_subscription_renewals` | Every hour | Expire cancelled subscriptions at period end |
| `generate_daily_analytics` | Daily | Pre-compute dashboard KPIs |
| `cleanup_expired_tokens` | Every hour | Remove blacklisted JWT tokens |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Rajeev Swami**

- GitHub: [@rajeevswami](https://github.com/rajeevswami)

---

<p align="center">
  <strong>⭐ Star this repo if you found it useful!</strong><br><br>
  <img src="https://img.shields.io/badge/Built%20with-❤️-ff0000?style=for-the-badge" alt="Built with love"/>
  <img src="https://img.shields.io/badge/Powered%20by-Django-092E20?style=for-the-badge&logo=django" alt="Django"/>
  <img src="https://img.shields.io/badge/Styled%20with-CSS3-1572B6?style=for-the-badge&logo=css3" alt="CSS3"/>
</p>
