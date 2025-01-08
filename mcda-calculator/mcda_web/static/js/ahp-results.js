function fetchAhpResults() {
    fetch('/api/ahp-results/')
        .then(response => response.json())
        .then(data => {
            displayResults(data[0]); 
        })
        .catch(error => console.error('Error fetching the AHP results:', error));
}

function displayResults(result) {
    document.getElementById('analysisDate').innerText = `Analysis Date: ${formatDateTime(new Date(result.created_at))}`;

    const criteriaTableBody = document.getElementById('criteriaList');
    const companyTableBody = document.getElementById('companyList');

    criteriaTableBody.innerHTML = '';
    companyTableBody.innerHTML = ''; 

    result.ranked_companies.criteria.forEach((criteria, index) => {
        const weight = result.criteria_weights.split(',')[index];
        const row = document.createElement('tr');
        const criteriaCell = document.createElement('td');
        criteriaCell.innerText = criteria[0];
        const weightCell = document.createElement('td');
        const selectElement = document.createElement('select');
        selectElement.setAttribute('class', 'form-control');
        selectElement.setAttribute('id', `weight-${index}`);
        selectElement.setAttribute('onchange', `updateWeight(${index}, this.value)`); 

        for (let i = 0; i <= 10; i++) {
            const option = document.createElement('option');
            option.value = i / 10;
            option.text = i / 10;
            option.selected = (i / 10 === parseFloat(weight));
            selectElement.appendChild(option);
        }

        weightCell.appendChild(selectElement);
        row.appendChild(criteriaCell);
        row.appendChild(weightCell);
        criteriaTableBody.appendChild(row);
    });

    result.ranked_companies.ranked_companies.slice(0, 8).forEach(company => {
        const row = document.createElement('tr');
        const companyCell = document.createElement('td');
        companyCell.innerText = company[0];
        const scoreCell = document.createElement('td');
        scoreCell.innerText = company[1];
        row.appendChild(companyCell);
        row.appendChild(scoreCell);
        companyTableBody.appendChild(row);
    });
}

function formatDateTime(dateTime) {
    return `${dateTime.getUTCDate()}/${dateTime.getUTCMonth() + 1}/${dateTime.getUTCFullYear()} ${dateTime.getUTCHours()}:${dateTime.getUTCMinutes() < 10 ? '0' + dateTime.getUTCMinutes() : dateTime.getUTCMinutes()}`;
}

function updateWeight(index, newWeight) {
    const weightElements = document.querySelectorAll('select');
    const weights = Array.from(weightElements).map(select => select.value);
    
    const url = `http://127.0.0.1:8000/api/calculation/?method=ahp&weights=${weights.join(',')}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log('Updated results:', data);
            window.location.reload();
            // displayResults(data);
        })
        .catch(error => console.error('Error updating weights:', error));
}