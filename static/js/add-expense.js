const form = document.querySelector("form");

form.addEventListener("submit", function (e) {

    const expenseName = document
        .getElementById("expenseName")
        .value
        .trim();

    const amount = document
        .getElementById("expenseAmount")
        .value
        .trim();

    const paidBy = document
        .getElementById("paidBy")
        .value;

    const checkedMembers = document.querySelectorAll(
        "input[name='splitAmong']:checked"
    );

    if (expenseName === "") {
        alert("Expense name cannot be empty.");
        e.preventDefault();
        return;
    }

    if (amount === "") {
        alert("Amount is required.");
        e.preventDefault();
        return;
    }

    if (Number(amount) <= 0) {
        alert("Amount must be greater than zero.");
        e.preventDefault();
        return;
    }

    if (paidBy === "") {
        alert("Please select who paid.");
        e.preventDefault();
        return;
    }

    if (checkedMembers.length === 0) {
        alert("Select at least one member to split the expense.");
        e.preventDefault();
        return;
    }

});