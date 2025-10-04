document.addEventListener('DOMContentLoaded', () => {
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('nav ul li a');

    const activateLink = (id) => {
        if (!id) return;
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${id}`) {
                link.classList.add('active');
            }
        });
    };
    const observer = new IntersectionObserver((entries) => {
        let maxIntersection = 0;
        let activeEntry = null;

        entries.forEach(entry => {
            if (entry.isIntersecting) {
                if (entry.intersectionRatio > maxIntersection) {
                    maxIntersection = entry.intersectionRatio;
                    activeEntry = entry;
                }
            }
        });

        if (activeEntry) {
            activateLink(activeEntry.target.id);
        }
    }, {
        rootMargin: '-30% 0px -70% 0px' // Adjust this to change when the link becomes active
    });
    sections.forEach(section => {
        observer.observe(section);
    });
});