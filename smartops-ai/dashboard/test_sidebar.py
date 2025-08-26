import streamlit as st
from sidebar_utils import show_sidebar, get_anomaly_data, kill_pod, ignore_anomaly

st.set_page_config(
    page_title="Sidebar Test - SmartOps",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Show the sidebar
show_sidebar()

# Main content
st.title("🧪 Sidebar Anomaly Notifications Test")
st.markdown("This page tests the sidebar anomaly notification system.")

# Test anomaly data
st.header("📊 Test Anomaly Data")
st.markdown("Click the button below to test fetching anomaly data from the database.")

if st.button("🔍 Test Fetch Anomalies"):
    anomalies = get_anomaly_data()
    if not anomalies.empty:
        st.success(f"✅ Found {len(anomalies)} anomalies!")
        st.dataframe(anomalies)
    else:
        st.warning("⚠️ No anomalies found or database connection failed")

# Test pod killing
st.header("🗑️ Test Pod Killing")
st.markdown("Test the pod killing functionality (be careful!)")

pod_name = st.text_input("Enter pod name to kill:", "stress-test")
namespace = st.text_input("Enter namespace:", "smartops")

if st.button("🚨 Test Kill Pod"):
    if pod_name:
        success, message = kill_pod(pod_name, namespace)
        if success:
            st.success(message)
        else:
            st.error(message)
    else:
        st.error("Please enter a pod name")

# Test ignore functionality
st.header("👁️ Test Ignore Anomaly")
st.markdown("Test ignoring anomalies")

ignore_pod = st.text_input("Enter pod name to ignore:", "stress-test")
if st.button("👁️ Test Ignore"):
    if ignore_pod:
        ignore_anomaly(ignore_pod)
        st.success(f"Pod {ignore_pod} marked as ignored")
        st.rerun()
    else:
        st.error("Please enter a pod name")

# Show current ignored anomalies
st.header("📋 Current Ignored Anomalies")
ignored = st.session_state.get('ignored_anomalies', set())
if ignored:
    for pod in ignored:
        st.info(f"👁️ {pod} (ignored)")
else:
    st.info("No anomalies are currently ignored")

# Database connection test
st.header("🔌 Database Connection Test")
st.markdown("Test different database paths")

db_paths = [
    '/app/dashboard/data/data.db',
    'smartops-ai/dashboard/data/data.db',
    'data/data.db',
    'dashboard/data/data.db'
]

for db_path in db_paths:
    try:
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM anomalies")
        count = cursor.fetchone()[0]
        conn.close()
        st.success(f"✅ {db_path}: {count} records")
    except Exception as e:
        st.error(f"❌ {db_path}: {str(e)}")

# Manual anomaly creation for testing
st.header("➕ Create Test Anomaly")
st.markdown("Create a test anomaly entry for testing")

if st.button("➕ Add Test Anomaly"):
    try:
        import sqlite3
        import datetime
        
        # Try to find a working database
        working_db = None
        for db_path in db_paths:
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='anomalies'")
                if cursor.fetchone():
                    working_db = db_path
                    conn.close()
                    break
                conn.close()
            except:
                continue
        
        if working_db:
            conn = sqlite3.connect(working_db)
            cursor = conn.cursor()
            
            # Insert test anomaly
            test_data = (
                datetime.datetime.now().isoformat(),
                0.95,  # 95% CPU
                1024 * 1024,  # 1MB memory
                'Anomaly detected',
                'test-pod',
                '{"app": "test"}'
            )
            
            cursor.execute("""
                INSERT INTO anomalies (timestamp, cpu, memory, prediction, pod_name, labels)
                VALUES (?, ?, ?, ?, ?, ?)
            """, test_data)
            
            conn.commit()
            conn.close()
            st.success(f"✅ Test anomaly added to {working_db}")
        else:
            st.error("❌ No working database found")
            
    except Exception as e:
        st.error(f"❌ Error creating test anomaly: {str(e)}")

st.markdown("---")
st.markdown("**Note:** This is a test page. Use it to verify that the sidebar anomaly notifications are working correctly.")
