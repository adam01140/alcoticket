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
    <title>Alco Ticketing System</title>
   <style>
   
   .tickets-container {
        display: block;              /* Enable Flexbox */
        justify-content: space-around; /* Distribute space evenly around the items */
        width: 100%;                /* Take full width of the container */
    }
	
	
    .ticket-item {
        border: 4px solid lightblue; /* Set the border color */
        border-radius: 10px;        /* Rounded corners */
        padding: 20px;              /* Some padding inside the border */
        margin: 10px;               /* Margin outside the border */
        background-color: #ffffff;  /* Light blue background */
        width: 50%;               /* Fixed width */
        height: auto;               /* Automatic height */
    }
	
	
	#ticketsinside {
        border: 4px solid lightblue; /* Set the border color */
        border-radius: 10px;        /* Rounded corners */
        padding: 20px;              /* Some padding inside the border */
        margin: 10px;               /* Margin outside the border */
        background-color: #ffffff;  /* Light blue background */
        width: 80%;               /* Fixed width */
        height: 100%               /* Automatic height adjustment */
    }

    #tickets {
        border: 4px solid lightblue; /* Set the border color */
        border-radius: 10px;        /* Rounded corners */
        padding: 20px;              /* Some padding inside the border */
        margin: 10px;               /* Margin outside the border */
        background-color: #ffffff;  /* Light blue background */
        width: 600px;               /* Fixed width */
        height: 100%               /* Automatic height adjustment */
    }

    /* Existing styles */
    body {
        font-family: Arial, sans-serif;
    }
    input[type="text"], textarea {
        width: 200px;
        height: 30px;
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
        border-radius: 5px;
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
        <h2>Submit a Ticket</h2>
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

    <!-- Display Tickets -->
	
	 <div class="tickets-container">
	 
	<div id = "tickets">
	
	<div id="openTicketsList">
    <h2>Open Tickets</h2>
</div>

</div>
<br>

<div id = "tickets">
<!-- Pending Tickets -->
<div id="pendingTicketsList">
    <h2>Pending Tickets</h2>
    <select id="sortFilter" onchange="loadTickets()">
        <option value="all">All</option>
        <option value="Adnen">Adnen</option>
        <option value="David">David</option>
        <option value="Octavio">Octavio</option>
    </select>
</div>

</div>



    
	</div>

    <script type="module">
        import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.0.0/firebase-app.js';
        import { getFirestore, doc, setDoc, getDoc, collection, getDocs, addDoc, updateDoc, deleteDoc } from 'https://www.gstatic.com/firebasejs/9.0.0/firebase-firestore.js';

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

window.loadTickets = async () => {
    const openTicketsList = document.getElementById('openTicketsList');
    const pendingTicketsList = document.getElementById('pendingTicketsList');
    const filter = document.getElementById('sortFilter').value;
    
    openTicketsList.innerHTML = '<h2>Open Tickets</h2>';
    pendingTicketsList.innerHTML = '<h2>Pending Tickets</h2>';

    const querySnapshot = await getDocs(collection(db, "tickets"));
    querySnapshot.forEach((doc) => {
        const ticket = doc.data();
        let statusDisplay = ticket.status !== "New" ? `<br> ${ticket.status}` : '';
        let isVisible = filter === 'all' || ticket.status.includes(`Assigned to ${filter}`);
        
        let assignmentControl = ticket.status === "New"
            ? `<select id='assign-${doc.id}'><option value=''>Assign Ticket</option><option value='Adnen'>Adnen</option><option value='David'>David</option><option value='Octavio'>Octavio</option></select>
              <br><button onclick='deleteTicket("${doc.id}")'>Delete</button> <button onclick='assignTicket("${doc.id}")'>Save</button>`
            : `<button onclick='deleteTicket("${doc.id}")'>Delete</button> <button onclick='unassignTicket("${doc.id}")'>Unassign</button>`;
        
        let ticketHTML = `<div class='ticket-item' style='display: ${isVisible ? "block" : "none"};'>
            <b><h2>${ticket.title}</h2></b> 
            <b> From:</b> ${ticket.requestor}
            <br>( ${ticket.priority} Priority )${statusDisplay}
            <br><br><b> Description: </b>
            <div id="ticketsinside">
            ${ticket.description}
            </div>
            <br> ${assignmentControl}</div>`;

        if (ticket.status === "New") {
            openTicketsList.innerHTML += ticketHTML;
        } else {
            pendingTicketsList.innerHTML += ticketHTML;
        }
    });
};



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

        window.deleteTicket = async (docId) => {
            if (confirm("Are you sure you want to delete this ticket?")) {
                await deleteDoc(doc(db, "tickets", docId));
                console.log("Ticket deleted!");
                loadTickets();  // Reload tickets to reflect the change
            }
        };

        window.onload = () => {
            loadTickets(); // Load tickets when the page loads
            //alert("hey");
        };
        
        loadTickets();
        
        
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



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    