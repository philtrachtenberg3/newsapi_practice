document.addEventListener("DOMContentLoaded", function () {
    let sourcesDropdown = document.getElementById("sources");
    let countryDropdown = document.getElementById("country");
    let categoryDropdown = document.getElementById("category");
    let searchTypeRadios = document.getElementsByName("searchType");

    // Load sources dynamically
    fetch('/get_sources')
        .then(response => response.json())
        .then(data => {
            data.forEach(source => {
                let option = document.createElement("option");
                option.value = source.id;
                option.textContent = source.name;
                sourcesDropdown.appendChild(option);
            });
        });

    // Load available countries dynamically
    fetch('/get_countries')
        .then(response => response.json())
        .then(countryCodes => {
            let countryList = [];

            countryCodes.forEach(code => {
                if (countryMapping[code]) {
                    countryList.push({ code: code, name: countryMapping[code] });
                }
            });

            // Sort by full country name
            countryList.sort((a, b) => a.name.localeCompare(b.name));

            // Populate dropdown
            countryList.forEach(country => {
                let option = document.createElement("option");
                option.value = country.code.toLowerCase();
                option.textContent = country.name;
                countryDropdown.appendChild(option);
            });
        });

    // Enable/Disable fields based on search type
    function updateSearchOptions() {
        let selectedType = document.querySelector('input[name="searchType"]:checked').value;

        if (selectedType === "sources") {
            sourcesDropdown.disabled = false;
            countryDropdown.disabled = true;
            categoryDropdown.disabled = true;
        } else if (selectedType === "country") {
            sourcesDropdown.disabled = true;
            countryDropdown.disabled = false;
            categoryDropdown.disabled = true;
        } else if (selectedType === "category") {
            sourcesDropdown.disabled = true;
            countryDropdown.disabled = true;
            categoryDropdown.disabled = false;
        }
    }

    searchTypeRadios.forEach(radio => {
        radio.addEventListener("change", updateSearchOptions);
    });

    document.getElementById("getNewsBtn").addEventListener("click", function () {
        let selectedType = document.querySelector('input[name="searchType"]:checked').value;
        let query = "/get_news?";

        if (selectedType === "sources") {
            let selectedSources = Array.from(sourcesDropdown.selectedOptions).map(option => option.value).join(",");
            query += `sources=${selectedSources}`;
        } else if (selectedType === "country") {
            query += `country=${countryDropdown.value}`;
        } else if (selectedType === "category") {
            query += `category=${categoryDropdown.value}`;
        }

        fetch(query)
            .then(response => response.json())
            .then(data => {
                let newsContainer = document.getElementById("newsResults");
                newsContainer.innerHTML = "";

                if (data.error) {
                    newsContainer.innerHTML = `<p>${data.error}</p>`;
                } else {
                    data.forEach(article => {
                        let articleDiv = document.createElement("div");
                        articleDiv.innerHTML = `<h3>${article.title}</h3>
                                                <p>${article.description || "No description available"}</p>
                                                <a href="${article.url}" target="_blank">Read more</a>`;
                        newsContainer.appendChild(articleDiv);
                    });
                }
            });
    });

    // Initialize UI state
    updateSearchOptions();
});
