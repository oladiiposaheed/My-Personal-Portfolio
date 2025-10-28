// Portfolio JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling
    initializeSmoothScrolling();
    
    // Scroll animations
    initializeScrollAnimations();
    
    // Form enhancements
    initializeFormEnhancements();
    
    // Card interactions
    initializeCardInteractions();
});

// Function to handle smooth scrolling
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const navbarHeight = document.querySelector('.navbar').offsetHeight;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navbarHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all animated elements
    document.querySelectorAll('.fade-in').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease';
        observer.observe(el);
    });
}

function initializeFormEnhancements() {
    // Add focus effects to form inputs
    const inputs = document.querySelectorAll('.form-control');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });
    });
}

function initializeCardInteractions() {
    // Add hover effects to cards
    const cards = document.querySelectorAll('.project-card, .certification-card, .skill-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.zIndex = '10';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.zIndex = '';
        });
    });
}

// Loading animations
window.addEventListener('load', function() {
    document.body.classList.add('loaded');
    
    // Add loading animation to profile image
    const profileImage = document.querySelector('.profile-image');
    if (profileImage) {
        profileImage.style.opacity = '0';
        profileImage.style.transform = 'scale(0.8)';
        
        setTimeout(() => {
            profileImage.style.transition = 'all 0.6s ease';
            profileImage.style.opacity = '1';
            profileImage.style.transform = 'scale(1)';
        }, 300);
    }
});

// Utility function for copying text to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        // Show success message
        const btn = event.target.closest('button');
        if (btn) {
            const originalHTML = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-check"></i>';
            btn.classList.remove('btn-outline-info');
            btn.classList.add('btn-success');
            
            setTimeout(() => {
                btn.innerHTML = originalHTML;
                btn.classList.remove('btn-success');
                btn.classList.add('btn-outline-info');
            }, 2000);
        }
    }).catch(function(err) {
        console.error('Could not copy text: ', err);
        alert('Failed to copy text to clipboard');
    });
}

// Filter functionality for projects and certifications
function updateFilter(type, value) {
    const url = new URL(window.location.href);
    
    if (value === 'all') {
        url.searchParams.delete(type);
    } else {
        url.searchParams.set(type, value);
    }
    
    // Remove page parameter when changing filters
    url.searchParams.delete('page');
    
    window.location.href = url.toString();
}

// Image modal functionality
function openModal(imageUrl, caption) {
    const modal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    const modalTitle = document.getElementById('modalImageTitle');
    
    if (modal && modalImage && modalTitle) {
        modalImage.src = imageUrl;
        modalTitle.textContent = caption || 'Image';
        
        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();
    }
}

// Initialize tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Call initialization functions when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeTooltips();
});