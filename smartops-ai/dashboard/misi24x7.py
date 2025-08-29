#!/usr/bin/env python3
"""
Misi 24x7 - Modern Professional Company Page
"""

import streamlit as st
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import sidebar utilities
try:
    from sidebar_utils import show_sidebar
except ImportError:
    def show_sidebar():
        st.sidebar.title("SmartOps Dashboard")
        st.sidebar.info("Navigation menu will appear here")

# Page configuration
st.set_page_config(
    page_title="Misi 24x7 - AI-Powered Solutions",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS with improved Streamlit compatibility
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    padding: 4rem 2rem;
    border-radius: 20px;
    margin: 2rem 0;
    text-align: center;
    color: white;
    box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    position: relative;
    overflow: hidden;
}

.main-header h1 {
    font-size: 3.5rem;
    margin-bottom: 1rem;
    font-weight: 900;
    text-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    position: relative;
    z-index: 2;
}

.main-header p {
    font-size: 1.5rem;
    opacity: 0.95;
    margin: 0;
    font-weight: 600;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    position: relative;
    z-index: 2;
}

.section-header {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 3rem 0 2rem 0;
    text-align: center;
    position: relative;
}

.section-header::after {
    content: '';
    position: absolute;
    bottom: -8px;
    left: 50%;
    transform: translateX(-50%);
    width: 60px;
    height: 3px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 2px;
}

.glass-card {
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid rgba(102, 126, 234, 0.2);
    border-radius: 20px;
    padding: 2rem;
    margin: 1rem 0;
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    border-color: rgba(102, 126, 234, 0.4);
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.feature-card {
    background: white;
    border: 1px solid rgba(102, 126, 234, 0.2);
    border-radius: 20px;
    padding: 2rem 1.5rem;
    text-align: center;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
}

.feature-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    display: block;
}

.feature-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #2d3748;
    margin-bottom: 1rem;
}

.feature-description {
    color: #4a5568;
    line-height: 1.6;
    font-size: 1rem;
}

.stats-container {
    background: rgba(102, 126, 234, 0.05);
    border-radius: 20px;
    padding: 2rem;
    margin: 2rem 0;
}

.stat-card {
    background: white;
    border-radius: 15px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
    transition: all 0.3s ease;
    border: 1px solid rgba(102, 126, 234, 0.1);
}

.stat-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
}

.stat-number {
    font-size: 2.5rem;
    font-weight: 900;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
}

.stat-label {
    font-size: 1rem;
    color: #4a5568;
    font-weight: 600;
}

.team-section {
    background: rgba(247, 250, 252, 0.8);
    border-radius: 20px;
    padding: 2rem;
    margin: 2rem 0;
}

.founder-card {
    background: white;
    border-radius: 20px;
    padding: 2rem 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
    text-align: center;
    transition: all 0.3s ease;
    border: 1px solid rgba(102, 126, 234, 0.1);
}

.founder-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
}

