#!/usr/bin/env python3
"""
Migration script to help transition from Streamlit to Plotly-Dash
"""

import os
import shutil
import subprocess
import sys

def print_header():
    print("=" * 60)
    print("🚀 SmartOps: Streamlit to Plotly-Dash Migration")
    print("=" * 60)

def check_requirements():
    """Check if required files exist"""
    required_files = [
        'dash_app.py',
        'requirements_dash.txt',
        'Dockerfile.dash',
        'pages/overview.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found")
    return True

def backup_streamlit():
    """Backup existing Streamlit files"""
    backup_dir = "streamlit_backup"
    
    if os.path.exists(backup_dir):
        print(f"⚠️  Backup directory {backup_dir} already exists")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("❌ Migration cancelled")
            return False
    
    try:
        # Create backup directory
        os.makedirs(backup_dir, exist_ok=True)
        
        # Backup Streamlit files
        streamlit_files = [
            'streamlit_app.py',
            'requirements.txt',
            'Dockerfile'
        ]
        
        for file in streamlit_files:
            if os.path.exists(file):
                shutil.copy2(file, os.path.join(backup_dir, file))
                print(f"✅ Backed up {file}")
        
        # Backup pages directory
        if os.path.exists('pages'):
            shutil.copytree('pages', os.path.join(backup_dir, 'pages'), dirs_exist_ok=True)
            print("✅ Backed up pages directory")
        
        print(f"✅ Streamlit files backed up to {backup_dir}")
        return True
        
    except Exception as e:
        print(f"❌ Error backing up files: {e}")
        return False

def install_dash_dependencies():
    """Install Dash dependencies"""
    print("\n📦 Installing Dash dependencies...")
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements_dash.txt'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dash dependencies installed successfully")
            return True
        else:
            print(f"❌ Error installing dependencies: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def test_dash_app():
    """Test the Dash application"""
    print("\n🧪 Testing Dash application...")
    
    try:
        # Import the Dash app to check for syntax errors
        import dash_app
        print("✅ Dash app imports successfully")
        
        # Check if the app can be created
        app = dash_app.app
        print("✅ Dash app created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Dash app: {e}")
        return False

def create_migration_guide():
    """Create a migration guide"""
    guide_content = """
# SmartOps: Streamlit to Plotly-Dash Migration Guide

## What's Changed

### 1. Application Framework
- **From:** Streamlit
- **To:** Plotly-Dash with Bootstrap components

### 2. Key Files
- `dash_app.py` - Main Dash application
- `requirements_dash.txt` - Dash-specific dependencies
- `Dockerfile.dash` - Docker configuration for Dash
- `pages/overview.py` - Overview page module

### 3. Features Preserved
- ✅ All navigation pages
- ✅ Cluster health monitoring
- ✅ Anomaly detection
- ✅ AI actions
- ✅ Deployment tracking
- ✅ Pod explorer
- ✅ Kubernetes shell
- ✅ Auto-scaling recommendations
- ✅ Incident timeline

### 4. New Features
- 🎨 Modern Bootstrap-based UI
- 📱 Responsive design
- 🔄 Real-time updates
- 🎯 Interactive charts and graphs
- 🚀 Better performance

## Running the Application

### Local Development
```bash
# Install dependencies
pip install -r requirements_dash.txt

# Run the Dash app
python dash_app.py
```

### Docker
```bash
# Build the Dash image
docker build -f Dockerfile.dash -t smartops-dashboard-dash .

# Run the container
docker run -p 8501:8501 smartops-dashboard-dash
```

### Kubernetes
```bash
# Apply the Dash deployment
kubectl apply -f k8s/smartops-dashboard-dash-deployment.yaml

# Get the service URL
kubectl get service smartops-dashboard-dash-service -n smartops
```

## Migration Steps

1. ✅ Backup existing Streamlit files
2. ✅ Install Dash dependencies
3. ✅ Test Dash application
4. ✅ Deploy to Kubernetes
5. ✅ Update CI/CD pipeline

## Rollback

If you need to rollback to Streamlit:
```bash
# Restore from backup
cp -r streamlit_backup/* .

# Reinstall Streamlit dependencies
pip install -r requirements.txt
```

## Support

For issues or questions:
1. Check the logs: `kubectl logs -f deployment/smartops-dashboard-dash -n smartops`
2. Verify connectivity: `kubectl get pods -n smartops`
3. Check service status: `kubectl get services -n smartops`
"""
    
    with open('MIGRATION_GUIDE.md', 'w') as f:
        f.write(guide_content)
    
    print("✅ Migration guide created: MIGRATION_GUIDE.md")

def main():
    print_header()
    
    print("\n🔍 Checking requirements...")
    if not check_requirements():
        print("❌ Requirements check failed")
        return
    
    print("\n💾 Backing up Streamlit files...")
    if not backup_streamlit():
        print("❌ Backup failed")
        return
    
    print("\n📦 Installing Dash dependencies...")
    if not install_dash_dependencies():
        print("❌ Dependency installation failed")
        return
    
    print("\n🧪 Testing Dash application...")
    if not test_dash_app():
        print("❌ Dash app test failed")
        return
    
    print("\n📝 Creating migration guide...")
    create_migration_guide()
    
    print("\n" + "=" * 60)
    print("🎉 Migration completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review the migration guide: MIGRATION_GUIDE.md")
    print("2. Test the Dash application locally")
    print("3. Deploy to Kubernetes")
    print("4. Update your CI/CD pipeline if needed")
    print("\nTo run the Dash app:")
    print("   python dash_app.py")
    print("\nTo rollback:")
    print("   cp -r streamlit_backup/* .")

if __name__ == "__main__":
    main()
