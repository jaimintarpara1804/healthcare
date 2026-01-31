# Healthcare Subscription System - Complete Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Features](#features)
4. [Installation & Setup](#installation--setup)
5. [User Roles & Permissions](#user-roles--permissions)
6. [Subscription Plans](#subscription-plans)
7. [API Documentation](#api-documentation)
8. [Security Features](#security-features)
9. [Deployment Guide](#deployment-guide)
10. [Troubleshooting](#troubleshooting)

## System Overview

The Healthcare Subscription System is a comprehensive Flask-based web application that provides controlled access to premium healthcare services through a subscription model. The system supports multiple user roles, advanced health tracking, AI-powered insights, telemedicine capabilities, and secure doctor-patient interactions.

### Key Components
- **Subscription Management**: Multi-tier subscription plans with feature-based access control
- **Role-Based Access Control**: Admin, Doctor, and User roles with specific permissions
- **Digital Health Twin**: AI-powered health simulation and tracking
- **Telemedicine**: Video consultation capabilities for Pro subscribers
- **Notification System**: WhatsApp, Email, and SMS notifications
- **Security Framework**: HIPAA-compliant data protection and encryption

## Architecture

### Technology Stack
- **Backend**: Flask (Python 3.11+)
- **Database**: SQLAlchemy with PostgreSQL (production) / SQLite (development)
- **Frontend**: Bootstrap 5, HTML5, JavaScript
- **Security**: Cryptography, Werkzeug security
- **Notifications**: WhatsApp Business API, SMTP, Twilio
- **Caching**: Redis (production)
- **Deployment**: Docker, Nginx, Gunicorn

### Database Schema
```
Users
├── Subscriptions (1:1)
├── HealthTwin (1:1)
├── HealthRecords (1:N)
├── HealthInsights (1:N)
├── HealthGoals (1:N)
├── Appointments (1:N)
├── Notifications (1:N)
└── DoctorProfile (1:1, if doctor)

Doctors
├── DoctorPatientAssignments (1:N)
└── Appointments (1:N)
```

## Features

### Core Features (All Plans)
- ✅ User registration and authentication
- ✅ BMI calculator
- ✅ Symptom checker
- ✅ Basic health tips
- ✅ Yoga and Ayurvedic recommendations
- ✅ Allopathic medicine suggestions

### Subscription Features

#### Free Plan
- Basic health tools
- 10 health records storage
- Limited access to features

#### Basic Plan ($9.99/month)
- AI health insights
- Digital Health Twin
- Wellness dashboard
- 100 health records
- Email notifications

#### Premium Plan ($19.99/month)
- Private doctor assignment
- WhatsApp notifications
- Priority support
- 500 health records
- Advanced analytics
- Health risk assessment

#### Pro Plan ($39.99/month)
- Video consultations (telemedicine)
- Unlimited health records
- 24/7 priority support
- Advanced AI features
- Health drift detection
- Personalized reports

## Installation & Setup

### Prerequisites
- Python 3.11+
- PostgreSQL (production) or SQLite (development)
- Redis (production)
- Node.js (for frontend dependencies)

### Development Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd healthcare-subscription-system
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set environment variables**
```bash
export FLASK_ENV=development
export SECRET_KEY=your-secret-key
export DATABASE_URL=sqlite:///healthcare.db
```

5. **Initialize database**
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

6. **Run the application**
```bash
python app.py
```

### Production Setup

1. **Use Docker Compose**
```bash
docker-compose up -d
```

2. **Or manual deployment**
```bash
# Install dependencies
pip install -r requirements.txt

# Set production environment variables
export FLASK_ENV=production
export DATABASE_URL=postgresql://user:password@localhost/healthcare
export REDIS_URL=redis://localhost:6379/0

# Run with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

## User Roles & Permissions

### Admin Role
- **Access**: Full system access
- **Capabilities**:
  - Manage all users and subscriptions
  - View system analytics
  - Assign doctors to patients
  - Monitor system health
  - Access audit logs

### Doctor Role
- **Access**: Assigned patients only
- **Capabilities**:
  - View patient health data
  - Manage appointments
  - Conduct video consultations
  - Send messages to patients
  - Update availability status

### User Role
- **Access**: Own data only
- **Capabilities**:
  - Manage personal health data
  - Book appointments
  - Access subscription features
  - Communicate with assigned doctor

## Subscription Plans

### Plan Comparison

| Feature | Free | Basic | Premium | Pro |
|---------|------|-------|---------|-----|
| BMI Calculator | ✅ | ✅ | ✅ | ✅ |
| Symptom Checker | ✅ | ✅ | ✅ | ✅ |
| Health Records | 10 | 100 | 500 | Unlimited |
| AI Insights | ❌ | ✅ | ✅ | ✅ |
| Digital Health Twin | ❌ | ✅ | ✅ | ✅ |
| Private Doctor | ❌ | ❌ | ✅ | ✅ |
| Video Consultations | ❌ | ❌ | ❌ | ✅ |
| WhatsApp Notifications | ❌ | ❌ | ✅ | ✅ |
| Priority Support | ❌ | ❌ | ✅ | ✅ |

### Subscription Management

#### Creating Subscriptions
```python
from subscription_manager import SubscriptionManager

# Create subscription
success, message = SubscriptionManager.create_subscription(
    user_id=1,
    plan=SubscriptionPlan.PREMIUM,
    is_yearly=True,
    payment_method="stripe",
    payment_id="pi_1234567890"
)
```

#### Checking Feature Access
```python
# Check if user can access feature
user = User.query.get(user_id)
can_access = user.can_access_feature('telemedicine')
```

## API Documentation

### Authentication Endpoints

#### POST /login_register
Register or login user
```json
{
  "action": "login|register",
  "email": "user@example.com",
  "password": "password123"
}
```

### Subscription Endpoints

#### GET /subscription/plans
Get available subscription plans

#### POST /subscription/subscribe
Subscribe to a plan
```json
{
  "plan": "premium",
  "billing": "monthly|yearly"
}
```

#### GET /subscription/dashboard
Get user subscription information

### Health Twin Endpoints

#### GET /api/health_twin/{user_id}
Get health twin data

#### POST /api/health_twin/{user_id}/update
Update health twin
```json
{
  "age": 30,
  "weight": 70,
  "height_cm": 175,
  "stress_level": 5,
  "sleep_quality": 8
}
```

#### GET /api/health_twin/{user_id}/insights
Get AI-generated health insights

### Notification Endpoints

#### POST /api/notifications/send
Send notification (testing)
```json
{
  "user_id": 1,
  "message": "Test notification",
  "channel": "email|whatsapp|sms"
}
```

### Doctor Endpoints

#### POST /api/doctor/toggle-availability
Toggle doctor availability
```json
{
  "available": true
}
```

#### GET /api/doctor/patients
Get assigned patients

## Security Features

### Data Protection
- **Encryption**: AES-256 encryption for sensitive health data
- **Password Security**: PBKDF2 with SHA-256 and salt
- **Session Management**: Secure session cookies with timeout
- **Rate Limiting**: API rate limiting to prevent abuse

### HIPAA Compliance
- **Audit Logging**: All PHI access is logged
- **Data Anonymization**: PII anonymization utilities
- **Access Controls**: Role-based access to patient data
- **Secure Communication**: Encrypted data transmission

### Authentication Security
- **Account Lockout**: Automatic lockout after failed attempts
- **Password Strength**: Enforced password complexity
- **Session Validation**: Regular session validation
- **Security Events**: Comprehensive security event logging

## Deployment Guide

### Docker Deployment

1. **Build and run with Docker Compose**
```bash
docker-compose up -d
```

2. **Environment Configuration**
Create `.env` file:
```env
FLASK_ENV=production
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:password@db:5432/healthcare
REDIS_URL=redis://redis:6379/0
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
WHATSAPP_TOKEN=your-whatsapp-token
```

### Manual Deployment

1. **Server Setup**
```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip postgresql redis-server nginx

# Create application user
sudo useradd -m -s /bin/bash healthcare
```

2. **Application Setup**
```bash
# Clone and setup application
sudo -u healthcare git clone <repo> /opt/healthcare
cd /opt/healthcare
sudo -u healthcare python3 -m venv venv
sudo -u healthcare ./venv/bin/pip install -r requirements.txt
```

3. **Database Setup**
```bash
# Create database
sudo -u postgres createdb healthcare
sudo -u postgres createuser healthcare_user
```

4. **Systemd Service**
```bash
# Copy service file
sudo cp healthcare.service /etc/systemd/system/
sudo systemctl enable healthcare
sudo systemctl start healthcare
```

5. **Nginx Configuration**
```bash
# Copy nginx config
sudo cp nginx.conf /etc/nginx/sites-available/healthcare
sudo ln -s /etc/nginx/sites-available/healthcare /etc/nginx/sites-enabled/
sudo systemctl reload nginx
```

## Troubleshooting

### Common Issues

#### Database Connection Errors
```bash
# Check database status
sudo systemctl status postgresql

# Check connection
psql -h localhost -U healthcare_user -d healthcare
```

#### Redis Connection Issues
```bash
# Check Redis status
sudo systemctl status redis

# Test connection
redis-cli ping
```

#### Email Notifications Not Working
1. Check SMTP settings in environment variables
2. Verify app password for Gmail
3. Check firewall settings for SMTP ports

#### WhatsApp Notifications Failing
1. Verify WhatsApp Business API token
2. Check phone number format
3. Ensure webhook is configured

### Performance Optimization

#### Database Optimization
```sql
-- Create indexes for better performance
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_subscription_user ON subscriptions(user_id);
CREATE INDEX idx_health_records_user_date ON health_records(user_id, record_date);
```

#### Caching Strategy
```python
# Use Redis for caching
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})

@cache.memoize(timeout=300)
def get_user_subscription_info(user_id):
    return SubscriptionManager.get_user_subscription_info(user_id)
```

### Monitoring and Logging

#### Application Monitoring
```python
# Sentry integration
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

#### Health Checks
```bash
# Application health check
curl http://localhost:5000/api/health

# Database health check
curl http://localhost:5000/api/health/database
```

## Support and Maintenance

### Regular Maintenance Tasks
1. **Database Backups**: Daily automated backups
2. **Log Rotation**: Weekly log cleanup
3. **Security Updates**: Monthly security patches
4. **Performance Monitoring**: Continuous monitoring
5. **Subscription Expiry**: Daily expiry checks

### Backup Strategy
```bash
# Database backup
pg_dump healthcare > backup_$(date +%Y%m%d).sql

# Application backup
tar -czf app_backup_$(date +%Y%m%d).tar.gz /opt/healthcare
```

### Update Procedure
1. **Backup current system**
2. **Test updates in staging**
3. **Deploy during maintenance window**
4. **Verify all services**
5. **Monitor for issues**

## License and Compliance

This system is designed to be HIPAA-compliant and suitable for healthcare applications. Ensure proper legal review and compliance verification before production deployment.

### Compliance Requirements
- HIPAA compliance documentation
- Data processing agreements
- Privacy policy and terms of service
- User consent mechanisms
- Data retention policies
- Incident response procedures

---

For additional support or questions, please refer to the project documentation or contact the development team.