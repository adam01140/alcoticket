import logging
from flask import Flask, request, jsonify, send_from_directory, send_file, redirect, url_for, session
import PyPDF2
import io
import csv
import threading

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = 'your_secret_key_here'

# In-memory storage for users (not suitable for production)
users = {}



def save_data_to_csv():
    with open('user_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['username', 'password', 'state', 'city','logged']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for username, data in users.items():
            writer.writerow({'username': username, 'password': data['password']
            , 'state': data.get('state', '')
            , 'logged': data.get('logged', '')
            , 'city': data.get('city', '')})

def load_data_from_csv():
    try:
        with open('user_data.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                users[row['username']] = {'password': row['password'], 'state': row['state'], 'city': row['city']}
    except FileNotFoundError:
        print("No existing CSV file found. Starting with an empty user database.")



def save_every_three_seconds():
    while True:
        save_data_to_csv()
        threading.Event().wait(3)









































@app.route('/get_html_content')
def get_html_content():
    html_content = """
    
    
    
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SCADA Ticketing System</title>
	
	


   <style>
   
   
   
   
   
   #deletedTicketsContainer {
    display: block;
    justify-content: center;
    margin-bottom: 20px;
	 border: 4px solid lightblue; /* Set the border color */
        border-radius: 10px;        /* Rounded corners */
        padding: 20px;              /* Some padding inside the border */
        margin: 10px;               /* Margin outside the border */
        background-color: #ffffff;  /* Light blue background */
        width: 100%;               /* Fixed width */
        height: 100% 
}
   
   
  #memberManagement {
    display: block;
    justify-content: center;
    margin-bottom: 20px;
	 border: 4px solid lightblue; /* Set the border color */
        border-radius: 10px;        /* Rounded corners */
        padding: 20px;              /* Some padding inside the border */
        margin: 10px;               /* Margin outside the border */
        background-color: #ffffff;  /* Light blue background */
        width: 100%;               /* Fixed width */
        height: 100% 
}

#memberList{
    display: flex;
    align-items: center;
    justify-content: center; /* Centers the content horizontally */
}

#memberList {
    margin-right: 10px;
	
}

#insidemembers {
        border: 4px solid lightblue; /* Set the border color */
        border-radius: 10px;        /* Rounded corners */
        padding: 20px;              /* Some padding inside the border */
        margin: 10px;               /* Margin outside the border */
        background-color: #ffffff;  /* Light blue background */
        width: 80%;               /* Fixed width */
        height: 100%               /* Automatic height adjustment */
    }
	
	

button {
    margin-left: 10px; /* Ensure consistent spacing between buttons */
}




   .tickets-container {
        display: flex;              /* Enable Flexbox */
        flex-wrap: wrap;            /* Allow items to wrap onto the next line */
        justify-content: center; /* Distribute space evenly around the items */
        width: 100%;                /* Take full width of the container */
    }
    
    .ticket-item {
        border: 4px solid lightblue; /* Set the border color */
        border-radius: 10px;        /* Rounded corners */
        padding: 20px;              /* Some padding inside the border */
        margin: 10px;               /* Margin outside the border */
        background-color: #ffffff;  /* Light blue background */
        width: calc(45% - 20px);    /* Calculate width, subtracting margins */
        box-sizing: border-box;     /* Include padding and border in the element's total width */
    }
	
	
	#ticketsinside {
        border: 4px solid lightblue; /* Set the border color */
        border-radius: 10px;        /* Rounded corners */
        padding: 20px;              /* Some padding inside the border */
        margin: 10px;               /* Margin outside the border */
        background-color: #ffffff;  /* Light blue background */
        width: 80%;               /* Fixed width */
        height: 10%               /* Automatic height adjustment */
    }
	
	

    #tickets {
        border: 4px solid lightblue; /* Set the border color */
        border-radius: 10px;        /* Rounded corners */
        padding: 20px;              /* Some padding inside the border */
        margin: 10px;               /* Margin outside the border */
        background-color: #ffffff;  /* Light blue background */
        width: 100%;               /* Fixed width */
        height: 100%               /* Automatic height adjustment */
    }

    /* Existing styles */
    body {
        font-family: Arial, sans-serif;
    }
    input[type="text"], textarea {
        width: 200px;
        height: 40px;
        padding: 10px;
        margin-top: 5px;
        margin-bottom: 10px;
        border: 2px solid #64adc4;
        border-radius: 5px;
        background-color: #eaf6f9;
        box-sizing: border-box;
    }
    button, select {
        background-color: #64adc4;
        color: #fff;
        border: none;
		height: 40px;
        border-radius: 40px;
        padding: 10px 20px;
        margin-top: 10px;
        cursor: pointer;
    }
    select {
        text-align: center;
        width: 200px;
        height: 40px;
        padding-left: 0px;
        border: 1px solid #4CAF50;
    }
</style>

</head>
<body>
<center>
    <!-- Ticket Submission Form -->
    <div id = "tickets">
        <h2><u>Submit a Ticket</u></h2>
		
		
		<div id="ticketsinside">
        <input type="text" id="ticketTitle" placeholder="Ticket Issue"><br>
        <input type="text" id="ticketName" placeholder="Requester"><br>
        <textarea id="ticketDesc" placeholder="Description"></textarea><br>
        <select id="ticketPriority">
            <option value="Low">Low Priority</option>
            <option value="Medium">Medium Priority</option>
            <option value="High">High Priority</option>
        </select><br>
        <button onclick="submitTicket()">Submit Ticket</button>
    </div>
	</div>





















	
	 <div class="tickets-container">
	 
	<div id = "tickets">
	<h2><u>Open Tickets</u></h2>
	
	<div id="openTicketsList" class="tickets-container">
    
</div>

</div>
<br>

<div id = "tickets">
<!-- Pending Tickets -->

<h2><u>Pending Tickets</u></h2>

<select id="sortFilter" onchange="loadTickets()">
    <option value="all">All</option> <!-- Ensure this is present -->
    <option value="Adnen">Adnen</option>
    <option value="David">David</option>
    <option value="Octavio">Octavio</option>
</select>

<br>
	<br>
	
<div id="pendingTicketsList" class="tickets-container">
    
</div>


</div>
<br>
	
	<br>

<div id="memberManagement">
    <h2>Manage Members</h2>
	
	<div id="allmembers">  </div>
	
	
	<div id = "insidemembers">
	<p><h3> Add a new member to the team </h3></p>
	<button onclick="addMember()"> Add New Member</button>
	</div>
	
	
	<br>
    
<div id = "insidemembers">

<p><h3> Remove a member from the team </h3> </p>

        <div id="memberList">
		
            <select id="memberSelect">
                <option value="Adnen">Adnen</option>
                <option value="David">David</option>
                <option value="Octavio">Octavio</option>
            </select>
        
        
        <button onclick="deleteMember()">Delete Member</button>
</div>
		</div>
		
    </div>
	
	
	

</div>



<div id="deletedTicketsContainer">
    <h2>Recently Deleted Tickets</h2>
    <div id="deletedTicketsList" class="tickets-container"></div>
</div>


	




    
	</div>

    <script type="module">
        import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.0.0/firebase-app.js';
import { getFirestore, doc, setDoc, getDoc, collection, getDocs, addDoc, updateDoc, deleteDoc, query, where } from 'https://www.gstatic.com/firebasejs/9.0.0/firebase-firestore.js';

        const firebaseConfig = {
            apiKey: "AIzaSyDgqB5FaU1Zreq3H5WwfDo7WSUEkVOdKxU",
            authDomain: "formfiller-b9856.firebaseapp.com",
            projectId: "formfiller-b9856",
            storageBucket: "formfiller-b9856.appspot.com",
            messagingSenderId: "424653050423",
            appId: "1:424653050423:web:dfae46bc004eaedefae5b2",
            measurementId: "G-9WPM6EEMQ7"
        };

        const app = initializeApp(firebaseConfig);
        const db = getFirestore(app);

       window.submitTicket = async () => {
    const title = document.getElementById('ticketTitle').value;
    const name = document.getElementById('ticketName').value;
    const description = document.getElementById('ticketDesc').value;
    const priority = document.getElementById('ticketPriority').value;

    if (title && name && description) {
        const docRef = await addDoc(collection(db, "tickets"), {
            title: title,
            requestor: name,
            description: description,
            priority: priority,
            status: "New", // Default status
            created: new Date()
        });

        console.log("Ticket submitted with ID:", docRef.id);
        loadTickets();  // Reload tickets after submission
    }
};



















window.deleteTicket = async (docId) => {
    if (confirm("Are you sure you want to delete this ticket?")) {
        const ticketRef = doc(db, "tickets", docId);
        await updateDoc(ticketRef, {
            status: "Recently Deleted",
            deletedAt: new Date()  // Ensure this field is updated when the ticket is deleted
        });
        console.log("Ticket marked as recently deleted!");
        loadTickets();  // Reload tickets to reflect changes
    }
};





window.deleteMember = async () => {
    const memberSelect = document.getElementById('memberSelect');
    const selectedMember = memberSelect.value;

    if (selectedMember) {
        // Confirm before deleting
        if (confirm(`Are you sure you want to delete ${selectedMember}?`)) {
            const membersRef = collection(db, "members");
            const q = query(membersRef, where("name", "==", selectedMember));
            const querySnapshot = await getDocs(q);
            querySnapshot.forEach(async (doc) => {
                await deleteDoc(doc.ref); // Delete the document
            });

            // Reload members to update UI
            loadMembers();
            alert(`${selectedMember} has been deleted.`);
        }
    } else {
        alert("Please select a member to delete.");
    }
};




window.loadMembers = async () => {
    const membersRef = collection(db, "members");
    const memberSnapshot = await getDocs(membersRef);
    const members = memberSnapshot.docs.map(doc => doc.data().name);

    // Update dropdowns
    updateMemberDropdowns(members);

    // Check if the paragraph already exists
    let memberNamesPara = document.getElementById('memberNamesPara');
    if (!memberNamesPara) {
        // Create a new paragraph if it doesn't exist
        memberNamesPara = document.createElement('p');
        memberNamesPara.id = 'memberNamesPara'; // Assign an ID for future reference
        const memberManagementDiv = document.getElementById('allmembers');
        memberManagementDiv.appendChild(memberNamesPara);
    }
    
    // Update the text content of the paragraph
    memberNamesPara.textContent = 'Members: ' + members.join(', '); // Concatenate all member names
    memberNamesPara.style.padding = '10px';
    memberNamesPara.style.marginTop = '10px';
    memberNamesPara.style.backgroundColor = '#e0f7fa';
};



function updateMemberDropdowns(members) {
    const memberSelect = document.getElementById('memberSelect');
    const sortFilter = document.getElementById('sortFilter');
    const assignSelects = document.querySelectorAll('[id^="assign-"]');

    memberSelect.innerHTML = '';
    sortFilter.innerHTML = '<option value="all">All Tickets</option>';

    members.forEach(member => {
        const option = document.createElement('option');
        option.value = member;
        option.text = member;

        memberSelect.appendChild(option.cloneNode(true));
        sortFilter.appendChild(option.cloneNode(true));

        assignSelects.forEach(select => {
            select.appendChild(option.cloneNode(true));
        });
    });
}

window.addMember = async () => {
    let newMemberName = prompt("Enter the name of the new member:");
    if (newMemberName) {
        // Add the new member to Firestore
        await addDoc(collection(db, "members"), { name: newMemberName });
		alert("New member added!");
        loadMembers(); // Reload members from Firestore
    }
};


window.restoreTicket = async (docId) => {
    if (confirm("Are you sure you want to re-open this ticket?")) {
        const ticketRef = doc(db, "tickets", docId);
        await updateDoc(ticketRef, {
            status: "New"
        });
        console.log("Ticket restored!");
        loadTickets();  // Reload tickets to update display
    }
};




function getAssignmentControl(docId, status) {
    let members = Array.from(document.getElementById('memberSelect').options).map(option => option.value);
    let optionsHTML = members.map(member => `<option value='${member}'>${member}</option>`).join('');

    if (status === "New") {
        return `<select id='assign-${docId}'>
                    <option value=''>Assign Ticket</option>
                    ${optionsHTML}
                </select>
                <br><button onclick='deleteTicket("${docId}")'>Delete</button> 
                <button onclick='assignTicket("${docId}")'>Save</button> <br><br>`;
    } else if (status === "Recently Deleted") {
        // Only show a "Restore" button for recently deleted tickets
        return `<button onclick='restoreTicket("${docId}")'>Restore</button><br><br>`;
    } else {
        // For all other statuses, provide a way to unassign or delete
        return `<button onclick='unassignTicket("${docId}")'>Unassign</button>
                <button onclick='deleteTicket("${docId}")'>Delete</button><br><br>`;
    }
}















window.loadTickets = async () => {
    console.log("Loading tickets...");
    const openTicketsList = document.getElementById('openTicketsList');
    const pendingTicketsList = document.getElementById('pendingTicketsList');
    const deletedTicketsList = document.getElementById('deletedTicketsList');
    const filter = document.getElementById('sortFilter').value;

    // Clear the existing content
    openTicketsList.innerHTML = '<h2></h2>';
    pendingTicketsList.innerHTML = '<h2></h2>';
    deletedTicketsList.innerHTML = '';  // Clear the deleted tickets list

    const querySnapshot = await getDocs(collection(db, "tickets"));
    console.log(`Number of tickets fetched: ${querySnapshot.size}`);

    querySnapshot.forEach((doc) => {
        const ticket = doc.data();
        const ticketHTML = createTicketHTML(doc.id, ticket);

        if (ticket.status === "Recently Deleted") {
            deletedTicketsList.innerHTML += ticketHTML;
        } else if (ticket.status === "New" && (filter === "all" || ticket.requestor === filter)) {
            openTicketsList.innerHTML += ticketHTML;
        } else if (filter === "all" || ticket.requestor === filter) {
            pendingTicketsList.innerHTML += ticketHTML;
        }
    });
};

function createTicketHTML(docId, ticket) {
    const createdAt = ticket.created.toDate();
    const formattedCreationDate = createdAt.toLocaleDateString("en-US", { year: 'numeric', month: 'long', day: 'numeric' });
    let ticketDetails = `<h2>${ticket.title}</h2>
        <b>From:</b> ${ticket.requestor}
        <p>${ticket.priority} Priority - Created: ${formattedCreationDate}</p>`;
    
    // Append the status, including deletion date if applicable
    if (ticket.status === "Recently Deleted" && ticket.deletedAt) {
        const deletedAt = ticket.deletedAt.toDate();
        const formattedDeletionDate = deletedAt.toLocaleDateString("en-US", { year: 'numeric', month: 'long', day: 'numeric' });
        ticketDetails += `<p>(Deleted on: ${formattedDeletionDate})</p>`;
    } else {
        ticketDetails += `<p>Status: ${ticket.status}</p>`;
    }

    let ticketHTML = `<div class='ticket-item' style='display: block;'>
        ${ticketDetails}
        <div id='ticketsinside'>${ticket.description}</div>
        <br>${getAssignmentControl(docId, ticket.status)}
    </div>`;

    return ticketHTML;
}





        window.assignTicket = async (docId) => {
            const selectedPerson = document.getElementById(`assign-${docId}`).value;
            const ticketRef = doc(db, "tickets", docId);
            if (selectedPerson !== '') {
                await updateDoc(ticketRef, {
                    status: `Assigned to ${selectedPerson}`
                });
                console.log("Ticket assigned!");
                loadTickets();  // Reload tickets to update status
            } else {
                alert("Please select someone to assign the ticket.");
            }
        };

        window.unassignTicket = async (docId) => {
            const ticketRef = doc(db, "tickets", docId);
            await updateDoc(ticketRef, {
                status: "New"
            });
            console.log("Ticket unassigned!");
            loadTickets();  // Reload tickets to reflect the change
        };

       

        
window.onload = async () => {
    await loadTickets(); // Load tickets when the page loads
    await loadMembers(); // Load members from Firestore
};



		// Ensure that onload setup is in place
window.onload = () => {
loadMembers();
    loadTickets(); // Initial load of tickets
    let members = Array.from(document.getElementById('memberSelect').options).map(option => option.value);
     
};


        //loadTickets();
        
        
    </script>
</body>
</html>








"""
    return jsonify({'html_content': html_content})



# Set the password as a variable
password = 'alco0114'

@app.route('/validate_password', methods=['POST'])
def validate_password():
    user_password = request.json['password']
    if user_password == password:
        return jsonify({'valid': True})
    else:
        return jsonify({'valid': False}), 401
        
        

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    if username in users:
        return 'Username already exists', 409
    users[username] = {'password': password, 'state': '', 'city': ''}  # Initialize with empty state and city
    return redirect(url_for('login'))
    
    
@app.route('/save_data', methods=['POST'])
def save_data():
    state = request.form['state']
    city = request.form['city']
    logged = request.form['logged']  # Retrieve logged status
    username = session.get('user')
    if not username:
        return jsonify({'error': 'User not logged in'}), 401
    if username in users:
        users[username].update({'state': state, 'city': city, 'logged': logged})
        save_data_to_csv()  # Save to CSV immediately after update
        print(f"Data saved for {username}: {users[username]}")
        return jsonify(success=True)
    else:
        return jsonify({'error': 'User does not exist'}), 404


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username]['password'] == password:
        session['user'] = username
        return redirect(url_for('index'))
    return 'Invalid credentials', 401



@app.route('/get_data', methods=['GET'])
def get_data():
    username = session.get('user')
    if not username:
        return jsonify({'error': 'User not logged in'}), 401
    user_data = users.get(username, {'state': '', 'city': '', 'logged': '0'})  # Default logged to '0' if not set
    return jsonify(user_data)
 



@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))



