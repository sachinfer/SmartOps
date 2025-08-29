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

# Import all page modules
try:
    import importlib.util
    import sys
    
    # Import pages using importlib to handle numeric filenames
    def import_page(module_name, function_name):
        spec = importlib.util.spec_from_file_location(
            module_name, 
            f"pages/{module_name}.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, function_name)
    
    show_overview = import_page("1_Overview", "show_page")
    show_pod_explorer = import_page("2_Pod_Explorer_and_Logs", "show_page")
    show_k8s_shell = import_page("3_Kubernetes_Shell_and_Cluster_Explorer", "show_page")
    show_anomaly_detection = import_page("4_Anomaly_Detection", "show_page")
    show_auto_scaling = import_page("5_Auto_Scaling_Recommendations_and_Control", "show_page")
    show_incident_timeline = import_page("6_Incident_Timeline_and_Postmortem_Report_Generator", "show_page")
    show_misi_ai = import_page("7_Misi_AI_Assistant", "show_page")
    show_ai_actions = import_page("8_AI_Actions", "show_page")
    show_deployments = import_page("9_Deployments", "show_page")
    
    PAGES_AVAILABLE = True
except ImportError as e:
    st.error(f"Error importing pages: {e}")
    PAGES_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Misi 24x7 - AI-Powered Solutions",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS with professional design
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Hero Section */
.hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    padding: 6rem 3rem;
    border-radius: 30px;
    margin: 2rem 0;
    text-align: center;
    color: white;
    position: relative;
    overflow: hidden;
    box-shadow: 0 25px 50px rgba(102, 126, 234, 0.3);
}

.hero-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
    opacity: 0.3;
}

.hero-title {
    font-size: 4rem;
    font-weight: 900;
    margin-bottom: 1.5rem;
    text-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
    position: relative;
    z-index: 2;
}

.hero-subtitle {
    font-size: 1.8rem;
    opacity: 0.95;
    margin-bottom: 2rem;
    font-weight: 600;
    text-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    position: relative;
    z-index: 2;
}

.hero-description {
    font-size: 1.2rem;
    opacity: 0.9;
    max-width: 800px;
    margin: 0 auto;
    line-height: 1.6;
    position: relative;
    z-index: 2;
}

/* Section Headers */
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

/* Content Cards */
.content-card {
    background: white;
    border-radius: 25px;
    padding: 3rem;
    margin: 2rem 0;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(102, 126, 234, 0.1);
    transition: all 0.3s ease;
}

.content-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 30px 60px rgba(0, 0, 0, 0.12);
}

/* Feature Grid */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
    margin: 3rem 0;
}

.feature-card {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.9));
    backdrop-filter: blur(20px);
    border: 1px solid rgba(102, 126, 234, 0.2);
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
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    transition: left 0.5s;
}

.feature-card:hover::before {
    left: 100%;
}

.feature-card:hover {
    transform: translateY(-15px) scale(1.02);
    box-shadow: 0 35px 70px rgba(0, 0, 0, 0.15);
    border-color: rgba(102, 126, 234, 0.4);
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

/* Stats Section */
.stats-container {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
    border-radius: 25px;
    padding: 3rem;
    margin: 3rem 0;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
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

/* Team Section */
.team-section {
    background: linear-gradient(135deg, rgba(247, 250, 252, 0.9), rgba(237, 242, 247, 0.9));
    border-radius: 25px;
    padding: 3rem;
    margin: 3rem 0;
}

.team-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

.team-card {
    background: white;
    border-radius: 25px;
    padding: 3rem 2rem;
    text-align: center;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
    border: 1px solid rgba(102, 126, 234, 0.1);
}

.team-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 30px 60px rgba(0, 0, 0, 0.12);
}

.team-avatar {
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

.team-name {
    color: #2d3748;
    margin-bottom: 0.5rem;
    font-size: 1.5rem;
    font-weight: 700;
}

.team-role {
    color: #667eea;
    margin-bottom: 1rem;
    font-size: 1.1rem;
    font-weight: 600;
}

.team-description {
    color: #4a5568;
    line-height: 1.6;
}

/* Contact Section */
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
    padding: 1.2rem 3rem;
    font-size: 1.2rem;
    font-weight: 600;
    color: white;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 15px 30px rgba(102, 126, 234, 0.3);
    position: relative;
    z-index: 2;
    text-decoration: none;
    display: inline-block;
}

.cta-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 20px 40px rgba(102, 126, 234, 0.4);
    color: white;
    text-decoration: none;
}

/* Footer */
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

