/**
 * Our Story Script - Handles navigation sticky headers, mobile menu toggles,
 * scroll reveals, interactive timeline highlighting, and mouse parallax.
 */

document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initScrollReveal();
  initTimelineHighlight();
  initHeroParallax();
});

/**
 * 1. Mobile Menu Drawer & Sticky Navbar Scroll Logic
 */
function initNavigation() {
  const header = document.getElementById('main-header');
  const mobileToggle = document.getElementById('mobile-toggle');
  const mobileMenu = document.getElementById('mobile-menu');

  // Sticky header background shift on scroll
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      header.classList.add('nav-scrolled');
      header.classList.add('scrolled'); // Ensure compatibility with main.css style
    } else {
      header.classList.remove('nav-scrolled');
      header.classList.remove('scrolled');
    }
  });

  // Toggle mobile overlay menu drawer
  if (mobileToggle && mobileMenu) {
    mobileToggle.addEventListener('click', () => {
      mobileToggle.classList.toggle('active');
      mobileMenu.classList.toggle('active');
      document.body.classList.toggle('no-scroll');
    });
  }
}

// Global mobile close helper for onclick events
window.toggleMobileMenu = () => {
  const mobileToggle = document.getElementById('mobile-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  if (mobileToggle && mobileMenu) {
    mobileToggle.classList.remove('active');
    mobileMenu.classList.remove('active');
    document.body.classList.remove('no-scroll');
  }
};

/**
 * 2. Scroll Reveal Animations
 */
function initScrollReveal() {
  const revealElements = document.querySelectorAll('.reveal');

  if ('IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('active');
          observer.unobserve(entry.target); // Trigger only once
        }
      });
    }, {
      threshold: 0.15,
      rootMargin: '0px 0px -50px 0px'
    });

    revealElements.forEach(el => revealObserver.observe(el));
  } else {
    // Fallback if IntersectionObserver is not supported
    revealElements.forEach(el => el.classList.add('active'));
  }
}

/**
 * 3. Interactive Scroll-tracked Timeline Node Highlighting
 */
function initTimelineHighlight() {
  const timelineNodes = document.querySelectorAll('.timeline-node-wrapper');

  if ('IntersectionObserver' in window) {
    const timelineObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        // Highlight when the node is in the center-ish area of the screen
        if (entry.isIntersecting) {
          entry.target.classList.add('active-node');
        } else {
          entry.target.classList.remove('active-node');
        }
      });
    }, {
      // Trigger when the element crosses the middle 40% of the viewport height
      rootMargin: '-30% 0px -30% 0px',
      threshold: 0
    });

    timelineNodes.forEach(node => timelineObserver.observe(node));
  } else {
    // Fallback: active first node by default
    if (timelineNodes.length > 0) {
      timelineNodes[0].classList.add('active-node');
    }
  }
}

/**
 * 4. Interactive Hero Avatar Mouse Parallax Effect
 */
function initHeroParallax() {
  const hero = document.getElementById('story-hero');
  const avatars = document.querySelectorAll('.avatar-float');
  
  if (!hero || avatars.length === 0) return;
  
  // Different factors create layered parallax speed (some positive, some negative)
  const parallaxFactors = [0.03, -0.04, 0.05, -0.025, 0.045, -0.03, 0.02, -0.045];

  hero.addEventListener('mousemove', (e) => {
    // Get mouse offsets relative to the center of the hero section
    const rect = hero.getBoundingClientRect();
    const heroCenterX = rect.left + rect.width / 2;
    const heroCenterY = rect.top + rect.height / 2;
    
    const mouseX = e.clientX - heroCenterX;
    const mouseY = e.clientY - heroCenterY;

    avatars.forEach((avatar, index) => {
      const factor = parallaxFactors[index % parallaxFactors.length];
      const xOffset = mouseX * factor;
      const yOffset = mouseY * factor;
      
      // Apply offset dynamically
      avatar.style.transform = `translate(${xOffset}px, ${yOffset}px)`;
    });
  });

  // Smooth return transition when mouse leaves
  hero.addEventListener('mouseleave', () => {
    avatars.forEach((avatar) => {
      avatar.style.transition = 'transform 0.8s cubic-bezier(0.16, 1, 0.3, 1)';
      avatar.style.transform = 'translate(0px, 0px)';
    });
  });

  // Snappy real-time transition on enter
  hero.addEventListener('mouseenter', () => {
    avatars.forEach((avatar) => {
      avatar.style.transition = 'transform 0.1s ease-out';
    });
  });
}
