const group =
JSON.parse(
    localStorage.getItem("selectedGroup")
);

const totalExpense =
document.getElementById("totalExpense");

const sharePerPerson =
document.getElementById("sharePerPerson");

const settlementContainer =
document.getElementById("settlementContainer");

let totalAmount = 0;

if(group && group.expenses){

    group.expenses.forEach(function(expense){

        totalAmount +=
        Number(expense.amount);

    });

}

totalExpense.textContent =
"₹" + totalAmount;

const share =
totalAmount / group.members.length;

sharePerPerson.textContent =
"₹" + share.toFixed(2);

const balances = {};

// Initialize balances
group.members.forEach(function(member){

    balances[member] = 0;

});

// Add payments
if(group.expenses){

    group.expenses.forEach(function(expense){

        balances[expense.paidBy] +=
        Number(expense.amount);

    });

}

// Subtract share
group.members.forEach(function(member){

    balances[member] -= share;

});

console.log("Balances:", balances);

const creditors = [];
const debtors = [];

for(const member in balances){

    if(balances[member] > 0){

        creditors.push({
            name: member,
            amount: balances[member]
        });

    }

    else if(balances[member] < 0){

        debtors.push({
            name: member,
            amount: Math.abs(balances[member])
        });

    }

}

console.log("Creditors:", creditors);
console.log("Debtors:", debtors);

while(
    debtors.length > 0 &&
    creditors.length > 0
){

    const debtor =
    debtors[0];

    const creditor =
    creditors[0];

    const amount =
    Math.min(
        debtor.amount,
        creditor.amount
    );

    const card =
    document.createElement("div");

    card.classList.add("settlement-card");

    card.innerHTML = `
        <div>
            <h3>
                ${debtor.name} ➜ ${creditor.name}
            </h3>

            <p>
                Needs to pay
            </p>
        </div>

        <span>
            ₹${amount.toFixed(2)}
        </span>
    `;

    settlementContainer.appendChild(card);

    debtor.amount -= amount;
    creditor.amount -= amount;

    if(debtor.amount < 0.01){

        debtors.shift();

    }

    if(creditor.amount < 0.01){

        creditors.shift();

    }

}
const settleBtn =
document.getElementById("settleBtn");

settleBtn.addEventListener("click", function(){

    group.expenses = [];

    let groups =
    JSON.parse(
        localStorage.getItem("groups")
    ) || [];

    groups = groups.map(function(g){

        if(g.name === group.name){

            return group;

        }

        return g;

    });

    localStorage.setItem(
        "groups",
        JSON.stringify(groups)
    );

    localStorage.setItem(
        "selectedGroup",
        JSON.stringify(group)
    );

    alert("Settlement completed!");

    window.location.href =
    "group.html";

});