.founder-avatar {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    margin: 0 auto 1rem auto;
    background: linear-gradient(135deg, #667eea, #764ba2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    color: white;
    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.contact-section {
    background: linear-gradient(135deg, #2d3748, #4a5568);
    color: white;
    border-radius: 20px;
    padding: 3rem 2rem;
    margin: 2rem 0;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.contact-title {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 1rem;
    position: relative;
    z-index: 2;
}

.contact-description {
    font-size: 1.2rem;
    margin-bottom: 2rem;
    opacity: 0.9;
    position: relative;
    z-index: 2;
}

.cta-button {
    background: linear-gradient(135deg, #667eea, #764ba2);
    border: none;
    border-radius: 50px;
    padding: 1rem 2.5rem;
    font-size: 1.1rem;
    font-weight: 600;
    color: white;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    position: relative;
    z-index: 2;
    text-decoration: none;
    display: inline-block;
}

.cta-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4);
    color: white;
    text-decoration: none;
}

.footer {
    background: rgba(247, 250, 252, 0.9);
    border-radius: 20px;
    padding: 2rem;
    margin: 2rem 0;
    text-align: center;
    border: 1px solid rgba(102, 126, 234, 0.1);
}

.footer-text {
    font-size: 1.1rem;
    color: #4a5568;
    margin-bottom: 0.5rem;
    font-weight: 600;
}

.footer-copyright {
    font-size: 0.9rem;
    color: #718096;
    opacity: 0.8;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Responsive design */
@media (max-width: 768px) {
    .main-header h1 { font-size: 2.5rem; }
    .main-header p { font-size: 1.2rem; }
    .section-header { font-size: 2rem; }
    .feature-grid { grid-template-columns: 1fr; }
    .main-header { padding: 3rem 1rem; }
}
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    try:
        # Show static sidebar (never changes)
        show_sidebar()
    except Exception as e:
        st.error(f"Sidebar error: {e}")
    
    # Hero Section with stunning gradient
    st.markdown("""
    <div class="main-header">
        <h1>Misi 24x7</h1>
        <p>AI-Powered Solutions for the Digital Age</p>
    </div>
    """, unsafe_allow_html=True)
    
    # About Us Section
    st.markdown('<div class="section-header">About Us</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        <div style="text-align: center; max-width: 900px; margin: 0 auto;">
            <p style="font-size: 1.3rem; line-height: 1.7; color: #2d3748; margin-bottom: 1.5rem;">
                Misi 24x7 is a cutting-edge technology company specializing in artificial intelligence, 
                machine learning, and innovative software solutions. We are committed to transforming 
                businesses through intelligent automation and data-driven insights.
            </p>
            <p style="font-size: 1.2rem; line-height: 1.6; color: #4a5568;">
                Our mission is to democratize AI technology and make advanced solutions accessible 
                to organizations of all sizes, enabling them to thrive in the digital economy.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Core Services with modern cards
    st.markdown('<div class="section-header">Our Core Services</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <div class="feature-title">AI & Machine Learning</div>
            <div class="feature-description">
                Custom AI solutions, predictive analytics, and intelligent automation systems 
                that transform your business operations and decision-making processes.
            </div>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">☁️</div>
            <div class="feature-title">Cloud Solutions</div>
            <div class="feature-description">
                Scalable cloud infrastructure, DevOps automation, and Kubernetes orchestration 
                for modern, resilient applications and services.
            </div>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Data Analytics</div>
            <div class="feature-description">
                Advanced data processing, real-time monitoring, and business intelligence 
                solutions that unlock actionable insights from your data.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Company Statistics with modern metrics
    st.markdown('<div class="section-header">Company Highlights</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="stats-container">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem;">
            <div class="stat-card">
                <div class="stat-number">50+</div>
                <div class="stat-label">Happy Clients</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">100+</div>
                <div class="stat-label">Projects Delivered</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">24/7</div>
                <div class="stat-label">Support Available</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">99.9%</div>
                <div class="stat-label">Uptime Guarantee</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Leadership Team
    st.markdown('<div class="section-header">Leadership Team</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="team-section">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem;">
            <div class="founder-card">
                <div class="founder-avatar">👨‍💼</div>
                <h3 style="color: #2d3748; margin-bottom: 1rem; font-size: 1.4rem;">CEO & Founder</h3>
                <p style="color: #4a5568; line-height: 1.6;">
                    Visionary leader with over 15 years of experience in AI and technology. 
                    Passionate about innovation and committed to delivering exceptional value to clients.
                </p>
            </div>
            
            <div class="founder-card">
                <div class="founder-avatar">👩‍💻</div>
                <h3 style="color: #2d3748; margin-bottom: 1rem; font-size: 1.4rem;">CTO & Co-Founder</h3>
                <p style="color: #4a5568; line-height: 1.6;">
                    Technical expert specializing in scalable architectures and cutting-edge technologies. 
                    Leads our engineering team in creating innovative solutions.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Contact Section with floating animation
    st.markdown("""
    <div class="contact-section">
        <h2 class="contact-title">Ready to Transform Your Business?</h2>
        <p class="contact-description">
            Let's discuss how Misi 24x7 can help you achieve your digital transformation goals.
        </p>
        <a href="mailto:contact@misi24x7.com" class="cta-button">
            Get In Touch
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <div class="footer-text">🚀 Powered by Misi 24x7 - AI-Powered Solutions</div>
        <div class="footer-copyright">© 2024 Misi 24x7. All rights reserved.</div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
