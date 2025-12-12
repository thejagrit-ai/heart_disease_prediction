/**
 * Heart Disease Prediction System - Frontend JavaScript
 * Project: Heart Disease Prediction using Machine Learning
 * Developers: Jagrit Sharma, Abhishek Godara, Deepanshu
 * Supervisor: Dr. Megha Chhabra
 */

// Configuration
const API_URL = 'http://localhost:5000/api';
let isAdminLoggedIn = false;
let adminUsername = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadSection('home');
    setupEventListeners();

    // Show home section by default
    document.getElementById('home').classList.add('active');
});

// Setup Event Listeners
function setupEventListeners() {
    const predictionForm = document.getElementById('prediction-form');
    if (predictionForm) {
        predictionForm.addEventListener('submit', handlePredictionSubmit);
    }

    const adminForm = document.getElementById('admin-form');
    if (adminForm) {
        adminForm.addEventListener('submit', handleAdminLogin);
    }
}

// Load different sections
function loadSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.remove('active');
    });

    // Show selected section
    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.classList.add('active');
        window.scrollTo(0, 0);
    }

    // Load data for specific sections
    if (sectionId === 'disease-info') {
        loadDiseaseInfo();
    } else if (sectionId === 'developers') {
        loadDevelopersInfo();
    }
}

// Handle Prediction Form Submission
async function handlePredictionSubmit(event) {
    event.preventDefault();

    // Get form data
    const formData = new FormData(document.getElementById('prediction-form'));
    const data = {
        age: parseFloat(formData.get('age')),
        sex: parseFloat(formData.get('sex')),
        cp: parseFloat(formData.get('cp')),
        trestbps: parseFloat(formData.get('trestbps')),
        chol: parseFloat(formData.get('chol')),
        fbs: parseFloat(formData.get('fbs')),
        restecg: parseFloat(formData.get('restecg')),
        thalach: parseFloat(formData.get('thalach')),
        exang: parseFloat(formData.get('exang')),
        oldpeak: parseFloat(formData.get('oldpeak')),
        slope: parseFloat(formData.get('slope')),
        ca: parseFloat(formData.get('ca')),
        thal: parseFloat(formData.get('thal'))
    };

    // Validate data
    if (!validateInput(data)) {
        alert('Please fill all fields with valid values');
        return;
    }

    // Show loading spinner
    document.getElementById('loading-spinner').style.display = 'block';
    document.getElementById('result-container').style.display = 'none';

    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error('Prediction failed');
        }

        const result = await response.json();
        displayPredictionResult(result, data);

    } catch (error) {
        console.error('Error:', error);
        alert('Error processing prediction: ' + error.message);
    } finally {
        document.getElementById('loading-spinner').style.display = 'none';
    }
}

// Validate input data
function validateInput(data) {
    const rules = {
        age: [18, 120],
        sex: [0, 1],
        cp: [0, 3],
        trestbps: [80, 250],
        chol: [100, 600],
        fbs: [0, 1],
        restecg: [0, 2],
        thalach: [60, 220],
        exang: [0, 1],
        oldpeak: [0, 10],
        slope: [1, 3],
        ca: [0, 3],
        thal: [0, 2]
    };

    for (const [key, [min, max]] of Object.entries(rules)) {
        const value = data[key];
        if (isNaN(value) || value < min || value > max) {
            return false;
        }
    }
    return true;
}