/* Responsive Design */
@media (max-width: 768px) {
    .hero-title { font-size: 2.5rem; }
    .hero-subtitle { font-size: 1.4rem; }
    .section-header { font-size: 2.5rem; }
    .feature-grid { grid-template-columns: 1fr; }
    .hero-section { padding: 4rem 2rem; }
    .content-card { padding: 2rem; }
}
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    try:
        # Show static sidebar
        show_sidebar()
    except Exception as e:
        st.error(f"Sidebar error: {e}")
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Misi 24x7</h1>
        <p class="hero-subtitle">AI-Powered Solutions for the Digital Age</p>
        <p class="hero-description">
            Transforming businesses through intelligent automation, machine learning, and innovative software solutions. 
            We make advanced AI technology accessible to organizations of all sizes.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # About Us Section
    st.markdown('<div class="section-header">About Us</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-card">
        <div style="text-align: center; max-width: 1000px; margin: 0 auto;">
            <p style="font-size: 1.4rem; line-height: 1.8; color: #2d3748; margin-bottom: 2rem;">
                Misi 24x7 is a cutting-edge technology company at the forefront of artificial intelligence and 
                digital transformation. Founded with a vision to democratize AI technology, we specialize in 
                creating intelligent solutions that drive business growth and operational excellence.
            </p>
            <p style="font-size: 1.3rem; line-height: 1.7; color: #4a5568; margin-bottom: 2rem;">
                Our team of experts combines deep technical expertise with industry knowledge to deliver 
                solutions that not only meet current needs but anticipate future challenges. We believe in 
                building long-term partnerships with our clients, understanding their unique requirements, 
                and delivering tailored solutions that drive measurable results.
            </p>
            <p style="font-size: 1.2rem; line-height: 1.6; color: #4a5568;">
                From startups to enterprise organizations, we've helped businesses across various industries 
                leverage the power of AI to optimize operations, enhance customer experiences, and unlock 
                new opportunities for growth and innovation.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Core Services Section
    st.markdown('<div class="section-header">Our Core Services</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <div class="feature-title">AI & Machine Learning</div>
            <div class="feature-description">
                Custom AI solutions, predictive analytics, and intelligent automation systems that transform 
                your business operations. We develop machine learning models that learn from your data to 
                provide actionable insights and automate complex processes.
            </div>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">☁️</div>
            <div class="feature-title">Cloud Solutions</div>
            <div class="feature-description">
                Scalable cloud infrastructure, DevOps automation, and Kubernetes orchestration for modern, 
                resilient applications. We help you build, deploy, and manage cloud-native solutions that 
                scale with your business needs.
            </div>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Data Analytics</div>
            <div class="feature-description">
                Advanced data processing, real-time monitoring, and business intelligence solutions that 
                unlock actionable insights from your data. Transform raw data into strategic decisions 
                with our comprehensive analytics platform.
            </div>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">Cybersecurity</div>
            <div class="feature-description">
                Advanced threat detection, security automation, and compliance solutions to protect your 
                digital assets. Our AI-powered security systems provide 24/7 monitoring and rapid 
                response to emerging threats.
            </div>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">🚀</div>
            <div class="feature-title">Digital Transformation</div>
            <div class="feature-description">
                End-to-end digital transformation services that modernize your business processes and 
                technology stack. We guide you through every step of your digital journey with proven 
                methodologies and best practices.
            </div>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">💡</div>
            <div class="feature-title">Innovation Consulting</div>
            <div class="feature-description">
                Strategic consulting services to help you identify opportunities for innovation and 
                technology adoption. Our experts work closely with your team to develop roadmaps that 
                align with your business objectives.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Company Statistics Section
    st.markdown('<div class="section-header">Company Highlights</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="stats-container">
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">100+</div>
                <div class="stat-label">Happy Clients</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">250+</div>
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
            <div class="stat-card">
                <div class="stat-number">5+</div>
                <div class="stat-label">Years Experience</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">50+</div>
                <div class="stat-label">Team Members</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Leadership Team Section
    st.markdown('<div class="section-header">Leadership Team</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="team-section">
        <div class="team-grid">
            <div class="team-card">
                <div class="team-avatar">👨‍💼</div>
                <div class="team-name">Alex Chen</div>
                <div class="team-role">CEO & Founder</div>
                <div class="team-description">
                    Visionary leader with over 15 years of experience in AI and technology. 
                    Passionate about innovation and committed to delivering exceptional value to clients. 
                    Former senior executive at leading tech companies with expertise in scaling AI solutions.
                </div>
            </div>
            
            <div class="team-card">
                <div class="team-avatar">👩‍💻</div>
                <div class="team-name">Sarah Rodriguez</div>
                <div class="team-role">CTO & Co-Founder</div>
                <div class="team-description">
                    Technical expert specializing in scalable architectures and cutting-edge technologies. 
                    Leads our engineering team in creating innovative solutions. PhD in Computer Science 
                    with focus on distributed systems and machine learning.
                </div>
            </div>
            
            <div class="team-card">
                <div class="team-avatar">👨‍🔬</div>
                <div class="team-name">Dr. Michael Park</div>
                <div class="team-role">Chief AI Officer</div>
                <div class="team-description">
                    Leading researcher in artificial intelligence and machine learning. Oversees our AI 
                    strategy and ensures we stay at the forefront of technological innovation. 
                    Published author with numerous patents in AI applications.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Contact Section
    st.markdown("""
    <div class="contact-section">
        <h2 class="contact-title">Ready to Transform Your Business?</h2>
        <p class="contact-description">
            Let's discuss how Misi 24x7 can help you achieve your digital transformation goals. 
            Our team is ready to understand your challenges and create tailored solutions that drive results.
        </p>
        <a href="mailto:contact@misi24x7.com" class="cta-button">
            Get In Touch Today
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <div class="footer-text">🚀 Powered by Misi 24x7 - AI-Powered Solutions</div>
        <div class="footer-copyright">© 2024 Misi 24x7. All rights reserved. | Privacy Policy | Terms of Service</div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
