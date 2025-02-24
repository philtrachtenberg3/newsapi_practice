document.addEventListener("DOMContentLoaded", function () {
    fetch('/get_sources')
        .then(response => response.json())
        .then(data => {
            let sourcesDropdown = document.getElementById("sources");
            data.forEach(source => {
                let option = document.createElement("option");
                option.value = source.id;
                option.textContent = source.name;
                sourcesDropdown.appendChild(option);
            });
        });

    document.getElementById("getNewsBtn").addEventListener("click", function () {
        let country = document.getElementById("country").value;
        let category = document.getElementById("category").value;
        let sources = document.getElementById("sources").value;

        let query = `/get_news?country=${country}&category=${category}&sources=${sources}`;
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
});