// Display Prediction Result
function displayPredictionResult(result, inputData) {
    const riskLevel = result.risk_level;
    const riskColor = result.color;
    const probability = result.disease_probability;
    const noProbability = result.no_disease_probability;

    let riskClass = '';
    if (riskLevel === 'LOW RISK') {
        riskClass = 'risk-low';
    } else if (riskLevel === 'MODERATE RISK') {
        riskClass = 'risk-moderate';
    } else {
        riskClass = 'risk-high';
    }

    const resultHTML = `
        <div class="result-header">Heart Disease Risk Assessment Result</div>

        <div class="result-risk ${riskClass}">
            ${riskLevel}
        </div>

        <p style="text-align: center; font-size: 1rem; color: #666; margin: 1rem 0;">
            Based on your health parameters and medical indicators
        </p>

        <div class="probability-bars">
            <div class="probability-item">
                <div class="probability-label">
                    <span>Disease Probability</span>
                    <span>${probability.toFixed(2)}%</span>
                </div>
                <div class="probability-bar">
                    <div class="probability-fill" style="width: ${probability}%; background: #e74c3c;"></div>
                </div>
            </div>

            <div class="probability-item">
                <div class="probability-label">
                    <span>No Disease Probability</span>
                    <span>${noProbability.toFixed(2)}%</span>
                </div>
                <div class="probability-bar">
                    <div class="probability-fill" style="width: ${noProbability}%; background: #27ae60;"></div>
                </div>
            </div>
        </div>

        <div class="recommendations">
            <h3>📋 Personalized Recommendations:</h3>
            <ul>
                ${result.recommendation.map(rec => `<li>${rec}</li>`).join('')}
            </ul>
        </div>

        <div style="margin-top: 1.5rem; padding: 1rem; background-color: #fff3cd; border-radius: 8px; border-left: 4px solid #f39c12;">
            <strong>⚠️ Disclaimer:</strong> This prediction is for informational purposes only and should not be considered as medical advice. 
            Always consult with a qualified healthcare professional for accurate diagnosis and treatment. In case of emergency symptoms, 
            call emergency services immediately.
        </div>
    `;

    document.getElementById('result-card').innerHTML = resultHTML;
    document.getElementById('result-container').style.display = 'block';
}

// Admin Login
async function showAdminLogin() {
    document.getElementById('admin-modal').style.display = 'block';
}

function closeAdminModal() {
    document.getElementById('admin-modal').style.display = 'none';
    document.getElementById('admin-message').innerHTML = '';
}

window.onclick = function(event) {
    const modal = document.getElementById('admin-modal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}

async function handleAdminLogin(event) {
    event.preventDefault();

    const email = document.getElementById('admin-email').value;
    const password = document.getElementById('admin-password').value;

    // Create Basic Auth header
    const credentials = btoa(`${email}:${password}`);

    try {
        const response = await fetch(`${API_URL}/admin-login`, {
            method: 'POST',
            headers: {
                'Authorization': `Basic ${credentials}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            isAdminLoggedIn = true;
            adminUsername = email;

            // Hide modal and show admin panel
            closeAdminModal();
            document.getElementById('admin-panel').style.display = 'block';

            // Clear form
            document.getElementById('admin-form').reset();

            alert('Admin login successful!');
        } else {
            throw new Error('Invalid credentials');
        }
    } catch (error) {
        document.getElementById('admin-message').innerHTML = 
            '<p style="color: red;">❌ Login failed: Invalid credentials</p>';
    }
}

function logoutAdmin() {
    isAdminLoggedIn = false;
    adminUsername = null;
    document.getElementById('admin-panel').style.display = 'none';
    alert('Logged out successfully');
}

// Load Disease Information
async function loadDiseaseInfo() {
    try {
        const response = await fetch(`${API_URL}/info/disease-info`);
        const data = await response.json();

        // This data is already displayed in HTML, but could be dynamically updated if needed
        console.log('Disease information loaded');
    } catch (error) {
        console.error('Error loading disease info:', error);
    }
}

// Load Developers Information
async function loadDevelopersInfo() {
    try {
        const response = await fetch(`${API_URL}/info/developers`);
        const data = await response.json();

        console.log('Developers information loaded');
    } catch (error) {
        console.error('Error loading developers info:', error);
    }
}

// Tab switching for disease info
function switchTab(tabName) {
    // Hide all tab contents
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active class from all buttons
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    const selectedTab = document.getElementById(tabName);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }

    // Mark button as active
    event.target.classList.add('active');
}

// Utility function to format numbers
function formatNumber(num) {
    return num.toFixed(2);
}

console.log('%c❤️ Heart Disease Prediction System', 
    'color: #e74c3c; font-size: 16px; font-weight: bold;');
console.log('%cDevelopers: Jagrit Sharma, Abhishek Godara, Deepanshu', 
    'color: #3498db; font-size: 12px;');
console.log('%cVersion 1.0.0 - Production Ready', 
    'color: #27ae60; font-size: 12px;');
