const search = document.getElementById("searchGroup");

search.addEventListener("keyup", function () {

    const value = search.value.toLowerCase();

    const groups = document.querySelectorAll(".group-item");

    groups.forEach(function(group){

        const name = group
            .querySelector(".group-name")
            .innerText
            .toLowerCase();

        if(name.includes(value)){
            group.style.display = "block";
        }
        else{
            group.style.display = "none";
        }

    });

});
const sort = document.getElementById("sortGroups");

sort.addEventListener("change", function () {

    const container = document.querySelector(".groups-container");

    const cards = Array.from(
        document.querySelectorAll(".group-item")
    );

    if (sort.value === "az") {

        cards.sort((a, b) => {

            return a.querySelector(".group-name")
                .innerText
                .localeCompare(
                    b.querySelector(".group-name").innerText
                );

        });

    }

    else if (sort.value === "za") {

        cards.sort((a, b) => {

            return b.querySelector(".group-name")
                .innerText
                .localeCompare(
                    a.querySelector(".group-name").innerText
                );

        });

    }

    else if (sort.value === "members") {

        cards.sort((a, b) => {

            const m1 = parseInt(
                a.querySelector(".member-count").innerText
            );

            const m2 = parseInt(
                b.querySelector(".member-count").innerText
            );

            return m2 - m1;

        });

    }

    container.innerHTML = "";

    cards.forEach(card => container.appendChild(card));

});