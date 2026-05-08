/* ===== MediCore Pro — Main JavaScript ===== */

document.addEventListener('DOMContentLoaded', () => {
    initParticles();
    initDNAHelix();
    initScrollAnimations();
    initCounters();
    initNavbar();
    initPricingToggle();
    initMobileMenu();
});

/* ===== Particles Background ===== */
function initParticles() {
    const container = document.getElementById('particles');
    if (!container) return;
    for (let i = 0; i < 40; i++) {
        const p = document.createElement('div');
        p.className = 'particle';
        p.style.left = Math.random() * 100 + '%';
        p.style.animationDuration = (8 + Math.random() * 15) + 's';
        p.style.animationDelay = Math.random() * 10 + 's';
        p.style.width = p.style.height = (2 + Math.random() * 3) + 'px';
        container.appendChild(p);
    }
}

/* ===== 3D DNA Helix ===== */
function initDNAHelix() {
    const helix = document.getElementById('dnaHelix');
    if (!helix) return;
    const rungs = 16;
    for (let i = 0; i < rungs; i++) {
        const rung = document.createElement('div');
        rung.className = 'dna-rung';
        rung.style.top = (i * (360 / rungs) / 360 * 100) + '%';
        rung.style.transform = `translateY(${i * 22}px) rotateY(${i * (360/rungs)}deg)`;
        rung.style.transformStyle = 'preserve-3d';
        rung.innerHTML = `
            <div class="dna-sphere left"></div>
            <div class="dna-connector"></div>
            <div class="dna-sphere right"></div>
        `;
        helix.appendChild(rung);
    }
}

/* ===== Scroll Animations ===== */
function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));

    // Stat bar fills
    const statObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.3 });
    document.querySelectorAll('.stat-card').forEach(el => statObserver.observe(el));
}

/* ===== Animated Counters ===== */
function initCounters() {
    const counters = document.querySelectorAll('.stat-number');
    let animated = false;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !animated) {
                animated = true;
                counters.forEach(counter => animateCounter(counter));
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(c => observer.observe(c));
}

function animateCounter(el) {
    const target = parseInt(el.dataset.target);
    const display = el.dataset.display;
    const suffix = el.dataset.suffix || '';
    const duration = 2000;
    const start = performance.now();

    function update(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3); // easeOutCubic

        if (display && progress >= 1) {
            el.textContent = display;
            return;
        }

        const current = Math.floor(eased * target);

        if (target >= 1000000) {
            el.textContent = (current / 1000000).toFixed(1) + 'M' + suffix;
        } else if (target >= 10000) {
            el.textContent = (current / 1000).toFixed(current >= 10000 ? 0 : 1) + 'K' + suffix;
        } else {
            el.textContent = current + suffix;
        }

        if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
}

/* ===== Navbar Scroll ===== */
function initNavbar() {
    const nav = document.getElementById('navbar');
    if (!nav) return;

    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(() => {
                nav.classList.toggle('scrolled', window.scrollY > 50);
                ticking = false;
            });
            ticking = true;
        }
    });
}

/* ===== Pricing Toggle ===== */
function initPricingToggle() {
    const toggle = document.getElementById('pricingToggle');
    const monthlyLabel = document.getElementById('toggleMonthly');
    const annualLabel = document.getElementById('toggleAnnual');
    if (!toggle) return;

    toggle.addEventListener('change', () => {
        const isAnnual = toggle.checked;
        monthlyLabel.classList.toggle('active', !isAnnual);
        annualLabel.classList.toggle('active', isAnnual);

        document.querySelectorAll('.price').forEach(price => {
            const val = isAnnual ? price.dataset.annual : price.dataset.monthly;
            if (val) price.textContent = val;
        });
    });
}

/* ===== Mobile Menu ===== */
function initMobileMenu() {
    const btn = document.getElementById('mobileToggle');
    const links = document.getElementById('navLinks');
    if (!btn || !links) return;

    btn.addEventListener('click', () => {
        links.classList.toggle('open');
        btn.classList.toggle('active');
    });

    links.querySelectorAll('a').forEach(a => {
        a.addEventListener('click', () => {
            links.classList.remove('open');
            btn.classList.remove('active');
        });
    });
}
