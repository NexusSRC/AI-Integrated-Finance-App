document.addEventListener('DOMContentLoaded', function () {
    // Initialize expense data
    let expensesData = {
        labels: ['Rent', 'Food', 'Entertainment', 'Utilities', 'Miscellaneous'],
        data: [1500, 1000, 500, 700, 300],
    };

    let totalExpenses = 7000;

    // Calendar events array
    let calendarEvents = [];

    // Update the charts on load
    updateCharts();
    initializeCalendar();

    // Form submission event listener
    const expenseForm = document.getElementById('expense-form');
    expenseForm.addEventListener('submit', function (e) {
        e.preventDefault(); // Prevent the form from submitting

        // Get the expense details
        const expenseName = document.getElementById('expense-name').value;
        const expenseAmount = parseFloat(document.getElementById('expense-amount').value);
        const expenseDate = document.getElementById('expense-date').value;

        // Update expenses data
        updateExpenses(expenseName, expenseAmount, expenseDate);

        // Reset the form
        expenseForm.reset();
    });

    function updateExpenses(name, amount, date) {
        // Add the new expense
        expensesData.labels.push(name);
        expensesData.data.push(amount);

        // Update total expenses
        totalExpenses += amount;
        document.getElementById('total-expenses').innerText = `$${totalExpenses.toLocaleString()}`;

        // Update current balance (assuming total revenue is fixed)
        const totalRevenue = 10000;
        document.getElementById('current-balance').innerText = `$${(totalRevenue - totalExpenses).toLocaleString()}`;

        // Add the expense to calendar events
        addEventToCalendar(name, amount, date);

        // Update charts
        updateCharts();
    }

    function addEventToCalendar(name, amount, date) {
        // Create a new calendar event
        calendarEvents.push({
            title: `${name} - $${amount}`,
            start: date,
        });

        // Reinitialize the calendar with the new events
        initializeCalendar();
    }

    function initializeCalendar() {
        const calendarEl = document.getElementById('calendar');
        const calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            events: calendarEvents,
            // Optional: Set aspect ratio to control size
            aspectRatio: 1.5, // Adjust ratio to make it more compact
        });
        calendar.render(); // Render the calendar
    }

    async function updateCharts() {
        // Pie Chart for Expenses Distribution
        const ctx1 = document.getElementById('expense-pie-chart').getContext('2d');
        if (ctx1) {
            const expensePieChart = new Chart(ctx1, {
                type: 'pie',
                data: {
                    labels: expensesData.labels,
                    datasets: [{
                        label: 'Expenses',
                        data: expensesData.data,
                        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4CAF50', '#FF9F40', '#FFA500', '#00CED1'],
                    }]
                },
                options: {
                    responsive: true
                }
            });
        } else {
            console.log("Canvas element for pie chart not found.");
        }

        // Line Chart for Goals Progress
        const ctx2 = document.getElementById('goals-line-chart').getContext('2d');
        if (ctx2) {
            const goalsLineChart = new Chart(ctx2, {
                type: 'line',
                data: {
                    labels: ['January', 'February', 'March', 'April', 'May', 'June'],
                    datasets: [{
                        label: 'Savings Goal',
                        data: [500, 1000, 1500, 2000, 2500, 3000],
                        borderColor: '#4CAF50',
                        fill: false
                    }]
                },
                options: {
                    responsive: true
                }
            });
        } else {
            console.log("Canvas element for line chart not found.");
        }

        // Bar Chart for Past Expenses (Last 6 Months)
        const ctx3 = document.getElementById('past-expenses-bar-chart').getContext('2d');
        if (ctx3) {
            const pastExpensesBarChart = new Chart(ctx3, {
                type: 'bar',
                data: {
                    labels: ['April', 'May', 'June', 'July', 'August', 'September'],
                    datasets: [{
                        label: 'Expenses',
                        data: [1200, 1300, 1400, 1500, 1600, 1700],
                        backgroundColor: '#FF6384'
                    }]
                },
                options: {
                    responsive: true
                }
            });
        } else {
            console.log("Canvas element for bar chart not found.");
        }
        // const response = await fetch('/model/chat', {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json',
        //     },
        //     body: JSON.stringify({prompt: "Your prompt here"})
        // });
        //
        // const data = await response.json();
        // console.log(data.response);
    }
});
