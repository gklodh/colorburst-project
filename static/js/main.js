// ColorBurst — small interactive touches

// Mobile nav toggle
const burger = document.querySelector(".burger");
const navLinks = document.querySelector(".nav-links");
if (burger && navLinks) {
    burger.addEventListener("click", () => navLinks.classList.toggle("open"));
    navLinks.querySelectorAll("a").forEach(a =>
        a.addEventListener("click", () => navLinks.classList.remove("open"))
    );
}

// Reveal-on-scroll animation
const observer = new IntersectionObserver(
    entries => entries.forEach(e => {
        if (e.isIntersecting) e.target.classList.add("visible");
    }),
    { threshold: 0.15 }
);
document.querySelectorAll(".reveal").forEach(el => observer.observe(el));

// Animated counters for the stats strip
const counters = document.querySelectorAll("[data-count]");
const counterObs = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        const target = +el.dataset.count;
        const dur = 1400, t0 = performance.now();
        const tick = now => {
            const p = Math.min((now - t0) / dur, 1);
            el.textContent = Math.floor(p * target).toLocaleString() + (el.dataset.suffix || "");
            if (p < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
        counterObs.unobserve(el);
    });
}, { threshold: 0.5 });
counters.forEach(el => counterObs.observe(el));
