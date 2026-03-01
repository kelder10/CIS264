const darkBtn = document.getElementById("darkModeBtn");

darkBtn.addEventListener("click", function() {
    document.body.classList.toggle("dark-mode");
});

// FILTER FUNCTIONALITY
const filter = document.getElementById("typeFilter");
const bikes = document.querySelectorAll(".bike-card");

if (filter) {
    filter.addEventListener("change", function() {
        const selected = this.value;

        bikes.forEach(function(bike) {
            if (selected === "all" || bike.dataset.type === selected) {
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
            if (selected === "all" || bike.dataset.size === selected) {
                bike.style.display = "block";
            } else {
                bike.style.display = "none";
            }
        });
    });
}