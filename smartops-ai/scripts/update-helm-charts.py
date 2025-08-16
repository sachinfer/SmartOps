#!/usr/bin/env python3
"""
Automated Helm Charts Updater for SmartOps
This script automatically updates image tags in helm-charts repository and pushes changes
to trigger ArgoCD auto-deploy. Run this after building new Docker images.
"""

import os
import sys
import subprocess
import json
import yaml
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import argparse

class HelmChartsUpdater:
    def __init__(self, helm_charts_repo, helm_charts_path, git_user, git_email):
        self.helm_charts_repo = helm_charts_repo
        self.helm_charts_path = helm_charts_path
        self.git_user = git_user
        self.git_email = git_email
        self.temp_dir = None
        
    def setup_git_config(self):
        """Configure git user and email for commits"""
        print("🔧 Setting up git configuration...")
        subprocess.run(["git", "config", "user.name", self.git_user], check=True)
        subprocess.run(["git", "config", "user.email", self.git_email], check=True)
        
    def clone_helm_charts_repo(self):
        """Clone the helm-charts repository to a temporary directory"""
        print(f"📥 Cloning helm-charts repository: {self.helm_charts_repo}")
        self.temp_dir = tempfile.mkdtemp(prefix="helm-charts-")
        
        subprocess.run([
            "git", "clone", 
            "--depth", "1",
            self.helm_charts_repo, 
            self.temp_dir
        ], check=True)
        
        print(f"✅ Repository cloned to: {self.temp_dir}")
        
    def get_latest_image_tags(self):
        """Get the latest image tags from your container registry"""
        print("🔍 Getting latest image tags...")
        
        # You can customize this to get tags from your specific registry
        # For now, using a timestamp-based tag
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        
        tags = {
            "smartops-anomaly": f"v1.0.{timestamp}",
            "smartops-dashboard": f"v1.0.{timestamp}",
            "smartops-monitor": f"v1.0.{timestamp}"
        }
        
        print(f"📋 Latest tags: {tags}")
        return tags
        
    def update_values_files(self, tags):
        """Update values.yaml files with new image tags"""
        print("📝 Updating values.yaml files...")
        
        for app_name, tag in tags.items():
            values_file = Path(self.temp_dir) / "smartops" / app_name / "values.yaml"
            
            if values_file.exists():
                print(f"  Updating {app_name} with tag: {tag}")
                
                # Read current values
                with open(values_file, 'r') as f:
                    values = yaml.safe_load(f)
                
                # Update image tag
                if 'image' in values:
                    values['image']['tag'] = tag
                    
                    # Write updated values
                    with open(values_file, 'w') as f:
                        yaml.dump(values, f, default_flow_style=False, indent=2)
                        
                    print(f"    ✅ Updated {app_name} to tag: {tag}")
            else:
                print(f"    ⚠️  Values file not found: {values_file}")
                
    def commit_and_push_changes(self, tags):
        """Commit and push changes to trigger ArgoCD auto-deploy"""
        print("🚀 Committing and pushing changes...")
        
        # Change to helm-charts directory
        os.chdir(self.temp_dir)
        
        # Add all changes
        subprocess.run(["git", "add", "."], check=True)
        
        # Create commit message
        commit_msg = f"🤖 Auto-update image tags: {', '.join([f'{k}={v}' for k, v in tags.items()])}"
        
        # Commit changes
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        
        # Push to main branch
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        print("✅ Changes pushed successfully!")
        print("🎯 ArgoCD will automatically detect changes and deploy!")
        
    def cleanup(self):
        """Clean up temporary directory"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            print(f"🧹 Cleaning up temporary directory: {self.temp_dir}")
            shutil.rmtree(self.temp_dir)
            
    def run(self):
        """Main execution method"""
        try:
            print("🚀 Starting automated Helm Charts update...")
            print(f"📁 Helm Charts Repo: {self.helm_charts_repo}")
            print(f"📂 Helm Charts Path: {self.helm_charts_path}")
            
            self.setup_git_config()
            self.clone_helm_charts_repo()
            tags = self.get_latest_image_tags()
            self.update_values_files(tags)
            self.commit_and_push_changes(tags)
            
            print("\n🎉 Success! Your helm-charts have been updated and pushed!")
            print("🔄 ArgoCD will automatically sync and deploy the new versions!")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git operation failed: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            sys.exit(1)
        finally:
            self.cleanup()

def main():
    parser = argparse.ArgumentParser(description="Automated Helm Charts Updater for SmartOps")
    parser.add_argument("--helm-repo", default="https://github.com/sachinfer/helm-charts.git",
                       help="Helm charts repository URL")
    parser.add_argument("--helm-path", default="smartops",
                       help="Path to smartops charts in helm-charts repo")
    parser.add_argument("--git-user", default="SmartOps Bot",
                       help="Git username for commits")
    parser.add_argument("--git-email", default="bot@smartops.ai",
                       help="Git email for commits")
    
    args = parser.parse_args()
    
    updater = HelmChartsUpdater(
        helm_charts_repo=args.helm_repo,
        helm_charts_path=args.helm_path,
        git_user=args.git_user,
        git_email=args.git_email
    )
    
    updater.run()

if __name__ == "__main__":
    main()
