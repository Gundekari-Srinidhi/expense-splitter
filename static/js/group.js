const group =
JSON.parse(localStorage.getItem("selectedGroup"));

const groupTitle =
document.getElementById("groupTitle");

const groupDescription =
document.getElementById("groupDescription");

const membersContainer =
document.getElementById("membersContainer");

const expensesContainer =
document.getElementById("expensesContainer");

if(group){

    groupTitle.textContent =
    "🏖 " + group.name;

    groupDescription.textContent =
    group.description;

    group.members.forEach(function(member){

        const div =
        document.createElement("div");

        div.classList.add("member");

        div.textContent =
        "👤 " + member;

        membersContainer.appendChild(div);

    });

    if(group.expenses){

        group.expenses.forEach(function(expense){

            const card =
            document.createElement("div");

            card.classList.add("expense-card");

            card.innerHTML = `
                <h3>${expense.name}</h3>
                <p>Paid by ${expense.paidBy}</p>
                <span>₹${expense.amount}</span>
            `;

            expensesContainer.appendChild(card);

        });

    }

}
const deleteGroupBtn =
document.getElementById("deleteGroupBtn");

deleteGroupBtn.addEventListener("click", function(){

    const confirmDelete =
    confirm("Delete this group?");

    if(!confirmDelete){
        return;
    }

    let groups =
    JSON.parse(
        localStorage.getItem("groups")
    ) || [];

    groups = groups.filter(function(g){

        return g.name !== group.name;

    });

    localStorage.setItem(
        "groups",
        JSON.stringify(groups)
    );

    localStorage.removeItem(
        "selectedGroup"
    );

    window.location.href =
    "/dashboard";

});