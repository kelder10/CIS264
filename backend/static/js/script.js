// DARK MODE FUNCTIONALITY WITH PERSISTENCE
const darkBtn = document.getElementById("darkModeBtn");

// 1. Check for saved theme on page load
if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark-mode");
    if (darkBtn) darkBtn.textContent = "☀️"; 
}

if (darkBtn) {
    darkBtn.addEventListener("click", function() {
        document.body.classList.toggle("dark-mode");
        
        // 2. Save the preference to localStorage
        if (document.body.classList.contains("dark-mode")) {
            localStorage.setItem("theme", "dark");
            darkBtn.textContent = "☀️";
        } else {
            localStorage.setItem("theme", "light");
            darkBtn.textContent = "🌙";
        }
    });
}

// FILTER FUNCTIONALITY (ADULTS)
const filter = document.getElementById("typeFilter");
const bikes = document.querySelectorAll(".bike-card");

if (filter) {
    filter.addEventListener("change", function() {
        const selected = this.value;

        bikes.forEach(function(bike) {
            if (selected === "all" || selected === "" || bike.dataset.type === selected) {
                bike.style.display = "block";
            } else {
                bike.style.display = "none";
            }
        });
    });
}

// KIDS FILTER
const kidsFilter = document.getElementById("kidsFilter");

if (kidsFilter) {
    const kidBikes = document.querySelectorAll(".bike-card");

    kidsFilter.addEventListener("change", function() {
        const selected = this.value;

        kidBikes.forEach(function(bike) {
            if (selected === "all" || selected === "" || bike.dataset.size === selected) {
                bike.style.display = "block";
            } else {
                bike.style.display = "none";
            }
        });
    });
}