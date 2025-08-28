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
from sidebar_utils import show_sidebar

# Page configuration
st.set_page_config(
    page_title="Misi 24x7 - AI-Powered Solutions",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS with glassmorphism and animations
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    padding: 6rem 3rem;
    border-radius: 30px;
    margin: 2rem 0;
    text-align: center;
    color: white;
    box-shadow: 0 30px 60px rgba(102, 126, 234, 0.4);
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
    opacity: 0.3;
}

.main-header h1 {
    font-size: 4.5rem;
    margin-bottom: 1.5rem;
    font-weight: 900;
    text-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
    position: relative;
    z-index: 2;
}

.main-header p {
    font-size: 1.8rem;
    opacity: 0.95;
    margin: 0;
    font-weight: 600;
    text-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    position: relative;
    z-index: 2;
}

.section-header {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 4rem 0 3rem 0;
    text-align: center;
    position: relative;
}

.section-header::after {
    content: '';
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 80px;
    height: 4px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 2px;
}

.glass-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 25px;
    padding: 2.5rem;
    margin: 1rem 0;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
}

.glass-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    transition: left 0.5s;
}

.glass-card:hover::before {
    left: 100%;
}

.glass-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 30px 60px rgba(0, 0, 0, 0.15);
    border-color: rgba(255, 255, 255, 0.3);
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin: 3rem 0;
}

.feature-card {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.7));
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 25px;
    padding: 3rem 2rem;
    text-align: center;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
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
    transform: translateY(-15px) scale(1.03);
    box-shadow: 0 35px 70px rgba(0, 0, 0, 0.15);
}

.feature-icon {
    font-size: 4rem;
    margin-bottom: 1.5rem;
    display: block;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.feature-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #2d3748;
    margin-bottom: 1.5rem;
}

.feature-description {
    color: #4a5568;
    line-height: 1.7;
    font-size: 1.1rem;
}

.stats-container {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
    border-radius: 25px;
    padding: 3rem;
    margin: 3rem 0;
}

.stat-card {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
    border: 1px solid rgba(102, 126, 234, 0.1);
}

.stat-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.12);
}

.stat-number {
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
}

.stat-label {
    font-size: 1.1rem;
    color: #4a5568;
    font-weight: 600;
}

.team-section {
    background: linear-gradient(135deg, rgba(247, 250, 252, 0.8), rgba(237, 242, 247, 0.8));
    border-radius: 25px;
    padding: 3rem;
    margin: 3rem 0;
}

.founder-card {
    background: white;
    border-radius: 25px;
    padding: 3rem 2rem;
    margin: 1.5rem 0;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
    text-align: center;
    transition: all 0.3s ease;
    border: 1px solid rgba(102, 126, 234, 0.1);
}

.founder-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 30px 60px rgba(0, 0, 0, 0.12);
}

.founder-avatar {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    margin: 0 auto 1.5rem auto;
    background: linear-gradient(135deg, #667eea, #764ba2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    color: white;
    box-shadow: 0 15px 30px rgba(102, 126, 234, 0.3);
}

.contact-section {
    background: linear-gradient(135deg, #2d3748, #4a5568);
    color: white;
    border-radius: 25px;
    padding: 4rem 3rem;
    margin: 3rem 0;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.contact-section::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
    animation: float 6s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(180deg); }
}

.contact-title {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 1.5rem;
    position: relative;
    z-index: 2;
}

.contact-description {
    font-size: 1.3rem;
    margin-bottom: 2.5rem;
    opacity: 0.9;
    position: relative;
    z-index: 2;
}

.cta-button {
    background: linear-gradient(135deg, #667eea, #764ba2);
    border: none;
    border-radius: 50px;
    padding: 1rem 3rem;
    font-size: 1.2rem;
    font-weight: 600;
    color: white;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 15px 30px rgba(102, 126, 234, 0.3);
    position: relative;
    z-index: 2;
}

.cta-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 20px 40px rgba(102, 126, 234, 0.4);
}

.footer {
    background: linear-gradient(135deg, #f7fafc, #edf2f7);
    border-radius: 25px;
    padding: 3rem;
    margin: 3rem 0;
    text-align: center;
    border: 1px solid rgba(102, 126, 234, 0.1);
}

.footer-text {
    font-size: 1.2rem;
    color: #4a5568;
    margin-bottom: 1rem;
    font-weight: 600;
}

.footer-copyright {
    font-size: 1rem;
    color: #718096;
    opacity: 0.8;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Responsive design */
@media (max-width: 768px) {
    .main-header h1 { font-size: 3rem; }
    .main-header p { font-size: 1.4rem; }
    .section-header { font-size: 2.5rem; }
    .feature-grid { grid-template-columns: 1fr; }
}
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Show static sidebar (never changes)
    show_sidebar()
    
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
            <p style="font-size: 1.4rem; line-height: 1.8; color: #2d3748; margin-bottom: 2rem;">
                Misi 24x7 is a cutting-edge technology company specializing in artificial intelligence, 
                machine learning, and innovative software solutions. We are committed to transforming 
                businesses through intelligent automation and data-driven insights.
            </p>
            <p style="font-size: 1.3rem; line-height: 1.7; color: #4a5568;">
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
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem;">
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
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
            <div class="founder-card">
                <div class="founder-avatar">👨‍💼</div>
                <h3 style="color: #2d3748; margin-bottom: 1rem; font-size: 1.5rem;">CEO & Founder</h3>
                <p style="color: #4a5568; line-height: 1.6;">
                    Visionary leader with over 15 years of experience in AI and technology. 
                    Passionate about innovation and committed to delivering exceptional value to clients.
                </p>
            </div>
            
            <div class="founder-card">
                <div class="founder-avatar">👩‍💻</div>
                <h3 style="color: #2d3748; margin-bottom: 1rem; font-size: 1.5rem;">CTO & Co-Founder</h3>
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
        <button class="cta-button" onclick="window.location.href='mailto:contact@misi24x7.com'">
            Get In Touch
        </button>
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
