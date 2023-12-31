// Function to Open Popup
document.getElementById("popupFormButton").onclick = function() {
    document.getElementById("popupForm").style.display = "block";
}

// Function to Close Popup
function closePopup() {
    document.getElementById("popupForm").style.display = "none";
}

// Function to Open Popup
document.getElementById("popupFormButton").onclick = function() {
    document.getElementById("popupForm").style.display = "block";
};

// Function to Close Popup
function closePopup() {
    document.getElementById("popupForm").style.display = "none";
};

// Function to Add a Member
function addMember() {
    var firstName = document.getElementById("firstName").value;
    var lastName = document.getElementById("lastName").value;
    if (firstName && lastName) {
        var membersList = document.getElementById("membersList");
        var li = document.createElement("li");
        li.className = "list-group-item";
        li.innerHTML = `${firstName} ${lastName} 
                        <button class="btn btn-sm btn-info" onclick="editMember(this)">Edit</button>
                        <button class="btn btn-sm btn-danger" onclick="deleteMember(this)">Delete</button>`;
        membersList.appendChild(li);
        // Clear input fields
        document.getElementById("firstName").value = '';
        document.getElementById("lastName").value = '';
    } else {
        alert("Please enter both first and last names.");
    }
};

// Function to Delete a Member
function deleteMember(button) {
    var li = button.parentElement;
    li.remove();
};

function validateForm() {
    var members = document.querySelectorAll("#membersList li");
    if (members.length === 0) {
        alert("Please add at least one member.");
        return false; // Prevent form submission
    }
    var startDateString = document.getElementById('startDate').value;
    var endDateString = document.getElementById('endDate').value;

    // Splitting date string into components
    var startDateComponents = startDateString.split('-');
    var endDateComponents = endDateString.split('-');

    var currentDate = new Date();
    currentDate.setHours(0,0,0,0);

    // Creating date objects using components (year, month - 1, day)
    var startDate = new Date(
        startDateComponents[0],
        startDateComponents[1] - 1,
        startDateComponents[2]
    );
    var endDate = new Date(
        endDateComponents[0],
        endDateComponents[1] - 1,
        endDateComponents[2]
    );

    if (startDate < currentDate) {
        document.getElementById('dateError').innerText = 'Start date cannot be earlier than the start date.';
        return false; // Prevent form submission
    }
    var maxEndDate = new Date(currentDate.getFullYear() + 1000000, currentDate.getMonth());
    if(endDate < startDate || endDate > maxEndDate){
        document.getElementById('dateError').innerText = "End date must be after the start date "
        return false;
    }

    return true; // Allow form submission
}


// Function to Edit a Member
function editMember(button) {
    var li = button.parentElement;
    var names = li.firstChild.textContent.split(" ");
    var firstName = prompt("Edit First Name:", names[0]);
    var lastName = prompt("Edit Last Name:", names[1]);

    if (firstName != null && lastName != null) {
        li.firstChild.textContent = `${firstName} ${lastName} `;
        li.appendChild(button.nextSibling); // Append Edit button
        li.appendChild(button); // Append Delete button
    }
};

function gatherListData() {
    let ul = document.getElementById("membersList");
    let items = ul.getElementsByTagName("li");
    let memberData = [];
    for (let i = 0; i < items.length; ++i) {
        memberData.push(items[i].textContent);
    }
    return memberData;
}

document.getElementById('submitForm').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent default form submission

    if (!validateForm()) {
        // If form validation fails, do not proceed with submission
        return;
    }

    let formData = new FormData(this);
    let membersList = gatherListData();
    formData.append('membersList', JSON.stringify(membersList));

    fetch('/recommendation', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url; // Redirect if Flask sends redirect
        } else {
            console.log('No redirect response');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