@app.route('/')
def index():
    return send_from_directory('.', 'index.html')



@app.route('/upload', methods=['POST'])
def upload_pdf():
    try:
        pdf_file = request.files['pdf']
        reader = PyPDF2.PdfReader(pdf_file.stream)
        fields = reader.get_fields()
        field_names = [{'name': name, 'is_checkbox': field.get('/FT') == '/Btn', 'is_text': field.get('/FT') == '/Tx'} for name, field in fields.items()] if fields else []
        return jsonify({'fields': field_names})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/edit_pdf', methods=['POST'])
def edit_pdf():
    try:
        pdf_file = request.files['pdf']
        reader = PyPDF2.PdfReader(pdf_file.stream)
        writer = PyPDF2.PdfWriter()

        for page in reader.pages:
            if '/Annots' in page:
                annots = page['/Annots']
                for annot in annots:
                    resolved_annot = annot.get_object()
                    field_name = resolved_annot.get('/T')
                    field_type = resolved_annot.get('/FT')

                    if field_name and field_name in request.form:
                        if field_type == PyPDF2.generic.NameObject('/Btn'):  # Checkbox
                            value = '/Yes' if request.form[field_name] == 'Yes' else '/Off'
                            resolved_annot.update({
                                PyPDF2.generic.NameObject('/V'): PyPDF2.generic.NameObject(value),
                                PyPDF2.generic.NameObject('/AS'): PyPDF2.generic.NameObject(value)
                            })
                        else:  # Text field
                            resolved_annot.update({
                                PyPDF2.generic.NameObject('/V'): PyPDF2.generic.TextStringObject(request.form[field_name])
                            })

            writer.add_page(page)

        output_stream = io.BytesIO()
        writer.write(output_stream)
        output_stream.seek(0)
        return send_file(output_stream, as_attachment=True, download_name='modified_pdf.pdf')

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    load_data_from_csv()  # Load data at start
    app.run(debug=True)



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    