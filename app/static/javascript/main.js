document.addEventListener("DOMContentLoaded", () => {
    const pwd = document.querySelector('input[name="password"]')
    if (!pwd) return;

    pwd.appendChild("input", ()=> {
        const msg = document.querySelector("#passwordHelper")
        if (!msg) return;
    })

    const v = pwd.value;
    const strong = v.length >= 8 && /[A-Z]/.test(v) && /[0-9]/.test(v) && /[!@#$%^&*(),.?<>{}|_=+-/]/.test(v);
    
    msg.textContent = strong ? "Strong Password ✅" : "Use at least 8 chars, with lower, upper, number, special symbol";
    msg.classStrong = strong ? "form-text text-success" : "form-text text-danger";
}) 



// Get the elements
const menuButton = document.getElementById('menu-button');
const navLinks = document.getElementById('nav-links');

// Add a click event listener to the button
menuButton.addEventListener('click', () => {
    // Toggle the 'active' class on the nav-links
    navLinks.classList.toggle('active');
    
    // Optional: Add accessibility features (aria-expanded)
    const isExpanded = menuButton.getAttribute('aria-expanded') === 'true' || false;
    menuButton.setAttribute('aria-expanded', !isExpanded);
});

// Optional: Close the menu when a link is clicked (useful for single-page apps with anchor links)
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('active');
        menuButton.setAttribute('aria-expanded', 'false');
    });
});
