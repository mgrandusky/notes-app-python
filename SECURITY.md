# Security Policy

## Supported Versions

Currently supported versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Security Updates

### Latest Security Patches (January 2024)

All security vulnerabilities have been addressed in the current version:

#### 1. Authlib Updated to 1.6.5

**Previous Version**: 1.3.0  
**Updated Version**: 1.6.5

**Vulnerabilities Fixed**:

- **CVE-2024-37568**: Denial of Service via Oversized JOSE Segments
  - Impact: DoS attack through malformed JWT tokens
  - Severity: High
  - Fixed in: 1.6.5

- **CVE-2024-26152**: JWS/JWT accepts unknown crit headers
  - Impact: RFC violation leading to possible authorization bypass
  - Severity: High
  - Fixed in: 1.6.4

- **Algorithm Confusion Vulnerability**
  - Impact: Algorithm confusion with asymmetric public keys
  - Severity: High
  - Fixed in: 1.3.1

#### 2. Gunicorn Updated to 22.0.0

**Previous Version**: 21.2.0  
**Updated Version**: 22.0.0

**Vulnerabilities Fixed**:

- **HTTP Request/Response Smuggling**
  - Impact: HTTP smuggling attacks could bypass security controls
  - Severity: High
  - Fixed in: 22.0.0

- **Request Smuggling Leading to Endpoint Restriction Bypass**
  - Impact: Attackers could bypass endpoint access restrictions
  - Severity: High
  - Fixed in: 22.0.0

## Security Best Practices

This application implements the following security measures:

### Authentication & Authorization
- OAuth 2.0 authentication (Google, GitHub)
- Secure session management with Flask-Login
- No passwords stored (OAuth only)
- HTTPOnly and Secure cookie flags
- SameSite cookie attribute

### Input Validation & Sanitization
- CSRF protection on all forms (Flask-WTF)
- XSS prevention with Bleach HTML sanitization
- SQL injection prevention via SQLAlchemy ORM
- Input validation for all user inputs

### Data Protection
- Sensitive data stored in environment variables
- Database credentials never committed to code
- Secure cookie configuration
- TLS/SSL recommended for production

### Dependency Management
- Regular dependency updates
- Security vulnerability scanning
- Automated dependency checks

## Reporting a Vulnerability

If you discover a security vulnerability, please follow these steps:

1. **Do Not** open a public issue
2. Email the security contact (if available) or create a private security advisory
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We aim to respond to security reports within 48 hours and provide a fix within 7 days for critical vulnerabilities.

## Security Checklist for Deployment

When deploying to production, ensure:

- [ ] All dependencies are up to date
- [ ] Environment variables are properly configured
- [ ] HTTPS/TLS is enabled
- [ ] `SESSION_COOKIE_SECURE=True` is set
- [ ] `FLASK_ENV=production` is set
- [ ] Database credentials are secured
- [ ] OAuth credentials are properly configured
- [ ] Regular security updates are scheduled
- [ ] Database backups are configured
- [ ] Rate limiting is implemented (recommended)
- [ ] Monitoring and logging are enabled

## Security Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/stable/security/)
- [OAuth 2.0 Security Best Current Practice](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)

## Update History

| Date | Component | Version | Security Fix |
|------|-----------|---------|--------------|
| 2024-01-18 | Authlib | 1.6.5 | DoS, JWT crit headers, algorithm confusion |
| 2024-01-18 | Gunicorn | 22.0.0 | HTTP request smuggling |

## Contact

For security concerns, please check the repository for security contact information or open a security advisory on GitHub.

---

Last Updated: January 18, 2024
