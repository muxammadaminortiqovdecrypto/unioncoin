// UnionCoin Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize animations
    initAnimations();
    
    // Initialize form validations
    initFormValidations();
    
    // Initialize wallet address copying
    initWalletCopy();
    
    // Initialize transaction form
    initTransactionForm();
});

// Animations
function initAnimations() {
    // Fade in elements
    const fadeElements = document.querySelectorAll('.card, .stat-card, .transaction-item');
    fadeElements.forEach((el, index) => {
        setTimeout(() => {
            el.classList.add('fade-in');
        }, index * 100);
    });
}

// Form validations
function initFormValidations() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (validateForm(form)) {
                submitForm(form);
            }
        });
    });
}

function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('.form-control');
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            showError(input, 'This field is required');
            isValid = false;
        } else {
            clearError(input);
        }
        
        // Special validation for wallet address
        if (input.name === 'wallet_address' && input.value.trim()) {
            if (!isValidWalletAddress(input.value.trim())) {
                showError(input, 'Invalid wallet address format');
                isValid = false;
            }
        }
        
        // Special validation for amount
        if (input.name === 'amount' && input.value.trim()) {
            const amount = parseFloat(input.value);
            if (isNaN(amount) || amount <= 0) {
                showError(input, 'Amount must be greater than 0');
                isValid = false;
            }
        }
    });
    
    return isValid;
}

function isValidWalletAddress(address) {
    // Check if address is 12 characters alphanumeric
    return /^[a-z0-9]{12}$/i.test(address);
}

function showError(input, message) {
    clearError(input);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.style.color = 'var(--danger-color)';
    errorDiv.style.fontSize = '0.9rem';
    errorDiv.style.marginTop = '5px';
    errorDiv.textContent = message;
    
    input.style.borderColor = 'var(--danger-color)';
    input.parentNode.appendChild(errorDiv);
}

function clearError(input) {
    input.style.borderColor = '';
    const errorDiv = input.parentNode.querySelector('.error-message');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Form submission
async function submitForm(form) {
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    
    // Show loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = originalText + '<span class="spinner"></span>';
    
    try {
        const formData = new FormData(form);
        const response = await fetch(form.action, {
            method: form.method,
            body: formData
        });
        
        if (response.ok) {
            showSuccess('Operation completed successfully!');
            form.reset();
            
            // If it's a transaction form, refresh the page after a delay
            if (form.action.includes('/send')) {
                setTimeout(() => {
                    window.location.reload();
                }, 2000);
            }
        } else {
            showError('Something went wrong. Please try again.');
        }
    } catch (error) {
        showError('Network error. Please check your connection.');
    } finally {
        // Reset button state
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
}

// Wallet address copying
function initWalletCopy() {
    const walletElements = document.querySelectorAll('.wallet-address, [data-wallet]');
    
    walletElements.forEach(element => {
        element.style.cursor = 'pointer';
        element.title = 'Click to copy';
        
        element.addEventListener('click', function() {
            const address = this.textContent || this.getAttribute('data-wallet');
            copyToClipboard(address);
        });
    });
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showSuccess('Wallet address copied to clipboard!');
    }).catch(() => {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showSuccess('Wallet address copied to clipboard!');
    });
}

// Transaction form
function initTransactionForm() {
    const receiverInput = document.querySelector('input[name="receiver_wallet"]');
    const amountInput = document.querySelector('input[name="amount"]');
    const balanceDisplay = document.querySelector('.balance-display');
    
    if (receiverInput && amountInput && balanceDisplay) {
        // Get current balance
        const currentBalance = parseFloat(balanceDisplay.textContent.replace(/[^\d.-]/g, ''));
        
        amountInput.addEventListener('input', function() {
            const amount = parseFloat(this.value);
            
            if (amount > currentBalance) {
                showError(this, 'Insufficient balance');
                this.value = currentBalance;
            }
        });
    }
}

// Toast notifications
function showSuccess(message) {
    showToast(message, 'success');
}

function showError(message) {
    showToast(message, 'error');
}

function showToast(message, type = 'info') {
    // Remove existing toasts
    const existingToast = document.querySelector('.toast');
    if (existingToast) {
        existingToast.remove();
    }
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
        max-width: 300px;
    `;
    
    if (type === 'success') {
        toast.style.background = 'var(--success-color)';
    } else if (type === 'error') {
        toast.style.background = 'var(--danger-color)';
    } else {
        toast.style.background = 'var(--primary-color)';
    }
    
    toast.textContent = message;
    document.body.appendChild(toast);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

// Real-time updates (if needed)
function startRealTimeUpdates() {
    // Update balance every 30 seconds
    setInterval(async () => {
        try {
            const response = await fetch('/api/balance');
            const data = await response.json();
            
            const balanceDisplay = document.querySelector('.balance-display');
            if (balanceDisplay && data.balance !== undefined) {
                balanceDisplay.textContent = `${data.balance.toFixed(2)} UC`;
                balanceDisplay.classList.add('success-animation');
                setTimeout(() => {
                    balanceDisplay.classList.remove('success-animation');
                }, 600);
            }
        } catch (error) {
            console.log('Failed to update balance:', error);
        }
    }, 30000);
}

// Initialize real-time updates if on dashboard
if (window.location.pathname.includes('/dashboard') || 
    window.location.pathname.includes('/login')) {
    startRealTimeUpdates();
}
