const emailInput =
document.getElementById("memberEmail");

const addBtn =
document.getElementById("addMemberBtn");

const membersList =
document.getElementById("membersList");

const createGroupBtn =
document.getElementById("createGroupBtn");

const groupName =
document.getElementById("groupName");

const groupDescription =
document.getElementById("groupDescription");
const membersInput =
document.getElementById("members");

let members = membersInput.value
    ? membersInput.value.split(",")
    : [];

    const removeButtons =
document.querySelectorAll(".remove-btn");

removeButtons.forEach(function(button){

    button.addEventListener("click", function(){

        const li = button.parentElement;

        const email = li.firstChild.textContent.trim();

        members = members.filter(function(member){
            return member !== email;
        });

        membersInput.value = members.join(",");

        li.remove();

    });

});

addBtn.addEventListener("click", function () {
    

    const email = emailInput.value;

    if(email === ""){
        return;
    }

   if(members.includes(email)){
        alert("Member already added");
        return;
    }

    members.push(email);

    membersInput.value = members.join(",");

    const li = document.createElement("li");

    li.innerHTML = `
        ${email}
        <button class="remove-btn">
            Remove
        </button>
    `;

    const removeBtn = li.querySelector(".remove-btn");

    removeBtn.addEventListener("click", function(){

        li.remove();

        members = members.filter(function(member){
            return member !== email;
        });

        membersInput.value = members.join(",");

        console.log(members);
    });

    membersList.appendChild(li);
    emailInput.value = "";
});
createGroupBtn.addEventListener("click", function(event){

    if(groupName.value.trim() === ""){
        alert("Group name cannot be empty");
        event.preventDefault();
        return;
    }
    
    if(groupDescription.value.trim() === ""){
        alert("Description cannot be empty");
        event.preventDefault();
        return;
    }

    if(members.length === 0){
        alert("Add at least one member");
        event.preventDefault();
        return;
    }

    membersInput.value = members.join(",");
});