# 🚀 Deployment Workflow Events System

## Overview
The Deployment Workflow Events system provides real-time tracking and monitoring of deployment activities across your Kubernetes clusters with **India Standard Time (IST)** timezone support.

## 🌟 Features

### ✅ Time Standard
- **India Standard Time (IST)** - Asia/Kolkata timezone (UTC+05:30)
- All timestamps displayed in 12-hour format with AM/PM
- Automatic timezone conversion for imported events

### 📊 Event Tracking
- **Success Events**: Successfully completed deployments
- **Failed Events**: Failed deployment attempts with error details
- **Started Events**: Deployment initiation events
- **Namespace Support**: Organize events by Kubernetes namespaces

### 🔍 Real-time Monitoring
- Live event count tracking
- New event detection and notifications
- Auto-refresh capabilities
- Search and filtering by status and message content

## 📁 File Structure

```
smartops-ai/dashboard/
├── data/
│   └── deployment_events.db          # SQLite database
├── pages/
│   └── 9_Deployments.py             # Main dashboard page
├── log_deployment_event.py           # Event logging script
├── add_deployment_event.py           # Interactive event adder
├── init_deployment_db.py             # Database initialization
└── DEPLOYMENT_EVENTS_README.md       # This file
```

## 🗄️ Database Schema

```sql
CREATE TABLE deployment_events (
    timestamp TEXT,      -- ISO format timestamp in IST
    status TEXT,         -- 'success', 'failed', or 'started'
    message TEXT,        -- Detailed deployment message
    namespace TEXT       -- Kubernetes namespace
);
```

## 🚀 Quick Start

### 1. Initialize Database
```bash
cd smartops-ai/dashboard
python init_deployment_db.py
```

### 2. Add New Events

#### Interactive Mode
```bash
python add_deployment_event.py
```

#### Command Line Mode
```bash
# Success event
python add_deployment_event.py success "Frontend deployed successfully" frontend

# Failed event
python add_deployment_event.py failed "Database connection timeout" database

# Started event
python add_deployment_event.py started "Deployment initiated" backend
```

### 3. View Dashboard
- Navigate to the **Deployments** page in your SmartOps dashboard
- View real-time deployment events with IST timestamps
- Filter by status, search messages, and analyze deployment patterns

## 📝 Event Logging

### Programmatic Logging
```python
from log_deployment_event import add_deployment_event

# Add a deployment event
add_deployment_event("success", "Service deployed", "production")
```

### Kubernetes Integration
```bash
# Log deployment success
python log_deployment_event.py success "Pod deployment completed" default

# Log deployment failure
python log_deployment_event.py failed "Image pull failed" frontend
```

## 🎯 Use Cases

### CI/CD Pipelines
- Track deployment success/failure rates
- Monitor deployment duration
- Identify common failure patterns

### Production Monitoring
- Real-time deployment status
- Incident response tracking
- Post-deployment verification

### Team Collaboration
- Deployment timeline visibility
- Status updates for stakeholders
- Historical deployment analysis

## 🔧 Configuration

### Timezone Settings
The system automatically uses **India Standard Time (IST)**:
- Timezone: `Asia/Kolkata`
- Offset: UTC+05:30
- Format: 12-hour with AM/PM

### Database Paths
The system checks multiple database locations:
1. `data/deployment_events.db` (local development)
2. `/app/dashboard/data/deployment_events.db` (Docker container)
3. `smartops-ai/dashboard/data/deployment_events.db` (relative path)

## 📊 Dashboard Features

### Real-time Metrics
- **Total Deployments**: Count of all tracked events
- **Success Rate**: Percentage of successful deployments
- **Failure Rate**: Percentage of failed deployments
- **Current Time**: Live IST time display

### Event Filtering
- Filter by status (success/failed/started)
- Search within deployment messages
- Filter by namespace
- Date range selection

### Event Analysis
- Failed deployment details with expandable views
- Recent successful deployments
- Status distribution charts
- Top failure reasons

## 🚨 Troubleshooting

### Database Connection Issues
```bash
# Check if database exists
ls -la data/deployment_events.db

# Reinitialize database
python init_deployment_db.py
```

### Timezone Issues
- Ensure `pytz` package is installed
- Verify system timezone settings
- Check for daylight saving time conflicts

### Missing Events
- Verify database path in dashboard configuration
- Check file permissions for data directory
- Ensure logging scripts have write access

## 🔄 Maintenance

### Database Backup
```bash
# Backup database
cp data/deployment_events.db data/deployment_events_backup.db

# Restore database
cp data/deployment_events_backup.db data/deployment_events.db
```

### Cleanup Old Events
```sql
-- Remove events older than 30 days
DELETE FROM deployment_events 
WHERE timestamp < datetime('now', '-30 days');
```

### Performance Optimization
- Regular database maintenance
- Archive old events to separate tables
- Monitor database size and growth

## 📚 API Reference

### Event Status Values
- `success`: Deployment completed successfully
- `failed`: Deployment failed with error
- `started`: Deployment process initiated

### Timestamp Format
- **Input**: ISO format with timezone (e.g., `2025-08-30T12:12:43+05:30`)
- **Display**: Human-readable IST format (e.g., `2025-08-30 12:12:43 PM`)

### Namespace Convention
- Use descriptive namespace names
- Follow Kubernetes naming conventions
- Avoid special characters and spaces

## 🤝 Contributing

### Adding New Event Types
1. Update database schema in `init_deployment_db.py`
2. Modify dashboard display logic in `9_Deployments.py`
3. Update logging scripts to handle new fields
4. Test with sample data

### Custom Timezones
1. Modify timezone handling in relevant files
2. Update timestamp formatting functions
3. Test timezone conversion accuracy
4. Update documentation

## 📞 Support

For issues or questions:
1. Check this README for common solutions
2. Review the troubleshooting section
3. Check database connectivity and permissions
4. Verify timezone configuration

---

**Last Updated**: August 30, 2025  
**Version**: 1.0.0  
**Timezone**: India Standard Time (IST)  
**Status**: ✅ Production Ready
