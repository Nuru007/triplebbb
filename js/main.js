/* Custom Interactive Scripting for Triple B website */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Sticky Navigation Scroll Effect
  const headerNav = document.getElementById('header-nav');
  const handleScroll = () => {
    if (window.scrollY > 50) {
      headerNav.classList.add('scrolled');
    } else {
      headerNav.classList.remove('scrolled');
    }
  };
  window.addEventListener('scroll', handleScroll);
  handleScroll(); // Check initial state

  // 2. Mobile Menu Toggle
  const mobileToggle = document.getElementById('mobile-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  const body = document.body;

  if (mobileToggle && mobileMenu) {
    mobileToggle.addEventListener('click', () => {
      mobileMenu.classList.toggle('active');
      body.classList.toggle('mobile-nav-active');
    });

    // Close menu when clicking navigation link
    const mobileLinks = mobileMenu.querySelectorAll('a');
    mobileLinks.forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.remove('active');
        body.classList.remove('mobile-nav-active');
      });
    });
  }

  // 3. Hero Carousel Logic
  const slides = document.querySelectorAll('.hero-slide');
  const indicators = document.querySelectorAll('.control-indicator');
  const slideContent = {
    taglines: [
      "Illuminating Her Potential",
      "Empowering Her Mind",
      "Cultivating Her Balance"
    ],
    headlines: [
      "Inspiring Young Women to <span>Lead & Excel.</span>",
      "Nurturing the Brightest <span>Minds of Tomorrow.</span>",
      "Creating Harmonious <span>Growth & Strength.</span>"
    ],
    descriptions: [
      "Triple B Global Initiative is a movement dedicated to empowering female tertiary students across Nigeria through mentorship, skills acquisition, and community building.",
      "Providing access to world-class educational leadership seminars, tech workshops, and high-impact guidance systems from top female professionals.",
      "Encouraging young women to find balance in all areas of life, uniting expressive self-confidence (Beauty) with critical intelligence (Brain)."
    ]
  };

  const taglineEl = document.getElementById('dynamic-tagline');
  const headlineEl = document.getElementById('dynamic-headline');
  const descEl = document.getElementById('dynamic-description');

  let currentSlide = 0;
  const slideIntervalTime = 5000; // 5 seconds per slide
  let slideInterval;

  const updateSlideContent = (index) => {
    // Fade out text contents briefly
    const textElements = [taglineEl, headlineEl, descEl];
    textElements.forEach(el => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(15px)';
    });

    setTimeout(() => {
      // Set new text content
      taglineEl.innerText = slideContent.taglines[index];
      headlineEl.innerHTML = slideContent.headlines[index];
      descEl.innerText = slideContent.descriptions[index];

      // Fade back in
      textElements.forEach(el => {
        el.style.opacity = '1';
        el.style.transform = 'translateY(0)';
      });
    }, 450); // Syncs with CSS fade transitions
  };

  const showSlide = (index) => {
    // Remove active class from previous active slide and indicator
    slides[currentSlide].classList.remove('active');
    indicators[currentSlide].classList.remove('active');

    // Set new active slide index
    currentSlide = index;

    // Add active class to new slide and indicator
    slides[currentSlide].classList.add('active');
    indicators[currentSlide].classList.add('active');

    // Update the layout texts to match slide themes
    updateSlideContent(currentSlide);
  };

  const nextSlide = () => {
    let nextIndex = (currentSlide + 1) % slides.length;
    showSlide(nextIndex);
  };

  const startSlideShow = () => {
    stopSlideShow();
    slideInterval = setInterval(nextSlide, slideIntervalTime);
  };

  const stopSlideShow = () => {
    if (slideInterval) {
      clearInterval(slideInterval);
    }
  };

  // Add click events to slide indicators
  indicators.forEach((indicator, index) => {
    indicator.addEventListener('click', () => {
      if (currentSlide !== index) {
        showSlide(index);
        startSlideShow(); // Reset interval timer on manual click
      }
    });
  });

  // Initialize Carousel
  if (slides.length > 0) {
    showSlide(0);
    startSlideShow();
  }

  // 4. Scroll Reveal / Intersection Observer Setup
  const revealElements = document.querySelectorAll('.reveal');
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
        observer.unobserve(entry.target); // Reveal only once
      }
    });
  }, {
    threshold: 0.15,
    rootMargin: '0px 0px -50px 0px' // Trigger slightly before element fits in view
  });

  revealElements.forEach(el => {
    revealObserver.observe(el);
  });

  // 5. About Section Tab Switcher
  const tabButtons = document.querySelectorAll('.about-tab-btn');
  const tabPanes = document.querySelectorAll('.about-tab-pane');

  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      // Deactivate all buttons
      tabButtons.forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      // Deactivate all panes
      tabPanes.forEach(p => p.classList.remove('active'));

      // Activate current button
      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');

      // Activate corresponding pane
      const paneId = btn.getAttribute('aria-controls');
      const pane = document.getElementById(paneId);
      if (pane) {
        pane.classList.add('active');
      }
    });
  });
});
